#coding: utf-8
#author: hwhaocool
#since: 2019-1-17

import yaml

class Config:
    """配置项"""

    conf = {}

    def __init__(self):
        f = open("config.yaml", 'rb')
        self.conf = yaml.load(f )
        f.close()

        print "config.json load completed"

    def ensureNameExist(self, name):
        """ensure rule name must exist"""
        if None == name or "" == name:
            print "rule name is required"
            exit(1)

    def getFilterRuleList(self):
        """get filter rule list"""
        ruleList = []
        for data in  self.conf['filter']:
            name = data['name']

            self.ensureNameExist(name)

            count = ruleList.count(name)
            if 0 == count:
                ruleList.append(name)
            else:
                print "erro! duplicate filter name: %s" % name
                exit(1)
                
        return ruleList

    def getFilterRuleByName(self, ruleName):
        for data in  self.conf['filter']:
            name = data['name']
            if name == ruleName:
                return data

    def getReplaceRuleList(self):
        """get replace rule list"""
        ruleList = []
        for data in  self.conf['replace']:
            name = data['name']

            self.ensureNameExist(name)

            count = ruleList.count(name)
            if 0 == count:
                ruleList.append(name)
            else:
                print "erro! duplicate replace name: %s" % name
                exit(1)
                
        return ruleList

    def getReplaceRuleByName(self, ruleName):
        for data in  self.conf['replace']:
            name = data['name']
            if name == ruleName:
                return data

    def validateActions(self, actions) :
        if 0 == len(actions):
            print "actions is required"
            exit(1)
        # for action in actions:
        #     action["matchStr"]
        #     action["replace"]

