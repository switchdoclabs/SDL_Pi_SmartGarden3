#!/usr/bin/env python3

#
# Smart Garden 3
#
# SwitchDoc Labs
#

from __future__ import division
from __future__ import print_function
from builtins import range
from past.utils import old_div

SGSVERSION = "055"

#imports 

import sys, traceback
import os
import RPi.GPIO as GPIO
import time
import threading
import json
import pickle
import picamera
import subprocess

import SkyCamera
import readJSON

import logging; 
logging.basicConfig(level=logging.ERROR) 


import bluetoothSensor
#appends

import InitExtenders
from neopixel import *

import MySQLdb as mdb

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import PictureManagement

import sendemail


import datetime

from apscheduler.schedulers.background import BackgroundScheduler

import apscheduler.events

import scanForResources


import config

if (config.enable_MySQL_Logging == True):
            import MySQLdb as mdb

import pclogging

import state

import Valves

import alarms

import AccessValves

import wiredSensors

#initialization

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

################
# Update State Lock - keeps smapling from being interrupted (like by checkAndWater) - Locks I2C Access
################
state.UpdateStateLock = threading.Lock()



import util

###############
# MQTT Setup for Wireless
###############

import MQTTFunctions




################
# BMP280 Setup 
################

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus



################
# SkyCamera Setup 
################


#Detect Camera WeatherSTEMHash
try:

    with picamera.PiCamera() as cam:
        if (config.SWDEBUG):
            print("Pi Camera Revision",cam.revision)
        cam.close()
    config.GardenCam_Present = True
except:
    config.GardenCam_Present = False

### set up directory
os.makedirs("static/SkyCam", exist_ok=True)


#############################
# apscheduler setup
#############################
# setup tasks
#############################

def tick():
    print('Tick! The time is: %s' % datetime.datetime.now())


def killLogger():
    state.scheduler.shutdown()
    print("Scheduler Shutdown....")
    exit()


def checkAndWater():


    pass


def ap_my_listener(event):
        if event.exception:
              print(event.exception)
              print(event.traceback)


def returnStatusLine(device, state):

        returnString = device
        if (state == True):
                returnString = returnString + ":   \t\tPresent"
        else:
                returnString = returnString + ":   \t\tNot Present"
        return returnString


#############################
# get and store sensor state
#############################

def checkForButtons():

    pass

    


def centerText(text,sizeofline):
        textlength = len(text)
        spacesCount = old_div((sizeofline - textlength),2)
        mytext = ""
        if (spacesCount > 0):
                for x in range (0, spacesCount):
                        mytext = mytext + " "
        return mytext+text

#############################
# initialize Smart Garden System
#############################

def initializeSGSPart1():
    print("###############################################")
    print("SG3 Version "+SGSVERSION+"  - SwitchDoc Labs")
    print("###############################################")
    print("")
    print("Program Started at:"+ time.strftime("%Y-%m-%d %H:%M:%S"))
    print("")
    
    
    
    # read in JSON
    # read in JSON
    if (readJSON.readJSON("") == False):
        print("#############################")
        print("No SGS.JSON file present - configure with 'sudo python3 SGSConfigure.py'")
        print("#############################")
        exit()

        
    readJSON.readJSONSGSConfiguration("")

    if (config.mailPassword != "yourmailpassword"):
        # try to send email for start
        sendemail.sendEmail("test", "SG3 Version %s"%SGSVERSION, "SmartGarden3 Startup ", config.notifyAddress,  config.fromAddress, "");



    #init blynk app state
    message = "SGS Version "+SGSVERSION+" Started"
    pclogging.systemlog(config.INFO,message)
    pclogging.systemlog(config.JSON,"SGS.JSON Loaded: "+json.dumps(config.JSONData ))
    pclogging.systemlog(config.JSON,"SGSConfigurationJSON.JSON Loaded: "+json.dumps(config.SGSConfigurationJSON ))
    pclogging.systemlog(config.CRITICAL,"No Alarm")
    if (config.GardenCam_Present):
        pclogging.systemlog(config.INFO,"Garden Cam Present")
    else:
        pclogging.systemlog(config.INFO,"Garden Cam NOT Present")
        
    # scan and check for resources

    alarms.readAlarmConfiguration()
    alarms.clearAllAlarms()
    alarms.readAlarmConfiguration()

    pass

