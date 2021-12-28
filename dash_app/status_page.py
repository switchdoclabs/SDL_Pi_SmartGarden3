import random
import subprocess
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import plotly.express as px 
import plotly.graph_objs as go

import datetime
import traceback
import sys
import psutil

# SGS imports
sys.path.append("../")

import state
import config
import readJSON
import json


import gpiozero

# demo mode
useRandom = False

# read JSON

readJSON.readJSON("../")
readJSON.readJSONSGSConfiguration("../")

import MySQLdb as mdb



################
# Status Page
################
def returnLatestValveRecord(myID):
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "SELECT State FROM ValveRecord WHERE( DeviceID = '%s')  ORDER BY TimeStamp DESC LIMIT 1" % (myID)
                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                #print ("Query records=", records)
                if (len(records) == 0):
                    return "V00000000" 
                return records[0][0]
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()


def returnLowestSensorValue(SensorType, timeDelta):
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT * FROM Sensors WHERE( SensorValue = ( SELECT MIN(SensorValue) FROM Sensors WHERE (TimeStamp > '%s') ) AND (SensorType = '%s') AND (TimeStamp > '%s')) ORDER BY TimeStamp DESC LIMIT 1" % (before,SensorType, before)
                print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                print ("Query records=", records)
                
                return records
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()





from vcgencmd import Vcgencmd

#########################
# vcgencmd get_throttled
#########################
 
def getPiThrottled():
 
    vcgm = Vcgencmd()
    thrott_state = vcgm.get_throttled()
    # print("Get Throttled = ", thrott_state)

    return thrott_state


#####################
#
#####################

GREEN = "#2bff00"

def returnPiThrottledColor(id):
     piUVDColor   = GREEN
     piAFCColor   = GREEN
     piCTColor    = GREEN
     piSTLAColor  = GREEN
     piUVHOColor  = GREEN
     piAFCHOColor = GREEN
     piSTLHOColor = GREEN
     piATHOColor  = GREEN
     piSTLHOColor = GREEN
 
     throttle_states = getPiThrottled()
     #print ("Throttle tilanne: ", throttle_states)

     for bit in throttle_states['breakdown']:
         #print("Now: ", bit)
         if  throttle_states['breakdown'][bit]:
             #print("State:", throttle_states['breakdown'][bit])
             if   bit == '0':
                  piUVDColor = "red"
             elif bit == '1':
                  piAFCColor = "red" 
             elif bit == '2':
                  piCTColor = "red"
             elif bit == '3':
                  piSTLAColor = "red"
             elif bit == '16':
                  piUVHOColor = "red"
             elif bit == '17':
                  piAFCHOColor = "red"
             elif bit == '18':
                  piATHOColor = "red"
             elif bit == '19': 
                  piSTLHOColor = "red"


     if (id['index'] == 100):
        return piUVDColor
     if (id['index'] == 110):
        return piAFCColor
     if (id['index'] == 111):
        return piCTColor
     if (id['index'] == 112):
        return piSTLAColor
     if (id['index'] == 113):
        return piUVHOColor
     if (id['index'] == 114):
        return piAFCHOColor
     if (id['index'] == 115):
        return piATHOColor
     if (id['index'] == 116):
        return piSTLHOColor
     return "orange"

#####################
#
#####################
 
