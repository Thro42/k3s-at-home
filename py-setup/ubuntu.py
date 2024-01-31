import yaml
import os.path
from config import *

class UbuntuSettings():
    def __init__(self, settings, drive, node):
        self.drive = drive
        self.node = node
        self.settings = settings
        self.net_config = {}
        self.net_config['version'] = 2
        self.user_data = {}
        with open(USER_DATA_TEMPLATE, 'r') as file:
            self.user_data = yaml.safe_load(file)

    def check_sd_os(self):
        user_file = self.drive + NET_CONF_OUTPUT
        return os.path.isfile(user_file)
    
    def save_net_config(self):
        ip = self.node['ip']+'/'+self.settings['ip_mask']
        sep = ','
        nameservers = sep.join(self.settings['nameservers'])
        if self.node['network'] == 'eth':
            teplite_file = NET_CONF_TEMPLATE_ETH
        elif self.node['network'] == 'wifi':
            teplite_file = NET_CONF_TEMPLATE_WIFI
        if os.path.isfile(teplite_file):
            with open(teplite_file, 'r') as file:
                data = file.read()
                data = data.replace('[ip_address]', ip)
                data = data.replace('[local-domain]', self.settings['domain'])
                data = data.replace('[gateway]', self.settings['gateway'])
                data = data.replace('[nameservers]', nameservers)
                data = data.replace('[ssid]', self.settings['access_point'])
                data = data.replace('[ssid_pwd]', self.settings['access_passwd'])
                net_file = self.drive + NET_CONF_OUTPUT
                print(net_file)
                with open(net_file, 'w') as file:
                    file.write(data)

    def save_net_config_yaml(self):
        ips = []
        ips.append(self.node['ip']+'/'+self.settings['ip_mask'])
        #search = []
        #search.append(self.settings['domain'])
        search = '['+ self.settings['domain'] + ']'
        #addresses = self.settings['nameservers']
        sep = ','
        addresses = '[' + sep.join(self.settings['nameservers']) + ']'
        nameservers = {}
        nameservers['nameservers'] = {'search':search, 'addresses':addresses}
        if self.node['network'] == 'eth':
            neteth = {'eth0': {'dhcp4': False, 'addresses': ips, 'gateway4': self.settings['gateway'], 'nameservers':nameservers}}
            self.net_config['ethernets'] = neteth
        elif self.node['network'] == 'wifi':
            netwifi = {'wlan0': {'dhcp4': False, 'addresses': ips, 'gateway4': self.settings['gateway'], 'nameservers':nameservers}}
            self.net_config['wifis'] = netwifi
        net_file = self.drive + NET_CONF_OUTPUT
        print(net_file)
        with open(net_file, 'w') as yaml_file:
            yaml.dump(self.net_config, yaml_file)
    
    def save_user_data_yaml(self):
        with open(USER_DATA_TEMPLATE, 'r') as file:
            self.user_data = yaml.safe_load(file)
        #users = {}
        self.user_data['hostname'] = self.node['name']
        self.user_data['users'][0]['name'] = self.settings['firstuser']
        self.user_data['users'][0]['passwd'] = self.settings['passwd']
        rsa = 'ssh-rsa ' + self.settings['ssh_rsa']
        self.user_data['users'][0]['ssh_authorized_keys'][0] = rsa
        user_file = self.drive + USER_DATA_OUTPUT
        print(user_file)
        with open(user_file, 'w') as yaml_file:
            yaml.dump(self.user_data, yaml_file)

    def save_user_data(self):
        with open(USER_DATA_TEMPLATE, 'r') as file:
            data = file.read()
            data = data.replace('[hostname]', self.node['name'])
            data = data.replace('[username]', self.settings['firstuser'])
            data = data.replace('[passwd]', self.settings['passwd'])
            rsa = 'ssh-rsa ' + self.settings['ssh_rsa']
            data = data.replace('[ssh-rsa]', self.settings['ssh_rsa'])
            user_file = self.drive + USER_DATA_OUTPUT
            print(user_file)
            with open(user_file, 'w') as file:
                file.write(data)