def initializeSGSPart2():

        # status reports
    
        print("----------------------")
        print("Local Devices")
        print("----------------------")
        #print(returnStatusLine("Sunlight Sensor",config.Sunlight_Present))
        #print(returnStatusLine("hdc1000 Sensor",config.hdc1000_Present))
        #print(returnStatusLine("Ultrasonic Level Sensor",config.UltrasonicLevel_Present))
    
        print("----------------------")
        print("Checking Wireless SGS Devices")
        print("----------------------")
    
        scanForResources.updateDeviceStatus(True)

        bluetoothSensor.assignBluetoothSensors()
 
        # turn off All Valves
        AccessValves.turnOffAllValves()
    
        wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
        for single in wirelessJSON:
            print(returnStatusLine(str(single["name"])+" - "+str(single["id"]),state.deviceStatus[str(single["id"])]))
    
   
        # Set up Wireless MQTT Links
        MQTTFunctions.startWirelessMQTTClient("SG3")
        

        # subscribe to IDs
        if (len(wirelessJSON) == 0):
            print("################################")
            print("ERROR")
            print("################################")
            print("No Wireless SGS uinits present - run SGSConfigure.py")
            print("################################")
            exit()

        for single in wirelessJSON:
            InitExtenders.initializeOneExtender(single["id"])


        # wait for connection
        while state.WirelessMQTTClientConnected != True:    #Wait for connection
            time.sleep(0.1)


        # subscribe to IDs

        for single in wirelessJSON:
            topic = "SGS/" + single["id"]
            print("subscribing to ", topic)
            state.WirelessMQTTClient.subscribe(topic)
            # write out to ValveChanges for startup
            myJSON = {}
            myJSON["id"] = single["id"]
            myJSON["valvestate"] = "V00000000"

            pclogging.writeMQTTValveChangeRecord(myJSON)

        print()
    
        print()
        print("----------------------")
        print("Plant / Sensor Counts")
        print("----------------------")
        config.valve_count = len(readJSON.getJSONValue("WirelessDeviceJSON"))*8 
        config.bluetooth_count = pclogging.countBluetooth()

        print( "Wireless Unit Count:", len(readJSON.getJSONValue("WirelessDeviceJSON")) )
        print("Valve Count: ",config.valve_count)
        print("Bluetooth Sensor Count: ",config.bluetooth_count)
        print()

        print("----------------------")
        print("Other Smart Garden System Expansions")
        print("----------------------")
        print(returnStatusLine("GardenCam",config.GardenCam_Present))
        print(returnStatusLine("Lightning Mode",config.Lightning_Mode))
        print(returnStatusLine("MySQL Logging Mode",config.enable_MySQL_Logging))
        print()
        print("----------------------")

        # Read in alarm data from mySQL

    
def initializeScheduler():


    
    
    
        state.scheduler.add_listener(ap_my_listener, apscheduler.events.EVENT_JOB_ERROR)	
    
        # prints out the date and time to console
        state.scheduler.add_job(tick, 'interval', seconds=5*60)
        
        # read wireless sensor package
        #print("Before Adding readSensors Job")
    
    
        # check device state
        state.scheduler.add_job(scanForResources.updateDeviceStatus, 'interval', seconds=6*120, args=[False])
        #state.scheduler.add_job(scanForResources.updateDeviceStatus, 'interval', seconds=60, args=[False])
    
    
   
        # sky camera
        if (config.GardenCam_Present):
           state.scheduler.add_job(SkyCamera.takeSkyPicture, 'interval', seconds=int(config.INTERVAL_CAM_PICS__SECONDS))



        # timelapse

        # SkyCam Management Programs
        state.scheduler.add_job(PictureManagement.cleanPictures, 'cron', day='*', hour=3, minute=4, args=["Daily Picture Clean"])

        state.scheduler.add_job(PictureManagement.cleanTimeLapses, 'cron', day='*', hour=3, minute=10, args=["Daily Time Lapse Clean"])
        
        state.scheduler.add_job(PictureManagement.buildTimeLapse, 'cron', day='*', hour=5, minute=30, args=["Time Lapse Generation"])



        # check for force water - note the interval difference with updateState
        #state.scheduler.add_job(forceWaterPlantCheck, 'interval', seconds=8)

        # every 10 seconds, check for button changes
        state.scheduler.add_job(checkForButtons, 'interval', seconds=10)
 
    
        # check for alarms
        #state.scheduler.add_job(alarms.checkForAlarms, 'interval', seconds=15)
        state.scheduler.add_job(alarms.checkForAlarms, 'interval', seconds=300)
    
    
    
        # MS sensor Read 
    
        # sensor timed water and Timed
        tNow  = datetime.datetime.now()
        # round to the next full hour
        tNow -= datetime.timedelta(minutes = tNow.minute, seconds = tNow.second, microseconds =  tNow.microsecond)
        state.nextMoistureSensorActivate = tNow
        
        state.scheduler.add_job(Valves.valveCheck, 'interval', minutes=1)

    
        # sensor manual water
        state.scheduler.add_job(Valves.manualCheck, 'interval', seconds=15)
    
    
    	
    	
    	
        
        
