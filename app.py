#coding: utf-8

import os
import json
import shutil
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
    return raw_input("please input path:")

useStart = False
useEnd = False
useConatins = False
searchInChild = False
matchStr = ""
fileNameSuffix = ""

def isThisLineMatch(data, matchStr):
    if useStart:
        return data.startswith(matchStr)
    elif useEnd:
        return data.endswith(matchStr)
    elif useConatins:
        return -1 != data.find(matchStr)
    else:
        print "error! no match rule specified"
        exit(1)

def doFilterInPath(dstPath):
    pathList = os.listdir(dstPath)

    matchPathList = []
    notMatchPathList = []

    for p in pathList:
        tempPath = os.path.join(dstPath, p)

        if os.path.isdir(tempPath):
            if not searchInChild:
                continue
            else:
                pass
                x, y = doFilterInPath(tempPath)
                matchPathList.extend(x)
                notMatchPathList.extend(y)
                continue

        if "" != fileNameSuffix:
            if not p.endswith(fileNameSuffix):
                continue

        r = open(tempPath, "r")

        isFind = False
        for data in r.readlines():
            if isThisLineMatch(data, matchStr):
                isFind = True
                continue

        r.close()

        # find
        if isFind:
            matchPathList.append(tempPath)
        else:
            notMatchPathList.append(tempPath)

    return (matchPathList, notMatchPathList)

def doFilter(rule, dstPath, returnMatchOrNot=True):
    
    global useStart
    global useEnd
    global useConatins
    global searchInChild
    global matchStr
    global fileNameSuffix

    temp = rule.get("searchInChild", False)
    if True == temp:
        searchInChild = True

    print "searchInChild is " + str(searchInChild)

    matchStr = rule.get("start", "")
    if "" != matchStr:
        useStart = True
        print "start -- %s" % matchStr
    else:
        matchStr = rule.get("end", "")
        if "" != matchStr:
            useEnd = True
            print "end -- %s" % matchStr
        else:
            matchStr = rule.get("contains", "")
            if "" != matchStr:
                useConatins = True
                print "contains -- %s" % matchStr

    fileNameSuffix = rule.get("fileNameSuffix", "")

    matchPathList, notMatchPathList = doFilterInPath(dstPath)

    print "match %d files" % len(matchPathList)
    print "not match %d files" % len(notMatchPathList)

    if returnMatchOrNot:
        print "match list are "
        for a in matchPathList:
            print a
        return matchPathList
    else:
        print "not match list are "
        for a in notMatchPathList:
            print a
        return notMatchPathList

def doReplace(replaceRule, dstPath):
    filterRuleName = replaceRule.get("filterRuleName", "")
    excludeRuleName = replaceRule.get("excludeRuleName", "")

    #get path list
    pathList = []

    if "" != excludeRuleName:
        excluseFilterRule = myConfig.getFilterRuleByName(excludeRuleName)

        pathList = doFilter(excluseFilterRule, dstPath, False)
    elif "" != filterRuleName:
        filterRule = myConfig.getFilterRuleByName(filterRuleName)

        pathList = doFilter(filterRule, dstPath, True)

    #get replace rule
    actions = replaceRule.get("actions", [])
    
    myConfig.validateActions(actions)

    replaceCount = 0

    for p in pathList:
        currentPath = os.path.join(dstPath, p)
        with open(currentPath,"r") as f:
            lines = f.readlines() 

        #open in wirte mode
        with open(currentPath,"w") as f_w:
            for line in lines:

                #each line only apply one replace rule
                waitReplace = True

                for action in actions:
                    matchStr = action["matchStr"]
                    replaceStr = action["replace"]

                    if waitReplace and -1 != line.find(matchStr):
                        #替换
                        replaceCount += 1
                        line = line.replace(matchStr, replaceStr)
                        waitReplace = False

                f_w.write(line)

        # newPath = os.path.join(dstPath, "model")
        # newPath = os.path.join(newPath, p)
        # shutil.move(currentPath, newPath)

    print "replace %d" % replaceCount
    pass



def filter():
    print "**********  filter                    ***"
    ruleList = myConfig.getFilterRuleList()
    num = 1
    for name in ruleList:
        print "%d   %s" % (num, name)
        num += 1

    num = getConfig()
    ruleName = ruleList[num-1]

    rule = myConfig.getFilterRuleByName(ruleName)

    dstPath = getDstFolder()

    doFilter(rule, dstPath)


def replace():
    print "**********  filter , find , replace   ***"

    ruleList = myConfig.getReplaceRuleList()
    num = 1
    for name in ruleList:
        print "%d   %s" % (num, name)
        num += 1

    num = getConfig()
    ruleName = ruleList[num-1]
    rule = myConfig.getReplaceRuleByName(ruleName)

    dstPath = getDstFolder()

    doReplace(rule, dstPath)




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
