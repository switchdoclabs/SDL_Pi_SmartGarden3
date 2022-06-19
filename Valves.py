import time
import config
import state
import datetime
import AccessValves
import scanForResources
import pclogging


def getDayDelay(DOWCoverage, currentDayOfWeek):
    
    if (DOWCoverage[currentDayOfWeek] == "Y"):
        return 0
    delay = 0
    for i in range(0,6):
       nextDay = (currentDayOfWeek +i ) % 7
       print("currentDayOfWeek =", currentDayOfWeek, i)
       if (DOWCoverage[nextDay] == "Y"):
        return delay
       else:
        delay = delay+1
    return delay
        
def checkDOWCoverage(DOWCoverage):
    if (DOWCoverage == "NNNNNNN"):
        return False
    return True




def valveCheck():
    if (config.SWDEBUG):
        print(">>>>>>Valve Check<<<<<<")


    if (config.LOCKDEBUG):
        print("UpdateStateLock Acquire Attempt - valveCheck")
    state.UpdateStateLock.acquire()
    if (config.LOCKDEBUG):
        print("UpdateStateLock Acquired - valveCheck")

    myValves = config.SGSConfigurationJSON["Valves"]
    for single in myValves:
        
      if(scanForResources.isDeviceActive(single["id"]) == True):

        ################# 
        # check for timed
        ################# 

        if ((single["Control"] == "Timed") and (single["DOWCoverage"] != "NNNNNNN")):
           
            if (config.SWDEBUG):
                print("ValveCheck single valve=", single)
            if (stateValveCheck(single["id"],single["ValveNumber"])):
                    if (config.SWDEBUG):
                        print("valveState Found for",single["id"],single["ValveNumber"])
                    NextTime = stateValveFetchTime(single["id"],single["ValveNumber"])
                    nowTime = datetime.datetime.now()
                    
                    if (NextTime <= nowTime): 
                  
                        myTempTime = single["StartTime"].split(":")
 
                        currentDayOfWeek = int(datetime.datetime.today().strftime('%w'))
                        # check for DOW coverage
                        dayDelay = getDayDelay(single["DOWCoverage"], currentDayOfWeek)
                        if (dayDelay > 0):
                            nowTime = datetime.datetime.now() + datetime.timedelta(days=dayDelay)
                            nowTime = nowTime.replace(hour=int(myTempTime[0]), minute=int(myTempTime[1]),second=0,microsecond=0)
                        else:
                             nowTime = datetime.datetime.now()


                        #set up next fire
                        timeDelta = getTimeDelta(single["TimerSelect"])
                        while NextTime < nowTime:
                            NextTime = NextTime + timeDelta
                        stateValveUpdateTime(single["id"],single["ValveNumber"],NextTime)
                        AccessValves.turnOnTimedValve(single)
                        if (config.SWDEBUG):
                             print("Timer Fired!  Next Fire=",NextTime)
                        pclogging.valvelog(single["id"], single["ValveNumber"], 1, "Timer Event ", "", single["OnTimeInSeconds"])

            else:
                
                myNextTime = calculateFirstTime(single)
                newValve = {
                    "id" : single["id"],
                    "ValveNumber" : single["ValveNumber"],
                    "NextTime": myNextTime,
                    "LengthTurnOn": single["OnTimeInSeconds"]
                    }
                state.valveStatus.append(newValve)
                if (config.SWDEBUG):
                    print("newValve=", newValve) 
        ################# 
        # check for BT MS Control
        ################# 
       
        myControl = single["Control"]
        #if (config.SWDEBUG):
        #    print("LatestBluetoothSensors=", state.LatestBluetoothSensors)
        
        if (myControl[0:2] == "BT"):   # found Moisture sensor
            if (config.SWDEBUG):
                print("Found Moisture Sensor =", myControl)
            # check for 15 minute lapse
            # never do pump turn ons because of BTMS control more than
            # every 15 minutes
            
            if (state.nextMoistureSensorActivate < datetime.datetime.now()):
                if (config.SWDEBUG):
                    print ("READY TO CHECK FOR MS and PUMP")
                mySplit = myControl.split("/")

                BTMSNumber = mySplit[1]
                Name = mySplit[2]
                myID = mySplit[3]
            

                myMoistureSensor = getMoistureReading(myID, BTMSNumber)
                if (myMoistureSensor == None):
                    if (config.SWDEBUG):
                        print("Sensor Reading %s Not Found Yet" % (BTMSNumber))
                    myMoistureReading = 100 
                    myMoistureSensorType = "BT"
                else:
                    myMoistureReading = myMoistureSensor["moisture"]
                    myMoistureSensorType = myMoistureSensor["sensorType"]
                if (config.SWDEBUG):
                    print("myMoistureSensor = ", myMoistureSensor )
                    print("myMoistureReading = ", myMoistureReading)
                    print("myMoistureSensorType =", myMoistureSensorType)
                
                # check for threshold
                
                if (float(myMoistureReading) >= 0.0):

                    # check for over Moisture threshold
                    if (config.SWDEBUG):
                        print("current valve=",single)
                        print("current MS Reading=",myMoistureSensor)
                    myThreshold = float(single["MSThresholdPercent"])
                    if (myThreshold > float(myMoistureReading)):
                        if (config.SWDEBUG):
                            print("turn ON Valve #", single["id"], single["ValveNumber"])
                        AccessValves.turnOnTimedValve(single)
                        if (config.SWDEBUG):
                            print("Valve Turned On by BTMS Sensor#%s/%s/%s for %s Seconds " % (BTMSNumber, Name, myID, single["OnTimeInSeconds"]  ))
                        pclogging.valvelog(single["id"], single["ValveNumber"], 1, "MS Sensor "+str(myThreshold) + ">" + str(myMoistureReading), "", single["OnTimeInSeconds"])
                    else:
                        if (config.SWDEBUG):
                            print("NO Change on Valve #", single["id"], single["ValveNumber"])
                        pass

                else:
                    if (config.SWDEBUG):
                        print("Bad Sensor Found:", myMoistureSensor)
      else:
          if (config.SWDEBUG):
                        print("Inactive Wireless Device %s / Valve %s " %( str(single["id"]), str(single["ValveNumber"])))

    # update nextMoistureSensorActivate
    myNow = datetime.datetime.now()
    while (state.nextMoistureSensorActivate < myNow):
        state.nextMoistureSensorActivate = state.nextMoistureSensorActivate + datetime.timedelta( minutes=15)
        if (config.SWDEBUG):
            print("nextMoistureValveSensorCheck = ", state.nextMoistureSensorActivate)

    
    if (config.LOCKDEBUG):
        print("UpdateStateLock Releasing - valveCheck ")
    state.UpdateStateLock.release()
    if (config.LOCKDEBUG):
        print("UpdateStateLock Released - valveCheck ")