def initializeSGSPart3():

    
        state.Last_Event = "SGS Started:"+time.strftime("%Y-%m-%d %H:%M:%S")
    
    
    
        alarms.checkForAlarms()


def pauseScheduler():

    state.scheduler.print_jobs()

    jobs = state.scheduler.get_jobs()
    print("get_jobs=", jobs)
    state.scheduler.print_jobs()
    for job in jobs:
        state.scheduler.remove_job(job.id)
        
    jobs = state.scheduler.get_jobs()
    print("After get_jobs=", jobs)
    state.scheduler.pause()
    print("After get_jobs=", jobs)
    state.scheduler.print_jobs()
    pass


def restartSGS():
    state.WirelessMQTTClient.disconnect()
    state.WirelessMQTTClient.loop_stop()
    pauseScheduler()
 

    initializeSGSPart1()
    initializeSGSPart2() 
    
    initializeScheduler()       
    state.scheduler.resume()
    print("After resume=" )
    state.scheduler.print_jobs()

    initializeSGSPart3()


    pass
#############################
# main program
#############################

    # Main Program
if __name__ == '__main__':
        
    '''
    if (config.SWDEBUG):
        print("Starting pigpio daemon")

    # kill all pigpio instances
    try:
        cmd = [ 'killall', 'pigpiod' ]
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        print(output)
        time.sleep(5)
    except:
        #print(traceback.format_exc())
        pass

    cmd = [ '/usr/bin/pigpiod' ]
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    print(output)
    '''  


if (config.enable_MySQL_Logging):
    # SmartGarden3 SQL Database

    try:

        con = mdb.connect(
          "localhost",
          "root",
          config.MySQL_Password,
          "SmartGarden3"
          )

    except:
        #print(traceback.format_exc())
        print("--------")
        print("MySQL Database SmartGarden3 Not Installed.")
        print("Run this command:")
        print("sudo mysql -u root -p < SmartGarden3.sql")
        print("SmartGarden3 Stopped")
        print("--------")
        sys.exit("SmartGarden3 Requirements Error Exit")


    # Check for updates having been applied
    try:

        con = mdb.connect(
          "localhost",
          "root",
          config.MySQL_Password,
          "SmartGarden3"
          )
        cur = con.cursor()
        query = "SELECT Temperature24Hour  FROM Hydroponics"
        cur.execute(query)
    except:
        #print(traceback.format_exc())
        print("--------")
        print("MySQL Database SmartGarden3 Updates Not Installed.")
        print("Delete the SmartGarden3 Database and reinstall")
        print("sudo mysql -u root -p < SmartGarden3.sql")
        print("SmartGarden3 Stopped")
        print("--------")
        sys.exit("SmartGarden3 Requirements Error Exit")










    initializeSGSPart1()
    
    # this is the big exception clause that will turn all pumps off if there is a problem
    try: 

        initializeSGSPart2() 
        state.scheduler = BackgroundScheduler()
    
        initializeScheduler()       

        # start state.scheduler
        state.scheduler.start()
        print("-----------------")
        print("Scheduled Jobs") 
        print("-----------------")
        state.scheduler.print_jobs()
        print("-----------------")


        initializeSGSPart3()
        
        #############
        #  Main Loop
        #############
                
    
    
        while True:
           # check for new JSON files
           if (os.path.exists('NEWJSON') == True):
                # remove file
                print("-----------------------")
                print("New JSON files detected")
                print("SG3 reloading JSON configuration")
                print("-----------------------")
                os.remove('NEWJSON')
                restartSGS()
                pclogging.systemlog(config.INFO,"Reloading SGS with New JSON")
           else:
                #print("No New JSON Files Detected")
                pass

           time.sleep(10.0)
    		
    
    
    except KeyboardInterrupt:  
        	    # here you put any code you want to run before the program   
        	    # exits when you press CTRL+C  
                print("exiting program") 
        #except:  
        	    # this catches ALL other exceptions including errors.  
        	    # You won't get any error messages for debugging  
        	    # so only use it once your code is working  
                    # print "Other error or exception occurred!"  
      
    finally:  
    	    #time.sleep(5)
            #GPIO.cleanup() # this ensures a clean exit 
            AccessValves.turnOffAllValves()
    	    #saveState()
            state.WirelessMQTTClient.disconnect()
            state.WirelessMQTTClient.loop_stop()
 
            print("done")
