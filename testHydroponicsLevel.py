# sets up tests for Hydroponics level calibration
import sys
import traceback
import requests

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


import readJSON

def getLevelFromResult(myResult):
    SensorString = myResult['return_string']
    SplitLevel = SensorString.split(",")
    Level = SplitLevel[4]
    return Level


readJSON.readJSON("")

print("###########################")
print("Calibrate Hydroponics Level")
print("###########################")

wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
myIP = None
myID = None
for single in wirelessJSON:
    if (single["hydroponicsmode"] == "true"):
        myIP = single['ipaddress']
        myID = single['id']
        break

if (myIP == None):
    print("No Hydroponics Found.  Run SG3Configure")
    sys.exit()
print("Hydroponics Found id=%s ip=%s" %(single["id"],  single["ipaddress"]))

print()
print("1) Remove Moisture Sensor from Hydroponics Tank and Dry")
print("Hit Return to Continue")
temp = input()
print()
print("Now reading Hydroponics Level Sensor 5 times (may take 3 minutes )")
print()
myCommand="readHydroponicsSensors?password=admin"
AveLevel = 0
for i in range(0,5):
    try:
        myResult=sendCommandToWireless(myIP, myCommand)
    except:
        print("Time out failure - make sure your Extender is on line and restart program")
        sys.exit()
        
    
    #print("myResult=", myResult)
    myLevel = getLevelFromResult(myResult)
    AveLevel = AveLevel + int(myLevel)

myLevel = AveLevel/5.0
print("####")
print("Empty Tank Value= ", round(myLevel,0))
print("####")

print("2) Fill Hydroponics Tank to Full");
print("Hit Return to Continue")
temp = input()
print("3) Insert Moisture Sensor into the Wiring Housing in Tank") 
print("Hit Return to Continue")
temp = input()
print()
print("Now reading Hydroponics Level Sensor 5 times (may take 3 minutes)")
print()
myCommand="readHydroponicsSensors?password=admin"
AveLevel = 0
for i in range(0,5):
    try:
        myResult=sendCommandToWireless(myIP, myCommand)
    except:
        print("Time out failure - make sure your Extender is on line and restart program")
        sys.exit()
        
    
    #print("myResult=", myResult)
    myLevel = getLevelFromResult(myResult)
    AveLevel = AveLevel + int(myLevel)

myLevel = AveLevel/5.0
print("####")
print("Full Tank Value= ", round(myLevel,0))
print("####")


print()
print("Run SG3Configure again and insert above values on 'Debug/Calibration' Tab")
print("###########################")
print("   Complete")
print("###########################")

