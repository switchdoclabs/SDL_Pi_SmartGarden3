

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import plotly.express as px 
import plotly.graph_objs as go

import datetime
import traceback
import sys

# SGS imports
sys.path.append("../")

import state
import config
import readJSON
import json

headerColor = 'grey'
rowEvenColor = 'lightgrey'
rowOddColor = 'white'
rowErrorColor = 'red'

# read JSON

readJSON.readJSON("../")
readJSON.readJSONSGSConfiguration("../")

import MySQLdb as mdb



################
# bluetooth status Page
################
def buildTableFig(myData, title):
    #print("myData=", myData)
    #print("title=", title)
    if (title=="Current Bluetooth Sensor Status"):
        myFillColor =  [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor]*10]
        # check for possibly bad sensors
        redCheck = False
        count = 0
        for moisture in myData[6]:
            if (moisture == ''):
                moisture = 0
            if (moisture < 5):
                myFillColor[0][count] = "red"
            count = count+1
        # next check battery
        count = 0
        for battery in myData[9]:
            if (battery == ''):
                battery = 0
            if (battery < 5):
                myFillColor[0][count] = "pink"
            count = count+1

        fig = go.Figure(data=[
		go.Table(
                   columnwidth = [200,100,120,250,250,150,150,150,150,150, 150 ],
                   header = dict(
                     values = [    ['<b>Name</b>'],
                                   ['<b>Pick Add</b>'],
                                   ['<b>Assign</b>'],
                                   ['<b>Date Added </b>'],
                                   ['<b>Last Reading </b>'],
                                   ['<b>Temp</b>'],
                                   ['<b>Moisture</b>'],
                                   ['<b>Light</b>'],
                                   ['<b>Conduct</b>'],
                                   ['<b>Battery  (%)</b>'],
                                   ['<b>Sensor Type</b>'],
                                   ],
                     line_color='darkslategray',
                     fill_color='royalblue',
                     align=['left','center'],
                     font=dict(color='white', size=12),
                     height=40
                   ),
                   cells=dict(
                     values=myData,
                     line_color='darkslategray',
                     # 2-D list of colors for alternating rows
                     fill_color = myFillColor,
                     fill=dict(color=['paleturquoise', 'white']),
                     align=['left', 'center'],
                     font_size=10,
                     height=30),
                     ) 
		 ],
		 layout= {"title" : title, "autosize" : True, "height" : 1500},
                     )
        #print ("fig=", fig)
        return fig
	
	
    fig = html.H1(children="Error in Sensor DB")


         
        
        
def getBluetoothPickName(myBluetooth):

        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "SELECT pickaddress FROM `BluetoothSensors` WHERE (fulladdress = '%s') ORDER BY id ASC" % (myBluetooth)

                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                #print ("Query records=", records)
                bluelist = []            
                for record in records:
                   bluelist.append(record[0]) 
                return bluelist
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

        return [] 

def getBluetoothName(myBluetooth):

        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "SELECT name FROM `BluetoothSensors` WHERE (fulladdress = '%s') ORDER BY id ASC" % (myBluetooth)

                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                #print ("Query records=", records)
                bluelist = []            
                for record in records:
                   bluelist.append(record[0]) 
                return bluelist
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

        return [] 

def getBluetoothData():
    
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "SELECT * FROM `BluetoothSensors` ORDER BY id ASC" 

                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                #print ("Query records=", records)
                bluelist = []            
                for record in records:
                   bluelist.append(record) 
                return bluelist
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

        return [] 

def getLastBTReading(btaddress):
    
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "SELECT * FROM `BluetoothSensorData` WHERE (MacAddress = '%s') ORDER BY id DESC LIMIT 1" % (btaddress) 

                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                #print ("Query records=", records)
                if (len(records) == 0):
                    return []
                return records[0]
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()

        return [] 

def fetchProgramming():
    myArray = []

    myNameList = []
    myPickAddressList = []
    myAssignmentList = []
    myDataAddedList = []
    myLastReadingList = []
    myTemperatureList = []
    myMoistureList = []
    myLightList = []
    myConductivityList = []
    myBatteryList = []
    mySensorTypeList = []

    bluetoothData = getBluetoothData()
    #print("bta=", bluetoothData)

    for bluetooth in bluetoothData:
        #print("bt=", bluetooth)
        myNameList.append(bluetooth[5])
        myPickAddressList.append(bluetooth[3])
        myAssignmentList.append(bluetooth[4])
        myDataAddedList.append(bluetooth[1])

        btreading = getLastBTReading(bluetooth[2])
        if (len(btreading) == 0):
            myLastReadingList.append("")
            myTemperatureList.append("")
            myMoistureList.append("")
            myLightList.append("")
            myConductivityList.append("")
            myBatteryList.append("")
            mySensorTypeList.append("")
        else:
            myLastReadingList.append(btreading[2])
            myTemperatureList.append(btreading[5])
            myMoistureList.append(btreading[7])
            myLightList.append(btreading[6])
            myConductivityList.append(btreading[8])
            myBatteryList.append(btreading[9])
            mySensorTypeList.append(btreading[10])


    myArray.append(myNameList)
    myArray.append(myPickAddressList)
    myArray.append(myAssignmentList) 
    myArray.append(myDataAddedList) 
    myArray.append(myLastReadingList) 
    myArray.append(myTemperatureList) 
    myArray.append(myMoistureList) 
    myArray.append(myLightList) 
    myArray.append(myConductivityList) 
    myArray.append(myBatteryList) 
    myArray.append(mySensorTypeList) 
    # set up table display
    #print('myArray=', myArray) 

    return myArray

def updateProgramming(): 
      layout = [] 
      data = fetchProgramming()
      fig = buildTableFig(data,"Current Bluetooth Sensor Status")
      #print("fig=", fig)
      layout.append(dcc.Graph(id={"type": "BSSdynamic", "index": "bluetoothsensorstatus"},figure=fig, ))	

      return layout

################
# Page Functions
################


def BTStatusPage():
    Row1 = html.Div(
        [ html.H1(children="Bluetooth Sensor Status"),
            #dbc.Row(
                #[
			html.Div(updateProgramming())
                #]
            #),
        ]
    )
    #layout = dbc.Container([
    layout = dbc.Container([
        Row1],
        className="p-5",
    )
    return layout







