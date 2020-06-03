Zabbix template for collecting GlusterFS volume usage
# Require
- Python 2.7
- Zabbix 3.x

# Installation
To install
```
cd /opt
git clone https://github.com/doreno39/zabbix_lld_glusterfs_volume.git
cd zabbix_lld_glusterfs_volume
cat userparameter_volume.conf >> /etc/zabbix/zabbix_agentd.conf

echo "#gen data gluster volume info for zabbix check" >>/var/spool/cron/root
echo "*/10 * * * * /usr/bin/python /opt/zabbix_lld_glusterfs_volume/get_vol_info.py > /dev/null 2>&1" >>/var/spool/cron/root

echo "zabbix ALL=(ALL:ALL) NOPASSWD: /usr/bin/python /opt/zabbix_lld_glusterfs_volume/lld_glusterfs_volume.py*" >>/etc/sudoers
```
Then restart zabbix agent

Go to Zabbix's web interface, Configuration->Templates and import Template GlusterFS Discovery Volume Capacity.xml. After that you should be able to monitor volume activity for all your cluster.