def returnPiThrottled():
 
     totalLayout = []
     piLabelLayout = []
     piIndicatorLayout = []
 
     piUVDColor   = GREEN
     piAFCColor   = GREEN
     piCTColor    = GREEN
     piSTLAColor  = GREEN
     piUVHOColor  = GREEN
     piAFCHOColor = GREEN
     piSTLHOColor = GREEN
     piATHOColor  = GREEN
     piSTLHOColor = GREEN
 
     throttle_states = getPiThrottled()
     #print ("Throttle tilanne: ", throttle_states)

     for bit in throttle_states['breakdown']:
         #print("Now: ", bit)
         if  throttle_states['breakdown'][bit]:
             #print("State:", throttle_states['breakdown'][bit])
             if   bit == '0':
                  piUVDColor = "red"
             elif bit == '1':
                  piAFCColor = "red" 
             elif bit == '2':
                  piCTColor = "red"
             elif bit == '3':
                  piSTLAColor = "red"
             elif bit == '16':
                  piUVHOColor = "red"
             elif bit == '17':
                  piAFCHOColor = "red"
             elif bit == '18':
                  piATHOColor = "red"
             elif bit == '19': 
                  piSTLHOColor = "red"

     piLabelLayout.append(

                     html.H6(["Pi CPU Throttled Status (Green=Good, Red=Bad)  ", html.A("Info-link", href="https://pypi.org/project/vcgencmd")])
                     ,
                     )

     piIndicatorLayout.append(
            daq.Indicator(
                        id = {'type' : 'VSPdynamic', 'index': 100},
                        color = piUVDColor,
                        label="Under-volted",
                        value=True,
                        style={
                            'margin': '10px'
                        }
                    )
                    )

     piIndicatorLayout.append(
            daq.Indicator(
                        id = {'type' : 'VSPdynamic', 'index': 110},
                        color = piAFCColor,
                        label="Capped",
                        value=True,
                        style={
                            'margin': '10px'
                        }
                    )
                    )

     piIndicatorLayout.append(
            daq.Indicator(
                        id = {'type' : 'VSPdynamic', 'index': 111},
                        color = piCTColor,
                        label="Throttled",
                        value=True,
                        style={
                            'margin': '10px'
                        }
                    )
                    )

     piIndicatorLayout.append(
            daq.Indicator(
                        id = {'type' : 'VSPdynamic', 'index': 112},
                        color = piSTLAColor,
                        label="Soft temp limit",
                        value=True,
                        style={
                            'margin': '10px'
                        }
                    )
                    )

     piIndicatorLayout.append(
            daq.Indicator(
                        id = {'type' : 'VSPdynamic', 'index': 113},
                        color = piUVHOColor,
                        label="Has Under-volted",
                        value=True,
                        style={
                            'margin': '10px'
                        }
                    )
                    )

     piIndicatorLayout.append(
            daq.Indicator(
                        id = {'type' : 'VSPdynamic', 'index': 114},
                        color = piAFCHOColor,
                        label="Has Capped",
                        value=True,
                        style={
                            'margin': '10px'
                        }
                    )
                    )

     piIndicatorLayout.append(
            daq.Indicator(
                        id = {'type' : 'VSPdynamic', 'index': 115},
                        color = piATHOColor,
                        label="Has Throttled",
                        value=True,
                        style={
                            'margin': '10px'
                        }
                    )
                    )

     piIndicatorLayout.append(
            daq.Indicator(
                        id = {'type' : 'VSPdynamic', 'index': 116},
                        color = piSTLHOColor,
                        label="Has Soft temp limit",
                        value=True,
                        style={
                            'margin': '10px'
                        }
                    )
                    )


     totalLayout.append(dbc.Row(piLabelLayout))
     totalLayout.append(dbc.Row(piIndicatorLayout))

     return totalLayout


def getBluetoothData():
    
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "SELECT * FROM `BluetoothSensors` ORDER BY id ASC" 

                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                #print ("Query records=", records)
                bluelist = []            
                for record in records:
                   bluelist.append(record) 
                return bluelist
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

        return [] 

def getLastBTReading(btaddress):
    
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "SELECT * FROM `BluetoothSensorData` WHERE (MacAddress = '%s') ORDER BY id DESC LIMIT 1" % (btaddress) 

                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                #print ("Query records=", records)
                if (len(records) == 0):
                    return []
                return records[0]
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

        return [] 

def returnIndicatorValue(state, number):
    if (state[number] == "0"):
        return False
    else:
        return True