def getMoistureReading(myID, myMSNumber):

    for singleSensor in state.LatestBluetoothSensors:
        if (singleSensor["id"].replace(" ", "") == myID.replace(" ", "")):
            if (singleSensor["pickaddress"] == myMSNumber):
                return singleSensor 

    return None

        



def getTimeDelta(timerValue):

    timeDelta = datetime.timedelta(minutes=15)

    if (timerValue == "Daily"):
        timeDelta = datetime.timedelta(days=1)
    if (timerValue == "12 Hours"):
        timeDelta = datetime.timedelta(hours=12)
    if (timerValue == "6 Hours"):
        timeDelta = datetime.timedelta(hours=6)
    if (timerValue == "3 Hours"):
        timeDelta = datetime.timedelta(hours=3)
    if (timerValue == "1 Hour"):
        timeDelta = datetime.timedelta(hours=1)
    if (timerValue == "30 Minutes"):
        timeDelta = datetime.timedelta(minutes=30)
    if (timerValue == "15 Minutes"):
        timeDelta = datetime.timedelta(minutes=15)
    return timeDelta 

def calculateFirstTime(single):
    
    nowTime = datetime.datetime.now() 
    myTempTime = single["StartTime"].split(":")
  
   
    timeDelta = getTimeDelta(single["TimerSelect"])

    
    
    
    myStartTime = nowTime.replace(hour=int(myTempTime[0]), minute=int(myTempTime[1]),second=0,microsecond=0)

    
    # check for DOW coverage
    currentDayOfWeek = int(datetime.datetime.today().strftime('%w'))
    dayDelay = getDayDelay(single["DOWCoverage"], currentDayOfWeek)
    if (dayDelay > 0):
        myDelta = datetime.timedelta(days=dayDelay)
    else:
        myDelta = datetime.timedelta(days=0)
        

    if (myStartTime > nowTime):
        NextTime = myStartTime 
    else:
        NextTime = myStartTime + timeDelta + myDelta

   
    return NextTime
    pass

