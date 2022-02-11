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
import MySQLdb as mdb

import SkyCamera

import traceback

import readJSON

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
                    pass
                else:
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
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "INSERT INTO InfraredSensorData (DeviceID, PixelData ) VALUES('%s', '%s' )" % (MQTTJSON["id"], MQTTJSON["infrareddata"])
                #print("query=", query)
                cur.execute(query)
                con.commit()
                SkyCamera.processInfraredPicture(MQTTJSON["id"],MQTTJSON["infrareddata"])
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

                splitline = MQTTJSON["macaddress"].split(" ")
                pickaddresslist = splitline[0].split(":")
                pickaddress = pickaddresslist[4] + ":" + pickaddresslist[5]

                query = "INSERT INTO BluetoothSensorData(DeviceID, MacAddress, PickAddress, Temperature, Brightness, Moisture, Conductivity, Battery, SensorType, TimeRead, ReadCount ) VALUES('%s', '%s', '%s',  %f, %d, %d, %d, %d, '%s', '%s', %d)" % (MQTTJSON["id"], MQTTJSON["macaddress"], pickaddress, round(float(MQTTJSON["temperature"])/10.0,1), int(MQTTJSON["brightness"]), int(MQTTJSON["moisture"]), int(MQTTJSON["conductivity"]), int(MQTTJSON["battery"]),  MQTTJSON["sensorType"], MQTTJSON["timestamp"], int(MQTTJSON["readCount"]))
                #print("query=", query)
                cur.execute(query)
                con.commit()
                # also update current sensor array
                sensorUpdated = False
                for sensor in state.LatestBluetoothSensors:
                    mypickaddress = sensor['macaddress'][len(sensor['macaddress'])-5:]
                    if (mypickaddress == pickaddress):
                        print("remove pickaddress=", pickaddress)
                        state.LatestBluetoothSensors.remove(sensor)
                        # add new one in
                        myDict = MQTTJSON
                        myDict["pickaddress"] = pickaddress
                        myDict["temperature"] = round(float(myDict["temperature"])/10.0, 1)
                        state.LatestBluetoothSensors.append(myDict)
                        sensorUpdated = True
                        break
                if (sensorUpdated == False):
                    # new item 
                    myDict = MQTTJSON
                    myDict["pickaddress"] = pickaddress
                    myDict["temperature"] = round(float(myDict["temperature"])/10.0, 1)
                    state.LatestBluetoothSensors.append(myDict)
                
                #print("state.LatestBluetoothSensors =", state.LatestBluetoothSensors)

        except:
                traceback.print_exc()
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

def convertRawToTurbidity(rawTurbidity):
    Turbidity = int(-4.49*float(rawTurbidity) + 6746.0)
    if (Turbidity > 3000):
        Turbidity = 3000
    if (Turbidity < 0):
        Turbidity = 0
    return Turbidity

def convertRawLevelToLevel(rawLevel):

    # piecewise linear

    DeltaSpread = int(config.Tank_Pump_Level_Empty)- int(config.Tank_Pump_Level_Full) 
    #Level = 100*(1- (rawLevel -  int(config.Tank_Pump_Level_Full))/DeltaSpread )
    myScale = float(rawLevel)/float(config.Tank_Pump_Level_Empty)
    print("rawLeve=", rawLevel)
    print("myScale = ", myScale)
    if (myScale >= 0.85): 
        Level = 41*(1-myScale)/0.15
    else:    
        if (myScale >= 0.69): 
            Level =62*(1-myScale)/0.31
        else: 
            if (myScale >= 0.64): 
                Level =83*(1-myScale)/0.36
            else: 
                if (myScale >= 0.61): 
                    Level =100*(1-myScale)/0.39
                else:
                    Level = 100
    if (Level > 100):
        Level = 100
    if (Level < 0):
        Level = 0
    print("Level=", Level) 
    return Level

def convertRawTDSToTDS(rawTDS):

    Voltage = rawTDS*0.003 #Convert analog reading to Voltage(0.29 from 3V 5V difference)
    #print("precale voltage=", Voltage)
    #Voltage = rawTDS*0.003*0.60 #Convert analog reading to Voltage(0.29 from 3V 5V difference)
    #print("postscale voltage=", Voltage)
    TDS=(133.42/Voltage*Voltage*Voltage - 255.86*(Voltage*Voltage) + 857.39*Voltage)*0.5; #Convert voltage value to TDS value
    #print("presccale TDS=", TDS)
    #TDS=TDS*0.141 # calibration
    #print("postscale TDS=", TDS)
    

    if (TDS < 0):
        TDS = 0
    return TDS

