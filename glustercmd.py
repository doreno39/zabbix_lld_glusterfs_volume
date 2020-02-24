#!/usr/bin/env python
#
import os
import signal
#
import subprocess
import threading
#
import xml.etree.ElementTree as ETree

class GlusterCommand(object):
    targetNode = 'localhost'  # default to local machine

    def __init__(self, cmd, timeout=1):
        self.cmd = cmd
        self.cmdProcess = None
        self.timeout = timeout
        self.rc = 0  # -1 ... timeout
        # 0 .... successful
        # n .... RC from command

        self.stdout = []
        self.stderr = []
        # Initialize the environment, and update PATH. In few cases there are
        # chances that the env is empty, in such cases set PATH.
        self.env = dict(os.environ)
        # Try to append to path, don't overwrite
        try:
            self.env['PATH'] += ':/usr/sbin:/usr/local/sbin'
        except KeyError:
            # Empty environment, create the varaible
            self.env['PATH'] =  ':/usr/sbin:/usr/bin:/usr/local/sbin'
            self.env['PATH'] += ':/usr/local/bin'

    def run(self):
        """ Run the command inside a thread to enable a timeout to be
            assigned """

        def command_thread():
            """ invoke subprocess to run the command """

            if GlusterCommand.targetNode is not "localhost":
                self.cmd += " --remote-host=%s" % GlusterCommand.targetNode

            self.cmdProcess = subprocess.Popen(self.cmd,
                                               shell=True,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE,
                                               env=self.env,
                                               preexec_fn=os.setsid)

            stdout, stderr = self.cmdProcess.communicate()
            self.stdout = stdout.split('\n')[:-1]
            self.stderr = stderr.split('\n')[:-1]

        # use cfg.CMD_TIMEOUT value, to wait till user specified timeout.
        self.timeout = 10

        thread = threading.Thread(target=command_thread)
        thread.start()

        thread.join(self.timeout)

        if thread.is_alive():
            if cfg.debug:
                print ('Gluster_Command. Response from glusterd has exceeded %d secs timeout, terminating the request'
                       % self.timeout)
            os.killpg(self.cmdProcess.pid, signal.SIGTERM)
            self.rc = -1

        else:
            # the thread completed normally
            if '--xml' in self.cmd:
                # set the rc based on the xml return code
                xmldoc = ETree.fromstring(''.join(self.stdout))
                self.rc = int(xmldoc.find('.//opRet').text)
            else:
                # set the rc based on the shell return code
                self.rc = self.cmdProcess.returncode
