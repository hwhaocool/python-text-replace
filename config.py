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

    def getFilterRuleList(self):
        """get filter rule list"""
        ruleList = []
        for data in  self.conf['filter']:
            name = data['name']
            count = ruleList.count(name)
            if 0 == count:
                ruleList.append(name)
            else:
                print "erro! duplicate filter name: %s" % name
                exit(1)
                
        return ruleList

    def getLoginUrl(self):
        """登录地址"""
        return self.doamin + self.conf["login_url"]

    def getSignUrl(self):
        """签到地址"""
        return self.doamin + self.conf["sign_url"]

    def getIndexUrl(self):
        """首页地址"""
        return self.doamin + self.conf["index_url"]

    def getUserName(self):
        return self.conf["user_name"]

    def getPassword(self):
        return self.conf["password"]

    def getQmIndexUrl(self):
        return self.doamin + self.conf["qm_index_url"]



