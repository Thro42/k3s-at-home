import yaml
import os.path
from PySide6.QtWidgets import QMessageBox
from config import *

class RaspbianSettings():
    def __init__(self, parent, settings, drive, node):
        self.parent = parent
        self.drive = drive
        self.node = node
        self.settings = settings

    def check_sd_os(self):
        user_file = self.drive + FIRSTRUN_OUTPUT
        print('Check ' + user_file)
        return os.path.isfile(user_file)

    def save_interface(self):
        ip = self.node['ip']+'/'+self.settings['ip_mask']
        sep = ','
        nameservers = sep.join(self.settings['nameservers'])
        if self.node['network'] == 'eth':
            teplite_file = INTERFACE_TEMPLATE_ETH
        elif self.node['network'] == 'wifi':
            teplite_file = INTERFACE_TEMPLATE_WIFI
        if os.path.isfile(teplite_file):
            with open(teplite_file, 'r') as file:
                data = file.read()
                data = data.replace('[ip_address]', ip)
                data = data.replace('[gateway]', self.settings['gateway'])
        user_file = self.drive + INTERFACE_OUTPUT
        print(user_file)
        with open(user_file, 'w', newline='\n') as file:
            file.write(data)

    def save_firstrun(self):
        ip = self.node['ip']+'/'+self.settings['ip_mask']
        sep = ','
        nameservers = sep.join(self.settings['nameservers'])
        if self.node['network'] == 'eth':
            teplite_file = FIRSTRUN_TEMPLATE_ETH
        elif self.node['network'] == 'wifi':
            teplite_file = FIRSTRUN_TEMPLATE_WIFI
        if os.path.isfile(teplite_file):
            with open(teplite_file, 'r') as file:
                data = file.read()
                data = data.replace('[hostname]', self.node['name'])
                data = data.replace('[username]', self.settings['firstuser'])
                data = data.replace('[passwd]', self.settings['passwd'])
                data = data.replace('[ssh-rsa]', self.settings['ssh_rsa'])
                data = data.replace('[ip_address]', ip)
                data = data.replace('[gateway]', self.settings['gateway'])
                data = data.replace('[nameservers]', nameservers)
                data = data.replace('[ssid]', self.settings['access_point'])
                data = data.replace('[ssid_pwd]', self.settings['access_passwd'])
            user_file = self.drive + FIRSTRUN_OUTPUT
            print(user_file)
            os.remove(user_file)
            with open(user_file, 'w', newline='\n') as file:
                file.write(data)

    def save_dhcpcd_conf(self):
        ip = self.node['ip']+'/'+self.settings['ip_mask']
        sep = ','
        teplite_file =' '
        nameservers = sep.join(self.settings['nameservers'])
        if self.node['network'] == 'eth':
            teplite_file = DHCPCD_CONF_TEMPLATE_ETH
        elif self.node['network'] == 'wifi':
            teplite_file = DHCPCD_CONF_TEMPLATE_WIFI
        if os.path.isfile(teplite_file):
            with open(teplite_file, 'r') as file:
                data = file.read()
                data = data.replace('[ip_address]', ip)
                data = data.replace('[gateway]', self.settings['gateway'])
                data = data.replace('[nameservers]', nameservers)
            user_file = self.drive + DHCPCD_CONF_OUTPUT
            print(user_file)
            with open(user_file, 'w', newline='\n') as file:
                file.write(data)
        else:
            QMessageBox.critical(self.parent, 'Wrong Template', 'Template ' + teplite_file + ' is not found')