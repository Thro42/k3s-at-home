import yaml
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

    def save_net_config(self):
        ips = []
        ips.append(self.node['ip'])
        search = []
        search.append(self.settings['domain'])
        addresses = self.settings['nameservers']
        nameservers = {}
        nameservers['nameservers'] = {'search':search, 'addresses':addresses}
        if self.node['network'] == 'eth':
            neteth = {'eth0': {'dhcp4': False, 'addresses': ips, 'gateway4': self.settings['gateway'], 'nameservers':nameservers}}
            self.net_config['ethernets'] = neteth
        elif self.node['network'] == 'wifi':
            netwifi = {'wlan0': {'dhcp4': False, 'addresses': ips, 'gateway4': self.settings['gateway'], 'nameservers':nameservers}}
            self.net_config['wifis'] = netwifi
        print(self.net_config)
        with open(NET_CONF_OUTPUT, 'w') as json_file:
            yaml.dump(self.net_config, json_file)
    
    def save_user_data(self):
        #users = {}
        self.user_data['hostname'] = self.node['name']
        self.user_data['users'][0]['name'] = self.settings['firstuser']
        self.user_data['users'][0]['passwd'] = self.settings['passwd']
        rsa = 'ssh-rsa ' + self.settings['ssh_rsa']
        self.user_data['users'][0]['ssh_authorized_keys'][0] = rsa
        print(self.user_data)
        with open(USER_DATA_OUTPUT, 'w') as json_file:
            yaml.dump(self.user_data, json_file)
