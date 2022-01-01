import os
import shutil
import glob
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, MATCH, ALL, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import traceback
import datetime

import time

import threading

import moisture_sensors 
import status_page 
import valve_graphs
import log_page
import p_v_programming
import valves_scheduled
import bluetoothTM_page
import bluetoothLC_page
import bt_status_page
import manual_page
import camera_page
import hydroponics_page
import alarm_page


from non_impl import NotImplPage 

from navbar import Navbar, Logo
logo = Logo()
nav = Navbar()

UpdateHPJSONLock = threading.Lock()
SGSDASHSOFTWAREVERSION = "005"

import logging

logging.getLogger('werkzeug').setLevel(logging.ERROR)

# SGS imports
import sys
sys.path.append("../")
import AccessValves
import MQTTFunctions
import state
###############
#Start MQTT
###############

### set up directory
os.makedirs("static/SkyCam", exist_ok=True)



newValveState = ""
newValveStateMC = {} 
# state of previous page
previousPathname = ""

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.SLATE])

app.config.suppress_callback_exceptions = True


app.layout =  html.Div(

        [

       html.Div(id='my-output-interval'),

       dcc.Interval(
            id='minute-interval-component',
            interval=60*1000, # in milliseconds - leave as 10 seconds
            n_intervals=0
            ) ,
       dcc.Interval(
            id='main-interval-component',
            interval=10*1000, # in milliseconds - leave as 10 seconds
            n_intervals=0
            ) ,
       dcc.Interval(
            id='fast-interval-component',
            interval=2*1000, # in milliseconds 
            n_intervals=0
            ) ,
       #dcc.Interval(
       #     id='weather-update-interval-component',
       #     interval=5*1000, # in milliseconds
       #     n_intervals=0
       #     ) ,
       
        #dbc.Spinner(id="main-spinner", color="white" ),
        #dcc.Location(id = 'url', refresh = True),
        dcc.Location(id = 'url', refresh = False),

        html.Div(id = 'page-content'),
        #html.Div(id = 'wp-placeholder', style={'display':'none'}) 
        ],

        id="mainpage"

    )


@app.server.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    #r.headers["Cache-Control"] = 'no-store'
    #r.headers["Pragma"] = "no-store"
    #r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'must-revalidate, max-age=10'
    return r



@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])


def display_page(pathname):
    global previousPathname

    print("--------------------->>>>>>>>>>>>>>>>new page")
    now = datetime.datetime.now()
    nowString =  now.strftime('%Y-%m-%d %H:%M:%S')
    print("begin=",nowString)
    
    print("pathname=", pathname)
    print("previousPathname=", previousPathname)
    i = [i['prop_id'] for i in dash.callback_context.triggered]
    print('i=', i)
    print('TRIGGER(S):', [i['prop_id'] for i in dash.callback_context.triggered])
    if (i[0] == '.'):
        print("---no page change--- ['.']")
        raise PreventUpdate	
    #if (pathname == previousPathname):
    #    print("---no page change---Equal Pathname")
    #    raise PreventUpdate	
    previousPathname = pathname
    
    myLayout = NotImplPage()
    myLayout2 = ""
    if pathname == '/status_page':
        myLayout = status_page.StatusPage() 
        myLayout2 = ""
    if pathname == '/camera_page':
        myLayout = camera_page.CameraPage()
        myLayout2 = ""
    if pathname == '/bluetoothTM_page':
        myLayout = bluetoothTM_page.BluetoothTMPage()
        myLayout2 = ""
    if pathname == '/bluetoothLC_page':
        myLayout = bluetoothLC_page.BluetoothLCPage()
        myLayout2 = ""
    if pathname == '/bluetooth_status_page':
        myLayout = bt_status_page.BTStatusPage()
        myLayout2 = ""
    if pathname == '/wired_page':
        myLayout = moisture_sensors.MoistureSensorPage()
        myLayout2 = ""
    if pathname == '/valve_graphs':
        myLayout = valve_graphs.ValveGraphPage()
        myLayout2 = ""
    if pathname == '/manual_page':
        myLayout = manual_page.ManualControlPage()
        myLayout2 = ""
    if pathname == '/hydroponics_page':
        myLayout = hydroponics_page.HydroponicsPage()
        myLayout2 = ""
    if pathname == '/log_page':
        myLayout = log_page.LogPage()
        myLayout2 = ""
    if pathname == '/p_v_programming':
        myLayout = p_v_programming.PVProgrammingPage()
        myLayout2 = ""
    if pathname == '/alarm_page':
        myLayout = alarm_page.AlarmPage()
        myLayout2 = ""
    if pathname == '/valves_scheduled':
        myLayout = valves_scheduled.ValvesScheduledPage()
        myLayout2 = ""
    
    #print("myLayout= ",myLayout)
    #print("myLayout2= ",myLayout2)
    #print("page-content= ",app.layout)
    now = datetime.datetime.now()
    nowString =  now.strftime('%Y-%m-%d %H:%M:%S')
    print("end=",nowString)
    return (logo, nav,myLayout, myLayout2 )

