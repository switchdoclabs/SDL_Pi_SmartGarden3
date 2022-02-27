# 
# 
# configuration file - DO NOT MODIFY!  
# Defaullts and Configuration are read from a JSON file.   SGS.JSON 
# 
SGSVERSION = "" # set in SG3.py
STATIONHARDWARE =""
import uuid

# JSON Holders
JSONData = {}
SGSConfigurationJSON = {}


#############
# Software Debug
############
SWDEBUG = True
LOCKDEBUG = False 
############
#MySQL Logging and Password Information
############
enable_MySQL_Logging = False
MySQL_Password = "password"
##########
# Mail / Text Configuration
#########
enableMail = False
mailUser = None
mailPassword = None 
notifyAddress = None
fromAddress = None 
enableText = False

#########
# Pixel Support
#########
enablePixel = False


INTERVAL_CAM_PICS__SECONDS = None
Camera_Night_Enable = False


############
# REST
############

REST_Enable = None

############
# MQTT
############

MQTT_Enable = False
MQTT_Server_URL = None
MQTT_Port_Number = None
MQTT_Send_Seconds = None


############
# Feature Enable/Disable
############
manual_water = False


############
# Bluetooth Sensor - Do not modify
############

bluetooth_count = 0


Tank_Pump_Level_Full = 500
Tank_Pump_Level_Empty = 900
############
#Hydroponics 
############
HydroponicsMode = True 


############
#Infrared
############

Infrared_High_Auto_Gain = False
Infrared_Low_Auto_Gain = False
Infrared_High_Temp = 22.0
Infrared_Low_Temp = 17.0




############
#pH Offset (not set by SG3Configure - must set here to change)
############
pHOffset = 4.7

############
#pin defines
############



############
# device present global variables - DO Not Modify
############


Lightning_Mode = False
GardenCam_Present = False

########
#Logging
########

CRITICAL=50
ERROR=40
ALARM=35
WARNING=30
INFO=20
JSON=15
DEBUG=10
NOTSET=0

######
#JSON Default Storage
######
dataDefaults = {}
