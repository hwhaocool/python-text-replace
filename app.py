#coding: utf-8

import os
from config import Config

myConfig = Config()

def printUseage():
    print "please input a number to select a function:"
    print "1  --  filter and print file name"
    print "2  --  filter then find and replace"

def getConfig():
    print "please input a number to select a config:"

    configNum = raw_input()
    return int(configNum)

def getDstFolder():
    print "please input path:"
    pass

def filter():
    print "**********  filter                    ***"
    ruleList = myConfig.getFilterRuleList()
    num = 1
    for name in ruleList:
        print "%d   %s" % (num, name)
        num += 1

    num = getConfig()
    print ruleList[num]


def replace():
    print "**********  filter , find , replace   ***"


printUseage()
funcNumStr = raw_input()
funcNum =  int(funcNumStr)

if 1 == funcNum:
    filter()
elif 2 == funcNum:
    replace()
else:
    print "not support yet"
    exit(1)
