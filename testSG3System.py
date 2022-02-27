#!/usr/bin/env python3
#
# Test SG3 System and Connectivity to a Wireless Extender
# SwitchDoc Labs
# January 2022

# set SGSEXT_IP to the IP address of your connected Wireless Extender to be tested
# Example:  SGSEXT_IP = "192.168.1.52"
SGSEXT_IP = ""

import sys, traceback
import os
import time
import config
import datetime
import requests
import socket
import subprocess



def sendCommandToWireless(myIP, myCommand):
        myURL = 'http://'+str(myIP)+'/'+myCommand
        print ("sending REST URL = ", myURL) 
        try:
                req = requests.get(myURL,timeout=30)
                returnJSON = req.json()

        except Exception:
                traceback.print_exc()
                return {} 
        return returnJSON 


def turnOnTimedValve(singleValve):

        myIP = singleValve["ipaddress"]

        myCommand = "setSingleValve?params=admin,"+str(singleValve["ValveNumber"])+",1,"+str(singleValve["OnTimeInSeconds"])
        return sendCommandToWireless(myIP, myCommand)

def turnOnAndReadMoistureSensors():
    myJSON = sendCommandToWireless(SGSEXT_IP, "testHydroponicsSensors?params=admin")
    return myJSON

def get_ip_address():
 ip_address = '';
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 s.connect(("8.8.8.8",80))
 ip_address = s.getsockname()[0]
 s.close()
 return ip_address

def setMQTT_IP():
        myMQTTIP = get_ip_address()
        myMQTTPort  = 1883
        myURL = 'checkForID?params='+myMQTTIP+','+str(myMQTTPort)
        myJSON = sendCommandToWireless(SGSEXT_IP, myURL)

# Main Program
if __name__ == '__main__':


    print("###########################")
    print("SmartGarden3 System Test")
    print("###########################")
    print('%s' % datetime.datetime.now())
    print()
    if (SGSEXT_IP == ""):
        print("###########################")
        print("Error: MUST SET SGSEXT_IP to run Wireless Extender test")
        print("###########################")
        exit()
    print("Wireless Extender Address Test Requested = ", SGSEXT_IP)


    print("###########################")
    print("Starting Wireless Extender Test")
    print("###########################")

    # test Connection to Wireless Extender
    setMQTT_IP()

    singleValve = {}
    singleValve["id"] = "TEST"
    singleValve["ipaddress"] = SGSEXT_IP
    singleValve["OnTimeInSeconds"] = "20"
    singleValve["ValveNumber"] = "1"
    myJSON = turnOnTimedValve(singleValve)


    if (len(myJSON) == 0):
        print("###########################")
        print("Wireless Extender ", SGSEXT_IP)
        print("NOT RESPONDING")
        print("###########################")
    else:
        print("###########################")
        print("Turning On USB1 Valve for 10 seconds on Extender: ", SGSEXT_IP)
        print("###########################")
        print("Wireless Extender: ", SGSEXT_IP)
        print("Successfuly Responding")
        print("###########################")
        print(myJSON)
        print("###########################")
        time.sleep(5)
        print("ADC Sensors:")
        myJSON = turnOnAndReadMoistureSensors()
        print(myJSON)
        print("###########################")