##################
# Moisture Sensors 
##################



@app.callback(Output({'type' : 'MSGdynamic', 'index' : MATCH, 'DeviceID' : MATCH, 'MSNumber' : MATCH, 'DeviceName' : MATCH, 'ValveNumber': MATCH}, 'figure' ),
              [Input('main-interval-component','n_intervals'),
                  Input({'type' : 'MSGdynamic', 'index' : MATCH, 'DeviceID' : MATCH, 'MSNumber' : MATCH, 'DeviceName' : MATCH, 'ValveNumber': MATCH}, 'id' )],
              [State({'type' : 'MSGdynamic', 'index' : MATCH, 'DeviceID' : MATCH, 'MSNumber' : MATCH, 'DeviceName' : MATCH, 'ValveNumber': MATCH}, 'value'  )]
              )


def update_moisturegraphs(n_intervals, id, value ):
    print("MS-n_intervals=", n_intervals)
    #if (True): # 5 minutes -10 second timer
    if ((n_intervals % (5*6)) == 0): # 5 minutes -10 second timer
 
        print(">moisture_sensors Graph Update started",id['index'], id['DeviceID'])
        #print("id=", id)
        #print ('Graph id {} / n_intervals = {}'.format(id['index'], n_intervals))
        myNewChart = moisture_sensors.updateGraph(id)
    
        fig = go.Figure(
            data=[go.Scatter(x=myNewChart[0], y=myNewChart[1])], layout=go.Layout(
                title = go.layout.Title( text = id['DeviceName'] +"/"+ str(id["DeviceID"])+"/"+ str(id["ValveNumber"])),
                yaxis= go.layout.YAxis( range = (0,101)),
                height= 300),
                        )
                     
    
        print("<moisture_sensors Graph Update complete",id['index'], id['DeviceID'])
        return fig 
    else:
        raise PreventUpdate

##################
# Log Page 
##################
@app.callback(Output({'type' : 'LPdynamic', 'index' : MATCH}, 'figure' ),
              [Input('main-interval-component','n_intervals'),
                  Input({'type' : 'LPdynamic', 'index' : MATCH}, 'id' )],
              [State({'type' : 'LPdynamic', 'index' : MATCH}, 'value'  )]
              )

def logpageupdate(n_intervals, id, value):
    
   #if (True): # 1 minutes -10 second timer
   if ((n_intervals % (1*6)) == 0): # 1 minutes -10 second timer
    print ("---->inputs:",dash.callback_context.inputs) 
    print(">log_page table Update started",id['index'])
    print("LG-n_intervals=", n_intervals) 
    if (id['index'] == "systemlog"):
        data = log_page.fetchSystemLog()
        fig = log_page.buildTableFig(data,"System Log")
    
    if (id['index'] == "valvelog"):
        data = log_page.fetchValveLog()
        fig = log_page.buildTableFig(data,"Valve Log")
        return fig
    
    if (id['index'] == "sensorlog"):
        data = log_page.fetchSensorLog()
        fig = log_page.buildTableFig(data,"Bluetooth Sensor Log")

    print("<log_page table Update complete",id['index'])
    return fig
   else:
    raise PreventUpdate
