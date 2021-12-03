
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import datetime
import traceback
import sys

# imports
sys.path.append("../")

import state
import config
import readJSON
import json



# read JSON

readJSON.readJSON("../")

import MySQLdb as mdb


###############
# Hydroponics
###############

################
# Conversion Functions
################

def CTUnits(temperature):

    English_Metric = readJSON.getJSONValue("English_Metric")

    if (English_Metric == False):  # english units
        temperature = (9.0/5.0 * temperature) +32.0
    return temperature

def TUnits():
    English_Metric = readJSON.getJSONValue("English_Metric")
    if (English_Metric == False):  # english units
        units = " F"
    else:
        units = " C"

    return units


def generateCurrentHydroJSON(DeviceID):
        print("generating current HydroJSON")
        try:
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                query = "SELECT * FROM `Hydroponics` WHERE DeviceID = '%s' ORDER BY id DESC LIMIT 1" % DeviceID
                print("query=", query)
                cur.execute(query)
                records = cur.fetchall()
                weatherRecordCount = len(records)

                #print ("queryrecords=",records)
                # get column names
                query = "SHOW COLUMNS FROM Hydroponics"
                cur.execute(query)
                names = cur.fetchall()
                fieldcount = len (names)
                print ("names=", names)
                CHJSON = {}
                for i in range(1,fieldcount):
                    if (names[i][0] == "TimeStamp"):
                        if (weatherRecordCount == 0):
                            CHJSON[names[i][0]] = 0;
                        else:
                            CHJSON[names[i][0]] = records[0][i]
                    else:
                        if (names[i][0] == "DeviceID"):
                          if (weatherRecordCount == 0):
                            CHJSON[names[i][0]] = "";
                          else:
                            CHJSON[names[i][0]] = records[0][i]
                        else:   
                            if (weatherRecordCount == 0):
                              CHJSON[names[i][0]] = 0;
                            else:
                              CHJSON[names[i][0]] = float(records[0][i])

                if (weatherRecordCount == 0):
                    CHJSON["StringTime"] = ""
                else:
                    CHJSON["StringTime"] = records[0][1]
                CHJSON["StringTimeUnits"] = ""



        except:
                traceback.print_exc()
                #sys.exit(1)

        finally:
                cur.close()
                con.close()
        print("done generating CHJSON=", CHJSON)
        return CHJSON


################
# Page Functions

###################
####  Graph ####
###################

def fetchData(Value, DeviceID, timeDelta):

        try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGarden3');
                cur = con.cursor()
                now = datetime.datetime.now()
                before = now - timeDelta
                before = before.strftime('%Y-%m-%d %H:%M:%S')
                query = "SELECT %s, timestamp FROM `Hydroponics` WHERE (timestamp > '%s') AND (DeviceID = '%s') ORDER BY id ASC" % (Value, before, DeviceID)
                print("query=", query)
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



def buildGraph(Value, Units):

    fig = buildGraphFigure(Value, Units)

    graph =  dcc.Graph(
                    id = {'type' : 'HPGdynamic', 'index': 'graph-%s' % Value },
                    figure=fig,
                    animate = False
                    )
    return graph

def buildGraphFigure(Value, Units):
    
    timeDelta = datetime.timedelta(days=7)
    records = fetchData(Value,CHJSON['DeviceID'],timeDelta)

    
    Time = []
    data = []
    for record in records:
        Time.append(record[1])
        data.append(record[0])

    units = ""
    
    # Create figure with secondary y-axis
    if (len(records) == 0):
        fig = go.Figure()
        fig.update_layout(
            height=800,
            title_text='No %s Data Available'% Value)
        return fig


    fig = go.Figure(
        data=[go.Scatter(x=Time, y=data, name=Value, line = dict(
                    color = ('blue'),
                    width = 2,
                    ),
        )]
        )

    # Add figure title
    fig.update_layout(
        title_text="Hydroponics %s" % Value, height=400
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text=Units)
   
    minTemp = min(data)*0.9
    maxTemp = max(data)*1.10
    # Set y-axes titles
    #fig.update_yaxes(title_text="<b>Turbidity</b>", range = (minTemp, maxTemp), secondary_y=False, side='left')
    
    return fig




################
# Page Functions
################

def HydroponicsPage():
    global CHJSON
    maintextsize = "2.0em"
    subtextcolor = "green"
    maintextcolor = "black"

    print("HP-CHJSON=", CHJSON)
    Row1 = html.Div(
        [ 
        dbc.Row( dbc.Col(html.Div(html.H6(id={'type' : 'HPdynamic', 'index': "StringTime"},children="Hydrponics Instruments")))),
            
            dbc.Row(
                [ 
                    dbc.Col(html.Div(
                     [
                     html.Div(
                         [html.H1(id={'type' : 'HPdynamic', 'index' : "Level"},
                            children=str(round(CHJSON["Level"],1))+" %", style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Water Level", style={"color":subtextcolor})
                         ], id="ht1", className="mini_container",),

                     html.Div(
                         [html.H1(id={'type' : 'HPdynamic', 'index' : "Temperature"},
                            children=str(round(CTUnits(float(CHJSON["Temperature"])),1))+TUnits(), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Temperature", style={"color":subtextcolor})
                         ], id="ht1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'HPdynamic', 'index' : "TDS"},
                            children=str(CHJSON["TDS"]), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Total Disolved Solids", style={"color":subtextcolor})
                         ], id="ht1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'HPdynamic', 'index' : "Turbidity"},
                            children=str(int(CHJSON["Turbidity"]))+" NTU ", style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Turbidity", style={"color":subtextcolor})
                         ], id="ht1", className="mini_container",),
                     html.Div(
                         [html.H1(id={'type' : 'HPdynamic', 'index' : "Ph"},
                            children=str(round(CHJSON["Ph"])), style={"font-size": maintextsize,"color":maintextcolor}), 
                         html.P("Ph", style={"color":subtextcolor})
                         ], id="ht1", className="mini_container",),
                     ],
                     ),
                     width=3,
                    ),
                     dbc.Col( html.Div(html.Figure(
                     [
                     html.Div(id={'type' : 'WPIdynamic', 'index' : "SkyCamImage"},
                          children = [
                            html.Img( height=350, width=350*1.77, src="/assets/skycamera.jpg"),
                            html.Figcaption("SkyWeather Cam"),
                            ]),

                     ]
                     ),
                    ),
                     width=6, align="center",
                    ),
      
	            ],
            ),
        ]
	    ) # end of Rwo1



# graphs
    Row3 = html.Div(
    [
            dbc.Row(
            [
                dbc.Col(
                [
                    buildGraph("RawLevel", "%"),
                    buildGraph("Temperature", "Degrees"),
                    buildGraph("TDS", "ppm"),
                    buildGraph("Turbidity", "NTU"),
                    buildGraph("Ph", ""),
                ],
                width = 12,
                )
            ]
            ),
   ]
   )



#########
# combined layout
#########


    layout = dbc.Container([
        html.H1("Hydroponics Instruments"),
        Row1, Row3 ],
        className="p-5",
    )
    return layout


CHJSON = generateCurrentHydroJSON('149D')


