

#scan and fix status of SG3 extenders
# Note:   Resets MQTT_IP address and port on extender
#

import scanForResources
import readJSON

print("before running, stop SG3.py if it is running (hit return when ready)", end='')
test = input()
readJSON.readJSON("")

wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
activeCount = 0
inactiveCount = 0
deviceCount = len(wirelessJSON)
for single in wirelessJSON:
    myID = str(single["id"])
    deviceResult = scanForResources.checkDeviceStatus(single["id"])
    if (deviceResult == False):   # check again if false
        deviceResult = scanForResources.checkDeviceStatus(single["id"])

    #print ("deviceResult =", deviceResult)
    if (deviceResult):
        activeCount = activeCount+1        
        print("Wireless Device ID %s Active" %(myID))
    else:
        print("Wireless Device ID %s Not Active" %(myID))
        inactiveCount = inactiveCount + 1

if (activeCount == deviceCount):
    print("All devices found")
else:
    print("Missing Extenders.  Scan for Missing and Fix? (y or n)", end='')
    temp = input()
    if (temp.lower() == "y"):
        print("Scanning for missing extender.  This will take up to 10 minutes.")
        scanForResources.fixWirelessExtenders()
print("Scan and Fix Extenders Complete")
print("Restart SG3.py")