##################
# Valve Graphs Page 
##################


@app.callback(Output({'type' : 'VGdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'figure' ),
              [Input('main-interval-component','n_intervals'),
                  Input({'type' : 'VGdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'id' )],
              [State({'type' : 'VGdynamic', 'index' : MATCH, 'DeviceID' : MATCH, }, 'value'  )]
              )


def update_valve_graphs(n_intervals, id, value ):
 
   #if (True): # 1 minutes -10 second timer
   if ((n_intervals % (1*6)) == 0): # 1 minutes -10 second timer
    
    print(">valve_graphs Graph Update started",id['index'], id['DeviceID'])
    #print("id=", id)
    print("VG-n_intervals=", n_intervals)

    timeDelta = datetime.timedelta(days = 1) 
    df = valve_graphs.fetchCurrentValveData(id['DeviceID'], id["index"], timeDelta)
    myName = valve_graphs.getNameFromID(id['DeviceID'])  
    Graphs = []
    Internal = []
    Time = []
    Y = []
    for single in df:
    	Time.append(single[0])
    	Y.append(valve_graphs.returnValveValue(single[1], id["index"]))

    extra = ""
    if (len(Y) == 0):
        Time = [1]
        Y = ["Off"]
        extra = "(No Valve Changes in Time Period)"
	
    fig = valve_graphs.returnaFig(id['DeviceID'],id['index'], Time, Y, extra)

                    

    print("<valve_graphs Graph Update complete",id['index'], id['DeviceID'])

    return fig 
   else:
    raise PreventUpdate


##################
# Status Page
##################
@app.callback(Output({'type' : 'SPAdynamic', 'index' : MATCH }, 'children' ),
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'SPAdynmaic', 'index' : MATCH }, 'id' )],
              [State({'type' : 'SPAdynmaic', 'index' : MATCH}, 'children'  )]
              )

def update_alarms(n_intervals, id, children):
   print("generate Current Alarms") 
   if ((n_intervals % (1*6)) == 0): # 1 minutes -10 second timer
    print("generate Current Alarms") 
    return status_page.generateCurrentAlarms()
   else:
    raise PreventUpdate


@app.callback(Output({'type' : 'VSPdynamic', 'index' : MATCH }, 'color' ),
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'VSPdynamic', 'index' : MATCH }, 'id' )],
              [State({'type' : 'VSPdynamic', 'index' : MATCH}, 'color'  )]
              )

def update_indicators(n_intervals, id, color):
   print("up_indicator_n_intervals=", n_intervals) 
   if ((n_intervals % (1*6)) == 0): # 1 minutes -10 second timer
   
    return status_page.returnPiThrottledColor(id)
   else:
    raise PreventUpdate


@app.callback(
	      [
	      Output({'type' : 'SPGdynamic', 'GaugeType' : MATCH}, 'value' ),
	      Output({'type' : 'SPGdynamic', 'GaugeType' : MATCH}, 'label' )
              ],
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'SPGdynamic', 'GaugeType' : MATCH}, 'id' )],
              [State({'type' : 'SPGdynamic', 'GaugeType' : MATCH}, 'value'  )]
              )

def update_gauges(n_intervals, id, value):
   if (True): # 1 minutes -10 second timer
   #if ((n_intervals % (1*6)) == 0): # 1 minutes -10 second timer
    
     #print(">status_page Gauge Update started",id['GaugeType'])
     newValue = status_page.updateGauges(id) 
     if (id['GaugeType'] == 'pi-disk'):
        myName = "Pi SD Card Free" 
     if (id['GaugeType'] == 'pi-memory'):
        myName = "Pi Memory Usage" 
     if (id['GaugeType'] == 'pi-loading'):
        myName = "Pi CPU Loading" 
     if (id['GaugeType'] == 'pi-temp'):
        myName = "Pi CPU Temperature(C) " 
     #print("<status_page Gauge Update complete",id['GaugeType'])

     return newValue, myName 
   else:
    raise PreventUpdate

