import state
import AccessValves
import readJSON
import config
import time
import datetime
import json
import pclogging



def initializeOneExtender(myID):
        # force read from wireless systems

        if (config.LOCKDEBUG):
            print("UpdateStateLock Acquire Attempt - initializeOneExtender ")
        state.UpdateStateLock.acquire()
        if (config.LOCKDEBUG):
            print("UpdateStateLock Acquired - initializeOneExtender ")

        #wireless extender
        wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
        for singleWireless in wirelessJSON:


            if (myID == singleWireless["id"]):
                myIP = singleWireless["ipaddress"]
                #print ("singleWireless=", singleWireless)
                if (singleWireless["hydroponicsmode"] == "true"):
                    myCommand = "enableHydroponicsMode?params=admin,1,0"
                    print("myCommand=%s myIP=%s"%(myCommand, myIP))
                    returnJSON = AccessValves.sendCommandToWireless(myIP, myCommand)
                else:
                    myCommand = "enableHydroponicsMode?params=admin,0,0"
                    print("myCommand=%s myIP=%s"%(myCommand, myIP))
                    returnJSON = AccessValves.sendCommandToWireless(myIP, myCommand)
                #print("returnJSON=", returnJSON)            
                break

        print("UpdateStateLock Releasing - initializeOneExtender")
        state.UpdateStateLock.release()
        if (config.LOCKDEBUG):
            print("UpdateStateLock Released - initializeOneExtender")


