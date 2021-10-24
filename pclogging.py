from __future__ import print_function
#
#
# logging system from Project Curacao 
# filename: pclogger.py
# Version 1.0 10/04/13
#
# contains logging data 
#



import sys
import time
import datetime
# Check for user imports
import config

import state
import updateBlynk
import MySQLdb as mdb

import SkyCamera

import traceback


def systemlog(level,  message):


 if (config.enable_MySQL_Logging == True):	
   LOWESTDEBUG = 0
	# open mysql database
	# write log
	# commit
	# close

   if (level >= LOWESTDEBUG):
        try:
                if (level == config.JSON):
                    if (config.USEBLYNK):
                        updateBlynk.blynkTerminalUpdate("JSON Loaded") 
                    pass
                else:
                    if (config.USEBLYNK):
                        updateBlynk.blynkTerminalUpdate(message) 
                    pass
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                #print "before query"
                query = "INSERT INTO SystemLog(TimeStamp, Level, SystemText ) VALUES(LOCALTIMESTAMP(), %i, '%s')" % (level, message)
                #print("query=%s" % query)
                cur.execute(query)
                con.commit()


        except: 
                traceback.print_exc()
                con.rollback()
                #sys.exit(1)
        finally:
                cur.close()
                con.close()

                del cur
                del con


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

def processInfraredSensor(MQTTJSON):
 if (config.enable_MySQL_Logging == True):	
	# open mysql database
	# write log
	# commit
	# close
        try:
                print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "INSERT INTO InfraredSensorData (DeviceID, PixelData ) VALUES('%s', '%s' )" % (MQTTJSON["id"], MQTTJSON["infrareddata"])
                print("query=", query)
                cur.execute(query)
                con.commit()
                SkyCamera.processInfraredPicture(MQTTJSON["infrareddata"])
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur
                del con


def processBluetoothSensor(MQTTJSON):
 if (config.enable_MySQL_Logging == True):	
	# open mysql database
	# write log
	# commit
	# close
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "INSERT INTO BluetoothSensorData(DeviceID, MacAddress, Temperature, Brightness, Moisture, Conductivity, Battery, SensorType, TimeRead, ReadCount ) VALUES('%s', '%s', %f, %d, %d, %d, %d, '%s', '%s', %d)" % (MQTTJSON["id"], MQTTJSON["macaddress"], round(float(MQTTJSON["temperature"])/10.0,1), int(MQTTJSON["brightness"]), int(MQTTJSON["moisture"]), int(MQTTJSON["conductivity"]), int(MQTTJSON["battery"]),  MQTTJSON["sensorType"], MQTTJSON["timestamp"], int(MQTTJSON["readCount"]))
                #print("query=", query)
                cur.execute(query)
                con.commit()
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur
                del con


def sensorlog(DeviceID, SensorNumber, SensorValue, RawSensorValue, SensorType, TimeRead ):
 if (config.enable_MySQL_Logging == True):	
	# open mysql database
	# write log
	# commit
	# close
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "INSERT INTO Sensors(DeviceID, SensorNumber, SensorValue, RawSensorValue, SensorType, TimeRead ) VALUES('%s', '%s', %f, %s, '%s', '%s')" % (DeviceID, SensorNumber, float(SensorValue), RawSensorValue, SensorType, TimeRead)
                #print("query=", query)
                cur.execute(query)
                con.commit()
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur
                del con



def getValveState(id):
 if (config.enable_MySQL_Logging == True):	
	# open mysql database
	# write log
	# commit
	# close
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "SELECT * From ValveRecord WHERE DeviceID = '%s' ORDER BY ID DESC LIMIT 1" % id
                #print("query=", query)
                cur.execute(query)
                myRecords = cur.fetchall()
                #print ('myRecords=',myRecords)
                if (len(myRecords) == 0):
                    return "V0000000"
                return  myRecords[0][2]
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur
                del con
        

def valvelog(DeviceID, ValveNumber, State, Source, ValveType, Seconds):
 if (config.enable_MySQL_Logging == True):	
	# open mysql database
	# write log
	# commit
	# close
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "INSERT INTO ValveChanges(DeviceID, ValveNumber, State, Source, ValveType, SecondsOn ) VALUES('%s', '%s', %d, '%s', '%s',%d)" % (DeviceID, ValveNumber, int(State), Source, ValveType, int(Seconds))
                #print("query=", query)
                cur.execute(query)
                con.commit()
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                #con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur
                del con



def writeMQTTValveChangeRecord(MQTTJSON):

 if (config.enable_MySQL_Logging == True):	
	# open mysql database
	# write log
	# commit
	# close
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "INSERT INTO ValveRecord(DeviceID, State) VALUES('%s', '%s')" % (MQTTJSON['id'], MQTTJSON['valvestate'])
                #print("query=", query)
                cur.execute(query)
                con.commit()
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur
                del con

        return "V00000000"

def readLastHour24AQI():

 if (config.enable_MySQL_Logging == True):	
	# open mysql database
	# write log
	# commit
	# close
        try:

                # first calculate the 24 hour moving average for AQI
                
                print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()

                query = "SELECT id, AQI24Average FROM WeatherData ORDER BY id DESC Limit 1" 

                cur.execute(query)
                myAQIRecords = cur.fetchall()
                if (len(myAQIRecords > 0)):
                    state.Hour24_AQI = myAQIRecords[0][1]
                else:
                    state.Hour24_AQI = 0.0 

                #print("AQIRecords=",myAQIRecords)

        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur

def writeHydroponicsRecord(MQTTJSON):

 if (config.enable_MySQL_Logging == True):	
	# open mysql database
	# write log
	# commit
	# close
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                # convert to values
                Turbidity = -1;
                TDS = -1;
                Level = -1;
                Ph = -1;
                query = "INSERT INTO Hydroponics(DeviceID, Temperature, Turbidity, RawTurbidity, TDS, RawTDS, Level, RawLevel, Ph, RawPH) VALUES('%s', '%6.2f', %6.2f, '%d', '%6.2f',%d, %6.2f, %6.2f, %6.2f, %d)" % (MQTTJSON["id"], float(MQTTJSON["temperature"]), Turbidity, int(MQTTJSON["rawturbidity"]), TDS, int(MQTTJSON["rawtds"]), Level, float(MQTTJSON["rawlevel"]), Ph, int(MQTTJSON["rawph"]))
                
                print("query=", query)
                cur.execute(query)
                con.commit()
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

                del cur
                del con


