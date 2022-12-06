#!/bin/sh python3
import os
import xml.etree.ElementTree as ET


config_file = ''
name = os.environ.get('USER')
# print(name)
exp_path = '/Users/'+name+'/.jenkins'
isExist = os.path.exists(exp_path)
# print(isExist)
J_HOME = os.getenv('JENKINS_HOME')

def configF_check():
    if isExist == True:
        print("Jenkins Default Dir")
        config_file = exp_path+'/config.xml'
        return config_file
    elif J_HOME != None:
        print(J_HOME)
        config_file = J_HOME+'/config.xml'
        return config_file
    else:
        print("Couldn't determine Jenkins Home")
        exit()

#Check 1: Verifies if 'No of executors' is set to 0.
def Check1():
    try:
        CF = configF_check()
        tree = ET.parse(CF)
        for ExecNum in tree.iter('numExecutors'):
            # print(ExecNum.text)
            if int(ExecNum.text) > 0:
                print("Configuration Error. The No of Executors has been set to more than zero. Severity: Medium")
                try:
                    ExecNum.text = str('0')
                except:
                    print("Error here")
        tree.write(exp_path+'/config.xml')
    except:
        print("Error Occurred while checking!!")


#Check 2: Verifies if Anonymous User read is disabled.
def Check2():
    try:
        CF = configF_check()
        tree = ET.parse(CF)
        for rAccess in tree.iter('denyAnonymousReadAccess'):
            # print(rAccess.text)
            if rAccess.text != 'true':
                print("Configuration Error. Anonymous User is granted read access. Severity: Medium")
    except:
        print("Error Occurred while checking!!")


#Check 3: Verifies if Private Security Realm is set.
def Check3():
    try:
        CF = configF_check()
        tree = ET.parse(CF)
        for sClass in tree.iter('securityRealm'):
            # print(sClass.attrib)
            if sClass.attrib['class'] == 'hudson.security.SecurityRealm$None':
                print("Configuration Error. Security Realm is set to None. Severity: High")
    except:
        print("Error Occurred while checking!!")


#Check 4: Verifies that not all users have free reign.
def Check4():
    try:
        CF = configF_check()
        tree = ET.parse(CF)
        for sClass in tree.iter('authorizationStrategy'):
            # print(sClass.attrib)
            if sClass.attrib['class'] == 'hudson.security.AuthorizationStrategy$Unsecured':
                print("Configuration Error. Anyone can do anything. Severity: High")
    except:
        print("Error Occurred while checking!!")

Check1()
Check2()
Check3()
Check4()
