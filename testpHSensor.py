
#Test pH Sensor
import config
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

def convertRawtopH(raw):
    pH = (raw/2048)*3.3*3.5+config.pHOffset
    return pH
    
def getpHFromResult(myResult):
    SensorString = myResult['return_string']
    SplitLevel = SensorString.split(",")
    Level = SplitLevel[3]
    print("pHRaw=", Level)
    print("pH Value= ", round(convertRawtopH(int(Level)),2))
    return Level


readJSON.readJSON("")

print("###########################")
print("Get pH Level")
print("###########################")
print("Configured Offset = ", config.pHOffset)
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

myCommand="readHydroponicsSensors?password=admin"
AveLevel = 0
for i in range(0,5):
    try:
        myResult=sendCommandToWireless(myIP, myCommand)
        #print("myResult=", myResult)
    except:
        print("Time out failure - make sure your Extender is on line and restart program")
        sys.exit()
        
    
    #print("myResult=", myResult)
    myLevel = getpHFromResult(myResult)
    AveLevel = AveLevel + int(myLevel)

myLevel = AveLevel/5.0
print("####")
print("Average Raw pH Value= ", round(myLevel,0))
print("Average pH Value= ", round(convertRawtopH(myLevel),2))
print("####")

print("###########################")

