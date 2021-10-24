# 
# contains all the state variables for SmartGarden3
#

# Check for user imports
from builtins import range
from builtins import object

import config

##################
#  English or Metric
##################
# if False, then English
# if True, then Metric
EnglishMetric = False 

##################
# blynk State Variable 
##################

blynkPlantNumberDisplay = 1


##################
# Moisture Sensors
##################
Moisture_Humidity = 100.0

Raw_Moisture_Humidity_Array = []
for i in range(1, config.moisture_sensor_count+1):
    Raw_Moisture_Humidity_Array.append(3400.0)
Moisture_Humidity_Array = []
for i in range(1, config.moisture_sensor_count+1):
    Moisture_Humidity_Array.append(100.0)

#water below this limit
Moisture_Threshold = 60.0   
##################
# Pump State
##################

Pump_Running = False
Pump_Water_Full = False

##################
# Tank State
##################

Tank_Level = 5.0
Tank_Empty_Level = 10.0
Tank_Full_Level = 2.0
Tank_Percentage_Full = 30.0


##################
# Alarm States
##################
Alarm_Temperature = 5.0  
Alarm_Moisture = 60.0
Alarm_Water = False
Alarm_Air_Quality = 10000 
Alarm_Moisture_Sensor_Fault = 15.0

Alarm_Active = True
Alarm_Cancel = False

Alarm_Last_State = False
Is_Alarm_Temperature = False
Is_Alarm_Moisture = False
Is_Alarm_MoistureFault = False
Is_Alarm_AirQuality = False
Is_Alarm_WaterEmpty = False

##################
# Internal States
##################

# apscheduler scheduler
scheduler = None

# run rainbow simulation on LEDs

runRainbow = False

# turn LED display on/off

runLEDs = True
# plant water requests

#-1 means no plant request
Plant_Number_Water_Request = -1   

Plant_Water_Request_Previous = False
Plant_Water_Request = False


######################
# Locks
######################
UpdateStateLock = None

######################
# extenders and device status
######################

deviceStatus = {}

valveStatus = []

valveTimeStates = []

moistureSensorStates =  []

nextMoistureSensorCheck = None
######################
#  Blynk State
######################


Last_Event = ""

######################
# MQTT From Wireless Units
######################

WirelessMQTTClient = None
WirelessMQTTClientConnected = False



# JSON state record

StateJSON = ""

# Blynk State Variables
WirelessDeviceSelectorPlant = 0
WirelessDeviceSelectorControl = 0
ValveSelector = 0
SecondsToTurnOn = 10
TurnOnValveButton = False
BlinkWirelessUnit = False




AQI = 0.0
Hour24_AQI = 0.0


# status Values

Last_Event = "My Last Event"
EnglishMetric = 0


# Solar Values


batteryVoltage = 0
batteryCurrent = 0
solarVoltage = 0
solarCurrent = 0
loadVoltage = 0
loadCurrent = 0
batteryPower = 0
solarPower = 0
loadPower = 0
batteryCharge = 0
SolarMAXLastReceived = "None"

SolarMaxIndoorTemperature = 0.0
SolarMaxIndoorHumidity = 0.0


def printState():

    print ("AQI = ",  AQI )
    print ("Hour24_AQI = ",  Hour24_AQI )

    print ("-------------")


    
    print ("-------------")


    print ("runRainbow = ", runRainbow )
    print ("flashStrip = ", flashStrip )
    print ("-------------")



    print ("Last_Event = ", Last_Event )
    print ("EnglishMetric = ", EnglishMetric )
    
    
    print ("-------------")

    print ("batteryVoltage", batteryVoltage )
    print ("batteryCurrent", batteryCurrent)
    print ("solarVoltage", solarVoltage )
    print ("solarCurrent", solarCurrent)
    print ("loadVoltage", loadVoltage)
    print ("loadCurrent", loadCurrent)
    print ("batteryPower", batteryPower)
    print ("solarPower", solarPower)
    print ("loadPower", loadPower)
    print ("batteryCharge", batteryCharge)

    print ("SolarMAX Indoor Temperature", SolarMaxIndoorTemperature)
    print ("SolarMAX Indoor Humidity", SolarMaxIndoorHumidity)
    print ("SolarMAX Last Received", SolarMAXLastReceived)
    print ("-------------")

    print ("-------------")



import threading
buildJSONSemaphore = threading.Semaphore()

