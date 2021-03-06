##TODO add checking to make sure it can connect to PIA
import os
import requests
import subprocess
import argparse
import logging

LOG = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class PiaAction:
    def __init__(self):
        self.configpath = '/etc/openvpn/client/'

    def select_connection(self):
        files = os.listdir(self.configpath)
        conn_dict = {}     
        i = 0                         
        for file in files: 
            if file.endswith(".ovpn"):
                conn_dict[i]=file   
                i+=1
        print(conn_dict)
        connection = conn_dict[int(input('Select Connection: '))]
        PiaAction.connect_pia(connection,self.configpath)

    def connect_pia(self,connection):
        LOG.info('Attempting to connect to PIA...')
        configpath = self.configpath
        vpn = subprocess.Popen("/usr/bin/sudo /usr/sbin/openvpn --cd {confdir} --config {confdir}{connection}".format(confdir=configpath, connection=connection
), shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        pid = vpn.pid 

    @staticmethod 
    def disconnect_pia():
        LOG.info('Disconnecting PIA VPN')
        command = subprocess.run(["/usr/bin/sudo", "/usr/bin/pkill", "openvpn"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if command.returncode != 0:
            LOG.error('Process not killed')
            LOG.error(command.stderr)
        else:
            LOG.info("PIA Killed!: {}".format(command.sterr))
    
    @staticmethod
    def check_pia():
        LOG.info('Checking status of PIA VPN')
        adapters = []
        for line in open('/proc/net/dev'):
            if ':' in line:
                adapters.append(line.split(':')[0].strip(' ').lower())
        exists = [i for i in adapters if "tun" in i]
        if exists:
            return True
            LOG.info('PIA is running!')
        else:
            LOG.warning('PIA is NOT running')
            return False

        
