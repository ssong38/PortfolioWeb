import unittest
from flask import Flask
from flask import request, redirect, url_for, render_template
import xml.etree.ElementTree as ET

# This dictionary will take all of file information according to version
dicttest = {}
# This dictionary will take all of version message according to version
versionmessage = {}
# This dictionary will be passed into index.html
webdict = {}
# This dictionary will store information according to the assignment
finaldict = {}


# process data
def processlist():
    '''
    This function is to process XML file and store them into dicttest according to the version
    Generally speaking, this keys of dicttest will be version. The value of dicttest will be another array(dict)
    Then it will take all of file of the certain version submission.
    Here, we build a new small xml file for testing purpose
    :return:
    '''
    tree = ET.ElementTree(file='/Users/AMsong/Desktop/cs242portfolio/data/test_list.xml')
    root = tree.getroot()
    name = ''
    commit = 0
    author = 'ssong38'
    date = 0

    for i in range(len(root[0])):
        subnode = root[0][i]
        file1 = root[0][i].attrib['kind']
        size = 0
        if file1 == 'dir':
            for i in range(len(subnode)):
                if subnode[i].tag == 'name':
                    name = subnode[i].text
                if i == 1:
                    commit = subnode[i].attrib['revision']
                    for child in subnode[1]:
                        if child.tag == 'author':
                            author = child.text
                        elif child.tag == 'date':
                            date = child.text
        else:
            for i in range(len(subnode)):
                if subnode[i].tag == 'name':
                    name = subnode[i].text
                if subnode[i].tag == 'size':
                    size = subnode[i].text
                if i == 2:
                    commit = subnode[i].attrib['revision']
                    for child in subnode[2]:
                        if child.tag == 'author':
                            author = child.text
                        elif child.tag == 'date':
                            date = child.text
        if commit not in dicttest.keys():
            dict1 = {}
            dicttest[commit] = []
            dict1[name] = {}
            dict1[name]['size'] = size
            dict1[name]['author'] = author
            dict1[name]['date'] = date
            dict1[name]['filetype'] = file1
            dicttest[commit].append(dict1)
        else:
            dict1 = {}
            dict1[name] = {}
            dict1[name]['size'] = size
            dict1[name]['author'] = author
            dict1[name]['date'] = date
            dict1[name]['filetype'] = file1
            dicttest[commit].append(dict1)


def processlog():
    '''
    This function is to handle log.xml. This file contains submission message.
    It's too annoying to put all of information into one dict.
    Therefore, I put all of message information into a new dict
    The key of dict is the version of submission. The value of dict is the message coming with each submission
    Here, we build a new small xml file for testing purpose
    :return:
    '''
    tree = ET.ElementTree(file='/Users/AMsong/Desktop/cs242portfolio/data/test_log.xml')
    root1 = tree.getroot()

    for i in range(len(root1)):
        root2 = root1[i]
        version = root2.attrib['revision']
        message = root2[3].text

        versionmessage[version] = message


def produceText():
    '''
    In this function, we have built two dicts.
    The first one is finaldict - categrized according to the homework
    The second one is webdict - I modified format of finaldict and add message into this webdict
    The goal of webdict is to build easy format for website to query
    Here, we build a new small xml file for testing purpose
    :return:
    '''
    for i in dicttest:
        if dicttest[i][0].keys()[0][0:13] not in finaldict.keys():
            finaldict[dicttest[i][0].keys()[0]] = {}
            finaldict[dicttest[i][0].keys()[0]][i] = dicttest[i]
        else:
            # print dicttest[i][0].keys()[0]
            finaldict[dicttest[i][0].keys()[0][0:13]][i] = dicttest[i]

    for i in finaldict:
        print i
        assiname = i
        webdict[assiname] = {}

        for j in finaldict[i]:
            versionname = j
            webdict[assiname][str(versionname)] = {}
            webdict[assiname][str(versionname)]['message'] = 'Version Messgae: ' + str(versionmessage[versionname])
            webdict[assiname][str(versionname)]['file'] = []
            webdict[assiname][str(versionname)]['file'].append(['filename', 'date', 'filetype', 'author', 'size'])
            for z in range(len(finaldict[i][j])):
                filename = finaldict[i][j][z].keys()[0]
                date = finaldict[i][j][z][filename]['date']
                filetype = finaldict[i][j][z][filename]['filetype']
                author = finaldict[i][j][z][filename]['author']
                size = finaldict[i][j][z][filename]['size']
                webdict[assiname][str(versionname)]['file'].append([filename, date, filetype, author, size])



class TestParse(unittest.TestCase):
    '''
    This class is the unittest class. It's for testing the data parse
    '''
    def testProcessList(self):
        '''
        Use this function to check the dicttest dictionary
        :return:
        '''
        processlist()
        self.assertEqual(dicttest.keys()[0], '2468')
        self.assertEqual(len(dicttest['2468']),4)

    def testProcessLog(self):
        '''
        Use this function to test the versionmessage dictionary
        :return:
        '''
        processlog()
        self.assertEqual(versionmessage.keys()[0], '2468')
        self.assertEqual(versionmessage['2468'],'previous project')

    def testProduceText(self):
        '''
        Use this function to test the webdict and finaldict dictionary
        :return:
        '''
        produceText()
        self.assertEqual(finaldict.keys(),['Assignment0'])
        self.assertEqual(finaldict['Assignment0'].keys(),['2468'])
        self.assertEqual(len(finaldict['Assignment0']['2468']), 4)

        self.assertEqual(webdict.keys(),['Assignment0'])
        self.assertEqual(len(webdict['Assignment0']),1)
        self.assertEqual(len(webdict['Assignment0']['2468']),2)
        self.assertEqual(webdict['Assignment0']['2468']['message'],'Version Messgae: previous project')
        self.assertEqual(len(webdict['Assignment0']['2468']['file']),5)

