
#check status of SG3 extenders
# Note:   Resets MQTT_IP address and port on extender
#

import scanForResources
import readJSON

readJSON.readJSON("")

wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
for single in wirelessJSON:
    myID = str(single["id"])
    deviceResult = scanForResources.checkDeviceStatus(single["id"])
    if (deviceResult == False):   # check again if false
        deviceResult = scanForResources.checkDeviceStatus(single["id"])


    if (deviceResult):
                
        print("Wireless Device ID %s Active" %(myID))
    else:
        print("Wireless Device ID %s Not Inactive" %(myID))

