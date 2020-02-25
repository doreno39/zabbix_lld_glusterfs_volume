#!/usr/bin/python
# Description: to get the volume quota of the GlusterFS write to the file.
# Require: Python 2.7 or later
# Author: TruongLN
# Date: 20200224

from glustercmd import GlusterCommand
import xml.etree.ElementTree as ETree
from xml.parsers.expat import ExpatError

def read_file_to_list(pathfile):
    with open(pathfile, 'r') as f:
        lines = f.readlines()
    result = [item for item in [line.strip() for line in lines] if item]
    return result

def write_file(vol, path, hard_limit, used_space, percent):
    f = open("limit_info/%s" % vol, "w")
    f.write("%s %s %s %s" % (path, hard_limit, used_space, percent))
    f.close()

if __name__ == "__main__":
    except_vol_path_file = "except_vol.txt"
    data = []

    cmd = GlusterCommand('gluster volume list', timeout=10)
    cmd.run()
    vols = cmd.stdout

    except_vols = read_file_to_list(except_vol_path_file)
    for vol in vols:
        if vol not in except_vols:
            #check qouta ghi xuong file de zabbix doc
            cmd = GlusterCommand('gluster volume quota %s list --xml' % (vol), timeout=10)
            cmd.run()
            
            field_list = ['path', 'hard_limit', 'used_space', 'avail_space']
            xml_string = ''.join(cmd.stdout)
            xml_root = ETree.fromstring(xml_string)
                            
            for elem in xml_root.iterfind('volQuota/limit/path'):
                path = elem.text
            for elem in xml_root.iterfind('volQuota/limit/hard_limit'):
                hard_limit = elem.text
            for elem in xml_root.iterfind('volQuota/limit/used_space'):
                used_space = elem.text
            
            percent = int(used_space) / int(hard_limit)
            
            write_file(vol, path, hard_limit, used_space, percent)