#345
@app.callback(Output({'type' : 'SPdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'color' ),
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'SPdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'id' )],
              [State({'type' : 'SPdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'color'  )]
              )

def update_statuspage(n_intervals, id, color):
   global newValveState
   #if (True): # 1 minutes -10 second timer
   if ((n_intervals % (1*6)) == 0): # 1 minutes -10 second timer
    
    #print(">status_page Indicator Update started",id['index'], id['DeviceID'])
    #print("id=", id)
    #print("newValveState=", newValveState)
    #print("n_intervals=", n_intervals)
    #print ('Indicator id {} / n_intervals = {}'.format(id['index'], n_intervals))
    if (newValveState == ""):
         newValveState = status_page.returnLatestValveRecord(id['DeviceID'] )

    status  = status_page.returnIndicatorValue(newValveState, id['index'])
    color = status_page.updateIndicator(status)

    if (id['index'] == 7):
     if (id['GaugeType'] == 'pi-loading'):
        myName = "Pi CPU Loading" 
     #print("<status_page Gauge Update complete",id['GaugeType'])

     return newValue, myName 
   else:
    raise PreventUpdate

# indicators
@app.callback(Output({'type' : 'SPVdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'color' ),
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'SPVdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'id' )],
              [State({'type' : 'SPVdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'color'  )]
              )

def update_statuspage(n_intervals, id, color):
   global newValveState
   #if (True): # 1 minutes -10 second timer
   if ((n_intervals % (1*6)) == 0): # 1 minutes -10 second timer
    
    #print(">status_page Indicator Update started",id['index'], id['DeviceID'])
    #print("id=", id)
    #print("newValveState=", newValveState)
    #print("n_intervals=", n_intervals)
    #print ('Indicator id {} / n_intervals = {}'.format(id['index'], n_intervals))
    if (newValveState == ""):
         newValveState = status_page.returnLatestValveRecord(id['DeviceID'] )

    status  = status_page.returnIndicatorValue(newValveState, id['index'])
    color = status_page.updateIndicator(status)

    if (id['index'] == 7):
        newValveState = ""    
    #print("<status_page Indicator Update complete",id['index'], id['DeviceID'])
    return color
   else:
    raise PreventUpdate
#470
@app.callback(Output({'type' : 'SPBdynamic', 'index' : MATCH, 'DeviceID' : MATCH, 'Indicator' : MATCH}, 'color' ),
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'SPBdynamic', 'index' : MATCH, 'DeviceID' : MATCH, 'Indicator' : MATCH}, 'id')],
              [State({'type' : 'SPBdynamic', 'index' : MATCH, 'DeviceID' : MATCH, 'Indicator' : MATCH}, 'color')]
              )

def bt_update_statuspage(n_intervals, id, color):
   #if (True): # 1 minutes -10 second timer
   if ((n_intervals % (5*6)) == 0): # 1 minutes -10 second timer
    
    #print("-status_page Bluetooth Indicator Update started",id['index'], id['DeviceID'])
    #print("id=", id)

    
    # fetch Bluetooth Sensor Data
    mySensorData = status_page.getLastBTReading(id['index'])
    # green if > 10 , red if < 10
    moistureIndicator = "gray"
    # green if > 10, red if less
    batteryIndicator = "gray"
    # not active if data is older than 1 Hour 
    activeIndicator = "gray"

    #print("mySensorData=", mySensorData)
    

    #check for null record
    if (len(mySensorData) == 0):
        # No sensor, all gray
        moistureIndicator = "gray"
        batteryIndicator = "gray"
        activeIndicator = "gray"
    else:
        # now do the active calculations
        sampleTimestamp =  mySensorData[2]
        #print("sampleTimeStamp =", sampleTimestamp)
        activeSpan = datetime.timedelta(hours=1)
        timespan = datetime.datetime.now() - sampleTimestamp
        #print("timespan=", timespan)
        if (timespan > activeSpan):
            #print("too old")
            moistureIndicator = "gray"
            batteryIndicator = "gray"
            activeIndicator = "red"
        else:
            #print("active")
            activeIndicator = "greenyellow"
            # now check for other
            myBattery = int(mySensorData[9])
            myMoisture = int(mySensorData[7])
            if (myBattery < 10):
                batteryIndicator = "red"
            else:
                batteryIndicator = "greenyellow"
            if (myMoisture < 10):
                moistureIndicator = "red"
            else:
                moistureIndicator = "greenyellow"
        
    #print("moistureIndicator = ", moistureIndicator )
    #print("batteryIndicator = ", batteryIndicator )
    #print("activeIndicator = ", activeIndicator )
    
    
    if (id['Indicator'] == 0):
        return [moistureIndicator]
 
    if (id['Indicator'] == 1):
        return [batteryIndicator]
 
    if (id['Indicator'] == 2):
        return [activeIndicator]

   else:
        raise PreventUpdate
   return ['purple' ]
##################
# p_v_programming
##################


@app.callback(
	      [
	      Output({'type' : 'PVPdynamic', 'index' : "pvprogramming"}, 'figure' ),
              ],
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'PVPdynamic', 'index' : "pvprogramming"}, 'id' )],
              [State({'type' : 'PVPdynamic', 'index' : "pvprogramming"}, 'value'  )]
              )

def updatePVProgramming(n_intervals,id, value):

    if (n_intervals == 0): # stop first update
        raise PreventUpdate

    #if (True): # 5 minutes -10 second timer
    if ((n_intervals % (5*6)) == 0): # 15 minutes -10 second timer
        data = p_v_programming.fetchProgramming()
        fig = p_v_programming.buildTableFig(data, "Pump and Valve Programming")

    else:
        raise PreventUpdate
    return [fig]


##################
# valves_scheduled
##################

@app.callback(
	      [
	      Output({'type' : 'VSdynamic', 'index' : "nextevents"}, 'figure' ),
              ],
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'VSdynamic', 'index' : "nextevents"}, 'id' )],
              [State({'type' : 'VSdynamic', 'index' : "nextevents"}, 'value'  )]
              )

def updatePVProgramming(n_intervals,id, value):

    if (n_intervals == 0): # stop first update
        raise PreventUpdate

    #if (True): # 5 minutes -10 second timer
    if ((n_intervals % (5*6)) == 0): # 15 minutes -10 second timer
        data = valves_scheduled.fetchProgramming()
        fig = valves_scheduled.buildTableFig(data, "Next Scheduled Events")

    else:
        raise PreventUpdate
    return [fig]

##################
# bluetoothTH
##################

@app.callback(
	      [
	      Output({'type' : 'BTGdynamic', 'index' : 1}, 'figure' ),
              ],
              [
              Input('main-interval-component','n_intervals'),
              Input({'type' : 'BTGdynamic', 'index' : 1}, 'id' )
              ],
              [State({'type' : 'BTGdynamic', 'index' : 1}, 'value'  )]
              )

def updatebluetoothTM(n_intervals,id, value):

    if (n_intervals == 0): # stop first update
        raise PreventUpdate
        
    #print("BT TH interval happening")
    #print ("id=", id)
    #if (True): # 5 minutes -10 second timer
    if ((n_intervals % (5*6)) == 0): # 15 minutes -10 second timer
       
      print ("wireless/bt =", id['index'])  
      splitIndex = id['index'].split("/")
      myWirelessID = splitIndex[0]
      btaddress = splitIndex[1]
      wireless = { 'id': myWirelessID }
      fig = bluetoothTM_page.buildSoilTemperature_Humidity_Graph_Figure(wireless, btaddress)
      print("fig=", fig)
    else:
        raise PreventUpdate
    return [fig]



##################
# SmartGarden3 Cams
##################



@app.callback(
    [
        Output({'type': 'SkyCamPic', 'index': 0}, 'children'),
    ],
    [Input('main-interval-component', 'n_intervals'),
     Input({'type': 'SkyCamPic', 'index': 0}, 'id')],
    [State({'type': 'SkyCamPic', 'index': 0}, 'value')]
)
def update_skypic_metrics(n_intervals, id, value):
    #print("skycampic_n_intervals=", n_intervals)
    print('index=', id['index'])
    myIndex = id['index']
    # build pictures
    SkyCamList = camera_page.getSkyCamList()
    output = camera_page.buildPics(SkyCamList)
    #print("picoutput=", output)
    return [output]

##########################
# Hydroponics 
##########################


@app.callback(
          [
          Output({'type' : 'HPdynamic', 'index' : MATCH}, 'children' ),
              ],
              [Input('main-interval-component','n_intervals'),
              Input({'type' : 'HPdynamic', 'index' : MATCH}, 'id' )],
              [State({'type' : 'HPdynamic', 'index' : MATCH}, 'value'  )]
              )
def updateHydroponicsUpdate(n_intervals,id, value):


    if ((n_intervals % (5*6)) == 0) or (n_intervals ==0): # 5 minutes -10 second timer
        #print("UpdateHydroponics n_intervals =", n_intervals, id['index'])

        if (id['index'] == "StringTime"):
            myID = hydroponics_page.getFirstWireless()
            hydroponics_page.CHJSON = hydroponics_page.generateCurrentHydroJSON(myID)
            value = str(hydroponics_page.CHJSON[id['index']]) +" "+ hydroponics_page.CHJSON[id['index']+'Units']
            value = "Extender: "+myID+" Updated at:" + value
            return [value]

        else:
            # OK.  Now we update the blocks

            if (id['index'] == "Temperature"):
                value = str(round(hydroponics_page.CTUnits(hydroponics_page.CHJSON[id['index']]),1)) +" "+ hydroponics_page.CHJSON[id['index']+'Units']
            else:
                value = str(hydroponics_page.CHJSON[id['index']]) +" "+ hydroponics_page.CHJSON[id['index']+'Units']
            if (hydroponics_page.CHJSON[id['index']] < 0):
                value = "N/A"
            #print ("value=", value)
            return [value]
    else:
        raise PreventUpdate

# now do graphs
@app.callback(Output({'type' : 'HPGdynamic', 'index' : MATCH}, 'figure' ),
              [Input('main-interval-component','n_intervals'),
                  Input({'type' : 'HPGdynamic', 'index' : MATCH}, 'id' )],
              [State({'type' : 'HPGdynamic', 'index' : MATCH}, 'value'  )]
              )

def hydrographupdate(n_intervals, id, value):
    
   #if (True): # 1 minutes -10 second timer
   if (n_intervals != 0) and ((n_intervals % (10*6)) == 0): # 1 minutes -10 second timer
    print ("---->inputs:",dash.callback_context.inputs) 
    print(">hydrograph table Update started",id['index'])
    print("HPG-n_intervals=", n_intervals) 
    myID = hydroponics_page.getFirstWireless()
    if (id['index'] == "graph-Level"):
        fig = hydroponics_page.buildGraphFigure("Level", "%",hydroponics_page.getActiveSensorWireless(myID, "Level"))
        return fig
    
    if (id['index'] == "graph-Temperature"):
        fig = hydroponics_page.buildGraphFigure("Temperature", "Degrees ("+hydroponics_page.TUnits()+")",hydroponics_page.getActiveSensorWireless(myID, "Temperature"))
        return fig
    
    if (id['index'] == "graph-TDS"):
        fig = hydroponics_page.buildGraphFigure("TDS", "ppm",hydroponics_page.getActiveSensorWireless(myID, "TDS"))
        return fig
    
    if (id['index'] == "graph-Turbidity"):
        fig = hydroponics_page.buildGraphFigure("Turbidity", "NTU",hydroponics_page.getActiveSensorWireless(myID, "Turbidity"))
        return fig
    
    if (id['index'] == "graph-Ph"):
        fig = hydroponics_page.buildGraphFigure("Ph", "",hydroponics_page.getActiveSensorWireless(myID, "Ph"))
        return fig
    
   else:
    raise PreventUpdate
##########################
# Manual Control
##########################


@app.callback(Output({'type' : 'WCVdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'color' ),
              [Input('fast-interval-component','n_intervals'),
              Input({'type' : 'WCVdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'id' )],
              [State({'type' : 'WCVdynamic', 'index' : MATCH, 'DeviceID' : MATCH}, 'color'  )]
              )

def update_manualpage(n_intervals, id, color):
   global newValveStateMC
   if ((n_intervals % (1)) == 0): # 1 
    
    #print(">manual_page Indicator Update started",id['index'], id['DeviceID'])
    #print("id=", id)
    #print("newValveStateMC=", newValveStateMC)
    #print("n_intervals=", n_intervals)
    #print ('Indicator id {} / n_intervals = {}'.format(id['index'], n_intervals))
     
    if (id['index'] == 0) or (id['DeviceID'] not in newValveStateMC) :
        newValveStateMC[id['DeviceID']] = status_page.returnLatestValveRecord(id['DeviceID'] )

    status  = manual_page.returnIndicatorValue(newValveStateMC[id['DeviceID']], id['index'])
    color = manual_page.updateIndicator(status)

    if (id['index'] == 7):
        newValveStateMC.pop(id['DeviceID']) 
    #print("<Manual_page Indicator Update complete",id['index'], id['DeviceID'])
    return color
   else:
    raise PreventUpdate


@app.callback(
	      [
	      Output( {'type' : 'MCdynamic', 'index' : MATCH}, 'children' )
              ],
              [
              #Input('main-interval-component','n_intervals'),
              Input( {'type' : 'MCdynamic', 'index' : MATCH}, 'id' ),
              Input( {'type' : 'MCdynamic', 'index' : MATCH}, 'n_clicks' ),
              
             ],
              [ 
                #State( {'type' : 'MCdynamic', 'index' : MATCH}, 'value' ),
                State('input-on-submit', 'value')]
        )



#def sendValveToggle(n_intervals, id, n_clicks, value, seconds):
def sendValveToggle( id, n_clicks, value):
    
    if (n_clicks == 0): # stop first update
        raise PreventUpdate
    print("value=", value)
    splitIndex=id["index"].split("/")
    myID = splitIndex[0]
    myCurrentState = splitIndex[1]
    myIP = splitIndex[2]
    myValve = splitIndex[3]
    myTime = str(value)
    if (myTime == 0):
        myTime = 1
    #if (myCurrentState == "0"):
    myToggle = "1"
    #else:
    #    myToggle = "0"

    myCommand = 'setSingleValve?params=admin,'+myValve+","+myToggle+","+str(myTime)

    print("button pushed")
    print("myCommand=", myCommand)
    print("id=", id)
    print("value=", value)
    print("n_clicks=", n_clicks)

    #AccessValves.sendCommandToWireless(myIP, myCommand)
    single={}
    single['id'] = myID
    single['ValveNumber'] = myValve
    single['OnTimeInSeconds'] = myTime
    # Set up Wireless MQTT Links
    MQTTFunctions.startWirelessMQTTClient("SG3DA")

    while state.WirelessMQTTClientConnected != True:    #Wait for connection
        time.sleep(0.1)

    print (single)
    AccessValves.turnOnTimedValve(single)

    state.WirelessMQTTClient.disconnect()
    state.WirelessMQTTClientConnected = False

    return ["TOn( %d )" % n_clicks ]

@app.server.route('/static/<resource>')
def serve_static(resource):
        return flask.send_from_directory(STATIC_PATH, resource)




##########################


if __name__ == '__main__':
    #app.run_server(host='0.0.0.0', port=8010)
    app.run_server(host='0.0.0.0', port=8010)
    #app.run_server(debug=True, host='0.0.0.0', port=8010)
