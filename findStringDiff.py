#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#find i18n diff
#找到翻译没有补全的部分，并在文件前标出对应的需要补全的语种
#python ~/script/findStringDiff.py /Users/cuijin/project-ies/国际化取出多语言差异/diff ~/project-ies/hotsoon

import os
import shutil
import sys
import xml.dom.minidom as Dom
import xml.etree.cElementTree as ElementTree

count = 0
yilou = 0
houbu = 0

#将一个xml文件的所有key获取，并放入一个hashset
def getXmlHashSet(fromFile):
    global count
    result = set()
    if not (os.path.exists(fromFile)):
        return result
    print("比较文件：" + fromFile)
    tree = ElementTree.ElementTree(file = fromFile)
    root = tree.getroot()
    for item in root:
        result.add(item.attrib["name"])
    return result

#找不同，并将key对应的后缀标出
def findDiff(baseFile, outFile, compareHashSet=[[]], argument=[]):
    global count
    global houbu
    global yilou

    tree = ElementTree.ElementTree(file = baseFile)
    root = tree.getroot()
    for item in root:
        key = item.attrib["name"]
        keyAdd = ""
        try:
            # print(item.text)
            count = count + len(item.text.strip())
            print(count)
        except:
            print("----error------")
        
        diffCount = 0
        for index in range(len(compareHashSet)):
            if not (compareHashSet[index].__contains__(key)):
                keyAdd += argument[index]
                diffCount = diffCount + 1
        print(diffCount)
        try:
            if diffCount == 4:
                # houbu = houbu + len(item.text)
                houbu = houbu + 1
            elif diffCount > 0:
                # yilou = yilou + len(item.text)
                yilou = yilou + 1
        except:
            print("-----翻译统计error------")

        item.attrib["name"] = keyAdd + item.attrib["name"]
    print("写入--------------" + outFile)
    tree.write(outFile, encoding="UTF-8")

#找到差异并输出到对应的文件夹
def findAllPath(fromPath, toPath):
    for path in os.listdir(fromPath):
        print("copy====> " + path)
        if os.path.isdir(os.path.join(fromPath, path)):
            destPath = ""
            destComparePath = []
            if os.path.exists(toPath + "/" + path + "/src/main/res/values"):
                destPath =  toPath + "/" + path + "/src/main/res/values"
            elif os.path.exists(toPath + "/" + path + "/res/values"):
                destPath = toPath + "/" + path + "/res/values"
            elif os.path.exists(toPath + "/" + path + "/demo/res/values"):
                destPath = toPath + "/" + path + "/demo/res/values"
            
            destComparePath = [destPath + "-pt", destPath + "-ja", destPath + "-en", destPath + "-in"]
            for stringPath in os.listdir(destPath):
                if (stringPath.__contains__("string")):
                    print(stringPath)
                    compareNode = [getXmlHashSet(os.path.join(destPath + "-pt", stringPath)), getXmlHashSet(os.path.join(destPath + "-ja", stringPath)), getXmlHashSet(os.path.join(destPath + "-en", stringPath)), getXmlHashSet(os.path.join(destPath + "-in", stringPath))]
                    compareParam = ["___pt___", "___ja___", "___en___", "___in___"]
                    findDiff(os.path.join(destPath, stringPath), os.path.join(os.path.join(fromPath, path), stringPath), compareNode, compareParam)

findAllPath(sys.argv[1], sys.argv[2])
print(count)
print(houbu)
print(yilou)