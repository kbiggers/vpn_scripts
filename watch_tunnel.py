import logging
import os
import subprocess

from pia_action import PiaAction

LOG = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

class Watcher:
    def __init__(self, process):
        self.process = process 
        self.pid = self.get_pid()

    def get_pid(self):
        command = subprocess.run(['/usr/bin/sudo','/bin/pidof',"{}".format(self.process)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if command.returncode != 0:
            log.info("{} is not running".format(self.process))
        else:
            return command.stdout.decode("utf-8").rstrip()

    def kill_process(self):
        LOG.info("killing {}...".format(self.process))
        command = subprocess.run(["/usr/bin/sudo", "/bin/kill","-9", "{}".format(self.pid)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if command.returncode != 0:
            LOG.error("{} not killed".format(self.process))
            LOG.error(command.stderr.decode('utf-8'))
        else:
            LOG.info("{} Killed!: {}".format(self.process, command.stderr.decode('utf-8')))

    def watch(self):
        pia = PiaAction()
        if pia.check_pia() == False and self.get_pid(): 
            LOG.info("{} is running without vpn tunnel, killing PID {}".format(self.process, self.pid))
            self.kill_process()
        