def returnIndicators():
    totalLayout = []
    PiThrottled = returnPiThrottled()
    totalLayout.append(dbc.Row(PiThrottled))    
    totalLayout.append(dbc.Row(html.H2("Extender Devices")))
    wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
    for singleWireless in wirelessJSON:
        myLabelLayout = [] 
        
        valveStatus =  returnLatestValveRecord(singleWireless['id'] )

        myLabelLayout.append(
                 
                     html.H6(singleWireless['name'] +"/"+singleWireless['id'],
		     )
                     )
        myIndicatorLayout = [] 
        for valve in range(1,9):

            currentValue = returnIndicatorValue(valveStatus, valve)
            if (currentValue):
                myColor = "greenyellow"
            else:
                myColor = "red"
            myIndicatorLayout.append( daq.Indicator(
                        id = {'type' : 'SPVdynamic', 'index': valve  , 'DeviceID' : singleWireless['id'] },
                        color = myColor,
                        label="Valve "+str(valve),
                        value=True,
                        style={
                            'margin': '10px'
                        }
                    )
                    )
            #myIndicatorCount = myIndicatorCount +1
        totalLayout.append(dbc.Row( myLabelLayout))
        totalLayout.append(dbc.Row(myIndicatorLayout))
    
    totalLayout.append(dbc.Row(html.H2("Bluetooth Sensors")))
   
    # now do Bluetooth Sensors
    myBTSensors = getBluetoothData()
    #print("BTSensors=", myBTSensors)
    #shortBTSensors = []
    #shortBTSensors.append(myBTSensors[0])
    #myBTSensors = shortBTSensors
    #print("BTSensors=", myBTSensors)
    for sensor in myBTSensors:
        # fetch Bluetooth Sensor Data
        mySensorData = getLastBTReading(sensor[2])
        # green if > 10 , red if < 10
        moistureIndicator = "gray"
        # green if > 10, red if less
        batteryIndicator = "gray"
        # not active if data is older than 1 Hour 
        activeIndicator = "gray"

        #print("mySensorData=", mySensorData)

        #check for null record
        if (len(mySensorData) == 0):
            # No sensor, all gray
            moistureIndicator = "gray"
            batteryIndicator = "gray"
            activeIndicator = "gray"
        else:
            # now do the active calculations
            sampleTimestamp =  mySensorData[2]
            #print("sampleTimeStamp =", sampleTimestamp)
            activeSpan = datetime.timedelta(hours=1)
            timespan = datetime.datetime.now() - sampleTimestamp
            #print("timespan=", timespan)
            if (timespan > activeSpan):
                #print("too old")
                moistureIndicator = "gray"
                batteryIndicator = "gray"
                activeIndicator = "red"
            else:
                #print("active")
                activeIndicator = "greenyellow"
                # now check for other
                myBattery = int(mySensorData[9])
                myMoisture = int(mySensorData[7])
                if (myBattery < 10):
                    batteryIndicator = "red"
                else:
                    batteryIndicator = "greenyellow"
                if (myMoisture < 10):
                    moistureIndicator = "red"
                else:
                    moistureIndicator = "greenyellow"

        mySensorLayout= []
        mySensorLayout.append(
                     
                     html.H6(sensor[3] +" / "+sensor[5]+ " / "+sensor[4],
		                    )
                        )
        myIndicatorLayout = [] 
        
        myIndicatorLayout.append( daq.Indicator(
                        id = {'type' : 'SPBdynamic', 'index': sensor[2]  , 'DeviceID' : 'BTIndicator', 'Indicator' : 0  },
                        color = moistureIndicator,
                        label="Moisture Fault ",
                        value=True,
                        style={
                            'margin': '10px'
                        }
                       )
                     )
       
        
        myIndicatorLayout.append( daq.Indicator(
                        id = {'type' : 'SPBdynamic', 'index': sensor[2]  , 'DeviceID' : 'BTIndicator', 'Indicator' : 1 },
                        color = batteryIndicator,
                        label="Battery Status",
                        value=True,
                        style={
                            'margin': '10px'
                        }
                       )
                     )
       
        myIndicatorLayout.append( daq.Indicator(
                        id = {'type' : 'SPBdynamic', 'index': sensor[2]  , 'DeviceID' : 'BTIndicator', 'Indicator' : 2 },
                        color = activeIndicator,
                        label="Device Reporting ",
                        value=True,
                        style={
                            'margin': '10px'
                        }
                       )
                     )
       
       
        totalLayout.append(dbc.Row(mySensorLayout))
        totalLayout.append(dbc.Row(myIndicatorLayout))
    # fetch latest value
   
    # setup each indicator appropriately
    return totalLayout

