import os.path
import configparser
from config import *

class Inventory:
    def __init__(self):
        self.filename = NODES_INVENTORY
        self.config = configparser.ConfigParser()
        self.isModify = False

    def generate(self, nodeArr):
        rolles = []
        for node in nodeArr:
            if not node['rolle'] in rolles:
                rolles.append(node['rolle'])
        print(rolles)
        for rolle in rolles:
            self.config[rolle] = {}
            rolleConf = self.config[rolle]
            for node in nodeArr:
                if node['rolle'] == rolle:
                    hostLine = node['name'] + ' ansible_host'
                    ipLine = node['ip']
                    rolleConf[hostLine]= ipLine

        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)