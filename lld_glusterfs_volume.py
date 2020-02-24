#!/usr/bin/python
# Description: to get the volume quota of the GlusterFS push to Zabbix server.
# Require: Python 2.7 or later
# Author: TruongLN
# Date: 20200224

from glustercmd import GlusterCommand

if __name__ == "__main__":
    cmd = GlusterCommand('gluster volume list', timeout=10)
    cmd.run()
    print cmd.stdout
