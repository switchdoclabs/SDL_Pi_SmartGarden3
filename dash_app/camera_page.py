import os, sys, glob
# import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


import pandas as pd
import MySQLdb as mdb
import datetime
import time


import plotly.graph_objs as go
# from dash.dependencies import Input, Output, MATCH, ALL, State

os.makedirs("static/SkyCam", exist_ok=True)


# build the path to import config.py from the parent directory
sys.path.append('../')
import config

# how long before you ignore the camera information
IGNOREAFTERDAYS = 7

def build_picture_figure(cameraID):

    return "../static/CurrentPicture/"+cameraID+".jpg"




def getSkyCamList():

    dir_path = '../static/SkyCam/'
    devices = os.listdir(dir_path)
    devices = sorted(devices)
    timeDelta = datetime.timedelta(days= IGNOREAFTERDAYS )
    now = datetime.datetime.now()
    before = now - timeDelta
    #before = before.strftime('%Y-%m-%d %H:%M:%S')
    
    newdevices = []
    for device in devices:
        lastMod= time.ctime(max(os.path.getmtime(root) for root,_,_ in os.walk(dir_path+device)))
        lastMod = datetime.datetime.strptime(lastMod, "%a %b %d %H:%M:%S %Y")
        #print ("last modified: %s" % lastMod) 
        if (lastMod > before):
            newdevices.append(device)

       
    #print(newdevices)
    return newdevices

def getTimeLapseList(cam):
    output = []
    try:
    
        dir_path = "../static/TimeLapses/"+cam
    
        myFiles = os.listdir(dir_path) 
        myFiles = [os.path.join(dir_path, f) for f in myFiles] # add path to each file
        #myFiles.sort(reverse=True)
        myFiles.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        #print(myFiles) 
        if (len(myFiles) > 14):
            myRange = range(0, 14)
        else:
            myRange = range(0,len(myFiles))
    
        #print(myRange)
        for i in myRange: 
            singleName = os.path.basename(myFiles[i])
            #output.append(html.P(singleName))
            output.append(dcc.Link(singleName, href="/static/TimeLapses/"+cam+"/"+singleName, target='blank'))
            output.append(html.Br())
        #print(output)
    except:
        pass 

    return output 


def buildPics(SkyCamList):

    output = []
    index = 0
    
    for cam in SkyCamList:
        if (cam != "GardenCamPi"):
            prefix = "Infrared "
            picwidth = 256
            picheight = 256
        else:
            prefix = ""
            picwidth = 350*1.77
            picheight = 350
        output.append( html.H3(prefix+cam))
        #output.append( html.Img( 
            #id={'type' : 'SkyCamPic', 'index' : index},
            #height=350, width=350*1.77, src="/assets/"+cam+".jpg"))
        picname = glob.glob("assets/"+cam+"*.jpg")
    
        #print("picname=", picname)
        output.append( 
            html.Div(        [
                dbc.Row(
                [
                    dbc.Col(html.Div(
                        html.Img( 
                            id={'type' : 'SkyCamPic', 'index' : index},
                            height=picheight, width=picwidth, src="/"+picname[0]))
                        ),
                    dbc.Col(html.Div([html.H4("Time Lapses"),
                    html.Br(),
                    html.Div(children = getTimeLapseList(cam))
                        ]
                            )
                            ),
                ]
                  ),
              ]  )
              )
        index = index+1
    #print(output)    
    return output


def CameraPage():

    SkyCamList = getSkyCamList()

    layout = html.Div(children=[

    html.H1("SmartGarden3 Cameras", style={'textAlign': 'center'}),

    html.Div(id={'type' : 'Cameras', 'index' :0}, children= buildPics(SkyCamList)),


    ], className="container" )

    # con.close()
    return layout


