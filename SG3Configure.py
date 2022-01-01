import time
import random
import threading
import remi.gui as gui
import urllib.request
from urllib.request import urlopen
from threading import Timer

from remi.gui import *
from remi import start, App
import json
import scanForResources
import requests
import ipaddress
import subprocess
import datetime
import sys
import os

import config
import MySQLdb as mdb
import traceback

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

myURLOpener = AppURLopener()

class SuperImage(gui.Image):
    def __init__(self, file_path_name=None, **kwargs):
        super(SuperImage, self).__init__("./static/SGfulllogocolor.png", **kwargs)
        
        self.imagedata = None
        self.mimetype = None
        self.encoding = None
        self.load(file_path_name)

    def load(self, file_path_name):
        self.mimetype, self.encoding = mimetypes.guess_type(file_path_name)
        with open(file_path_name, 'rb') as f:

            self.imagedata = f.read()
        self.refresh()

    def refresh(self):
        i = int(time.time() * 1e6)
        self.attributes['src'] = "/%s/get_image_data?update_index=%d" % (id(self), i)

    def get_image_data(self, update_index):
        headers = {'Content-type': self.mimetype if self.mimetype else 'application/octet-stream'}
        return [self.imagedata, headers]

class SGSConfigure(App):
    def __init__(self, *args):
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')
        super(SGSConfigure, self).__init__(*args, static_file_path={'my_resources':res_path})

    def idle(self):
        try:
            self.progress.set_value((self.count/256.0)*100)
        
        except:
            pass

    def display_counter(self):
       
       #print ("self.count=", self.count)
       #print ("self.stop_flag=", self.stop_flag)
       self.progress.set_value((self.count/256.0)*100)
        
       Timer(1, self.display_counter).start() 
    
    def setDefaults(self):
        self.SWDEBUG = False
        self.enable_MySQL_Logging = True
        self.English_Metric = False
        self.MySQL_Password = "password"
        self.mailUser = "yourusername"
        self.mailPassword = "yourmailpassword"
        self.notifyAddress = "you@example.com"
        self.fromAddress = "yourfromaddress@example.com"
        self.enableText = False
        self.textnotifyAddress = "yournumber@yourprovider"
        self.INTERVAL_CAM_PICS__SECONDS = 60
        self.USEBLYNK = False
        self.BLYNK_AUTH = ""
        #self.AS3935_Lightning_Config = "[2,1,3,0,3,3]"
        self.Camera_Night_Enable =  False
        self.REST_Enable = False 
        self.MQTT_Enable = False 
        self.MQTT_Server_URL = "" 
        self.MQTT_Port_Number = 1883 
        self.MQTT_Send_Seconds = 500 
        self.Tank_Pump_Level_Full = 500
        self.Tank_Pump_Level_Empty = 900
        self.Infrared_High_Auto_Gain = False
        self.Infrared_Low_Auto_Gain = False
        self.Infrared_Low_Temp = 17.0
        self.Infrared_High_Temp = 22.0
        self.manual_water = True
        self.Send_Status_Email = False
        self.Status_Send_Email_Minutes = 300
        self.Send_Status_Text = False
        self.Status_Send_Text_Minutes = 300
        self.WirelessDeviceJSON = ""

       
       
        self.dataDefaults = {} 

        self.dataDefaults['SWDEBUG'] = self.SWDEBUG 
        self.dataDefaults['enable_MySQL_Logging'] = self.enable_MySQL_Logging 
        self.dataDefaults['English_Metric'] = self.English_Metric 
        self.dataDefaults['MySQL_Password'] = self.MySQL_Password 
        self.dataDefaults['mailUser'] = self.mailUser 
        self.dataDefaults['mailPassword'] = self.mailPassword 
        self.dataDefaults['notifyAddress'] = self.notifyAddress 
        self.dataDefaults['fromAddress'] = self.fromAddress 
        self.dataDefaults['enableText'] = self.enableText 
        self.dataDefaults['textnotifyAddress'] = self.textnotifyAddress 
        self.dataDefaults['INTERVAL_CAM_PICS__SECONDS'] = self.INTERVAL_CAM_PICS__SECONDS 
        self.dataDefaults['USEBLYNK'] = self.USEBLYNK 
        self.dataDefaults['BLYNK_AUTH'] = self.BLYNK_AUTH 
        #self.dataDefaults['AS3935_Lightning_Config'] = self.AS3935_Lightning_Config 
        self.dataDefaults['REST_Enable'] = self.REST_Enable 
        self.dataDefaults['MQTT_Enable'] = self.MQTT_Enable 
        self.dataDefaults['MQTT_Server_URL'] = self.MQTT_Server_URL 
        self.dataDefaults['MQTT_Port_Number'] = self.MQTT_Port_Number 
        self.dataDefaults['MQTT_Send_Seconds'] = self.MQTT_Send_Seconds 
        self.dataDefaults['Tank_Pump_Level_Full'] = self.Tank_Pump_Level_Full 
        self.dataDefaults['Tank_Pump_Level_Empty'] = self.Tank_Pump_Level_Empty 
        self.dataDefaults['Infrared_Low_Auto_Gain'] = self.Infrared_Low_Auto_Gain 
        self.dataDefaults['Infrared_High_Auto_Gain'] = self.Infrared_High_Auto_Gain 
        self.dataDefaults['Infrared_Low_Temp'] = self.Infrared_Low_Temp 
        self.dataDefaults['Infrared_High_Temp'] = self.Infrared_High_Temp 
        self.dataDefaults['manual_water'] = self.manual_water 
        self.dataDefaults['Send_Status_Email'] = self.Send_Status_Email 
        self.dataDefaults['Status_Send_Email_Minutes'] = self.Status_Send_Email_Minutes 
        self.dataDefaults['Send_Status_Text'] = self.Send_Status_Text 
        self.dataDefaults['Status_Send_Text_Minutes'] = self.Status_Send_Text_Minutes 
        self.dataDefaults['WirelessDeviceJSON'] = self.WirelessDeviceJSON 
        

    def getJSONValue(self, entry):
        try:
            returnData = self.JSONData[entry]
            return returnData
        except:
            print("JSON value not found - Set to Defaults:", entry)
            return self.dataDefaults[entry]



    def readJSONSGSConfiguration(self):
        if os.path.isfile('SGSConfiguration.JSON'):
            print ("SGSConfiguration.JSON File exists")
            with open('SGSConfiguration.JSON') as json_file:
                JSONData = json.load(json_file)
                #print("JSONData from SGSConfigFile=", JSONData)
                self.SGSConfigurationJSON  = JSONData 
        else:
            print ("SGSConfiguration.JSON File does not exist")
            self.SGSConfigurationJSON = {"SGSConfigVersion": "001",
                                        "Valves":  [] 
                                        }
            #print("Default JSONData for SGSConfigFile=", self.SGSConfigurationJSON)
            #self.setDefaults()

        
    def readJSON(self):

        self.setDefaults()

        if os.path.isfile('SGS.JSON'):
            print ("SGS.JSON File exists")
            with open('SGS.JSON') as json_file:
                self.JSONData = json.load(json_file)


                #print("JSONData from File=", self.JSONData)
                self.SWDEBUG = self.getJSONValue('SWDEBUG')
                self.enable_MySQL_Logging = self.getJSONValue('enable_MySQL_Logging')
                #print("enable_mySQL_Logging=", self.enable_MySQL_Logging)
                self.English_Metric = self.getJSONValue('English_Metric')
                self.MySQL_Password = self.getJSONValue('MySQL_Password')
                self.mailUser = self.getJSONValue('mailUser')
                self.mailPassword = self.getJSONValue('mailPassword')
                self.notifyAddress = self.getJSONValue('notifyAddress')
                self.fromAddress = self.getJSONValue('fromAddress')
                self.enableText = self.getJSONValue('enableText')
                self.textnotifyAddress = self.getJSONValue('textnotifyAddress')
                self.INTERVAL_CAM_PICS__SECONDS = self.getJSONValue('INTERVAL_CAM_PICS__SECONDS')
                self.USEBLYNK = self.getJSONValue('USEBLYNK')
                self.BLYNK_AUTH = self.getJSONValue('BLYNK_AUTH')
                #self.AS3935_Lightning_Config = self.getJSONValue('AS3935_Lightning_Config')
                self.Camera_Night_Enable = self.getJSONValue('Camera_Night_Enable')
                self.REST_Enable = self.getJSONValue('REST_Enable')
                self.MQTT_Enable = self.getJSONValue('MQTT_Enable')
                self.MQTT_Server_URL = self.getJSONValue('MQTT_Server_URL')
                self.MQTT_Port_Number = self.getJSONValue('MQTT_Port_Number')
                self.MQTT_Send_Seconds = self.getJSONValue('MQTT_Send_Seconds')
                self.Tank_Pump_Level_Full = self.getJSONValue('Tank_Pump_Level_Full') 
                self.Tank_Pump_Level_Empty = self.getJSONValue('Tank_Pump_Level_Empty') 
                self.Infrared_High_Auto_Gain = self.getJSONValue('Infrared_High_Auto_Gain') 
                self.Infrared_Low_Auto_Gain = self.getJSONValue('Infrared_Low_Auto_Gain') 
                self.Infrared_Low_Temp = self.getJSONValue('Infrared_Low_Temp') 
                self.Infrared_High_Temp = self.getJSONValue('Infrared_High_Temp') 
                self.WirelessDeviceJSON = self.getJSONValue('WirelessDeviceJSON') 
        else:
            print ("SGS.JSON File does not exist")
            self.setDefaults()


    def saveSGSConfigurationJSON(self):

        data = self.SGSConfigurationJSON
        #print(data)

        #json_data = json.dumps(data)        
        
        
        with open('SGSConfiguration.JSON', 'w') as outfile:
            json.dump(data, outfile)

    def saveJSON(self):


        data = {}
        data['key'] = 'value'
        
        data['ProgramName'] = 'SmartGarden3' 
        data['ConfigVersion'] = '001'        

        data['SWDEBUG'] = self.F_SWDEBUG.get_value()

        data['enable_MySQL_Logging'] = self.F_enable_MySQL_Logging.get_value()
        data['English_Metric'] = self.F_English_Metric.get_value()
        data['MySQL_Password'] = self.F_MySQL_Password.get_value()

        data['mailUser'] = self.F_mailUser.get_value()
        data['mailPassword'] = self.F_mailPassword.get_value()
        data['notifyAddress'] = self.F_notifyAddress.get_value()
        data['fromAddress'] = self.F_fromAddress.get_value()

        data['enableText'] = self.F_enableText.get_value()
        data['textnotifyAddress'] = self.F_textnotifyAddress.get_value()
        data['INTERVAL_CAM_PICS__SECONDS'] = self.F_INTERVAL_CAM_PICS__SECONDS.get_value()
        data['USEBLYNK'] = self.F_USEBLYNK.get_value()
        data['BLYNK_AUTH'] = self.F_BLYNK_AUTH.get_value()
        #data['AS3935_Lightning_Config'] = self.F_AS3935_Lightning_Config.get_value()
        data['REST_Enable'] = self.F_REST_Enable.get_value()
        data['Camera_Night_Enable'] = self.F_Camera_Night_Enable.get_value()
        data['MQTT_Enable'] = self.F_MQTT_Enable.get_value()
        data['MQTT_Server_URL'] = self.F_MQTT_Server_URL.get_value()
        data['MQTT_Port_Number'] = self.F_MQTT_Port_Number.get_value()
        data['MQTT_Send_Seconds'] = self.F_MQTT_Send_Seconds.get_value()

        data['manual_water'] = self.F_manual_water.get_value()
        data['Send_Status_Email'] = self.F_Send_Status_Email.get_value()
        data['Status_Send_Email_Minutes'] = self.F_Status_Send_Email_Minutes.get_value()
        data['Send_Status_Text'] = self.F_Send_Status_Text.get_value()
        data['Status_Send_Text_Minutes'] = self.F_Status_Send_Text_Minutes.get_value()
        data['Tank_Pump_Level_Full'] = self.F_Tank_Pump_Level_Full.get_value()
        data['Tank_Pump_Level_Empty'] = self.F_Tank_Pump_Level_Empty.get_value()
        data['Infrared_High_Auto_Gain'] = self.F_Infrared_High_Auto.get_value()
        data['Infrared_Low_Auto_Gain'] = self.F_Infrared_Low_Auto.get_value()
        data['Infrared_Low_Temp'] = self.F_Infrared_Low_Temp.get_value()
        data['Infrared_High_Temp'] = self.F_Infrared_High_Temp.get_value()

        data['WirelessDeviceJSON'] = self.WirelessDeviceJSON




        #print(data)

        json_data = json.dumps(data)        
        # strip double or triple \\
        
        with open('SGS.JSON', 'w') as outfile:
            json.dump(data, outfile)

    # screen builds

    def establishMenu(self,vbox):
        menu = gui.Menu(width='100%', height='60px')
        m0 = gui.MenuItem('SGS Configure', width=90, height=60)
        m0.onclick.do(self.menu_screen0_clicked)
        m05 = gui.MenuItem('Valve Report', width=90, height=60)
        m05.onclick.do(self.menu_screen05_clicked)
        m06 = gui.MenuItem('Configure Extender', width=90, height=60)
        m06.onclick.do(self.menu_screen06_clicked)
        m1 = gui.MenuItem('Debug Calibration', width=70, height=60)
        m1.onclick.do(self.menu_screen1_clicked)
        m2 = gui.MenuItem('Mail and Text', width=70, height=60)
        m2.onclick.do(self.menu_screen2_clicked)
        #m3 = gui.MenuItem('PSMax', width=70, height=60)
        #m3.onclick.do(self.menu_screen3_clicked)
        m4 = gui.MenuItem('Cameras Bluetooth', width=70, height=60)
        m4.onclick.do(self.menu_screen4_clicked)
        m5 = gui.MenuItem('Blynk', width=70, height=60)
        m5.onclick.do(self.menu_screen5_clicked)
        #m6 = gui.MenuItem('Pins', width=70, height=60)
        #m6.onclick.do(self.menu_screen6_clicked)
        m7 = gui.MenuItem('CMQTTR', width=70, height=60)
        m7.onclick.do(self.menu_screen7_clicked)
        m8 = gui.MenuItem('Alarm/Status Configuration', width=90, height=60)
        m8.onclick.do(self.menu_screen8_clicked)

        menu.append([m0, m05, m06, m1, m2, m4, m5,  m7, m8])
    
    
        self.menubar = gui.MenuBar(width='100%', height='30px')
        self.menubar.append(menu)
        vbox.append(self.menubar)
        return vbox

    def getBluetoothList(self):
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                
                query = "SELECT * FROM BluetoothSensors" 

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

        return myRecords


    def returnAssignedBluetooth(self):

        myRecords = self.getBluetoothList()
        print ("Myrecords=", myRecords)
        bluetoothAssignedCount = [] 
        for record in myRecords:
            print("record=", record)
            if (record[4] != None):
                if (len(record[4]) == 4):
                    bluetoothAssignedCount.append(record)
        return bluetoothAssignedCount

    def buildScreen0(self):
        #screen 0

        # toplevel box
        vbox = gui.Container(width=1000, height=510, layout_orientation=gui.Container.LAYOUT_HORIZONTAL,  style="background: LightBlue")
        vbox.style['justify-content'] = 'center'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'

        # Menu
        menubox =  gui.Container(width=1000, height=60, style="background: LightGray")
        menubox = self.establishMenu(menubox)
        vbox.append(menubox)

        # Top Status block

        statusbox = gui.Container(width=1000, height=50, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style="background: LightBlue")
        #statusbox.style['justify-content'] = 'right'
        statusbox.style['align-items'] = 'right'
        statusbox.style['border'] = '2px'
        statusbox.style['border-color'] = 'blue'
        statusbox.style['flex-direction'] = 'row'

        # elements

        self.Display_IP = gui.Label('',width=130, height=30, margin='5px')

        self.Display_WEXT = gui.Label('', width=130, height=30, margin='5px')
        self.Display_EXT = gui.Label('', width=130, height=30, margin='5px')

        self.Display_WEXT.set_text('Found Wireless Extenders: ' )
        self.Display_IP.set_text('Scanning IP: N/A ' )
        
        self.Display_WEXT2 = gui.Label('', width=130, height=30, margin='5px', style=' color: red')
        self.Display_WEXT2.set_text("Click 'Save and Exit' After Scan and Restart")


        #print("WirelessDeviceJSON=", self.WirelessDeviceJSON)
        #print("Length WirelessDeviceJSON=", len(self.WirelessDeviceJSON))
        if (len(self.WirelessDeviceJSON) == 0):

            scanForHardware = gui.Button('Scan For SGS Hardware',style='height: 30px; width:200px;  margin: 10px;  top:5px')
            scanForHardware.onclick.do(self.ScanForHardware)
            statusbox.append(scanForHardware,'scanForHardware') 


        else:
            RescanForHardware = gui.Button('ReScan For SGS Hardware',style=' height: 30px; width:200px;  margin: 10px;  top:5px')
            RescanForHardware.onclick.do(self.ScanForHardware)
            statusbox.append(RescanForHardware,'RescanForHardware') 
       


        statusbox.append(self.progress, 'progress')
        statusbox.append(self.Display_IP, 'DIP')
        statusbox.append(self.Display_WEXT, 'DWEXT')
        statusbox.append(self.Display_EXT, 'DEXT')
        statusbox.append(self.Display_WEXT2, 'DEXT2')

        vbox.append(statusbox)


    
        self.Display_WEXT.set_text('Found Wireless Extenders: '+ str(len(self.WirelessDeviceJSON) ))


        # Now set up the rows for configuation

        # set up valve configuration
        valves = []

    
        # wireless units 
        for wireless in self.WirelessDeviceJSON:
            wirelessDevice = wireless 
            #wirelessDevice = json.loads(str(wireless).replace("'", "\""))
            
            id = wirelessDevice['id'] 
            ipAddress = wirelessDevice['ipaddress']
            name = wirelessDevice['name']
            valves.append([id, name, ipAddress ])
            self.buildMissingValves(wirelessDevice['id'], wirelessDevice['name'])

            #vbox.append(wirelessBlock)
             

        
        items = ()
        self.ValveControlItems = ("Off","Timed")
        btList = self.returnAssignedBluetooth()
        for btItem in btList: 

            vcitem= ("BT/" + btItem[3]+ "/" + btItem[5] +"/"+ btItem[4])
            self.ValveControlItems = self.ValveControlItems + (vcitem, )

        for ext in valves:
            if (len(str(ext[0])) < 4):
                    item = (str(ext[1])+" / "+str(ext[0]) +" / "+str(ext[2]))

            else:
                    item = (str(ext[1])+" / "+str(ext[0])+ " / " +str(ext[2]))

            items = items +  (item, )

        self.TimedItems = ("15 Minutes", "30 Minutes" , "1 Hour", "3 Hours", "6 Hours", "12 Hours", "Daily")


        # now set up new block
        self.ValveBlock = gui.Container(width=1000, height=700, layout_orientation=gui.Container.LAYOUT_HORIZONTAL)
        self.ValveBlock.style['background'] = "LightGray"

        self.ValveBlock.style['align-items'] = 'right'
        self.ValveBlock.style['border'] = '2px'
        self.ValveBlock.style['border-color'] = 'blue'
        self.ValveBlock.style['flex-direction'] = 'row'


        print("pre listView2 items=", items)

        self.listView2 = gui.ListView.new_from_list(items, width=400, height=25*len(valves), margin='10px')
        self.listView2.onselection.do(self.list_view_on_selected)
        self.ValveBlock.append(self.listView2)

        vbox.append(self.ValveBlock)
        

        return vbox

    def list_view_on_selected(self, widget, selected_item_key):
        """ The selection event of the listView, returns a key of the clicked event.
            You can retrieve the item rapidly
        """
        print("selected_item_key=", selected_item_key)
        print("widget =", widget)
        myUnit =  widget.children[selected_item_key].get_text()
        #myUnit =  self.listView2.children[selected_item_key].get_text()
        print("myUnit=", myUnit)
        # for on save
        self.current_listView_key = myUnit

        id = myUnit.split("/")[1]
        name = myUnit.split("/")[0]
        
        self.myValve = self.buildAValve(id, name,myUnit)
        print(self.myValve)

        self.ValveBlock.append(self.myValve, "currentValve") 

    def wireless_list_view_on_selected(self, widget, selected_item_key):
        """ The selection event of the listView, returns a key of the clicked event.
            You can retrieve the item rapidly
        """
        myUnit =  self.listView8.children[selected_item_key].get_text()
        print("list_view: myUnit=", myUnit)
        # for on save
        self.current_listView_key = myUnit

        id = myUnit.split("/")[1]
        name = myUnit.split("/")[0]
        myBTName = myUnit.split("/")[2]

        mySplit = myUnit.split(":")
        assignedAddress = mySplit[3]
        assignedAddress = assignedAddress.replace(" ", "")
        print("assignedAddress=", assignedAddress)

        wirelessUnits=[]
        wirelessItems =('Not Assigned',) 
        selectAddress = "Not Assigned"
        # wireless units
        for wireless in self.WirelessDeviceJSON:
            wirelessDevice = wireless
            id = wirelessDevice['id']
            ipAddress = wirelessDevice['ipaddress']
            name = wirelessDevice['name']
            wirelessUnits.append([id, name, ipAddress ])
            wirelessItems = wirelessItems + (id+"/"+name+"/"+ipAddress,)
            if (id == assignedAddress):
                selectAddress = id+"/"+name+"/"+ipAddress
            #vbox.append(wirelessBlock)

        self.DisplaySelect = gui.Label('Select Wireless Device ',width=100, height=15, margin='5px')


        self.dropDownWireless = gui.DropDown.new_from_list(wirelessItems,  width=300, height=20, margin='5px')
        self.dropDownWireless.onchange.do(self.wireless_drop_down_valve_changed)
        self.dropDownWireless.select_by_value(selectAddress )
 

        self.BTNameLabel = gui.Label('Bluetooth Sensor Name',width=200, height=15, margin='10px')
        self.BTNameInput = gui.TextInput(width=100, height=15, style="margin:10px")
        self.BTNameInput.set_value( myBTName)
        self.BTNameSaveButton = gui.Button('Save Name',height=30, width=100, margin=10)
        self.BTNameSaveButton.onclick.do(self.onBTNameSaveButton)

        #self.myValve = self.buildAValve(id, name,myUnit)
        #self.ValveBlock.append(self.DisplaySelect, "currentwireless") 
        self.ValveBlock1.append(self.dropDownWireless, "currentwireless") 
        self.ValveBlock1.append(self.BTNameLabel, "1jcurrentwireless") 
        self.ValveBlock1.append(self.BTNameInput, "2jcurrentwireless") 
        self.ValveBlock1.append(self.BTNameSaveButton, "3jcurrentwireless") 

    def onBTNameSaveButton (self, widget, name='', surname=''):
        print("onBTNameSaveButton Clicked")
        myUnit = self.current_listView_key 
        print("myUnit=", myUnit)    
        myID = myUnit.split("/")[1]
        name = myUnit.split("/")[0]
        newName = self.BTNameInput.get_value()
        
        try:
                    #print("trying database")
                    con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                    cur = con.cursor()
                 
                    query = "UPDATE BluetoothSensors SET name = '%s' WHERE pickaddress= '%s'" % ( newName, myID)
    
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
        # refresh
        self.removeAllScreens()
        self.screen4 = self.buildScreen4()
        self.mainContainer.append(self.screen4,'screen4')


