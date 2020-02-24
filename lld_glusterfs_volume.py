#!/usr/bin/python
# Description: to get the volume quota of the GlusterFS push to Zabbix server.
# Require: Python 2.7 or later
# Author: TruongLN
# Date: 20200224

from glustercmd import GlusterCommand

def read_file_to_list(pathfile):
    with open(pathfile, 'r') as f:
        lines = f.readlines()
    result = [item for item in [line.strip() for line in lines] if item]
    return result

if __name__ == "__main__":
    except_vol_path_file = "except_vol.txt"
    data = []

    cmd = GlusterCommand('gluster volume list', timeout=10)
    cmd.run()
    all_vol = cmd.stdout

    except_vols = read_file_to_list(except_vol_path_file)
    vols = (vol for vol in all_vol if not any(ignore in vol for ignore in except_vols))
    print vols