def convertRawPhToPh(rawPh):
    phValue = (rawPh/2048)*3.3*3.5+config.pHOffset
    return phValue;

def fetch24HourData(Value):


 if (config.enable_MySQL_Logging == True):	
	    # open mysql database
	    # write log
	    # commit
	    # close
        try:

           
                
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                
                timeDelta = datetime.timedelta(minutes=24*60)
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                # 24 Hours
                query = "SELECT id, %s, TimeStamp FROM Hydroponics WHERE TimeStamp > '%s' ORDER by id ASC" % (Value, before)
                print("query=", query)
                cur.execute(query)
                records = cur.fetchall()
                Hour24 = 0.0
                Total = 0.0
                for myRecord in records:
                    Total = Total + float(myRecord[1])
                if (len(records) > 0):    
                    Hour24 = Total/len(records) 
                    
                
                return Hour24

        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

 return 0.0 


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
                rawTurbidity = float(MQTTJSON["rawturbidity"]) 
                rawLevel = float(MQTTJSON["rawlevel"]) 
                rawTDS = float(MQTTJSON["rawtds"]) 
                rawPh = float(MQTTJSON["rawph"]) 
                Turbidity = convertRawToTurbidity(rawTurbidity)
                TDS = convertRawTDSToTDS(rawTDS) 
                Level = convertRawLevelToLevel(rawLevel) 
                Ph = convertRawPhToPh(rawPh) 
                Temperature = MQTTJSON["temperature"]
                # now adjust for enabled
                # scan for wireless match to get constants
                myID = MQTTJSON["id"]
                wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
                myWireless = []
                for wireless in wirelessJSON:
                    if (myID == wireless["id"]):
                        myWireless = wireless
                        if (myWireless['hydroponics_temperature'] == "false"):
                                Temperature = -1
                        if (myWireless['hydroponics_tds'] == "false"):
                                TDS = -1
                        if (myWireless['hydroponics_ph'] == "false"):
                                Ph = -1
                        if (myWireless['hydroponics_turbidity'] == "false"):
                                Turbidity = -1
                        if (myWireless['hydroponics_level'] == "false"):
                                Level = -1
                        break;
                # insert information into state hydroponics information
                state.LatestHydroponicsValues.update({"ID" : myID})
                state.LatestHydroponicsValues.update({"Temperature" : Temperature})
                state.LatestHydroponicsValues.update({"TDS" : TDS})
                state.LatestHydroponicsValues.update({"Ph" : Ph})
                state.LatestHydroponicsValues.update({"Turbidity" : Turbidity})
                state.LatestHydroponicsValues.update({"Level" : Level})

                Temperature24Hour = fetch24HourData("Temperature")
                TDS24Hour = fetch24HourData("TDS")
                Turbidity24Hour = fetch24HourData("Turbidity")
                Ph24Hour = fetch24HourData("Ph")
                Level24Hour = fetch24HourData("Level")

                #state.LatestHydroponicsValues.update({"Timestamp" : datetime.now()})
                    
                query = "INSERT INTO Hydroponics(DeviceID, Temperature, Turbidity, RawTurbidity, TDS, RawTDS, Level, RawLevel, Ph, RawPH, Temperature24Hour, TDS24Hour, Turbidity24Hour, Ph24Hour, Level24Hour) VALUES('%s', '%6.2f', %6.2f, '%d', '%6.2f',%d, %6.2f, %6.2f, %6.2f, %d, %6.2f, %6.2f, %6.2f, %6.2f, %6.2f)" % (MQTTJSON["id"], float(Temperature), Turbidity, int(MQTTJSON["rawturbidity"]), TDS, int(MQTTJSON["rawtds"]), Level, float(MQTTJSON["rawlevel"]), Ph, int(MQTTJSON["rawph"]), Temperature24Hour, TDS24Hour, Turbidity24Hour, Ph24Hour, Level24Hour)
                
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


