#!/usr/bin/python
# Description: to get the volume of the GlusterFS push to Zabbix server.
# Require: Python 2.7 or later
# Author: TruongLN
# Date: 20200224

import os, sys
import json
from glustercmd import GlusterCommand

def read_file_to_list(pathfile):
    with open(pathfile, 'r') as f:
        lines = f.readlines()
    result = [item for item in [line.strip() for line in lines] if item]
    return result

def hlp ():
    print "using lld_glusterfs_volume.py or lld_glusterfs_volume.py allvol"
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 2:
        hlp()
    
    path_script = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    except_vol_path_file = "%s/except_vol.txt" % path_script
    data = []

    cmd = GlusterCommand('gluster volume list', timeout=10)
    cmd.run()
    vols = cmd.stdout

    if len(sys.argv) == 1:       
        except_vols = read_file_to_list(except_vol_path_file)
        dict_title = "{#GLTVOLUMENAME}"
    elif len(sys.argv) == 2:  #get all volume info
        if sys.argv[1] == "allvol":
            except_vols = []
            dict_title = "{#VOLUMENAME}"
        else:
            hlp()
    else:
        hlp()
    
    for vol in vols:
        if vol not in except_vols:
            #append vao dict sau do dump json lam input cho zabbix
            data.append({ dict_title : vol})

    print(json.dumps({"data": data}, indent=4))