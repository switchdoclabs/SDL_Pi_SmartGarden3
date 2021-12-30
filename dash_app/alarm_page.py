

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

# read JSON

readJSON.readJSON("../")
readJSON.readJSONSGSConfiguration("../")

import MySQLdb as mdb



################
# Alarm Page
################


def fetchData():

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

        return myRecords

	
def updateProgramming():

    myData = fetchData()
    print("myData=", myData)
    layout=[]
    if (len(myData) == 0):
        layout.append(html.H2("No Alarms Set"))
    else:
       for record in myData:
        if (record[2] == "True"):
            myType = "Bluetooth"
        else: 
            myType = "Hydroponics"
        if (record[11] == None):
            TriggerTime = "Never"
        else:
            TriggerTime = datetime.datetime.strftime(record[11],'%Y-%m-%d %H:%M:%S') 
            #TriggerTime = datetime.datetime.strptime(record[11], '%Y-%m-%d %H:%M:%S') 
        layout.append(html.Div(
            [  html.H2(myType+" "+ record[4] ),
               dbc.Row(
                    [
                            dbc.Col(html.Div(dbc.Alert( "Type: "+myType, color="primary"))),
                            dbc.Col(html.Div(dbc.Alert( "Address: "+record[4], color="primary"))),
                            dbc.Col(html.Div(dbc.Alert( "Trigger Limit: "+str(record[12]), color="primary"))),
                    ]
                    ),
               dbc.Row(
                    [
                            dbc.Col(html.Div(dbc.Alert( "Moisture Alarm: "+record[5], color="primary"))),
                            dbc.Col(html.Div(dbc.Alert( "Moisture Trigger Minimum: "+str(record[6]), color="primary"))),
                            dbc.Col(html.Div(dbc.Alert( "Moisture Trigger Maximum: "+str(record[7]), color="primary"))),
                    ]
                    ),
               dbc.Row(
                    [
                            dbc.Col(html.Div(dbc.Alert( "Temperature Alarm: "+record[8], color="primary"))),
                            dbc.Col(html.Div(dbc.Alert( "Temperature Trigger Minimum: "+str(record[9]), color="primary"))),
                            dbc.Col(html.Div(dbc.Alert( "Temperature Trigger Maximum: "+str(record[10]), color="primary"))),
                    ]
                    ),
               dbc.Row(
                    [
                            dbc.Col(html.Div(dbc.Alert( "Email Notification: "+record[14], color="primary"))),
                            dbc.Col(html.Div(dbc.Alert( "Text Notification: "+record[15], color="primary"))),
                            dbc.Col(html.Div())
                    ]
                    ),
               dbc.Row(
                    [
                            dbc.Col(html.Div(dbc.Alert( "Last Trigger: "+TriggerTime, color="primary"))),
                            dbc.Col(html.Div(dbc.Alert( "Trigger Count: "+str(record[13]), color="primary"))),
                            dbc.Col(html.Div())
                    ]
                    ),

                    ]))
    return layout      
################
# Page Functions
################


def AlarmPage():
    Row1 = html.Div(
        [ html.H1(children="Alarm Programming"),
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







