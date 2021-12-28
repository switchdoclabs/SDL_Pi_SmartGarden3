# alarms and status code

import state
import config

import datetime
import traceback
import sys
import readJSON
import pclogging

# read JSON

readJSON.readJSON("")
readJSON.readJSONSGSConfiguration("")

import MySQLdb as mdb

def readAlarmConfiguration():

        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                
                query = "SELECT * FROM Alarms" 

                print("query=", query)
                cur.execute(query)
                myRecords = cur.fetchall()
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                myRecords = []
        finally:
                cur.close()
                con.close()

                del cur
                del con

        state.alarms = myRecords

def getMoistureFromSensor(address):

    return 70

def getTemperatureFromSensor(address):

    return 21


def clearAlarm(myAlarm):
            pclogging.systemlog(config.ALARM, "Alarm %s Cleared" %(myAlarm[4]))
            try:
                    #print("trying database")
                    con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                    cur = con.cursor()
                    now = datetime.datetime.now()
                    formatted_date =  now.strftime('%Y-%m-%d %H:%M:%S')
                    query = "UPDATE Alarms SET lasttriggered = Null, triggercount = 0, currentmoisture = Null, currenttemperature = Null WHERE address= '%s'" % ( myAlarm[4])

                    print("query=", query)
                    cur.execute(query)
                    con.commit()
            except mdb.Error as e:
                    traceback.print_exc()
                    print("Error %d: %s" % (e.args[0],e.args[1]))
            finally:
                    cur.close()
                    con.close()

                    del cur
                    del con


def updateActiveAlarm(myAlarm, myMoisture, myTemperature):
            try:
                    #print("trying database")
                    con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                    cur = con.cursor()
                    now = datetime.datetime.now()
                    formatted_date =  now.strftime('%Y-%m-%d %H:%M:%S')
                    query = "UPDATE Alarms SET lasttriggered = '%s', triggercount = %d, currentmoisture=%d, currenttemperature=%d WHERE address= '%s'" % ( formatted_date, myAlarm[13]+1, myMoisture, myTemperature, myAlarm[4])

                    print("query=", query)
                    cur.execute(query)
                    con.commit()
            except mdb.Error as e:
                    traceback.print_exc()
                    print("Error %d: %s" % (e.args[0],e.args[1]))
            finally:
                    cur.close()
                    con.close()

                    del cur
                    del con

def processAlarm(myType, myAlarm, myMoisture, myTemperature):

    print("Processing alarm: %s %s", myType, myAlarm[4])
    if ((myAlarm[12] == 0) or (myAlarm[13] < myAlarm[12])):
        # process alarm
        updateActiveAlarm(myAlarm, myMoisture, myTemperature)

    else:
        if (alarm[12] >= alarm[13]):
            pclogging.systemlog(config.ALARM, "MAX Reached %s - %s" %(myAlarm[4], myType))

    pclogging.systemlog(config.ALARM, "%s - %s" %(myAlarm[4], myType))

    checkForAlarmEmailOrText(myType, myAlarm)

def checkForClearAlarms():

    # reset alarms that have triggers > 1 day old
    now = datetime.datetime.now()
    timeDelta = datetime.timedelta(days = 1)

    AlarmCleared = False 
    for alarm in state.alarms:
        print("checkForClearAlarms - alarm[11] = ", alarm[11])
        if (alarm[11] != None):
            # check date
            #alarmDate = datetime.datetime.strptime(alarm[11], '%Y-%m-%d %H:%M:%S')
            alarmDate = alarm[11]

            if (now - alarmDate > timeDelta ):
                clearAlarm(alarm)
                AlarmCleared = True
            else:
                print("no Alarm Clear")

    if (AlarmCleared):
        readAlarmConfiguration()
    pass

def clearAllAlarms():
    
    for myAlarm in state.alarms:
        clearAlarm(myAlarm)
    
    pass

def checkForAlarmEmailOrText(myType, myAlarm):
    print("------>Check for Alarm Email or Text")
    # only send email or text on new trigger (transition from Null to date)
    print("myAlarm[11]=", myAlarm[11])
    if (myAlarm[11] == None):
        # send the email or text
        if (myAlarm[14] == "True"):
            sendEmailAlarm(myType, myAlarm)        
        if (myAlarm[15] == "True"):
            sendTextAlarm(myType, myAlarm)
    pass


def checkForAlarms(): 
    print("------>Check for Alarm Clears")
    checkForClearAlarms()
    print("------>Check for Alarms")
    print("state.alarms=", state.alarms)
    AlarmFired = False
    for alarm in state.alarms:
        print("checking alarm %s"  %( alarm[4]))
        myMoisture = getMoistureFromSensor(alarm[4])
        myTemperature = getTemperatureFromSensor(alarm[4])

        #split hydroponics and bluetooth
        if (alarm[3] == "True"):
            # hydroponics alarms
            print("hydroponic alarm check")
        else:
            # bluetooth alarms
            print("bluetooth alarm check")
             

        # moisture alarm
        if (alarm[5] == "True"):
            print("moisture check")

            if (myMoisture < int(alarm[6])):
                print(">>>>Low moisture alarm!")
                processAlarm("Low Moisture: %d < %d" % (myMoisture, int(alarm[6])), alarm, myMoisture, myTemperature)
                AlarmFired = True
            else:
                if (myMoisture > int (alarm[7])):
                    print(">>>>High moisture alarm!")
                    processAlarm("High Moisture: %d > %d" % (myMoisture, int(alarm[6])), alarm, myMoisture, myTemperature)
                    AlarmFired = True

            
        # temperature alarm
        if (alarm[8] == "True"):
            print("temperature check")
            if (myTemperature < int(alarm[9])):
                print(">>>>Low Temperature alarm!")
                processAlarm("Low Temperature: %d < %d" % (myTemperature, int(alarm[9])), alarm, myMoisture, myTemperature)
                AlarmFired = True
            else:
                if (myTemperature > int (alarm[10])):
                    print(">>>>High Temperature alarm!")
                    processAlarm("High Temperature: %d > %d" % (myTemperature, int(alarm[10])), alarm, myMoisture, myTemperature)
                    AlarmFired = True
        

            
    if (AlarmFired):
        readAlarmConfiguration()
            
    pass


def sendEmailAlarm(myType, myAlarm):
    print("------>Email Alarm %s" % (myType))
    pclogging.systemlog(config.INFO, "Alarm Email Sent: %s %s " %(myAlarm[4], myType))

    pass


def sendTextAlarm(myType, myAlarm):
    print("------>Text Alarm %s" % (myType))
    pclogging.systemlog(config.INFO, "Alarm Text Sent: %s %s " %(myAlarm[4], myType))

    pass


def sendEmailStatus():
    print("------>Email Status")
    pclogging.systemlog(config.INFO, "Status Email Sent") 

    pass


def sendTextStatus():
    print("------>Text Status")
    pclogging.systemlog(config.INFO, "Status Text Sent") 

    pass
