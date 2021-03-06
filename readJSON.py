import config
import json
import os



def saveJSON():



        json_data = config.JSONData 
        #json_data = json.dumps(config.JSONData)        
        # strip double or triple \\
        
        with open('SGS.JSON', 'w') as outfile:
            json.dump(json_data, outfile)


def readJSONSGSConfiguration(addPath):
        if os.path.isfile(addPath+'SGSConfiguration.JSON'):
            print (addPath+"SGSConfiguration.JSON File exists")
            with open(addPath+'SGSConfiguration.JSON') as json_file:
                JSONData = json.load(json_file)
                #print("JSONData from SGSConfigFile=", JSONData)
                config.SGSConfigurationJSON  = JSONData 
        else:
            print (addPath+"SGSConfiguration.JSON File does not exist")
            config.SGSConfigurationJSON = {"SGSConfigVersion": "001",
                                        "Valves":  [] 
                                        }
            #print("Default JSONData for SGSConfigFile=", config.SGSConfigurationJSON)
            JSONsetDefaults()
        updateValves()

def updateValves():

    # this is for updating existing valve files to new functionality on read in
    #
    for singleValve in config.SGSConfigurationJSON["Valves"]:
        # new for Version 020 - DOW Coverage
        try:
            temp = singleValve["DOWCoverage"]
        except:
            singleValve["DOWCoverage"] = "YYYYYYY"

        
def readJSON(addPath):

        JSONsetDefaults()

        if os.path.isfile(addPath+'SGS.JSON'):
            print (addPath+"SGS.JSON File exists")
            with open(addPath+'SGS.JSON') as json_file:
                config.JSONData = json.load(json_file)


                #print("JSONData from File=", config.JSONData)
                config.SWDEBUG = getJSONValue('SWDEBUG')
                config.enable_MySQL_Logging = getJSONValue('enable_MySQL_Logging')
                config.English_Metric = getJSONValue('English_Metric')
                config.MySQL_Password = getJSONValue('MySQL_Password')
                config.mailUser = getJSONValue('mailUser')
                config.mailPassword = getJSONValue('mailPassword')
                config.notifyAddress = getJSONValue('notifyAddress')
                config.fromAddress = getJSONValue('fromAddress')
                config.enableText = getJSONValue('enableText')
                config.textnotifyAddress = getJSONValue('textnotifyAddress')
                config.INTERVAL_CAM_PICS__SECONDS = getJSONValue('INTERVAL_CAM_PICS__SECONDS')
                config.Camera_Night_Enable = getJSONValue('Camera_Night_Enable')
                config.REST_Enable = getJSONValue('REST_Enable')
                config.MQTT_Enable = getJSONValue('MQTT_Enable')
                config.MQTT_Server_URL = getJSONValue('MQTT_Server_URL')
                config.MQTT_Port_Number = getJSONValue('MQTT_Port_Number')
                config.MQTT_Send_Seconds = getJSONValue('MQTT_Send_Seconds')
                config.Tank_Pump_Level_Empty = getJSONValue('Tank_Pump_Level_Empty') 
                config.Tank_Pump_Level_Full = getJSONValue('Tank_Pump_Level_Full') 
                config.manual_water = getJSONValue('manual_water')

                config.Infrared_High_Auto_Gain = getJSONValue('Infrared_High_Auto_Gain')  
                config.Infrared_Low_Auto_Gain =  getJSONValue('Infrared_Low_Auto_Gain')  
                config.Infrared_High_Temp = getJSONValue('Infrared_High_Temp')  
                config.Infrared_Low_Temp = getJSONValue('Infrared_Low_Temp')  
                config.WirelessDeviceJSON = getJSONValue('WirelessDeviceJSON') 
                #print("WirelessDeviceJSON Read from file", config.WirelessDeviceJSON)
                return True
        else:
            #print ("SGS.JSON File does not exist")
            JSONsetDefaults()
            return False



    
def JSONsetDefaults():
        config.SWDEBUG = False
        config.enable_MySQL_Logging = False
        config.English_Metric = False
        config.MySQL_Password = "password"
        config.mailUser = "yourusername"
        config.mailPassword = "yourmailpassword"
        config.notifyAddress = "you@example.com"
        config.fromAddress = "yourfromaddress@example.com"
        config.enableText = False
        config.textnotifyAddress = "yournumber@yourprovider"
        config.INTERVAL_CAM_PICS__SECONDS = 60
        config.Camera_Night_Enable =  False
        config.REST_Enable = False 
        config.MQTT_Enable = False 
        config.MQTT_Server_URL = "" 
        config.MQTT_Port_Number = 1883 
        config.MQTT_Send_Seconds = 500 
        config.Tank_Pump_Level_Full = 500 
        config.Tank_Pump_Level_Empty = 900
        config.manual_water = True
        config.Infrared_High_Auto_Gain = False
        config.Infrared_Low_Auto_Gain = False
        config.Infrared_High_Temp = 22.0
        config.Infrared_Low_Temp = 17.0
        config.WirelessDeviceJSON = ""

       
        config.dataDefaults = {} 

        config.dataDefaults['SWDEBUG'] = config.SWDEBUG 
        config.dataDefaults['enable_MySQL_Logging'] = config.enable_MySQL_Logging 
        config.dataDefaults['English_Metric'] = config.English_Metric 
        config.dataDefaults['MySQL_Password'] = config.MySQL_Password 
        config.dataDefaults['mailUser'] = config.mailUser 
        config.dataDefaults['mailPassword'] = config.mailPassword 
        config.dataDefaults['notifyAddress'] = config.notifyAddress 
        config.dataDefaults['fromAddress'] = config.fromAddress 
        config.dataDefaults['enableText'] = config.enableText 
        config.dataDefaults['textnotifyAddress'] = config.textnotifyAddress 
        config.dataDefaults['INTERVAL_CAM_PICS__SECONDS'] = config.INTERVAL_CAM_PICS__SECONDS 
        config.dataDefaults['REST_Enable'] = config.REST_Enable 
        config.dataDefaults['MQTT_Enable'] = config.MQTT_Enable 
        config.dataDefaults['MQTT_Server_URL'] = config.MQTT_Server_URL 
        config.dataDefaults['MQTT_Port_Number'] = config.MQTT_Port_Number 
        config.dataDefaults['MQTT_Send_Seconds'] = config.MQTT_Send_Seconds 
        config.dataDefaults['Tank_Pump_Level_Empty'] = config.Tank_Pump_Level_Empty 
        config.dataDefaults['Tank_Pump_Level_Full'] = config.Tank_Pump_Level_Full 
        config.dataDefaults['manual_water'] = config.manual_water 
        config.dataDefaults['Infrared_High_Auto_Gain'] = config.Infrared_High_Auto_Gain 
        config.dataDefaults['Infrared_Low_Auto_Gain'] = config.Infrared_Low_Auto_Gain 
        config.dataDefaults['Infrared_High_Temp'] = config.Infrared_High_Temp 
        config.dataDefaults['Infrared_Low_Temp'] = config.Infrared_Low_Temp 
        config.dataDefaults['WirelessDeviceJSON'] = config.WirelessDeviceJSON 
        

       
       
def getJSONValue( entry):
        try:
            returnData = config.JSONData[entry]
            return returnData
        except:
            print("JSON value not found - Set to Defaults:", entry)
            return config.dataDefaults[entry]