################
# Page Functions
################

def countBluetooth():

 if (config.enable_MySQL_Logging == True):	
	# open mysql database
	# write log
	# commit
	# close
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "SELECT * From BluetoothSensors " 
                #print("query=", query)
                cur.execute(query)
                myRecords = cur.fetchall()
                #print ('myRecords=',myRecords)
                return len(myRecords) 
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur
                del con
        return 0  

def generateMyTypeOfAlarm(alarm):
        myMoisture = alarm[16]
        myTemperature = alarm[17]
        myType = ""
        AlarmFired = False
            
        if ((alarm[16] != None) and (alarm[5] == "True")):
                
            if (myMoisture < int(alarm[6])):
                print(">>>>Low moisture alarm!")
                myType = myType + "/ Low Moisture: %d < %d" % (myMoisture, int(alarm[6]))
                AlarmFired = True
            else:
                if (myMoisture > int (alarm[7])):
                    print(">>>>High moisture alarm!")
                    myType = myType + "/ High Moisture: %d > %d" % (myMoisture, int(alarm[6]))
                    AlarmFired = True

            
        # temperature alarm
        if ((alarm[17] != None) and (alarm[8] == "True")):
            print("temperature check")
            if (myTemperature < int(alarm[9])):
                print(">>>>Low Temperature alarm!")
                myType = myType + "/ Low Temperature: %d < %d" % (myTemperature, int(alarm[9]))
                AlarmFired = True
            else:
                if (myTemperature > int (alarm[10])):
                    print(">>>>High Temperature alarm!")
                    myType = myType + "/ High Temperature: %d > %d" % (myTemperature, int(alarm[9]))
                    AlarmFired = True
        

            
        if (AlarmFired == False):
         myType = "No Alarm" 
            
        return myType 

def  generateCurrentAlarms():

    myCurrentAlarmLayout = []
    try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()

                query = "SELECT * FROM Alarms"

                print("query=", query)
                cur.execute(query)
                myRecords = cur.fetchall()
    except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                myRecords = []
    finally:
                cur.close()
                con.close()

                del cur
                del con

    AlarmFound = False
    for alarm in myRecords:
        if (alarm[12] != None):
            myType = generateMyTypeOfAlarm(alarm)
            if (myType != ""):
                if (myType != "No Alarm"):
                    myAlarm = "Alarm Address: %s %s"  % (alarm[4], myType)
                    myCurrentAlarmLayout.append(dbc.Alert(myAlarm, color="danger"))
                    AlarmFound = True
            
    if (AlarmFound == False):
           myCurrentAlarmLayout.append(dbc.Alert("No Alarms"))

                
    return myCurrentAlarmLayout 