######################
# JSON Valve Functions
######################

    def checkValveJSON(self, myID, valveNumber):
        myJSON=self.SGSConfigurationJSON
        #print("myJSON=", self.SGSConfigurationJSON) 
        #myLoadedJSON = json.loads(str(myJSON).replace("'","\"" ))
        myLoadedJSON = myJSON
        #print("myValves=",myLoadedJSON["Valves"])
        myValves = myLoadedJSON["Valves"]

        Present = False
        for singleValve in myValves:

            if (str(singleValve["id"]).replace(" ","") == str(myID).replace(" ", "")):
                if (str(singleValve["ValveNumber"]) == str(valveNumber)):
                    Present = True
                    break

        return Present
    
    def addNewValveJSON(self, myID, valveNumber):

        # setup new Valve
        newValve = {
                "id": myID,
                "ValveNumber": valveNumber,
                "Control": "Off",
                "MSThresholdPercent": "65",
                "TimerSelect": "Daily",
                "DOWCoverage": "YYYYYYY",
                "StartTime": "05:00",
                "OnTimeInSeconds": "10",
                "ShowGraph" : False
                }
                

        myJSON=self.SGSConfigurationJSON
       
        
        myLoadedJSON = myJSON
        print(type(myLoadedJSON))
        #myLoadedJSON = myLoadedJSON.replace("'", "\"") 
        
        #myLoadedJSON = json.loads(myLoadedJSON)
        #print(type(myLoadedJSON))
        #print("myLoadedJSON A", myLoadedJSON)
        #myLoadedJSON = json.loads(str(myJSON).replace("'","\"" ))
        myLoadedJSON["Valves"].append(newValve)
        self.SGSConfigurationJSON = myLoadedJSON
        #self.SGSConfigurationJSON = json.dumps(myLoadedJSON)
    
         
        
    def fetchValveJSON(self, myID, valveNumber):
       
        myJSON=self.SGSConfigurationJSON
        
        #myLoadedJSON = json.loads(str(myJSON))
        #myLoadedJSON = json.loads(str(myJSON).replace("'","\"" ))
        myValves = myJSON["Valves"]

        for singleValve in myValves:
            #singleValve = json.loads(str(singleValve).replace("'","\"" ))
            #singleValve = json.loads(str(singleValve))
            if (str(singleValve["id"]).replace(" ", "") == str(myID).replace(" ", "")):
                if (str(singleValve["ValveNumber"]) == str(valveNumber)):
                    # check for update to Valve Info
                    try:
                        DWO = singleValve["DOWCoverage"]
                    except:
                        singleValve["DOWCoverage"] = "YYYYYYY"

                    #print (singleValve)
                    return singleValve
        return {}
        

    def checkDOW(self,singleValve, DOW):

        if (DOW == "Su"):
            if (singleValve["DOWCoverage"][0] == "Y"):
                return True
            else:
                return False
        if (DOW == "Mo"):
            if (singleValve["DOWCoverage"][1] == "Y"):
                return True
            else:
                return False
        if (DOW == "Tu"):
            if (singleValve["DOWCoverage"][2] == "Y"):
                return True
            else:
                return False
        if (DOW == "We"):
            if (singleValve["DOWCoverage"][3] == "Y"):
                return True
            else:
                return False
        if (DOW == "Th"):
            if (singleValve["DOWCoverage"][4] == "Y"):
                return True
            else:
                return False
        if (DOW == "Fr"):
            if (singleValve["DOWCoverage"][5] == "Y"):
                return True
            else:
                return False
        if (DOW == "Sa"):
            if (singleValve["DOWCoverage"][0] == "Y"):
                return True
            else:
                return False

        return False


    def setDOW(self,singleValve, DOW, value):

        if (value):
            checkValue = "Y"
        else:
            checkValue = "N"
        print("Args pre DOW", singleValve, DOW, value, checkValue)

        newValue = ""
        
        if (DOW == "Su"):
            newValue += checkValue
        else:
            newValue += singleValve["DOWCoverage"][0]
        if (DOW == "Mo"):
            newValue += checkValue
        else:
            newValue += singleValve["DOWCoverage"][1]
            
        if (DOW == "Tu"):
            newValue += checkValue
        else:
            newValue += singleValve["DOWCoverage"][2]
           
        if (DOW == "We"):
            newValue += checkValue
        else:
            newValue += singleValve["DOWCoverage"][3]
          
        if (DOW == "Th"):
            newValue += checkValue
        else:
            newValue += singleValve["DOWCoverage"][4]
         
        if (DOW == "Fr"):
            newValue += checkValue
        else:
            newValue += singleValve["DOWCoverage"][5]
        
        if (DOW == "Sa"):
            newValue += checkValue
        else:
            newValue +=  singleValve["DOWCoverage"][6]
      
        singleValve["DOWCoverage"] = newValue

        print("singleValve Post DOW", singleValve)
        return False




        
    def updateValveJSON(self, myID, valveNumber):
        # update the JSON and return the list of Valves
        
        myValves = self.SGSConfigurationJSON["Valves"]

        for singleValve in myValves:
            #singleValve = json.loads(str(singleValve).replace("'","\"" ))
            #singleValve = json.loads(str(singleValve))
            
            #print("singleValve=", singleValve)
            #print("id=", singleValve["id"])
            #print("myID=", myID)
            #print("ValveNumber=", singleValve["ValveNumber"])
            #print("valveNumber=", valveNumber)
            if (str(singleValve["id"]).replace(" ", "") == str(myID).replace(" ", "")):
                if (str(singleValve["ValveNumber"]) == str(valveNumber)):
                    # OK, we have the correct one, so fix it
                    print("Valve Found for update")
                    print ("Before: updatedSingleValve=", singleValve)
                    singleValve["Control"] =  self.dropDownMSSensor.get_value()
                    singleValve["MSThresholdPercent"] = self.DisplayST_MS.get_text()
                    singleValve["TimerSelect"] = self.dropDownTimed.get_value()
                    singleValve["StartTime"] = self.DisplayST_TB.get_text()
                    #print("Before-OTS", singleValve["OnTimeInSeconds"])
                    singleValve["OnTimeInSeconds"] = self.DisplayOTS_TB.get_text()
                    singleValve["ShowGraph"] = self.DisplaySG_CB.get_value() 

                    # DOW Filter
                    self.setDOW(singleValve, "Su", self.Display_Su.get_value())
                    self.setDOW(singleValve, "Mo", self.Display_Mo.get_value())
                    self.setDOW(singleValve, "Tu", self.Display_Tu.get_value())
                    self.setDOW(singleValve, "We", self.Display_We.get_value())
                    self.setDOW(singleValve, "Th", self.Display_Th.get_value())
                    self.setDOW(singleValve, "Fr", self.Display_Fr.get_value())
                    self.setDOW(singleValve, "Sa", self.Display_Sa.get_value())
                    
            
                    print("aftersingleValve-OTS", singleValve["OnTimeInSeconds"])
                    print ("updatedSingleValve=", singleValve)
                    #singleValve = json.dumps(singleValve)
             #myNewValves.append(singleValve)


        #print("myValves=", myValves)
        
        self.SGSConfigurationJSON["Valves"] = myValves

        #print ("updatedSGSConfigurationJSON=", self.SGSConfigurationJSON)

            
        pass
    
