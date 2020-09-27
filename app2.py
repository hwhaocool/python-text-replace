#coding: utf-8

import os
import json
import shutil
from config import Config

myConfig = Config()
useStart = False
useEnd = False
useConatins = False
searchInChild = False
matchStr = ""
fileNameSuffix = ""
newProjectName = ""

def printUseage():
    print "generate a new project"

def getConfig():
    print "please input a number to select a config:"

    configNum = raw_input()
    return int(configNum)

def getDstFolder():
    return raw_input("please input path:")

def getNewProjectName():
    global newProjectName
    newProjectName = raw_input("please input new project name( all low case):   ")


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

    for p in pathList:
        tempPath = os.path.join(dstPath, p)

        if os.path.isdir(tempPath):
            if not searchInChild:
                continue
            else:
                pass
                x = doFilterInPath(tempPath)
                matchPathList.extend(x)
                continue

        if "" != fileNameSuffix:
            if not p.endswith(fileNameSuffix):
                continue

        matchPathList.append(tempPath)

    return matchPathList

def doFilter(rule, dstPath):
    """
    过滤
    """
    
    global useStart
    global useEnd
    global useConatins
    global searchInChild

    # 文件名后缀(可以包含 点号)
    global fileNameSuffix

    temp = rule.get("searchInChild", False)
    if True == temp:
        searchInChild = True

    print "searchInChild is " + str(searchInChild)

    fileNameSuffix = rule.get("fileNameSuffix", "")

    matchPathList = doFilterInPath(dstPath)

    print "match %d files" % len(matchPathList)

    print "match list are "
    for a in matchPathList:
        print a
    return matchPathList

def doReplaceFolderNameInPath(replaceRule, dstPath):
    """
    递归替换文件夹的名称
    """

    actions = replaceRule.get("actions", [])

    pathList = os.listdir(dstPath)

    # p  是当前 文件夹name
    for p in pathList:

        tempPath = os.path.join(dstPath, p)

        if os.path.isdir(tempPath):
            pass

            doReplaceFolderNameInPath(replaceRule, tempPath)
            # if 

            for action in actions:
                matchPrefix = action["matchPrefix"]
                replaceStr = action["replace"].replace("newProjectName", newProjectName)

                if p.startswith(matchPrefix):
                    print "doReplaceFolderNameInPath change %s" % tempPath

                    newP = p.replace(matchPrefix, replaceStr, 1)
                    newPath = os.path.join(dstPath, newP)

                    os.rename(tempPath, newPath)

def doReplaceFileContent(replaceRule, dstPath):
    """
    替换文件内容
    """

    filterRuleName = replaceRule.get("filterRuleName", "")

    #get path list
    pathList = []

    if "" != filterRuleName:
        filterRule = myConfig.getFilterRuleByName(filterRuleName)

        pathList = doFilter(filterRule, dstPath)

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
                    replaceStr = action["replace"].replace("newProjectName", newProjectName)

                    if waitReplace and -1 != line.find(matchStr):
                        #替换
                        replaceCount += 1
                        line = line.replace(matchStr, replaceStr)
                        waitReplace = False

                f_w.write(line)


    print "replace %d" % replaceCount
    pass
    pass

def doReplaceFolderName(replaceRule, dstPath):

    #get path list
    doReplaceFolderNameInPath(replaceRule, dstPath)


def doReplace(replaceRule, dstPath):
    filterRuleName = replaceRule.get("filterRuleName", "")

    #get path list
    pathList = []

    if "" != filterRuleName:
        filterRule = myConfig.getFilterRuleByName(filterRuleName)

        pathList = doFilter(filterRule, dstPath)

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
                    replaceStr = action["replace"].replace("newProjectName", newProjectName)

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

    isFolder = replaceRule.get("folder", False)
    if isFolder:
        doReplaceFolderName(replaceRule, dstPath)

def replaceImpl(ruleName, dstPath):
    """
    执行一个 替换规则
    """
    rule = myConfig.getReplaceRuleByName(ruleName)

    doReplace(rule, dstPath)


def replace():
    print "**********  filter , find , replace   ***"

    dstPath = getDstFolder()

    ruleList = myConfig.getReplaceRuleList()
    for name in ruleList:
        replaceImpl(name, dstPath)

printUseage()

getNewProjectName()

replace()