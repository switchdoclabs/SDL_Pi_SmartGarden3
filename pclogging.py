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
import HydroConstants

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
                #print("state.LatestBluetoothSensors =", state.LatestBluetoothSensors)
                for sensor in state.LatestBluetoothSensors:
                    if (sensor["pickaddress"] == pickaddress):
                        state.LatestBluetoothSensors.remove(sensor)
                        # add new one in
                        myDict = MQTTJSON
                        myDict["pickaddress"] = pickaddress
                        state.LatestBluetoothSensors.append(myDict)
                        sensorUpdated = True
                if (sensorUpdated == False):
                    # new item 
                    myDict = MQTTJSON
                    myDict["pickaddress"] = pickaddress
                    state.LatestBluetoothSensors.append(myDict)

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

def convertRawToTurbidity(rawTurbidity):
    Turbidity = int(-4.49*float(rawTurbidity) + 6746.0)
    if (Turbidity > 3000):
        Turbidity = 3000
    if (Turbidity < 0):
        Turbidity = 0
    return Turbidity

def convertRawLevelToLevel(rawLevel):

    # piecewise linear

    DeltaSpread = HydroConstants.CapLevelZero - HydroConstants.CapLevelFull
    Level = 100*(1- (rawLevel - HydroConstants.CapLevelFull)/DeltaSpread )

    if (Level > 100):
        Level = 100
    if (Level < 0):
        Level = 0
    return Level

def convertRawTDSToTDS(rawTDS):

    Voltage = rawTDS*0.003 #Convert analog reading to Voltage
    TDS=(133.42/(Voltage*Voltage*Voltage) - 255.86*(Voltage*Voltage) + 857.39*Voltage)*0.5; #Convert voltage value to TDS value
    if (TDS < 0):
        TDS = 0
    return TDS

def convertRawPhToPh(rawPh):

    voltage = rawPh *0.003
    print("voltage=", voltage)
    '''
    this->_temperature    = 25.0;
    this->_phValue        = 7.0;
    this->_acidVoltage    = 2032.44;    //buffer solution 4.0 at 25C
    this->_neutralVoltage = 1500.0;     //buffer solution 7.0 at 25C
    this->_voltage        = 1500.0;
    float slope = (7.0-4.0)/((this->_neutralVoltage-1500.0)/3.0 - (this->_acidVoltage-1500.0)/3.0);  // two point: (_neutralVoltage,7.0),(_acidVoltage,4.0)
    float intercept =  7.0 - slope*(this->_neutralVoltage-1500.0)/3.0;
    //Serial.print("slope:");
    //Serial.print(slope);
    //Serial.print(",intercept:");
    //Serial.println(intercept);
    this->_phValue = slope*(voltage-1500.0)/3.0+intercept;  //y = k*x + b
    '''
    
    _temperature    = 25.0;
    _phValue        = 7.0;
    _acidVoltage    = 2032.44;    #/buffer solution 4.0 at 25C
    _neutralVoltage = 1500.0;     #/buffer solution 7.0 at 25C
    _voltage        = 1500.0;
    slope = (7.0-4.0)/((_neutralVoltage-1500.0)/3.0 - (_acidVoltage-1500.0)/3.0);  #/ two point: (_neutralVoltage,7.0),(_acidVoltage,4.0)
    intercept =  7.0 - slope*(_neutralVoltage-1500.0)/3.0;
    print("slope:");
    print(slope);
    print(",intercept:");
    print(intercept);
    phValue = slope*(voltage-1500.0)/3.0+intercept;  #/y = k*x + b
    return phValue;


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


