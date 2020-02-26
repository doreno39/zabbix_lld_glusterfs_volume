#!/usr/bin/python
# Description: to get the volume of the GlusterFS push to Zabbix server.
# Require: Python 2.7 or later
# Author: TruongLN
# Date: 20200224

import os
import json
from glustercmd import GlusterCommand

def read_file_to_list(pathfile):
    with open(pathfile, 'r') as f:
        lines = f.readlines()
    result = [item for item in [line.strip() for line in lines] if item]
    return result

if __name__ == "__main__":
    path_script = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    except_vol_path_file = "%s/except_vol.txt" % path_script
    data = []

    cmd = GlusterCommand('gluster volume list', timeout=10)
    cmd.run()
    vols = cmd.stdout

    except_vols = read_file_to_list(except_vol_path_file)
    for vol in vols:
        if vol not in except_vols:
            #append vao dict sau do dump json lam input cho zabbix
            data.append({"{#VOLUMENAME}": vol})

    print(json.dumps({"data": data}, indent=4))