def stateValveCheck(myID, myValveNumber):
   
    print("state.valveStatus=", state.valveStatus)
    
    for vState in state.valveStatus:
        print("vState=", vState)
        if(str(vState["id"]).replace(" ","") == str(myID).replace(" ","")):
            if(str(vState["ValveNumber"]).replace(" ","") == str(myValveNumber).replace(" ","")):
                 return True 
        
    return False

def stateValveFetchTime(myID, myValveNumber):
    
    for vState in state.valveStatus:
        if(str(vState["id"]).replace(" ","") == str(myID).replace(" ","")):
            if(str(vState["ValveNumber"]).replace(" ","") == str(myValveNumber).replace(" ","")):
                 return vState["NextTime"] 
        
    return None

def stateValveUpdateTime(myID, myValveNumber,NextTime):

    for vState in state.valveStatus:
        if(str(vState["id"]).replace(" ","") == str(myID).replace(" ","")):
            if(str(vState["ValveNumber"]).replace(" ","") == str(myValveNumber).replace(" ","")):
                vState["NextTime"] = NextTime 


def manualCheck():
   
    if (config.LOCKDEBUG):
        print("UpdateStateLock Acquire Attempt -  manualCheck ")
    state.UpdateStateLock.acquire()
    if (config.LOCKDEBUG):
        print("UpdateStateLock Acquired -  manualCheck ")

    pass

    if (config.LOCKDEBUG):
        print("UpdateStateLock Releasing -  manualCheck ")
    state.UpdateStateLock.release()
    if (config.LOCKDEBUG):
        print("UpdateStateLock Released -  manualCheck ")


def checkAndSetValveCurrentState(myExt):

    if (config.SWDEBUG):
        print(">>>>>>Valve Reboot State Check <<<<<<")


    if (config.LOCKDEBUG):
        print("UpdateStateLock Acquire Attempt - Reboot valveCheck")
    state.UpdateStateLock.acquire()
    if (config.LOCKDEBUG):
        print("UpdateStateLock Acquired - Reboot valveCheck")

    myValves = config.SGSConfigurationJSON["Valves"]
    for single in myValves:
        
      if(scanForResources.isDeviceActive(single["id"]) == True):

        ################# 
        # check for timed
        ################# 

        if ((single["Control"] == "Timed") and (single["DOWCoverage"] != "NNNNNNN")):
           
            if (config.SWDEBUG):
                print("Reboot ValveCheck single valve=", single)
            #if (stateValveCheck(single["id"],single["ValveNumber"])):
            if (True):
                    if (config.SWDEBUG):
                        print("Reboot valveState Found for",single["id"],single["ValveNumber"])
                    TurnValveOn = shouldValveBeOn(single["id"],single["ValveNumber"])
                    
                    if (TurnValveOn): 
                  
                        AccessValves.turnOnTimedValveWithDiff(single)
                        if (config.SWDEBUG):
                             print("Reboot Valve Set On")
                        pclogging.valvelog(single["id"], single["ValveNumber"], 1, "Reboot Event ", "", single["OnTimeInSeconds"])

            else:
                
                #myNextTime = calculateFirstTime(single)
                if (config.SWDEBUG):
                    print("Reboot Valve Not Turned On") 
      else:
          if (config.SWDEBUG):
                        print("Inactive Wireless Device %s / Valve %s " %( str(single["id"]), str(single["ValveNumber"])))

    
    if (config.LOCKDEBUG):
        print("UpdateStateLock Releasing - Reboot valveCheck ")
    state.UpdateStateLock.release()
    if (config.LOCKDEBUG):
        print("UpdateStateLock Released - Reboot valveCheck ")


def shouldValveBeOn(myExt, ValveNumber):

    pass
    return True