def StatusPage():


    wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
    numberOfWireless = len(wirelessJSON)
    numberOfValves = numberOfWireless * 8
    numberOfSensors = countBluetooth()
    f = open("/proc/device-tree/model")
    piType = f.read()
    boottime =datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S") 
    
    Row1 = html.Div(
        [
                    dbc.Button(
                        ["Number of Wireless Units", dbc.Badge(numberOfWireless, color="light", className="ml-1")],
                        color="primary",),
                    dbc.Button(
                        ["Number of Valves", dbc.Badge(numberOfValves, color="light", className="ml-1")],
                        color="primary",),
                    dbc.Button(
                        ["Number of BluetoothSensors", dbc.Badge(numberOfSensors, color="light", className="ml-1")],
                        color="primary",),
                    dbc.Button(
                        ["Number of Hydroponic Units", dbc.Badge("1", color="light", className="ml-1")],
                        color="primary",),
                    dbc.Button(
                        ["Raspberry Pi", dbc.Badge(piType, color="light", className="ml-1")],
                        color="primary",),
                    dbc.Button(
                        ["SGS Start Time ", dbc.Badge(boottime, color="light", className="ml-1")],
                        color="primary",),
                    dbc.Button(
                        ["Pi Boot Time ", dbc.Badge(boottime, color="light", className="ml-1")],
                        color="primary",),
        ])

    Row2 = dbc.Row(
                [
                    daq.Gauge(
                        id = {'type' : 'SPGdynamic', 'GaugeType' :'pi-loading'},
                        label="Pi CPU Loading",
                        value=0,
                        color={"gradient":True,"ranges":{"green":[0,50],"yellow":[50,85],"red":[85,100]}},
                        showCurrentValue=True,
                        units="%",
                        size=190,
                        max = 100,
                        min = 0,
                    ),
                    daq.Gauge(
                        id = {'type' : 'SPGdynamic', 'GaugeType' :'pi-memory'},
                        label="Pi Memory Usage",
                        value=0,
                        color={"gradient":True,"ranges":{"green":[0,50],"yellow":[50,85],"red":[85,100]}},
                        min = 0,
                        max=100,
                        size=190,
                        showCurrentValue=True,
                        units="%",

                    ),
                    daq.Gauge(
                        id = {'type' : 'SPGdynamic', 'GaugeType' :'pi-disk'},
                        label="Pi Disk Free",
                        value=0,
                        showCurrentValue=True,
                        units="%",
                        size=190,
                        color={"gradient":True,"ranges":{"red":[0,30],"yellow":[30,65],"green":[65,100]}},
                        max = 100,
                        min = 0,
                        ),


                    daq.Gauge(
                        id = {'type' : 'SPGdynamic', 'GaugeType' :'pi-temp'},
                        label="Pi CPU Temperature(C)",
                        value=0,
                        color={"gradient":True,"ranges":{"green":[0,50],"yellow":[50,85],"red":[85,130]}},
                        showCurrentValue=True,
                        units="C",
                        size=190,
                        max = 130,
                        min = 0,
                    ),

                ],
		no_gutters=True,

		)

    Layouts = returnIndicators()
    Row3 = html.Div(
                   Layouts ,
         )

    Row5 = html.Div(html.H2("Active Alarms"))

    myAlarmLayout = html.Div(
                        dbc.Container(
                        id={'type' : 'SPAdynamic', 'index' :"activealarms"},
                        children=generateCurrentAlarms() 
                        ))



    print("myAlarmLayout=", myAlarmLayout)
    Row4 = html.Div(
            [
    html.Div(id='log')
            ]
            )
    #print("SPRow2=", Row2)
    #print("SPRow5=", Row5)
    
    layout = dbc.Container([
        Row1, Row2, Row5, myAlarmLayout, Row3, Row4],
        #Row1, Row2, Row5, Row3, Row4],
        className="status-1",
    )
    return layout


####
# Callback functions
####
def updateIndicator(myValue ):

    if (useRandom == True):
    	myValue = random.randint(0,1)

    if (myValue ==1):
        myColor = "greenyellow"
    else:
        myColor = "red"

        
    return myColor

def updateGauges(id):
    myValue = 0
    #if (useRandom == True):
    #   myValue = random.randint(0,100)
    #   return myValue

    # update Lowest Percent Moisture Sensor
    if (id['GaugeType'] == "pi-disk"):
        #timeDelta = datetime.timedelta(days = 5)
        #myRecord = returnLowestSensorValue("C1", timeDelta)
        #print("driestValue=",myRecord)
        #return (myRecord[0][1],myRecord[0][2], myRecord[0][3],myRecord[0][5])
        myValue = psutil.disk_usage('/')
        myDPercent = myValue[3]
        #print("myDPercent=", myDPercent)
        myDPercent = 100.0 - myDPercent
        #print("myDPercent=", myDPercent)
        return myDPercent 

		
    # update CPU Loading
    if (id['GaugeType'] == "pi-loading"):
        myValue = psutil.cpu_percent()
        return myValue


    # update Pi Memory usage
    if (id['GaugeType'] == "pi-memory"):
    	myValue = psutil.virtual_memory().percent
    	return myValue

    # update Pi Memory usage
    if (id['GaugeType'] == "pi-temp"):
        cpu = gpiozero.CPUTemperature()
        CPUTemperature = cpu.temperature
        myValue = CPUTemperature
        return myValue