######################
# End JSON Valve Functions
######################

        
    def buildMissingValves(self, DeviceID, name ):
        #print("DeviceID=", DeviceID)
        #print("name=", name)
        
        if (len(str(DeviceID).replace(" ","")) < 4):
            for i in range(1,5):
                 if (self.checkValveJSON(DeviceID, i) == False):
                         # add a new one in
                         self.addNewValveJSON(DeviceID, i)
        else:
            for i in range(1,9):
                 if (self.checkValveJSON(DeviceID, i) == False):
                         # add a new one in
                         self.addNewValveJSON(DeviceID, i)

        pass



    def buildAValve(self, DeviceID, name, myUnit):
        myValve = gui.Container(width=300, height=700, layout_orientation=gui.Container.LAYOUT_VERTICAL)
        myValve.style['background'] = "LightBlue"

        myValve.style['align-items'] = 'right'
        myValve.style['border'] = '2px'
        myValve.style['border-color'] = 'blue'
        myValve.style['flex-direction'] = 'row'

        self.valvelist = ('None Selected',) 
        ext = myUnit.split("/")

        print ("myUnit---->=",myUnit)
        self.ValveJSON = {}

        if (len(str(ext[1])) < 4):
            for i in range(1,5):
                 self.valvelist = self.valvelist + (str(ext[0]) + "/" +str(ext[1]) + "/Valve "+str(i),)
                 # check to see if Valve is in JSON, add if not
                 myID = str(ext[1])
                 if (self.checkValveJSON(myID, i) == False):
                         # add a new one in
                         self.addNewValveJSON(myID, i)
                                          

        else:
            for i in range(1,9):
                 self.valvelist = self.valvelist + (str(ext[0]) + "/" +str(ext[1]) + "/Valve "+str(i),)
                 # check to see if Valve is in JSON, add if not
                 myID = str(ext[1])
                 if (self.checkValveJSON(myID, i) == False):
                         # add a new one in
                         self.addNewValveJSON(myID, i)
                                          



        self.DisplaySelect = gui.Label('Valve Select (%s)'% (myID),width=200, height=15, margin='5px')
        self.dropDownValve = gui.DropDown.new_from_list(self.valvelist, width=200, height=20, margin='10px')
        
        self.dropDownValve.onchange.do(self.drop_down_valve_changed)
        self.dropDownValve.select_by_value('None' )        
        self.DisplayControl = gui.Label('Valve Control',width=100, height=15, margin='5px')

        self.dropDownMSSensor = gui.DropDown.new_from_list(self.ValveControlItems, width=200, height=20, margin='10px')

        self.dropDownMSSensor.select_by_value('Off' )        
        self.dropDownMSSensor.onchange.do(self.drop_down_MS_changed)

        self.DisplayMS = gui.Label('Moisture Sensor Threshold Percent',width=300, height=15, margin='10px')
        self.DisplayST_MS = gui.TextInput(width=100, height=15, style="margin:10px")
        self.DisplayDOW = gui.Label('Day of Week Filter',width=200, height=15, margin='10px')
        self.Display_Su = gui.CheckBoxLabel( 'Su', True, height=30, style='margin:5px; background: LightGray ')
        self.Display_Mo = gui.CheckBoxLabel( 'Mo', True, height=30, style='margin:5px; background: LightGray ')
        self.Display_Tu = gui.CheckBoxLabel( 'Tu', True, height=30, style='margin:5px; background: LightGray ')
        self.Display_We = gui.CheckBoxLabel( 'We', True, height=30, style='margin:5px; background: LightGray ')
        self.Display_Th = gui.CheckBoxLabel( 'Th', True, height=30, style='margin:5px; background: LightGray ')
        self.Display_Fr = gui.CheckBoxLabel( 'Fr', True, height=30, style='margin:5px; background: LightGray ')
        self.Display_Sa = gui.CheckBoxLabel( 'Sa', True, height=30, style='margin:5px; background: LightGray ')

        self.DisplayTimed = gui.Label('Timer Selection',width=200, height=15, margin='10px')
        self.dropDownTimed = gui.DropDown.new_from_list(self.TimedItems, width=200, height=20, margin='10px')

        self.dropDownTimed.select_by_value('N/A' )        
        self.dropDownTimed.set_enabled(False)
        
       


        self.DisplayST = gui.Label('Start Time',width=200, height=15, margin='10px')

        self.DisplayST_TB = gui.TextInput(width=100, height=15, style="margin:10px")
        self.DisplayST_TB.set_enabled(False)

        self.DisplayOTS = gui.Label('On Time Length in Seconds',width=200, height=15, margin='10px')

        self.DisplayOTS_TB = gui.TextInput(width=100, height=15, style="margin:10px")
        self.DisplaySG_CB = gui.CheckBoxLabel( 'Display Graph', False, height=30, style='margin:5px; background: LightGray ')
       
        self.ValveSaveButton = gui.Button('Save Valve',height=30, width=100, margin=10)
        self.ValveSaveButton.set_enabled(False)

        self.ValveSaveButton.onclick.do(self.onValveSaveButton)

        
        myValve.append(self.DisplaySelect)
        myValve.append(self.dropDownValve)
        myValve.append(self.DisplayControl)
        myValve.append(self.dropDownMSSensor)
        myValve.append(self.DisplayMS)
        myValve.append(self.DisplayST_MS)
        myValve.append(self.DisplayDOW)
        myValve.append(self.Display_Su)
        myValve.append(self.Display_Mo)
        myValve.append(self.Display_Tu)
        myValve.append(self.Display_We)
        myValve.append(self.Display_Th)
        myValve.append(self.Display_Fr)
        myValve.append(self.Display_Sa)
        myValve.append(self.DisplayTimed)
        myValve.append(self.dropDownTimed)
        myValve.append(self.DisplayST)
        myValve.append(self.DisplayST_TB)
        myValve.append(self.DisplayOTS)
        myValve.append(self.DisplayOTS_TB)
        myValve.append(self.DisplaySG_CB)
        myValve.append(self.ValveSaveButton)


        return myValve 

    def onValveSaveButton (self, widget, name='', surname=''):
        print("onValveSaveButton Clicked")
        myUnit = self.current_listView_key 
        print("myUnit=", myUnit)    
        myID = myUnit.split("/")[1]
        name = myUnit.split("/")[0]
        
        self.updateValveJSON(myID, self.currentValveNumber)
        self.ValveSaveButton.set_enabled(False)
        self.dropDownValve.select_by_value('None' )        

    def drop_down_MS_changed (self, widget, selected_item_key):
        myUnit = selected_item_key
        print ("myUnit=", myUnit)
        if (myUnit == 'Timed'):
            print('enabled')
            self.DisplayST_TB.set_enabled(True)
            self.dropDownTimed.set_enabled(True)
        else:
            print('disabled')
            self.DisplayST_TB.set_enabled(False)
            self.dropDownTimed.set_enabled(False)



    def wireless_drop_down_valve_changed (self, widget, selected_item_key):
        print("selected item key=", selected_item_key)
        # update the selected bluetooth sensor with the wireless ID
        try:
            print("listView key=",self.current_listView_key)
            
            mySplit = self.current_listView_key.split('/')

            print("mySplit=", mySplit)
            if (selected_item_key  == "Not Assigned"):
                myPickaddress = mySplit[1]
                myWirelessAddress = ""
            else: 
                myPickaddress = mySplit[1]
                mySplit = selected_item_key.split("/")
                myWirelessAddress = mySplit[0]

            self.CurrentBTAddress = myPickAddreess

            # open the sql file and update
        
            try:
                    #print("trying database")
                    con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                    cur = con.cursor()
                 
                    query = "UPDATE BluetoothSensors SET assignedwirelessid = '%s' WHERE pickaddress= '%s'" % ( myWirelessAddress, myPickaddress)
    
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
    
        except:
            widget.select_by_value('Not Assigned' )        
            pass
        # refresh
        self.removeAllScreens()
        self.screen4 = self.buildScreen4()
        self.mainContainer.append(self.screen4,'screen4')



    def drop_down_valve_changed (self, widget, selected_item_key):
        print("myUnit=", selected_item_key)
        myUnit = selected_item_key
        # parse values
        splitMyUnit = myUnit.split("/")
        # get the default values
        #print ('valveJSON=', valveJSON)
        if (myUnit != "None Selected"):
            self.ValveSaveButton.set_enabled(True)
            values = myUnit.split("/")
            vnum = values[2].split(" ")
            self.currentValveNumber = vnum[1]
            valveJSON = self.fetchValveJSON(values[1], self.currentValveNumber)

            print (type(valveJSON))
            print ("myValveJSON=", valveJSON)
            # now set up the other menu items
            #valveJSON = json.loads(str(valveJSON))
            #valveJSON = json.loads(str(valveJSON).replace("'","\"" ))

            self.dropDownMSSensor.select_by_value(valveJSON["Control"] )        
            self.dropDownTimed.select_by_value(valveJSON["TimerSelect"])
            self.DisplayST_MS.set_text(valveJSON["MSThresholdPercent"])
            self.DisplayST_TB.set_text(valveJSON["StartTime"])
            self.DisplayOTS_TB.set_text(valveJSON["OnTimeInSeconds"])
            self.DisplaySG_CB.set_value(valveJSON["ShowGraph"])
            if (valveJSON["Control"]  == 'Timed'):
                print('enabled')
                self.DisplayST_TB.set_enabled(True)
                self.dropDownTimed.set_enabled(True)
            else:
                print('disabled')
                self.DisplayST_TB.set_enabled(False)
                self.dropDownTimed.set_enabled(False)
       
            self.Display_Su.set_value(self.checkDOW(valveJSON, "Su"))
            self.Display_Mo.set_value(self.checkDOW(valveJSON, "Mo"))
            self.Display_Tu.set_value(self.checkDOW(valveJSON, "Tu"))
            self.Display_We.set_value(self.checkDOW(valveJSON, "We"))
            self.Display_Th.set_value(self.checkDOW(valveJSON, "Th"))
            self.Display_Fr.set_value(self.checkDOW(valveJSON, "Fr"))
            self.Display_Sa.set_value(self.checkDOW(valveJSON, "Sa"))


        else:
            print ("None Selected")
                
        

    

    def buildScreen05(self):


        #screen 05

        vbox = VBox(width=1000, height=510, style="background: LightGray")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'


        #screen 05

        vbox = self.establishMenu(vbox)



        screen1header = gui.Label("Valve Configuration Report", style='margin:10px; background: LightGray')
        vbox.append(screen1header)



        myValves = self.SGSConfigurationJSON["Valves"]
        myArray = [('ID', 'Unit Name', 'Valve Number','Control','MS Threshold','DOW Filter (Su-Sa)', 'Time Select', 'Start Time', 'On Time (seconds)')]

            
        # loop through wireless
        for wireless in self.WirelessDeviceJSON:
            myID = wireless["id"]
            myName = wireless["name"]

            for i in range (0,9):
                # first get the description
                myList = []
                myList.append(str(myID))
                myList.append(str(myName))
                currentValve = self.fetchValveJSON(myID, i)
                if len(currentValve) > 0:
                    #print ('currentValve=', currentValve)

                    myList.append(str(currentValve["ValveNumber"]))
                    myList.append(str(currentValve["Control"]))
                    myList.append(str(currentValve["MSThresholdPercent"]))
                    myList.append(str(currentValve["DOWCoverage"]))
                    myList.append(str(currentValve["TimerSelect"]))
                    myList.append(str(currentValve["StartTime"]))
                    myList.append(str(currentValve["OnTimeInSeconds"]))
                    myTuple = tuple(myList)
                    myArray.append(myTuple)
                

    
        # set up table display
        #print('myArray=', myArray) 

        self.table = gui.Table.new_from_list(myArray,
                                    width=600, height=400, margin='10px')

        vbox.append(self.table)

        return vbox

    #screen 06
    def buildScreen06(self):


        #screen 06


        vbox = gui.Container(width=1000, height=510, layout_orientation=gui.Container.LAYOUT_HORIZONTAL,  style="background: LightBlue")
        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'


        #screen 06
        # Menu
        menubox =  gui.Container(width=1000, height=60, style="background: LightGray")
        menubox = self.establishMenu(menubox)
        vbox.append(menubox)



        # Top Status block

        statusbox = gui.Container(width=1000, height=50, layout_orientation=gui.Container.LAYOUT_HORIZONTAL, style="background: LightBlue")
        #statusbox.style['justify-content'] = 'right'
        statusbox.style['align-items'] = 'flex-start'
        statusbox.style['border'] = '2px'
        statusbox.style['border-color'] = 'blue'
        statusbox.style['flex-direction'] = 'row'

        # elements
        self.Display_WEXT.set_text('Configure Wireless Extenders' )

        statusbox.append(self.Display_WEXT, 'DWEXT')


        vbox.append(statusbox)



        #screen6header = gui.Label("Configure Extender", style='margin:10px; background: LightGray')
        #vbox.append(screen6header)

        # now set up new block
        self.ExtenderConfig = gui.Container(width=1000, height=700, layout_orientation=gui.Container.LAYOUT_HORIZONTAL)
        self.ExtenderConfig.style['background'] = "LightGray"

        self.ExtenderConfig.style['align-items'] = 'flex-start'
        self.ExtenderConfig.style['border'] = '2px'
        self.ExtenderConfig.style['border-color'] = 'blue'
        self.ExtenderConfig.style['flex-direction'] = 'row'
        
        # now setup wireless units for configuration
        wirelessitems = () 
        for wireless in self.WirelessDeviceJSON:
            myID = wireless["id"]
            myName = wireless["name"]
            item = "wireless:/"+ str(myID) + "/" + str(myName)

            wirelessitems = wirelessitems + (item,)
        #print("wirelessitems=", wirelessitems)

        self.listView4 = gui.ListView.new_from_list(wirelessitems, width=400, height=25*len(wirelessitems), margin='10px')
        self.listView4.onselection.do(self.configext_list_view_on_selected)
        vbox.append(self.listView4)
       

        vbox.append(self.ExtenderConfig)


        return vbox


    def buildAnExtender(self, myUnit):
        myExtender = gui.Container(width=300, height=700, layout_orientation=gui.Container.LAYOUT_VERTICAL)
        print("buildAnExtender=", myUnit)
        myExtender.style['position'] = "absolute"
        myExtender.style['background'] = "LightBlue"
        myExtender.style['align-items'] = 'flex-start'
        myExtender.style['border'] = '2px'
        myExtender.style['border-color'] = 'blue'
        myExtender.style['flex-direction'] = 'row'

        myExtenderTop1 = gui.Container(width=300, height=50)
        myExtenderTop1.style['position'] = "relative"
        myExtenderTop1.style['background'] = "LightBlue"
        myExtenderTop1.style['border'] = '2px'
        myExtenderTop1.style['border-color'] = 'blue'

        myExtenderTop2 = gui.Container(width=300, height=30)
        myExtenderTop2.style['position'] = "relative"
        myExtenderTop2.style['background'] = "LightBlue"
        myExtenderTop2.style['border'] = '2px'
        myExtenderTop2.style['border-color'] = 'blue'

        myExtenderTop3 = gui.Container(width=300, height=300)
        myExtenderTop3.style['position'] = "relative"
        myExtenderTop3.style['background'] = "LightBlue"
        myExtenderTop3.style['border'] = '2px'
        myExtenderTop3.style['border-color'] = 'blue'

        #self.valvelist = ('None Selected',)
        ext = myUnit.split("/")
        myID = ext[1]

        self.Display_ExWEXT = gui.Label('', width=130, height=30, margin='5px')
        self.Display_ExWEXT.set_text('Configuring '+myUnit )
        self.Display_ExWEXT.style['position'] = "absolute"
        self.Display_ExWEXT.style['left'] = "10px"

        self.Display_Hydro =     gui.CheckBoxLabel( 'Assign to Hydroponics', False, height=30, style='margin:5px; background: LightBlue; padding-left: 0px; text-indent: 15px' )
        self.Display_Hydro.style['position'] = "absolute"
        self.Display_Hydro.style['left'] = "10px"
        self.Display_Hydro.onclick.do(self.onBoxChange)

        self.Display_Level = gui.CheckBoxLabel( 'Level Sensor', False, height=30, style='margin:5px; background: LightBlue; padding-left: 15px; text-indent: 15px')
        self.Display_Level.style['position'] = "absolute"
        self.Display_Level.style['left'] = "10px"
        self.Display_Level.style['top'] = "10px"
        self.Display_Level.onclick.do(self.onBoxChange)

        self.Display_Temp =      gui.CheckBoxLabel( 'Temperature Sensor', False, height=30, style='margin:5px; background: LightBlue; padding-left: 15px; text-indent: 15px')
        self.Display_Temp.style['position'] = "absolute"
        self.Display_Temp.style['left'] = "10px"
        self.Display_Temp.style['top'] = "40px"
        self.Display_Temp.onclick.do(self.onBoxChange)
        self.Display_TDS =       gui.CheckBoxLabel( 'TDS Sensor', False, height=30, style='margin:5px; background: LightBlue; padding-left: 15px; text-indent: 15px')
        self.Display_TDS.style['position'] = "absolute"
        self.Display_TDS.style['left'] = "10px"
        self.Display_TDS.style['top'] = "70px"
        self.Display_TDS.onclick.do(self.onBoxChange)
        self.Display_Ph =        gui.CheckBoxLabel( 'Ph Sensor', False, height=30, style='margin:5px; background: LightBlue; padding-left: 15px; text-indent: 15px')
        self.Display_Ph.style['position'] = "absolute"
        self.Display_Ph.style['left'] = "10px"
        self.Display_Ph.style['top'] = "100px"
        self.Display_Ph.onclick.do(self.onBoxChange)
        self.Display_Turbidity = gui.CheckBoxLabel( 'Turbidity Sensor', False, height=30, style='margin:5px; background: LightBlue; padding-left: 15px; text-indent: 15px')
        self.Display_Turbidity.style['position'] = "absolute"
        self.Display_Turbidity.style['left'] = "10px"
        self.Display_Turbidity.style['top'] = "130px"
        self.Display_Turbidity.onclick.do(self.onBoxChange)



        self.DisplayExtName = gui.Label('Name for Extender ',width=200, height=30,  style='margin:5px; background: LightBlue ')
        self.DisplayExtName.style['position'] = "absolute"
        self.DisplayExtName.style['left'] = "10px"
        self.DisplayExtName.style['top'] = "170px"

        self.Display_ExtName = gui.TextInput(width=100, height=30, style='margin:5px; background: white; padding-left: 15px' )
        self.Display_ExtName.style['position'] = "absolute"
        self.Display_ExtName.style['left'] = "10px"
        self.Display_ExtName.style['top'] = "190px"
        self.Display_ExtName.onclick.do(self.onBoxChange)

        self.ExtSaveButton = gui.Button('Save Configuration',height=30, width=100, margin=10)
        self.ExtSaveButton.style['position'] = "absolute"
        self.ExtSaveButton.style['left'] = "30px"
        self.ExtSaveButton.style['top'] = "240px"

        self.ExtSaveButton.set_enabled(False)
        self.ExtSaveButton.onclick.do(self.onExtSaveButton)

        self.current_listView_key = myUnit
        # set values
        print ("myID---->=",myID)
        for wireless in self.WirelessDeviceJSON:
            
            myName = wireless["name"]
            if (myID == wireless["id"]):
                # now set the fields
                print("wireless=", wireless)
                self.Display_ExtName.set_value(wireless["name"]) 

                if (wireless["hydroponicsmode"] == 'false'):
                    self.Display_Hydro.set_value(False)
                else:
                    self.Display_Hydro.set_value(True)
                if (wireless["hydroponics_level"] == 'false'):
                    self.Display_Level.set_value(False)
                else:
                    self.Display_Level.set_value(True)
                if (wireless["hydroponics_temperature"] == 'false'):
                    self.Display_Temp.set_value(False)
                else:
                    self.Display_Temp.set_value(True)
                if (wireless["hydroponics_tds"] == 'false'):
                    self.Display_TDS.set_value(False)
                else:
                    self.Display_TDS.set_value(True)
                if (wireless["hydroponics_ph"] == 'false'):
                    self.Display_Ph.set_value(False)
                else:
                    self.Display_Ph.set_value(True)
                if (wireless["hydroponics_turbidity"] == 'false'):
                    self.Display_Turbidity.set_value(False)
                else:
                    self.Display_Turbidity.set_value(True)
                    
                    

        # add to container

        myExtenderTop1.append(self.Display_ExWEXT)
        myExtenderTop2.append(self.Display_Hydro)

        myExtenderTop3.append(self.Display_Level)
        myExtenderTop3.append(self.Display_Temp)
        myExtenderTop3.append(self.Display_TDS)
        myExtenderTop3.append(self.Display_Ph)
        myExtenderTop3.append(self.Display_Turbidity)
        myExtenderTop3.append(self.DisplayExtName)
        myExtenderTop3.append(self.Display_ExtName)
        myExtenderTop3.append(self.ExtSaveButton)

        myExtender.append(myExtenderTop1)
        myExtender.append(myExtenderTop2)
        myExtender.append(myExtenderTop3)

        return myExtender

    def onBoxChange(self, widget, name='', surname=''):
        print("onBoxChange")
        self.ExtSaveButton.set_enabled(True)


    def onExtSaveButton (self, widget, name='', surname=''):
        print("onExtSaveButton Clicked")
        myUnit = self.current_listView_key 
        print("myUnit=", myUnit)    
        myID = myUnit.split("/")[1]
        name = myUnit.split("/")[0]
        # updater the check boxes and name
        print ("myID---->=",myID)
        newWireless = []
        for wireless in self.WirelessDeviceJSON:
            if (myID == wireless["id"]):
                wireless["name"] = self.Display_ExtName.get_value()

                if (self.Display_Hydro.get_value() == True):
                    wireless["hydroponicsmode"] = 'true'
                else:
                    wireless["hydroponicsmode"] = 'false'
                if (self.Display_Level.get_value() == True):
                    wireless["hydroponics_level"] = 'true'
                else:
                    wireless["hydroponics_level"] = 'false'
                if (self.Display_Temp.get_value() == True):
                    wireless["hydroponics_temperature"] = 'true'
                else:
                    wireless["hydroponics_temperature"] = 'false'
                if (self.Display_TDS.get_value() == True):
                    wireless["hydroponics_tds"] = 'true'
                else:
                    wireless["hydroponics_tds"] = 'false'
                if (self.Display_Ph.get_value() == True):
                    wireless["hydroponics_ph"] = 'true'
                else:
                    wireless["hydroponics_ph"] = 'false'
                if (self.Display_Turbidity.get_value() == True):
                    wireless["hydroponics_turbidity"] = 'true'
                else:
                    wireless["hydroponics_turbidity"] = 'false'
                print("wirelessC=", wireless)
            newWireless.append(wireless)
        self.WirelessDeviceJSON = newWireless
        print("wirelessJSON=", self.WirelessDeviceJSON)
        
        self.ExtSaveButton.set_enabled(False)

    def configext_list_view_on_selected(self, widget, selected_item_key):
        """ The selection event of the listView, returns a key of the clicked event.
            You can retrieve the item rapidly
        """
        print("select_item_key=", selected_item_key)
        myUnit =  self.listView4.children[selected_item_key].get_text()
        print("myUnit =", myUnit)
        
        self.myExtender = self.buildAnExtender(myUnit)
        print(self.myExtender)

        self.ExtenderConfig.append(self.myExtender, "currentExtender") 

       
    def wireless_names_list_view_on_selected(self, widget, selected_item_key):
        """ The selection event of the listView, returns a key of the clicked event.
            You can retrieve the item rapidly
        """
        print("wireless_select_item_key=", selected_item_key)
        myUnit =  self.listView2.children[selected_item_key].get_text()

        print("myUnit =", myUnit)
        # put dropdown on unit


        # for on save
        self.current_listView_key = myUnit

        id = myUnit.split("/")[1]
        name = myUnit.split("/")[2]
       

    def open_input_dialog(self, widget, myUnit):

        id = myUnit.split("/")[1]
        name = myUnit.split("/")[2]
        self.renameMyUnit = myUnit
       
        self.inputDialog = gui.InputDialog('Changing '+myUnit, 'New name?',
                                           initial_value=name, 
                                           width=200)
        self.inputDialog.confirm_value.do(
            self.on_input_dialog_confirm)

        # here is returned the Input Dialog widget, and it will be shown
        self.inputDialog.show(self)

    def on_input_dialog_confirm(self, widget, value):
        print("value = ", value) 

        id = self.renameMyUnit.split("/")[1]
        name = self.renameMyUnit.split("/")[2]

        # rename unit
        if (len(id) > 1):
        
            newWireless = [] 
            for wireless in self.WirelessDeviceJSON:
                myID = wireless["id"]
                myName = wireless["name"]
                if (str(id) == str(myID)):
                    # we have the record
                    wireless["name"] = value

                    # now write it out to the unit
                    scanForResources.sendNewNameToUnit(wireless["ipaddress"], value)
                newWireless.append(wireless)
            self.WirelessDeviceJSON = newWireless
             
        self.removeAllScreens()
        self.screen06 = self.buildScreen06()
        self.mainContainer.append(self.screen06,'screen06')


    def buildScreen1(self):


        #screen 1

        vbox = VBox(width=1000, height=600, style="background: LightGray")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'


        #screen 1

        vbox = self.establishMenu(vbox)



        screen1header = gui.Label("Debug / MySQL /MW Tab", style='margin:10px; background: LightGray')
        vbox.append(screen1header)

        #debug config

        debugheader = gui.Label("Debug Configuration", style='position:absolute; left:5px; top:30px; '+self.headerstyle)
        vbox.append(debugheader,'debugheader') 
        self.F_SWDEBUG = gui.CheckBoxLabel( 'enable SW Debugging', self.SWDEBUG, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_SWDEBUG,'self.F_SWDEBUG') 
       
        # mysql configurattion 
        mysqlheader = gui.Label("MySQL Configuration", style='position:absolute; left:5px; top:40px;'+self.headerstyle)
        vbox.append(mysqlheader,'mysqlheader') 
        self.F_enable_MySQL_Logging = gui.CheckBoxLabel('enable MySQL Logging ', False , height=30, style='margin:5px; background:LightGray')
        self.F_enable_MySQL_Logging.set_value(self.enable_MySQL_Logging)
        vbox.append(self.F_enable_MySQL_Logging,'enable_MySQL_Logging') 

        plabel = gui.Label("MySQL Password", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(plabel,'plabel') 
        
        self.F_MySQL_Password = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_MySQL_Password.set_value(self.MySQL_Password)
        vbox.append(self.F_MySQL_Password,'MySQLPassword') 


        plabel = gui.Label("SGS Manual and Tank Control", style='position:absolute; left:5px; top:40px;'+self.labelstyle)

        self.F_manual_water = gui.CheckBoxLabel( 'enable Manual Watering', self.manual_water, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_manual_water,'self.F_manual_water') 
        
        plabel = gui.Label("Hydroponics Tank Calibration", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(plabel,'plabel') 
        
        plabel10 = gui.Label("Full Tank", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(plabel10,'plabelF') 
        self.F_Tank_Pump_Level_Full = gui.TextInput(width=300, height=30, style="margin:10px")
        self.F_Tank_Pump_Level_Full.set_value(str(self.Tank_Pump_Level_Full))
        vbox.append(self.F_Tank_Pump_Level_Full,'Tank_Pump_LevelH') 

        plabelE = gui.Label("Empty Tank", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(plabelE,'plabelE') 
        self.F_Tank_Pump_Level_Empty = gui.TextInput(width=300, height=30, style="margin:10px")
        self.F_Tank_Pump_Level_Empty.set_value(str(self.Tank_Pump_Level_Empty))
        vbox.append(self.F_Tank_Pump_Level_Empty,'Tank_Pump_LevelL') 

        plabel1 = gui.Label("English Or Metric Units ", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(plabel1) 
        self.F_English_Metric = gui.CheckBoxLabel('Use Metric Units (default English)', False , height=30, style='margin:5px; background:LightGray')
        vbox.append(self.F_English_Metric,'english_metric') 


        return vbox


    def buildScreen2(self):

        #screen 2

        vbox = VBox(width=1000, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
       
        vbox = self.establishMenu(vbox)
    

        #screen 
        screenheader = gui.Label("Main and Text Notification Tab", style='margin:10px')
        vbox.append(screenheader)
        
        # mail and text notifications
        MTheader = gui.Label("Mail and Text Notification Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(MTheader,'MTheader') 
        

        plabel = gui.Label("Mail Username", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(plabel,'plabel') 
        
        self.F_mailUser = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_mailUser.set_value(self.mailUser)
        vbox.append(self.F_mailUser,'mailUser') 

        p1label = gui.Label("Mail Password", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p1label,'p1label') 
        
        self.F_mailPassword = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_mailPassword.set_value(self.mailPassword)
        vbox.append(self.F_mailPassword,'mailPassword') 

        p3label = gui.Label("Notify Address", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p3label,'p3label') 
        
        self.F_notifyAddress = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_notifyAddress.set_value(self.notifyAddress)
        vbox.append(self.F_notifyAddress,'notifyAddress') 

        p4label = gui.Label("From Address", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p4label,'p4label') 
        
        self.F_fromAddress = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_fromAddress.set_value(self.fromAddress)
        vbox.append(self.F_fromAddress,'fromAddress') 

        self.F_enableText = gui.CheckBoxLabel( 'enable Text Messaging', self.SWDEBUG, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_enableText,'self.F_enableText') 

        p5label = gui.Label("Text Notify Address", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p5label,'p5label') 
        
        self.F_textnotifyAddress = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_textnotifyAddress.set_value(self.textnotifyAddress)
        vbox.append(self.F_textnotifyAddress,'textnotifyAddress') 

        return vbox
    
    def buildScreen3(self):

        #screen 3

        vbox = VBox(width=1000, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
        
        vbox = self.establishMenu(vbox)
       

       
        #screen 1
        screen1header = gui.Label("Pixel / NeoPixel / SolarMAX Configuration Tab", style='margin:10px')
        vbox.append(screen1header)


        #P1Nheader = gui.Label("Solar Max Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        #vbox.append(P1Nheader,'P1Nheader') 

        #self.F_SolarMAX_Present = gui.CheckBoxLabel( 'SolarMAX Present', self.SolarMAX_Present, height=30, style='margin:5px; background: LightGray ')
        #vbox.append(self.F_SolarMAX_Present,'self.F_SolarMAX_Present') 


        #self.F_SolarMAX_Type = gui.DropDown(width='200px')
        #self.F_SolarMAX_Type.style.update({'font-size':'large'})
        #self.F_SolarMAX_Type.add_class("form-control dropdown")
        #item1 = gui.DropDownItem("LEAD")
        #item2 = gui.DropDownItem("LIPO")
        #self.F_SolarMAX_Type.append(item1,'item1')
        #self.F_SolarMAX_Type.append(item2,'item2')
        #self.F_SolarMAX_Type.select_by_value(self.SolarMAX_Type)
        #vbox.append(self.F_SolarMAX_Type, 'self.F_SolarMAX_Type')

        #P2Nheader = gui.Label("Station Height in Meters", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        #vbox.append(P2Nheader,'P2Nheader') 





        return vbox



    def buildScreen4(self):
        #screen 4

        vbox = VBox(width=1000, height=800, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
        vbox = self.establishMenu(vbox)
   
        #screen 
        screen1header = gui.Label("Garden Camera / Bluetooth Sensors Configuration Tab", style='margin:10px')
        vbox.append(screen1header)


        p5label1 = gui.Label("Garden Cam Interval between pictures (seconds)", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p5label1,'p5label1') 
        
        self.F_INTERVAL_CAM_PICS__SECONDS = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_INTERVAL_CAM_PICS__SECONDS.set_value(str(self.INTERVAL_CAM_PICS__SECONDS))
        vbox.append(self.F_INTERVAL_CAM_PICS__SECONDS,'INTERVAL_CAM_PICS__SECONDS') 
        p5label2 = gui.Label("Infrared Camera Gain Configuration", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p5label2,'p5label2') 
        
        self.F_Infrared_High_Auto = gui.CheckBoxLabel( 'High Auto Gain', self.Infrared_High_Auto_Gain, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_Infrared_High_Auto,'self.F_Infrared_High_Auto') 
        
        p5label3 = gui.Label("Infrared High Temp Set (degrees C) ", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p5label3,'p5label3') 
        self.F_Infrared_High_Temp = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_Infrared_High_Temp.set_value(str(self.Infrared_High_Temp))
        vbox.append(self.F_Infrared_High_Temp,'Infrared_High_Temp') 
        
        self.F_Infrared_Low_Auto = gui.CheckBoxLabel( 'Low Auto Gain', self.Infrared_Low_Auto_Gain, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_Infrared_Low_Auto,'self.F_Infrared_Low_Auto') 

        p5label4 = gui.Label("Infrared Low Temp Set  (degrees C)", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p5label4,'p5label4') 


        self.F_Infrared_Low_Temp = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_Infrared_Low_Temp.set_value(str(self.Infrared_Low_Temp))
        vbox.append(self.F_Infrared_Low_Temp,'Infrared_Low_Temp') 
        
        

        p5label = gui.Label("Bluetooth Sensor Assignment (select one) ", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p5label,'p5label') 
       
        # get list of bluetooth sensors

        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                
                query = "SELECT * FROM BluetoothSensors" 

                print("query=", query)
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




        btitems = ()
        for record in myRecords: 
            myID = record[3]
            myName = record[5]
            if (myName == None):
                myName = "No Name"
            if (record[4] == ""):
                myAssign = "Not Assigned"
            else:
                myAssign = record[4]

            btitem = "bluetooth sensor:/"+ str(myID) + "/" + str(myName) + "/ Assigned To: %s" % (myAssign) 

            btitems = btitems + (btitem,)

        print("btitem count=", len(btitems))
       

        # list out wireless units
       
        wirelessList = ('Not Assigned',)
        for wireless in self.WirelessDeviceJSON:
            myID = wireless["id"]
            myName = wireless["name"]
            wirelessItem = "wireless:/"+ str(myID) + "/" + str(myName)

            wirelessList = wirelessList + (wirelessItem,)


        items = ()
        for ext in wirelessList:
            item = (str(ext[1])+" / "+str(ext[0])+ " / " +str(ext[2]))
            
            items = items +  (item, )

        
        # now set up new block
        self.ValveBlock1 = gui.Container(width=1000, height=700, layout_orientation=gui.Container.LAYOUT_HORIZONTAL)
        self.ValveBlock1.style['background'] = "LightGray"

        self.ValveBlock1.style['align-items'] = 'right'
        self.ValveBlock1.style['border'] = '2px'
        self.ValveBlock1.style['border-color'] = 'blue'
        self.ValveBlock1.style['flex-direction'] = 'row'



        self.listView8 = gui.ListView.new_from_list(btitems, width=500, height=25*len(btitems), margin='10px')
        self.listView8.onselection.do(self.wireless_list_view_on_selected)
        self.ValveBlock1.append(self.listView8)
        
        vbox.append(self.ValveBlock1)

        return vbox

    def buildScreen5(self):
        #screen 5

        vbox = VBox(width=1000, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'


        vbox = self.establishMenu(vbox)
   
   

        #screen 1
        screen1header = gui.Label("Blynk", style='margin:10px')
        vbox.append(screen1header)



        P5Nheader = gui.Label("Blynk Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P5Nheader,'P5Nheader') 

        self.F_USEBLYNK = gui.CheckBoxLabel( 'Enable Blynk', self.USEBLYNK, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_USEBLYNK,'self.F_USEBLYNK') 

        p8label = gui.Label("Blynk App Authorization", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p8label,'p8label') 
        
        self.F_BLYNK_AUTH = gui.TextInput(width=300, height=30, style="margin:5px")
        self.F_BLYNK_AUTH.set_value(self.BLYNK_AUTH)
        vbox.append(self.F_BLYNK_AUTH,'BLYNK_AUTH') 
        #
        #P1Nheader = gui.Label("ThunderBoard AS3935 Configuration", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        #vbox.append(P1Nheader,'P1Nheader') 

        #P2Nheader = gui.Label("Format:[NoiseFloor, Indoor, TuneCap, DisturberDetection, WatchDogThreshold, SpikeDetection] ", style='position:absolute; left:5px; top:30px;'+self.labelstyle)
        #vbox.append(P2Nheader,'P2Nheader') 
        

        #p9label = gui.Label("Thunderboard Configuration", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        #vbox.append(p9label,'p9label') 
        
        #self.F_AS3935_Lightning_Config  = gui.TextInput(width=300, height=30, style="margin:5px")
        #self.F_AS3935_Lightning_Config .set_value(self.AS3935_Lightning_Config )
        #vbox.append(self.F_AS3935_Lightning_Config ,'AS3935_Lightning_Config ') 


        return vbox

    def buildScreen6(self):
        #screen 6

        vbox = VBox(width=1000, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
        vbox = self.establishMenu(vbox)
   

        #screen 
        screenheader = gui.Label("Pin Config Tab", style='margin:10px')
        vbox.append(screenheader)
        
        # short headers

        shortlabelstyle = 'font-family:monospace; width:200; font-size:15px; margin:5px; background:LightGray' 



        P5Nheader = gui.Label("Pin Configurations", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P5Nheader,'P5Nheader') 

        p8label = gui.Label("Ultrasonic Pin ", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p8label,'p8label') 
        

        p1label = gui.Label("Pixel Pin", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p1label,'p1label') 
        self.F_pixelPin = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_pixelPin.set_value(str(self.pixelPin))
        vbox.append(self.F_pixelPin,'pixelPin') 
        

        return vbox


    def buildScreen7(self):
        #screen 7

        vbox = VBox(width=1000, height=510, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
        vbox = self.establishMenu(vbox)

        #screen 
        screenheader = gui.Label("Camera / MQTT / Rest Tab", style='margin:10px')
        vbox.append(screenheader)
        
        # short headers

        shortlabelstyle = 'font-family:monospace; width:200; font-size:15px; margin:5px; background:LightGray' 



        P5Nheader = gui.Label("Night Camera Enable", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P5Nheader,'P5Nheader') 
        self.F_Camera_Night_Enable = gui.CheckBoxLabel( 'Night Vision Enable', self.Camera_Night_Enable, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_Camera_Night_Enable,'self.F_Camera_Night_Enable') 

        P7Nheader = gui.Label("REST Interface", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P7Nheader,'P7Nheader') 
        self.F_REST_Enable = gui.CheckBoxLabel( 'REST Enable', self.REST_Enable, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_REST_Enable,'self.F_REST_Enable') 


        P6Nheader = gui.Label("MQTT Configuration (SGS OUT to other broker)", style='position:absolute; left:5px; top:30px;'+self.headerstyle)
        vbox.append(P6Nheader,'P6Nheader') 

        self.F_MQTT_Enable = gui.CheckBoxLabel( 'MQTT Enable', self.MQTT_Enable, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_MQTT_Enable,'self.F_MQTT_Enable') 

        p4label = gui.Label("MQTT Server URL ", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p4label,'p4label') 
        
        self.F_MQTT_Server_URL = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_MQTT_Server_URL.set_value(self.MQTT_Server_URL)
        vbox.append(self.F_MQTT_Server_URL,'MQTT_Server_URL') 

        p3label = gui.Label("MQTT Server Port Number ", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p3label,'p3label') 
        
        self.F_MQTT_Port_Number = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_MQTT_Port_Number.set_value(str(self.MQTT_Port_Number))
        vbox.append(self.F_MQTT_Port_Number,'MQTT_Port_Number') 

        p2label = gui.Label("How Often MQTT Sent in Seconds ", style='position:absolute; left:5px; top:40px;'+shortlabelstyle)
        vbox.append(p2label,'p2label') 
        
        self.F_MQTT_Send_Seconds = gui.TextInput(width=200, height=30, style="margin:5px")
        self.F_MQTT_Send_Seconds.set_value(str(self.MQTT_Send_Seconds))
        vbox.append(self.F_MQTT_Send_Seconds,'MQTT_Send_Seconds') 





        return vbox

    def StoreC(self, temperature):
        EorM = self.F_English_Metric.get_value()

        if (EorM == False):  # english units
            temperature = 5.0/9.0*(float(temperature) - 32.0) 
        return int(round(temperature,0))



    def CTUnits(self, temperature):

        EorM = self.F_English_Metric.get_value()

        if (EorM == False):  # english units
            temperature = (9.0/5.0 * float(temperature)) +32.0
        return int(round(temperature,0))


    def TUnit(self):
        EorM = self.F_English_Metric.get_value()
        if (EorM == False):
            return "F"
        else:
            return "C"

    def buildScreen8(self):
        #screen 8

        vbox = VBox(width=1000, height=800, style="background: LightGray; border: 5px solid red")

        vbox.style['justify-content'] = 'flex-start'
        vbox.style['align-items'] = 'flex-start'
        vbox.style['border'] = '2px'
        vbox.style['border-color'] = 'blue'
       
        vbox = self.establishMenu(vbox)
   
        #screen 
        screen1header = gui.Label("Alarm and Status Tab", style='margin:10px')
        vbox.append(screen1header)
        
        self.F_Send_Status_Email = gui.CheckBoxLabel( 'Send Status Email', self.Send_Status_Email, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_Send_Status_Email,'self.F_Send_Status_Email') 
        p8label1 = gui.Label("Send every how many minutes", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p8label1,'p8label1') 
        self.F_Status_Send_Email_Minutes = gui.TextInput(width=100, height=30, style="margin:5px")
        self.F_Status_Send_Email_Minutes.set_value(str(self.Status_Send_Email_Minutes))
        vbox.append(self.F_Status_Send_Email_Minutes,'Status_Send_Email_Minutes') 
        
        self.F_Send_Status_Text = gui.CheckBoxLabel( 'Send Status Text', self.Send_Status_Text, height=30, style='margin:5px; background: LightGray ')
        vbox.append(self.F_Send_Status_Text,'self.F_Send_Status_Text') 

        p8label2 = gui.Label("Send every how many minutes", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p8label2,'p8label2') 
        self.F_Status_Send_Text_Minutes = gui.TextInput(width=100, height=30, style="margin:5px")
        self.F_Status_Send_Text_Minutes.set_value(str(self.Status_Send_Text_Minutes))
        vbox.append(self.F_Status_Send_Text_Minutes,'Status_Send_Text_Minutes') 
       
        p5label = gui.Label("Sensor Alarm Assignment", style='position:absolute; left:5px; top:40px;'+self.labelstyle)
        vbox.append(p5label,'p5label') 
       
        # get list of bluetooth sensors

        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                
                query = "SELECT * FROM BluetoothSensors" 

                print("query=", query)
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




        btitems = ()
        for record in myRecords: 
            myID = record[3]
            myName = record[5]
            if (myName == None):
                myName = "No Name"
            if (record[4] == ""):
                myAssign = "Not Assigned"
            else:
                myAssign = record[4]

            btitem = "bluetooth sensor:/"+ str(myID) + "/" + str(myName) + "/ Assigned To: %s" % (myAssign) 

            btitems = btitems + (btitem,)
        
        myHydroID = "" 
        for wireless in self.WirelessDeviceJSON:
            print("wireless=", wireless)

            if (wireless['hydroponicsmode'] == "true"):
                myHydroID = wireless['id']
                break

        if (myHydroID != ""): 
            btitem = "hydroponics sensors/"+ myHydroID 
            btitems = btitems + (btitem,)
        print("btitem count=", len(btitems))
       

        # list out wireless units
       
        wirelessList = ('Not Assigned',)
        for wireless in self.WirelessDeviceJSON:
            myID = wireless["id"]
            myName = wireless["name"]
            wirelessItem = "wireless:/"+ str(myID) + "/" + str(myName)

            wirelessList = wirelessList + (wirelessItem,)


        items = ()
        for ext in wirelessList:
            item = (str(ext[1])+" / "+str(ext[0])+ " / " +str(ext[2]))
            
            items = items +  (item, )

        
        # now set up new block
        self.AlarmBlock1 = gui.Container(width=1000, height=700, layout_orientation=gui.Container.LAYOUT_HORIZONTAL)
        #self.AlarmBlock1.style['position'] = "absolute"
        #self.AlarmBlock1.style['left'] = '400px'
        self.AlarmBlock1.style['background'] = "lightgray"
        self.AlarmBlock1.style['align-items'] = 'right'
        self.AlarmBlock1.style['border'] = '6px'
        self.AlarmBlock1.style['border-color'] = 'black'
        self.AlarmBlock1.style['flex-direction'] = 'row'




        self.listView1 = gui.ListView.new_from_list(btitems, width=500, height=25*len(btitems), margin='10px')
        self.listView1.onselection.do(self.alarm_wireless_list_view_on_selected)
        self.AlarmBlock1.append(self.listView1)
        
        vbox.append(self.AlarmBlock1)

        return vbox

    def alarm_wireless_list_view_on_selected(self, widget, selected_item_key):
        """ The selection event of the listView, returns a key of the clicked event.
            You can retrieve the item rapidly
        """
        myUnit =  self.listView1.children[selected_item_key].get_text()
        print("list_view: myUnit=", myUnit)
        # for on save
        self.current_listView_key = myUnit

        myID = myUnit.split("/")[1]
        name = myUnit.split("/")[0]

        #mySplit = myUnit.split(":")
        #assignedAddress = mySplit[3]
        #assignedAddress = assignedAddress.replace(" ", "")
        #print("assignedAddress=", assignedAddress)
        myOffsetX = 510
        myOffsetY = 445
        self.SelectedAlarmID = myID
        self.SelectedAlarmName = name 


        self.BackBlock = gui.Container(width=445, height=445, layout_orientation=gui.Container.LAYOUT_HORIZONTAL)
        self.BackBlock.style['background'] = "lightblue"
        self.BackBlock.style['border'] = '6px'
        self.BackBlock.style['border-color'] = 'black'
        self.BackBlock.style['flex-direction'] = 'row'
        self.BackBlock.style['position'] = "absolute"
        self.BackBlock.style['left'] = str(myOffsetX + 0)+"px" 
        self.BackBlock.style['top'] = str(myOffsetY + 0 )+"px"




        self.DisplaySelect1 = gui.Label('Set Alarms ',width=100, height=20, margin='5px')
        self.DisplaySelect1.style['font-size'] = "20px"
        self.DisplaySelect1.style['position'] = "absolute"
        self.DisplaySelect1.style['left'] = str(myOffsetX + 0)+"px" 
        self.DisplaySelect1.style['top'] = str(myOffsetY + 0 )+"px"
        
        self.Display_ExWEXT1 = gui.Label('', width=400, height=60, margin='5px')
        self.Display_ExWEXT1.set_text('Configuring '+myUnit )
        self.Display_ExWEXT1.style['position'] = "absolute"
        self.Display_ExWEXT1.style['left'] = str(myOffsetX + 0)+"px" 
        self.Display_ExWEXT1.style['top'] = str(myOffsetY + 30 )+"px"

        self.Display_Moisture =     gui.CheckBoxLabel( 'Moisture Alarm', False, height=30, style='margin:5px; background: LightBlue; padding-left: 0px; text-indent: 15px ' )
        self.Display_Moisture.style['position'] = "absolute"
        self.Display_Moisture.style['left'] = str(myOffsetX + 0)+"px" 
        self.Display_Moisture.style['top'] = str(myOffsetY + 60 )+"px"
        self.Display_Moisture.onclick.do(self.onAlarmBoxChange)

        self.Display_MoistureMinLabel = gui.Label('less than',width=70, height=30,  style='margin:5px; background: LightBlue ')
        self.Display_MoistureMinLabel.style['position'] = "absolute"
        self.Display_MoistureMinLabel.style['left'] = str(myOffsetX + 0)+"px" 
        self.Display_MoistureMinLabel.style['top'] = str(myOffsetY + 90 )+"px"

        self.Display_MoistureMin = gui.TextInput(width=50, height=15, style='margin:5px; background: white; padding-left: 15px' )
        self.Display_MoistureMin.set_text("65")
        self.Display_MoistureMin.style['position'] = "absolute"
        self.Display_MoistureMin.style['left'] = str(myOffsetX + 75)+"px" 
        self.Display_MoistureMin.style['top'] = str(myOffsetY + 90 )+"px"
        self.Display_MoistureMin.onchange.do(self.onAlarmBoxChange)

        self.Display_MoistureLabel2 = gui.Label(' %   or greater than',width=150, height=30,  style='margin:5px; background: LightBlue ')
        self.Display_MoistureLabel2.style['position'] = "absolute"
        self.Display_MoistureLabel2.style['left'] = str(myOffsetX + 147)+"px" 
        self.Display_MoistureLabel2.style['top'] = str(myOffsetY + 90 )+"px"

        self.Display_MoistureMax = gui.TextInput(width=50, height=15, style='margin:5px; background: white; padding-left: 15px' )
        self.Display_MoistureMax.set_text("100")
        self.Display_MoistureMax.style['position'] = "absolute"
        self.Display_MoistureMax.style['left'] = str(myOffsetX + 295)+"px" 
        self.Display_MoistureMax.style['top'] = str(myOffsetY + 90 )+"px"
        self.Display_MoistureMax.onchange.do(self.onAlarmBoxChange)

        self.Display_MoistureLabel3 = gui.Label(' %',width=30, height=30,  style='margin:5px; background: LightBlue ')
        self.Display_MoistureLabel3.style['position'] = "absolute"
        self.Display_MoistureLabel3.style['left'] = str(myOffsetX + 360)+"px" 
        self.Display_MoistureLabel3.style['top'] = str(myOffsetY + 90 )+"px"



        self.Display_Temperature =     gui.CheckBoxLabel( 'Temperature Alarm', False, height=30, style='margin:5px; background: LightBlue; padding-left: 0px; text-indent: 15px' )
        self.Display_Temperature.style['position'] = "absolute"
        self.Display_Temperature.style['left'] = str(myOffsetX + 0)+"px" 
        self.Display_Temperature.style['top'] = str(myOffsetY + 130 )+"px"
        self.Display_Temperature.onclick.do(self.onAlarmBoxChange)

        self.Display_TemperatureLabel = gui.Label('less than',width=70, height=30,  style='margin:5px; background: LightBlue ')
        self.Display_TemperatureLabel.style['position'] = "absolute"
        self.Display_TemperatureLabel.style['left'] = str(myOffsetX + 0)+"px" 
        self.Display_TemperatureLabel.style['top'] = str(myOffsetY + 160 )+"px"

        self.Display_TemperatureMin = gui.TextInput(width=50, height=15, style='margin:5px; background: white; padding-left: 15px' )
        self.Display_TemperatureMin.set_text("-100")
        self.Display_TemperatureMin.style['position'] = "absolute"
        self.Display_TemperatureMin.style['left'] = str(myOffsetX + 75)+"px" 
        self.Display_TemperatureMin.style['top'] = str(myOffsetY + 160 )+"px"
        self.Display_TemperatureMin.onchange.do(self.onAlarmBoxChange)

        self.Display_TemperatureLabel2 = gui.Label(" "+self.TUnit()+'   or greater than',width=150, height=30,  style='margin:5px; background: LightBlue ')
        self.Display_TemperatureLabel2.style['position'] = "absolute"
        self.Display_TemperatureLabel2.style['left'] = str(myOffsetX + 145)+"px" 
        self.Display_TemperatureLabel2.style['top'] = str(myOffsetY + 160 )+"px"

        self.Display_TemperatureMax = gui.TextInput(width=50, height=15, style='margin:5px; background: white; padding-left: 15px' )
        self.Display_TemperatureMax.set_text("200")
        self.Display_TemperatureMax.style['position'] = "absolute"
        self.Display_TemperatureMax.style['left'] = str(myOffsetX + 295)+"px" 
        self.Display_TemperatureMax.style['top'] = str(myOffsetY + 160 )+"px"
        self.Display_TemperatureMax.onchange.do(self.onAlarmBoxChange)

        self.Display_TemperatureLabel3 = gui.Label(" "+self.TUnit(),width=30, height=30,  style='margin:5px; background: LightBlue ')
        self.Display_TemperatureLabel3.style['position'] = "absolute"
        self.Display_TemperatureLabel3.style['left'] = str(myOffsetX + 360)+"px" 
        self.Display_TemperatureLabel3.style['top'] = str(myOffsetY + 160 )+"px"


        self.DisplaySelect2 = gui.Label('Trigger Count',width=150, height=20, margin='5px')
        self.DisplaySelect2.style['font-size'] = "20px"
        self.DisplaySelect2.style['position'] = "absolute"
        self.DisplaySelect2.style['left'] = str(myOffsetX + 0)+"px" 
        self.DisplaySelect2.style['top'] = str(myOffsetY + 190 )+"px"
        
        self.Display_TriggerMaxL = gui.Label('Trigger Max',width=120, height=30,  style='margin:5px; background: LightBlue ')
        self.Display_TriggerMaxL.style['position'] = "absolute"
        self.Display_TriggerMaxL.style['left'] = str(myOffsetX + 0)+"px" 
        self.Display_TriggerMaxL.style['top'] = str(myOffsetY + 220 )+"px"

        self.Display_TriggerMax = gui.TextInput(width=50, height=15, style='margin:5px; background: white; padding-left: 15px' )
        self.Display_TriggerMax.set_text("0")
        self.Display_TriggerMax.style['position'] = "absolute"
        self.Display_TriggerMax.style['left'] = str(myOffsetX + 120)+"px" 
        self.Display_TriggerMax.style['top'] = str(myOffsetY + 220 )+"px"
        self.Display_TriggerMax.onchange.do(self.onAlarmBoxChange)

        self.DisplaySelect3 = gui.Label('Notifications',width=150, height=20, margin='5px')
        self.DisplaySelect3.style['font-size'] = "20px"
        self.DisplaySelect3.style['position'] = "absolute"
        self.DisplaySelect3.style['left'] = str(myOffsetX + 0)+"px" 
        self.DisplaySelect3.style['top'] = str(myOffsetY + 250 )+"px"
        
        self.Display_AEmail =     gui.CheckBoxLabel( 'Email Notification of Alarm', False, height=30, style='margin:5px; background: LightBlue; padding-left: 0px; text-indent: 15px' )
        self.Display_AEmail.style['position'] = "absolute"
        self.Display_AEmail.style['left'] = str(myOffsetX + 0)+"px" 
        self.Display_AEmail.style['top'] = str(myOffsetY + 280 )+"px"

        self.Display_AText =     gui.CheckBoxLabel( 'Text Notification of Alarm', False, height=30, style='margin:5px; background: LightBlue; padding-left: 0px; text-indent: 15px' )
        self.Display_AText.style['position'] = "absolute"
        self.Display_AText.style['left'] = str(myOffsetX + 0)+"px" 
        self.Display_AText.style['top'] = str(myOffsetY + 310 )+"px"

        self.SaveAlarm = gui.Button('Save Alarm',height=50, width=100, margin=10)
        self.SaveAlarm.style['font-size'] = "20px"
        self.SaveAlarm.style['position'] = "absolute"
        self.SaveAlarm.style['left'] = str(myOffsetX + 10)+"px" 
        self.SaveAlarm.style['top'] = str(myOffsetY + 360 )+"px"
        self.SaveAlarm.set_enabled(False)
        self.SaveAlarm.onclick.do(self.onAlarmSaveButton)


        self.AlarmBlock1.append(self.BackBlock, "BB1")
        self.AlarmBlock1.append(self.DisplaySelect1, "DS1") 
        self.AlarmBlock1.append(self.Display_ExWEXT1, "EX1") 

        self.AlarmBlock1.append(self.Display_Moisture, "DM1") 
        self.AlarmBlock1.append(self.Display_MoistureMinLabel, "DM2") 
        self.AlarmBlock1.append(self.Display_MoistureMin, "DM3") 
        self.AlarmBlock1.append(self.Display_MoistureLabel2, "DM4") 
        self.AlarmBlock1.append(self.Display_MoistureMax, "DM5") 
        self.AlarmBlock1.append(self.Display_MoistureLabel3, "DM6") 

        self.AlarmBlock1.append(self.Display_Temperature, "DT1") 
        self.AlarmBlock1.append(self.Display_TemperatureLabel, "DT2") 
        self.AlarmBlock1.append(self.Display_TemperatureMin, "DT3") 
        self.AlarmBlock1.append(self.Display_TemperatureLabel2, "DT4") 
        self.AlarmBlock1.append(self.Display_TemperatureMax, "DT5") 
        self.AlarmBlock1.append(self.Display_TemperatureLabel3, "DT6") 

        self.AlarmBlock1.append(self.DisplaySelect2, "BB2") 
        self.AlarmBlock1.append(self.Display_TriggerMaxL, "TM1") 
        self.AlarmBlock1.append(self.Display_TriggerMax, "TM2") 

        self.AlarmBlock1.append(self.DisplaySelect3, "N1") 
        self.AlarmBlock1.append(self.Display_AEmail, "N2") 
        self.AlarmBlock1.append(self.Display_AText, "N3") 

        self.AlarmBlock1.append(self.SaveAlarm, "SA1") 
 

        # now set up values right
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                
                query = "SELECT * FROM Alarms WHERE address = '%s'" % (myID)

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
        if (len(myRecords) > 0):

            # deal with C to F conversion
            print("temp min Records=", myRecords[0][9])
            print("temp max Records=", myRecords[0][10])
            temperatureminimum = self.CTUnits(float(myRecords[0][9]))
            temperaturemaximum = self.CTUnits(float(myRecords[0][10]))
            print("temp min =", temperatureminimum)
            print("temp max =", temperaturemaximum) 
            triggerlimit = myRecords[0][12] 
            emailnotification = myRecords[0][14] 
            textnotification = myRecords[0][15] 
            moisturealarm = myRecords[0][5] 
            moistureminimum = myRecords[0][6] 
            moisturemaximum = myRecords[0][7] 
            temperaturealarm = myRecords[0][8] 
        
            if (moisturealarm == "True"):
                self.Display_Moisture.set_value(True)
            else:
                self.Display_Moisture.set_value(False)
            self.Display_MoistureMin.set_value(str(moistureminimum))
            self.Display_MoistureMax.set_value(str(moisturemaximum))
         
            if (temperaturealarm == "True"):
                self.Display_Temperature.set_value(True)
            else:
                self.Display_Temperature.set_value(False)
            self.Display_TemperatureMin.set_value(str(temperatureminimum))
            self.Display_TemperatureMax.set_value(str(temperaturemaximum))
         
            self.Display_TriggerMax.set_value(str(triggerlimit))

            if (emailnotification == "True"):
                self.Display_AEmail.set_value(True)
            else:
                self.Display_AEmail.set_value(False)

            if (textnotification == "True"):
                self.Display_AText.set_value(True)
            else:
                self.Display_AText.set_value(False)

       
 
        
    def onAlarmBoxChange(self, widget, name='', surname=''):
        print("onAlarmBoxChange")
        self.SaveAlarm.set_enabled(True)

    def onAlarmSaveButton (self, widget, name='', surname=''):
        print("On Alarm Save Button Push")
        self.SaveAlarm.set_enabled(False)
        myName = self.SelectedAlarmName.strip() 
        myID = self.SelectedAlarmID.strip()
        print("id=", myID) 
        print("name=", myName)
        if (myName == "bluetooth sensor:"):
            bluetooth = "True"
            hydroponics = "False"
        else:
            bluetooth = "False"
            hydroponics = "True"

        address = myID
        moisturealarm = self.Display_Moisture.get_value()
        moistureminimum = self.Display_MoistureMin.get_value()
        moisturemaximum = self.Display_MoistureMax.get_value()
        temperaturealarm = self.Display_Temperature.get_value()
        temperatureminimum = self.StoreC( float(self.Display_TemperatureMin.get_value()))
        temperaturemaximum = self.StoreC(float(self.Display_TemperatureMax.get_value()))
        triggerlimit = self.Display_TriggerMax.get_value()
        emailnotification = self.Display_AEmail.get_value()
        textnotification = self.Display_AText.get_value()

        triggercount = 0

        '''
        print("bluetooth=", bluetooth)
        print("hydroponics=", hydroponics)
        print("MA=", moisturealarm)
        print("MM=", moistureminimum)
        print("MX=", moisturemaximum)
        print("TA=", temperaturealarm)
        print("TM=", temperatureminimum)
        print("TX=", temperaturemaximum)
        print("TL=", triggerlimit)
        print("TC=", triggercount)
        '''
        # deal with list of Alarms
        

        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                
                query = "DELETE FROM Alarms WHERE address = '%s'" % (address)

                #print("query=", query)
                cur.execute(query)
                con.commit()
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                myRecords = [];
        finally:
                cur.close()
                con.close()

                del cur
                del con
        # put in new record
        
        if ((moisturealarm== True) or (temperaturealarm== True)): 
        # ignore if alarms are not asked for (record deleted)

            try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
               
                myFields = "bluetooth, hydroponics, address, moisturealarm, moistureminimum, moisturemaximum, temperaturealarm, temperatureminimum, temperaturemaximum, triggerlimit, triggercount, emailnotification, textnotification"

                myValues = "'%s', '%s', '%s', '%s',  %d, %d, '%s', %d, %d, %d, %d, '%s', '%s' " % (bluetooth, hydroponics, address, moisturealarm, int(moistureminimum), int(moisturemaximum), temperaturealarm, int(temperatureminimum), int(temperaturemaximum), int(triggerlimit), int(triggercount), emailnotification, textnotification)

                query = "INSERT INTO Alarms(%s) VALUES (%s) " % (myFields, myValues)

                #print("query=", query)
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
        


    def main(self):

        self.readJSON()
        self.readJSONSGSConfiguration()

        #this flag will be used to stop the display_counter Timer
        self.stop_flag = True 
        self.count = 0
        self.ScanRunning = False
        self.SFHWorking = False
        # progress counter 
        self.progress = gui.Progress(1, 100, width=200, height=30, style='margin: 10px')

        # kick off regular display of counter
        self.display_counter() 

        # GUI default information
        self.dropDownValveSelected = "None"





        widthBox = 1000
        heightBox = 900
        self.mainContainer = Container(width=widthBox, height=heightBox, margin='0px auto', style="position: relative")
        self.mainContainer.style['justify-content'] = 'flex-start'
        self.mainContainer.style['align-items'] = 'flex-start'


        logo = SuperImage("./static/SGfulllogocolor.png", width=400, height =142)
        header = gui.Label("SmartGarden3 Configuration Tool V010", style='position:absolute; left:150px; top:120px')
        # bottom buttons

        cancel = gui.Button('Cancel',style='position:absolute; left:550px; height: 30px; width:100px; margin:10px; top:5px')
        cancel.onclick.do(self.onCancel)
        save = gui.Button('Save',style='position:absolute; left:400px; height: 30px; width:100px;  margin: 10px;  top:5px')
        save.onclick.do(self.onSave)
        saveandreload = gui.Button('Save and Reload SGS',style='position:absolute; left:675px; height: 30px; width:100px;  margin: 10px;  top:5px')
        saveandreload.onclick.do(self.onSaveAndReloadSGS)
        exit = gui.Button('Save and Exit',style='position:absolute; left:500px; height: 30px; width:100px;  margin: 10px;  top:95px')
        exit.onclick.do(self.onExit)
        reset = gui.Button('Reset to Defaults',style='position:absolute; left:400px;height: 30px;   width:250px; margin: 10px; top:50px')
        reset.onclick.do(self.onReset)
        # appending a widget to another
        self.mainContainer.append(logo)
        self.mainContainer.append(header)
        self.mainContainer.append(cancel)
        self.mainContainer.append(save)
        self.mainContainer.append(saveandreload)
        self.mainContainer.append(exit)
        self.mainContainer.append(reset)


        # configuation fields
       

        self.headerstyle= 'width:400px; font-family:monospace; font-size:20px; margin:10px; background:LightBlue'
        self.labelstyle = 'font-family:monospace; font-size:15px; margin:5px; background:LightGray' 

        # build screens


        self.screen0 = self.buildScreen0()
        self.screen05 = self.buildScreen05()
        self.screen06 = self.buildScreen06()
        self.screen1 = self.buildScreen1()
        self.screen2 = self.buildScreen2()
        #self.screen3 = self.buildScreen3()
        self.screen4 = self.buildScreen4()
        self.screen5 = self.buildScreen5()
        #self.screen6 = self.buildScreen6()
        self.screen7 = self.buildScreen7()
        self.screen8 = self.buildScreen8()


        self.mainContainer.append(self.screen0,'screen0')
        



        # returning the root widget
        
        return self.mainContainer


    # listener functions


    def removeAllScreens(self):
        
        self.mainContainer.remove_child(self.screen0)
        self.mainContainer.remove_child(self.screen05)
        self.mainContainer.remove_child(self.screen06)
        self.mainContainer.remove_child(self.screen1)
        self.mainContainer.remove_child(self.screen2)
        #self.mainContainer.remove_child(self.screen3)
        self.mainContainer.remove_child(self.screen4)
        self.mainContainer.remove_child(self.screen5)
        #self.mainContainer.remove_child(self.screen6)
        self.mainContainer.remove_child(self.screen7)
        self.mainContainer.remove_child(self.screen8)
        
    # listener functions

    def menu_screen0_clicked(self, widget):
        self.removeAllScreens()
        self.screen0 = self.buildScreen0()
        self.mainContainer.append(self.screen0,'screen0')
        print("menu screen0 clicked")  

    def menu_screen05_clicked(self, widget):
        self.removeAllScreens()
        self.screen05 = self.buildScreen05()
        self.mainContainer.append(self.screen05,'screen05')
        print("menu screen05 clicked")  

    def menu_screen06_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen06,'screen06')
        print("menu screen06 clicked")  

    def menu_screen1_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen1,'screen1')
        print("menu screen1 clicked")  

    def menu_screen2_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen2,'screen2')
        print("menu screen2 clicked")

    def menu_screen3_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen3,'screen3')
        print("menu screen3 clicked")

    def menu_screen4_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen4,'screen4')
        print("menu screen4 clicked")

    def menu_screen5_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen5,'screen5')
        print("menu screen5 clicked")

    def menu_screen6_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen6,'screen6')
        print("menu screen6 clicked")


    def menu_screen7_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen7,'screen7')
        print("menu screen7 clicked")

    def menu_screen8_clicked(self, widget):
        self.removeAllScreens()
        self.mainContainer.append(self.screen8,'screen8')
        print("menu screen8 clicked")

    # scanning sofrware

    def ScanForHardware(self, widget, name='', surname=''):
        print("self.SFHWorking =", self.SFHWorking)
        # disable menu
        self.menubar.set_enabled(False)
        if (self.SFHWorking == False): 
            self.SFHWorking = True
            SFHThread = threading.Thread(target=self.ScanForHardwareWorker, args=('name',))

            SFHThread.start()
    

    def ScanForHardwareWorker(self, name): 
       

        print ("Scanning for Hardware")
        self.stop_flag = False
        
        
        IPAddr = subprocess.check_output(['hostname', '-I'])
       
        IPAddr = IPAddr.decode()
        IPAddr = IPAddr.split(" ")
        print("Your Computer IP Address is:" + IPAddr[0])  
        myNetIP = IPAddr[0].split(".")
        myNetIP = myNetIP[0]+"."+myNetIP[1]+"."+myNetIP[2]+".0"
        CIDR = ipaddress.IPv4Network(myNetIP+"/24")
        print("Your Computer CIDR is:", CIDR)
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Start Time =", str(now))
        returnJSON = []
       
        for ip in ipaddress.IPv4Network(CIDR):

    
            self.count = self.count+1
            self.Display_IP.set_text('Scanning IP: ' + str(ip))
            self.Display_WEXT.set_text('Found Wireless Extenders: '+ str(len(returnJSON)))
            JSON = "" 
            JSON = scanForResources.checkForDeviceFromIP(ip)
            #print("JSON=", JSON)
            #print("JSONLength=", len(JSON))
            if len(JSON) != 0 :
                print("JSON=", JSON)
                JSON['hydroponicsmode'] = 'false'
                JSON['hydroponics_temperature'] = 'false'
                JSON['hydroponics_tds'] = 'false'
                JSON['hydroponics_ph'] = 'false'
                JSON['hydroponics_turbidity'] = 'false'
                JSON['hydroponics_level'] = 'false'
                print("Post_JSON=", JSON)
# check for SGS JSON
                #print("JSON[1]=", JSON[1])
             
                #DumpedJSON = json.dumps(JSON)
                #DumpedJSON = json.loads(JSON)
                #print("DumpedJOSN =", DumpedJSON)
                try:
                    if (len(JSON["id"]) == 4):
                        if (len(JSON["return_string"]) > 0):
                            print ("SGS Wireless Extender Found.  ID=", JSON["id"])
                            returnJSON.append(JSON)

                except:
                    #traceback.print_exc()
                    pass
            
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Finish Time =", str(now))
        print ("returnJSON", returnJSON)
      
        self.WirelessDeviceJSON = returnJSON

        self.WirelessDeviceJSON = returnJSON
        self.mainContainer.remove_child(self.screen0)
        self.screen0 = self.buildScreen0()
        self.mainContainer.append(self.screen0,'screen0')
       
        self.progress.set_value(100)
        self.menubar.set_enabled(True)
        self.SFHWorking = False
        
    # Buttons

    def onCancel(self, widget, name='', surname=''):
        print("onCancel clicked")
        self.server.server_starter_instance._alive = False
        self.server.server_starter_instance._sserver.shutdown()
        print("server stopped") 
        os._exit(os.EX_OK)
        
    def onExit(self, widget, name='', surname=''):
        # save and exit
        print("onSaveExit clicked")
        self.saveJSON()
        self.saveSGSConfigurationJSON()
        self.server.server_starter_instance._alive = False
        self.server.server_starter_instance._sserver.shutdown()
        print("server stopped") 
        os._exit(os.EX_OK)


    def onReset(self, widget, name='', surname=''):
        print("Reset clicked")
        self.removeAllScreens()
        self.mainContainer.append(self.screen1,'screen1')
        self.setDefaults()

        self.screen0 = self.buildScreen0()
        self.screen05 = self.buildScreen05()
        self.screen06 = self.buildScreen06()
        self.screen1 = self.buildScreen1()
        self.screen2 = self.buildScreen2()
        #self.screen3 = self.buildScreen3()
        self.screen4 = self.buildScreen4()
        self.screen5 = self.buildScreen5()
        #self.screen6 = self.buildScreen6()
        self.screen7 = self.buildScreen7()
        self.screen8 = self.buildScreen8()


        self.mainContainer.append(self.screen1,'screen1')
        
        
    def onSave(self, widget, name='', surname=''):
        print("onSave clicked")
        self.saveJSON()
        self.saveSGSConfigurationJSON()

        
    def onSaveAndReloadSGS(self, widget, name='', surname=''):
        print("onSave and Reload SGS clicked")
        self.saveJSON()
        self.saveSGSConfigurationJSON()
        fname = 'NEWJSON'
        with open(fname, 'a'):
            try:                     # Whatever if file was already existing
                os.utime(fname, None)  # => Set current time anyway
            except OSError:
                pass  # File deleted between open() and os.utime() call

#Configuration
configuration = {'config_enable_file_cache': True, 'config_multiple_instance': True, 'config_port': 8001, 'config_address': '0.0.0.0', 'config_start_browser': False, 'config_project_name': 'SGS Configuration', 'config_resourcepath': './res/'}

# starts the web server
#start(SGSConfigure, address='0.0.0.0', port=8001)

start(SGSConfigure, address=configuration['config_address'], port=configuration['config_port'],
                        multiple_instance=configuration['config_multiple_instance'],
                        enable_file_cache=configuration['config_enable_file_cache'],
                        start_browser=configuration['config_start_browser'])
