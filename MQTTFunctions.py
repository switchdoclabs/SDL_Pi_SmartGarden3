# MQTT Functions


import paho.mqtt.client as mqttClient
import time
import state
import config
import json
import pclogging
import datetime
import traceback
import InitExtenders
import scanForResources

import readJSON

def on_WirelessMQTTClientconnect(client, userdata, flags, rc):

    if rc == 0:

        #print("WirelessMQTTClient Connected to broker")

        state.WirelessMQTTClientConnected = True                #Signal connection

    else:

        print("WirelessMQTTClient Connection failed")

##############
#MQTT Message Types
##############

MQTTTESTMESSAGE = 0
MQTTVALVECHANGE = 1
MQTTALARM = 2
MQTTDEBUG = 3
MQTTSENSORS = 4
MQTTBLUETOOTHSENSOR = 5
MQTTREBOOT = 6
MQTTHYDROPONICS = 7
MQTTHYDROPONICSLEVEL = 8
MQTTINFRARED = 9
#############
# MQTT Publish Message Type
#############
MQTTPUBVALVESET = 10


##############
#MQTT Data Receiving
##############


def on_WirelessMQTTClientmessage(client, userdata, message):
    if (config.SWDEBUG):
        print ("Wireless MQTT Message received: ",   message.payload)
        
    MQTTJSON = json.loads(message.payload.decode("utf-8"))

    if (str(MQTTJSON['messagetype']) == str(MQTTVALVECHANGE)):
        if (config.SWDEBUG):
            print("Valve Change Received")
        pclogging.writeMQTTValveChangeRecord(MQTTJSON)

    if (str(MQTTJSON['messagetype']) == str(MQTTALARM)):
        if (config.SWDEBUG):
            print("Alarm Message Received")
        pclogging.systemlog(config.CRITICAL,MQTTJSON['argument'])

    if (str(MQTTJSON['messagetype']) == str(MQTTDEBUG)):
        if (config.SWDEBUG):
            print("Debug Message Recieved")
        temp = str(MQTTJSON['id'])+", "+str(MQTTJSON['value'])
        pclogging.systemlog(config.DEBUG,temp)
    
    if (str(MQTTJSON['messagetype']) == str(MQTTREBOOT)):
        if (config.SWDEBUG):
            print("REBOOT Message Recieved")

        temp = str(MQTTJSON['id'])+", "+str(MQTTJSON['value'])
        pclogging.systemlog(config.DEBUG,temp)
        print("MQTTJSON=", MQTTJSON)
        processRebootMessage(MQTTJSON)

    if (str(MQTTJSON['messagetype']) == str(MQTTHYDROPONICS)):
        if (config.SWDEBUG):
            print("Hydroponics Message Recieved")
        processHydroponicsSensorMessage(MQTTJSON)

    if (str(MQTTJSON['messagetype']) == str(MQTTHYDROPONICSLEVEL)):
        if (config.SWDEBUG):
            print("Sensor Message Recieved")
        processHydroponicsLevelSensorMessage(MQTTJSON)

    if (str(MQTTJSON['messagetype']) == str(MQTTBLUETOOTHSENSOR)):
        if (config.SWDEBUG):
            print("Bluetooth Sensor Message Recieved")
        processBluetoothSensorMessage(MQTTJSON)

    if (str(MQTTJSON['messagetype']) == str(MQTTINFRARED)):
        if (config.SWDEBUG):
            print("Infrared Sensor Message Recieved")
        processInfraredSensorMessage(MQTTJSON)

def processRebootMessage(MQTTJSON):
  try:
    print("+++++++++++++++++++++");
    print("Processing Reboot"); 
    print("+++++++++++++++++++++");
    extIP = MQTTJSON["ipaddress"]
    myID = MQTTJSON["id"]      
    # update JSON with IP

    wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
    newWireless = []
    for single in wirelessJSON:
        if (single["id"] == myID):
            single['ipaddress'] = extIP 
        newWireless.append(single)
    print("newWireless=", newWireless)
    config.JSONData['WirelessDeviceJSON'] = newWireless 
    readJSON.saveJSON()
    InitExtenders.initializeOneExtender(myID)
    scanForResources.updateDeviceStatus(True)
  except:
    print(traceback.format_exc())



def processHydroponicsSensorMessage(MQTTJSON):
    try:
        print("Processing HydroponicsSensorMessage")
        pclogging.writeHydroponicsRecord(MQTTJSON)
    except:
        print(traceback.format_exc())

def processHydroponicsLevelSensorMessage(MQTTJSON):

    print("Processing HydroponicsLevelSensorMessage")






def processBluetoothSensorMessage(MQTTJSON):

    # add bluetooth reading to database

    pclogging.processBluetoothSensor(MQTTJSON)

def processInfraredSensorMessage(MQTTJSON):
    print("Processing InfraredSensorMessage")

    pclogging.processInfraredSensor(MQTTJSON)




##############
#End of MQTT Data Receiving
##############



def on_WirelessMQTTClientlog(client, userdata, level, buf):
    if (config.SWDEBUG):
        print("MQTT: ",buf)
    pass

def startWirelessMQTTClient(ClientName):


    broker_address= "127.0.0.1"  #Broker address
    port = 1883                         #Broker port

    state.WirelessMQTTClient = mqttClient.Client(ClientName)               #create new instance
    #client.username_pw_set(user, password=password)    #set username and password
    state.WirelessMQTTClient.on_connect= on_WirelessMQTTClientconnect                      #attach function to callback
    state.WirelessMQTTClient.on_message= on_WirelessMQTTClientmessage                      #attach function to callback
    state.WirelessMQTTClient.on_log = on_WirelessMQTTClientlog
    
    state.WirelessMQTTClient.connect(broker_address, port=port)          #connect to broker
    
    state.WirelessMQTTClient.loop_start()        #start the loop

#############
# MQTT Publish
#############

def sendMQTTValve(myID, Valve, State, TimeOn):

    myMessage = {
                    "id" : str(myID),
                    "messagetype" : str(MQTTPUBVALVESET),
                    "timestamp" : datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'),
                    "valve" : Valve,
                    "state" : State,
                    "timeon" : TimeOn
                    


                }
    myMessageJSON = json.dumps(myMessage)
    #print(myMessageJSON)
    state.WirelessMQTTClient.publish("SGS/"+str(myID)+"/Valves",myMessageJSON )

