# manual valve control


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
import random

import scanForResources
headerColor = 'grey'
rowEvenColor = 'lightgrey'
rowOddColor = 'white'


# read JSON

readJSON.readJSON("../")
readJSON.readJSONSGSConfiguration("../")

import MySQLdb as mdb





################
# manual Page
################

         
        
def fetchValveJSON(myID, valveNumber):
       
        # read JSON

        readJSON.readJSON("../")
        readJSON.readJSONSGSConfiguration("../")

        myJSON=config.SGSConfigurationJSON

        #print("myJSON=", myJSON) 
        #myLoadedJSON = json.loads(str(myJSON))
        #myLoadedJSON = json.loads(str(myJSON).replace("'","\"" ))
        myValves = myJSON["Valves"]

        for singleValve in myValves:
            #singleValve = json.loads(str(singleValve).replace("'","\"" ))
            #singleValve = json.loads(str(singleValve))
            if (str(singleValve["id"]).replace(" ", "") == str(myID).replace(" ", "")):
                if (str(singleValve["ValveNumber"]) == str(valveNumber)):
                    return singleValve
        return {}



def returnLatestValveRecord(myID):
        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "SELECT State FROM ValveRecord WHERE( DeviceID = '%s')  ORDER BY TimeStamp DESC LIMIT 1" % (myID)
                #print("query=", query)
                cur.execute(query)
                con.commit()
                records = cur.fetchall()
                #print ("Query records=", records)
                if (len(records) == 0):
                    return "V00000000"
                return records[0][0]
        except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                con.rollback()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()
def returnIndicatorValue(state, number):
    if (state[number] == "0"):
        return False
    else:
        return True

useRandom = False

def updateIndicator(myValue ):

    if (useRandom == True):
    	myValue = random.randint(0,1)

    if (myValue ==1):
        myColor = "greenyellow"
    else:
        myColor = "red"

        
    return myColor

        
def returnIndicators():
    totalLayout = []
    wirelessJSON = readJSON.getJSONValue("WirelessDeviceJSON")
    for singleWireless in wirelessJSON:
        myLabelLayout = [] 
        
        valveStatus =  returnLatestValveRecord(singleWireless['id'] )
        deviceStatus = scanForResources.checkDeviceStatus(singleWireless['id'])
        if deviceStatus == False:
            myDeviceStatus = "Not Active"
            myDeviceColor = "red"
        else:
            myDeviceStatus = "Active"
            myDeviceColor = "green"

        myIndicatorLayout = [] 
        myButtonLayout = [] 
        for valve in range(1,9):

            currentValue = returnIndicatorValue(valveStatus, valve)
            if (currentValue):
                myColor = "greenyellow"
            else:
                myColor = "red"
            if (myDeviceStatus == "Active"):
                myIndicatorLayout.append( daq.Indicator(
                        id = {'type' : 'WCVdynamic', 'index': valve  , 'DeviceID' : singleWireless['id'] },
                        color = myColor,
                        label="Valve "+str(valve),
                        value=True,
                        style={
                            'margin': '14px'
                        }
                    )
                    )
                
                myMatch = "%s/%d/%s/%d"% (singleWireless['id'], currentValue, singleWireless['ipaddress'],valve)
                myButtonLayout.append(html.Button('Turn On', id={'type': 'MCdynamic', 'index' : myMatch} , n_clicks=0, style={'margin': '2px'}) )

         
        totalLayout.append(
                     dbc.Row(html.H6(singleWireless['name'] +"/"+singleWireless['id'],)) )
        totalLayout.append(
                     dbc.Row(html.H6(myDeviceStatus, style={'color' :myDeviceColor}))
                     )
        totalLayout.append(dbc.Row(myIndicatorLayout))
        totalLayout.append(dbc.Row(myButtonLayout))

    return totalLayout

def updateProgramming(): 
      layout = [] 
     
      Layouts = returnIndicators()
      layout.append( html.Div(
                   Layouts ,
        ))



      #layout.append(dcc.Graph(id={"type": "MCdynamic", "index": "pvmanual"},figure=fig, ))	

      return layout

################
# Page Functions
################


def ManualControlPage():
    Row1 = html.Div(
        [   html.H1(children="Manual Control"),
            html.Br(),
            html.H4("Note:  These commands  will override any currently on Valves and turn off the valve after the interval below. The timed valve programming is left as is in SmartGarden3 and will resume on the next valve programmed event. Refresh the page if your extender shows not active."),
            html.Br(),
            dbc.Row([
                html.H5("Number of Seconds to Turn On", style={"margin" : "10px"}
                ),
                html.Div(dcc.Input(id='input-on-submit', type='text', value='10',style={'margin' : '10px', 'width' : '50px', 'text-align':'right'})
                ),

            ]),
            html.Br(),
            html.Br(),
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







