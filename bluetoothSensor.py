import readJSON

import config
import MySQLdb as mdb
import traceback

import scanForResources


def assignBluetoothSensors():

    wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
    for single in wirelessJSON:
        # loop through each ID and look for assigned bluetooth sensors 
        myID = single["id"]
        myIP = single["ipaddress"]

        # get list of bluetooth sensors

        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                
                query = "SELECT * FROM BluetoothSensors WHERE assignedwirelessid = '%s'" % (myID) 

                #print("query=", query)
                cur.execute(query)
                myRecords = cur.fetchall()
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                myRecords = [];
        finally:
                cur.close()
                con.close()

                del cur
                del con



        mySendString = ""
        if (len(myRecords) > 0):
            for record in myRecords: 
                mySendString = mySendString + record[2]  + "," 

            mySendString = mySendString[:-1] # remove last "," 
            #print ("mySendString =", mySendString)
            
            myCommand = "assignBluetoothSensors?params=admin,"+mySendString
            print("myCommand=", myCommand)
            scanForResources.sendCommandToWireless(myIP, myCommand)
        else:
            myCommand = "assignBluetoothSensors?params=admin,NONE"
            print("myCommand=", myCommand)
            scanForResources.sendCommandToWireless(myIP, myCommand)
