#!/usr/bin/python
# Description: to get the volume quota of the GlusterFS write to the file.
# Require: Python 2.7 or later
# Author: TruongLN
# Date: 20200224

import os
from glustercmd import GlusterCommand
import xml.etree.ElementTree as ETree
from xml.parsers.expat import ExpatError

def read_file_to_list(pathfile):
    with open(pathfile, 'r') as f:
        lines = f.readlines()
    result = [item for item in [line.strip() for line in lines] if item]
    return result

def write_file(path_file, path, hard_limit, used_space, used_percent):
    f = open(path_file, "w")
    f.write("%s %s %s %s" % (path, hard_limit, used_space, used_percent))
    f.close()

if __name__ == "__main__":
    path_script = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    except_vol_path_file = "%s/except_vol.txt" % path_script
    data = []

    cmd = GlusterCommand('gluster volume list', timeout=10)
    cmd.run()
    vols = cmd.stdout

    # except_vols = read_file_to_list(except_vol_path_file)
    except_vols = []
    for vol in vols:
        if vol not in except_vols:
            #check qouta ghi xuong file de zabbix doc
            cmd = GlusterCommand('gluster volume quota %s list --xml' % (vol), timeout=10)
            err = 0
            try:
                cmd.run()
            except:
                err = 1
                pass
            if cmd.rc == 0 and err == 0:
                field_list = ['path', 'hard_limit', 'used_space', 'avail_space']
                xml_string = ''.join(cmd.stdout)
                xml_root = ETree.fromstring(xml_string)
                                
                for elem in xml_root.iterfind('volQuota/limit/path'):
                    path = elem.text
                for elem in xml_root.iterfind('volQuota/limit/hard_limit'):
                    hard_limit = elem.text
                for elem in xml_root.iterfind('volQuota/limit/used_space'):
                    used_space = elem.text
                used_percent = round((float(used_space) / float(hard_limit))*100, 2)
                
                path_dir = "%s/limit_info" % (path_script)
                path_file = "%s/%s" % (path_dir, vol)
                if not os.path.isdir(path_dir):
                    try:
                        os.mkdir(path_dir)
                    except OSError:
                        print "Creation of the directory %s failed." % path_dir

                write_file(path_file, path, hard_limit, used_space, used_percent)
