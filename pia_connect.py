import os
import requests
import subprocess
import argparse

In [55]: LOG = logging.getLogger(__name__)
    ...: logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class PiaAction:
    def __init__(args):
        self.config_path = '/etc/openvpn/client/'

    def select_connection(self):
        files = os.listdir(self.config_path)
        conn_dict = {}     
        i = 0                         
        for file in files: 
            if file.endswith(".ovpn"):
                conn_dict[i]=file   
                i+=1
        print(conn_dict)
        connection = conn_dict[int(input('Select Connection: '))]
        return connection
    def connect_pia(self,connection):
        vpn = subprocess.Popen("/usr/bin/sudo /usr/sbin/openvpn --cd {confdir} --config {confdir}{connection}".format(confdir=self.config_path, connection=connection
), shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        pid = vpn.pid 

    def disconnect_pia(self):
        LOG.info('Disconnecting PIA VPN')
        command = subprocess.run("/usr/bin/sudo /usr/bin/pkill openvpn")
        if command.returncode != 0:
            LOG.error('Process not killed')
    
    def check_pia():
        LOG.info('Checking status of PIA VPN')
        adapters = []
        for line in open('/proc/net/dev'):
            if ':' in line:
                adapters.append(line.split(':')[0].strip(' ').lower())
        exists = [i for i in adapters if "tun" in i]
        if exists:
            LOG.info('PIA is running!')
        else:
            LOG.warning('PIA is NOT running, killing rtorrent...')

    def kill_rtorrent():
        
