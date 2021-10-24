import os, sys, glob
# import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import pandas as pd
import MySQLdb as mdb
import datetime
import time
import traceback



# SGS imports
sys.path.append("../")

import state
import config
import readJSON


import plotly.graph_objs as go
# from dash.dependencies import Input, Output, MATCH, ALL, State

os.makedirs("static/SkyCam", exist_ok=True)


# build the path to import config.py from the parent directory
sys.path.append('../')
import config
# how long of Graph 
NUMBEROFDAYS = 14



def getWirelessList():
        
    wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")

    return wirelessJSON


def fetchSTH(timeDelta, wireless, btaddress):

        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT Temperature, Moisture, TimeStamp FROM `BluetoothSensorData` WHERE (TimeStamp > '%s') AND (DeviceID = '%s') AND (MacAddress = '%s')  ORDER BY id ASC" % (before, wireless["id"], btaddress)

                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                #print ("Query records=", records)
                return records
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()


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

def getBluetoothAddresses(myID):
    
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "SELECT fulladdress FROM `BluetoothSensors` WHERE (assignedwirelessid = '%s') ORDER BY id ASC" % (myID)

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


def buildSoilTemperature_Humidity_Graph_Figure(wireless, btaddress):
   
    BTName = getBluetoothName(btaddress)[0]
    BTPick = getBluetoothPickName(btaddress)[0]
    timeDelta = datetime.timedelta(days=NUMBEROFDAYS)
    records = fetchSTH(timeDelta, wireless, btaddress)
    #print("fetchSTHrecords=", records) 
    Time = []
    Temperature = []
    Humidity = []
    for record in records:
        Time.append(record[2])
        Temperature.append(record[0])
        Humidity.append(record[1])

    if (len(records) == 0):
    #if (True):
        fig = go.Figure()
        fig.update_layout(
            height=100,
            title_text='No Data Available')
        return fig

    # set units
    English_Metric = readJSON.getJSONValue("English_Metric")

    if (English_Metric == False):  # english units
        for i in range(0, len(Temperature)):
            Temperature[i] = (9.0/5.0 * Temperature[i]) +32.0
        units = "F"
    else:
        units = "C"
    
    # Create figure with secondary y-axis
    fig = go.Figure()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=Time, y=Temperature, name="Soil Temperature",
        line = dict(
                    color = ('red'),
                    width = 2,
                    ),
       ), 
                    secondary_y = False,
    )

    fig.add_trace(
        go.Scatter(x=Time, y=Humidity, name="Soil Moisture", 
        line = dict(
                    color = ('blue'),
                    width = 2,
                    ),
        ),
                    secondary_y = True
    )

    # Add figure title
    fig.update_layout(
        title_text="Soil Temperature and Moisture ("+BTName+"/"+BTPick+")", height=400
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Time ("+returnNakedTimeString()+")")
   
    minTemp = min(Temperature)*0.9
    maxTemp = max(Temperature)*1.10
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Temperature ("+units+")</b>", range = (minTemp, maxTemp), secondary_y=False, side='left')
    fig.update_yaxes(title_text="<b>Moisture (%)</b>", range = (0,100), secondary_y=True, side='right')
    
    return fig

def buildSoilTemperature_Humidity_Graph(wireless, bluetooth):

    fig = buildSoilTemperature_Humidity_Graph_Figure(wireless, bluetooth)
    graph =  dcc.Graph(
                    id = {'type' : 'BTGdynamic', 'index': wireless['id']+"/"+bluetooth },
                    figure=fig,
                    animate = False
                    )

    return graph

    
def build_th_graphs(WirelessList):
    
    
    
    output = [html.Br(), html.Br()]
    index = 0
    for wireless in WirelessList:  
       
       #print("wireless=", wireless)
       bluetoothaddresses = getBluetoothAddresses(wireless["id"])
       #print("bluetoothaddresses=", bluetoothaddresses)
       if (len(bluetoothaddresses) == 0):
        output.append(html.Br())
        output.append( html.H2(wireless["name"] + " / " +wireless["id"] + " (No Bluetooth Sensors Assigned)") )
        output.append(html.Br())
       else:
        output.append( html.H2(wireless["name"] + " / " +wireless["id"] + " Soil Temperature Moisture"))

    
       #output.append (wireless["id"])
       for bluetooth in bluetoothaddresses:
            output.append (buildSoilTemperature_Humidity_Graph(wireless, bluetooth))
       
       index=index+1

       #for bluetooth in bluetoothaddresses:
       #     output.append (buildSoilBrightness_Conductivity_Graph(wireless, bluetooth))

       index=index+1

    return output

def returnTimeString():
    now = datetime.datetime.now()
    nowString =  now.strftime('%Y-%m-%d %H:%M:%S')
    return html.Div([html.H6(children="updated: "+nowString) ])

def returnNakedTimeString():
    now = datetime.datetime.now()
    nowString =  now.strftime('%Y-%m-%d %H:%M:%S')
    return "updated: "+nowString

def BluetoothTMPage():

    print("in bluetooth page TM")
    WirelessList = getWirelessList()
    #layout = []

    layout = html.Div(children=[
        html.H1("Bluetooth Soil Charts (%d Days)"%(NUMBEROFDAYS), style={'textAlign': 'center'}),
        returnTimeString(),
    
        html.Div(id={'type' : 'BluetoothGraphsTM', 'index' : 0}, children = build_th_graphs(WirelessList)),
    
        ], className="container" )
        


    print("btlayout=", layout)
    return layout
