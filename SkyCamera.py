from __future__ import print_function

import requests
import time 
import picamera
import state
import glob

import hashlib

import os
import math
import time
import numpy as np

from PIL import ImageFont, ImageDraw, Image
import traceback
import util
import datetime as dt

import MySQLdb as mdb

from scipy.interpolate import griddata

from colour import Color

# Check for user imports
import config

def SkyWeatherKeyGeneration(userKey):

    catkey = "AZWqNqDMhvK8Lhbb2jtk1bucj0s2lqZ6" +userKey

    md5result = hashlib.md5(catkey.encode())
    #print ("hashkey =", md5result.hexdigest())
    return md5result.hexdigest()

# some utility functions
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def processInfraredPicture(myID, inputpixels):
   

    inputpixels = inputpixels[0:len(inputpixels)-1]
    #print("inputpixels=", inputpixels)
    mypixels = inputpixels.split(",")
    fpixels = []
    for singlepixel in mypixels:
        fpixels.append(float(singlepixel))

    print("fpixels=", fpixels)
    pixels = fpixels
    if (config.irgain == 0):
        # auto gain
        # find minimum in pixels
        MINTEMP = min(pixels) 

        # find maximum in pixles
        MAXTEMP = max(pixels) 
    
    else:

        # low range of the sensor (this will be blue on the screen)
        MINTEMP = 26.0
    
        # high range of the sensor (this will be red on the screen)
        MAXTEMP = 32.0
    print ("MINTEMP=%d MAXTEMP=%d" % (MINTEMP, MAXTEMP))
    # how many color values we can have
    COLORDEPTH = 1024
    
    # pylint: disable=invalid-slice-index
    points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
    grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]
    # pylint: enable=invalid-slice-index

    # sensor is an 8x8 grid so lets do a square
    height = 256
    width = 256

    # the list of colors we can choose from
    blue = Color("indigo")
    colors = list(blue.range_to(Color("red"), COLORDEPTH))

    # create the array of colors
    colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

    displayPixelWidth = width / 30
    displayPixelHeight = height / 30
 

    # the list of colors we can choose from
    blue = Color("indigo")
    colors = list(blue.range_to(Color("red"), COLORDEPTH))

    # create the array of colors
    colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]



    pixels = [map_value(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]

    # perform interpolation
    bicubic = griddata(points, pixels, (grid_x, grid_y), method="cubic")
    
    
    array = np.zeros((height, width, 3), np.uint8)
    #array = np.reshape(array, (height, width,3))

    #array = np.zeros((height, width))

    # draw everything
    array[:,:] = [255, 128, 0]
    for ix, row in enumerate(bicubic):
        for jx, pixel in enumerate(row):
            pixelWidth = 8
            pixelHeight = 8
            for ixf in range(ix*pixelHeight, ix*pixelHeight+8):
                for jxf in range(jx*pixelWidth, jx*pixelWidth+8):
                    array[ixf, jxf] = colors[constrain(int(pixel), 0, COLORDEPTH - 1)]


    cameraID = myID+"-IR"
    currentpicturefilename = "static/CurrentPicture/"+cameraID+".jpg"
    currentpicturedashfilename = "dash_app/assets/"+cameraID+"_1.jpg"
    for name in glob.glob("dash_app/assets/"+cameraID+"_*.jpg"):
        os.remove(name)

    # put together the file name
    fileDate = dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    fileDay = dt.datetime.now().strftime("%Y-%m-%d")

    singlefilename =cameraID+"_1_"+fileDate+".jpg"
    dirpathname="static/SkyCam/" + cameraID+ "/"+fileDay

    os.makedirs(dirpathname, exist_ok=True)
    os.makedirs("static/CurrentPicture", exist_ok=True)
    filename = dirpathname+"/"+singlefilename
    #print("filename=", filename)
    im = Image.fromarray(array)

    # Choose a font
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 10)


    # add timestamp
    myText = "%s " % (dt.datetime.now().strftime('%d-%b-%Y %H:%M:%S'))
    myText2 = "MinTemp:%6.1fC MaxTemp:%6.1fC"%(MINTEMP, MAXTEMP)
    # Draw the text
    color = 'rgb(255,255,255)'
    #draw.text((0, 0), myText,fill = color, font=font)

    # get text size
    text_size = font.getsize(myText)
    text_size2 = font.getsize(myText2)

    # set button size + 10px margins
    button_size = (text_size[0]+20, text_size[1]+10)
    button_size2 = (text_size2[0]+20, text_size2[1]+10)

    # create image with correct size and black background
    button_img = Image.new('RGBA', button_size, "black")
    button_img2 = Image.new('RGBA', button_size2, "black")
 
    # put text on button with 10px margins
    button_draw = ImageDraw.Draw(button_img)
    button_draw.text((10, 5), myText, fill = color, font=font)
    im.paste(button_img, (0, 0))

    button_draw2 = ImageDraw.Draw(button_img2)
    button_draw2.text((10, 5), myText2, fill = color, font=font)
    im.paste(button_img2, (0, 240))
    bg_w, bg_h = im.size 




    im.save(currentpicturefilename)
    im.save(currentpicturedashfilename)
    im.save(filename)

    FileSize =os.path.getsize(currentpicturefilename)


    if (config.enable_MySQL_Logging == True):
        # open mysql database
        # write log
        # commit
        # close
        try:

            con = mdb.connect(
                "localhost",
                "root",
                config.MySQL_Password,
                "SmartGarden3" 
            )

            cur = con.cursor()

            fields = "cameraID, picturename, picturesize, messageID, resends,resolution"

            values = "\'%s\', \'%s\', %d, %d, %d, %d" % (cameraID, singlefilename, FileSize, 1, 0, 0)  
            query = "INSERT INTO SkyCamPictures (%s) VALUES(%s )" % (fields, values)
            #print("query=", query)
            cur.execute(query)
            con.commit()
        except mdb.Error as e:
            traceback.print_exc()
            print("Error %d: %s" % (e.args[0], e.args[1]))
            con.rollback()
            # sys.exit(1)

        finally:
            cur.close()
            con.close()

            del cur
            del con


def takeSkyPicture():

    if (config.SWDEBUG):
        print ("--------------------")
        print ("Garden Cam Picture Taken")
        print ("--------------------")
    camera = picamera.PiCamera()

    camera.exposure_mode = "auto"
    try:
        camera.rotation = 180
        #camera.rotation = 270
        camera.resolution = (1920, 1080)
        # Camera warm-up time
        time.sleep(2)

        camera.capture('static/skycamera.jpg')

        # now add timestamp to jpeg
        pil_im = Image.open('static/skycamera.jpg')
      
        draw = ImageDraw.Draw(pil_im)
        
        # Choose a font
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 25)

        # set up units
        #wind
        myText = "SmartGarden %s %s " % (config.SGSVERSION,dt.datetime.now().strftime('%d-%b-%Y %H:%M:%S'))

        # Draw the text
        color = 'rgb(255,255,255)'
        #draw.text((0, 0), myText,fill = color, font=font)

        # get text size
        text_size = font.getsize(myText)

        # set button size + 10px margins
        button_size = (text_size[0]+20, text_size[1]+10)

        # create image with correct size and black background
        button_img = Image.new('RGBA', button_size, "black")
     
        # put text on button with 10px margins
        button_draw = ImageDraw.Draw(button_img)
        button_draw.text((10, 5), myText, fill = color, font=font)

        # put button on source image in position (0, 0)

        pil_im.paste(button_img, (0, 0))
        bg_w, bg_h = pil_im.size 
        # WeatherSTEM logo in lower left
        size = 64
        WSLimg = Image.open("static/WeatherSTEMLogoSkyBackground.png")
        WSLimg.thumbnail((size,size),Image.ANTIALIAS)
        pil_im.paste(WSLimg, (0, bg_h-size))

        # SkyWeather log in lower right
        SWLimg = Image.open("static/SkyWeatherLogoSymbol.png")
        SWLimg.thumbnail((size,size),Image.ANTIALIAS)
        pil_im.paste(SWLimg, (bg_w-size, bg_h-size))

        # Save the image
        pil_im.save('dash_app/assets/skycamera.jpg', format= 'JPEG')
        pil_im.save('static/skycamera.jpg', format= 'JPEG')
        pil_im.save('static/skycameraprocessed.jpg', format= 'JPEG')

        cameraID = "GardenCamPi"
        currentpicturefilename = "static/CurrentPicture/"+cameraID+".jpg"
        currentpicturedashfilename = "dash_app/assets/"+cameraID+"_1.jpg"
        for name in glob.glob("dash_app/assets/"+cameraID+"_*.jpg"):
            os.remove(name)

        # put together the file name
        fileDate = dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileDay = dt.datetime.now().strftime("%Y-%m-%d")

        singlefilename =cameraID+"_1_"+fileDate+".jpg"
        dirpathname="static/SkyCam/" + cameraID+ "/"+fileDay

        os.makedirs(dirpathname, exist_ok=True)
        os.makedirs("static/CurrentPicture", exist_ok=True)
        filename = dirpathname+"/"+singlefilename


        pil_im.save(filename, format= 'JPEG')
        pil_im.save(currentpicturefilename, format= 'JPEG')
        pil_im.save(currentpicturedashfilename, format= 'JPEG')

        FileSize =os.path.getsize(currentpicturefilename)

        if (config.enable_MySQL_Logging == True):
            # open mysql database
            # write log
            # commit
            # close
            try:
    
                con = mdb.connect(
                    "localhost",
                    "root",
                    config.MySQL_Password,
                    "SmartGarden3" 
                )

                cur = con.cursor()
    
                fields = "cameraID, picturename, picturesize, messageID, resends,resolution"

                values = "\'%s\', \'%s\', %d, %d, %d, %d" % (cameraID, singlefilename, FileSize, 1, 0, 0)  
                query = "INSERT INTO SkyCamPictures (%s) VALUES(%s )" % (fields, values)
                #print("query=", query)
                cur.execute(query)
                con.commit()
            except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0], e.args[1]))
                con.rollback()
                # sys.exit(1)
    
            finally:
                cur.close()
                con.close()
    
                del cur
                del con



        time.sleep(2)

    except:
            if (config.SWDEBUG):
                print(traceback.format_exc()) 
                print ("--------------------")
                print ("Garden Cam Picture Failed")
                print ("--------------------")


    finally:
        try:
            camera.close()
        except:
            if (config.SWDEBUG):
                print ("--------------------")
                print ("Garden Cam Close Failed ")
                print ("--------------------")




import base64


def sendSkyWeather():

    # defining the api-endpoint  
    API_ENDPOINT = "https://skyweather.weatherstem.com/"
     
  

    with open("static/skycamera.jpg", "rb") as image_file:
       encoded_string = base64.b64encode(image_file.read())

    if (config.SWDEBUG):
        print ("--------------------")
        print ("SkyCam Package Sending")
        print ("--------------------")

    if(state.barometricTrend == True):
        bptrendvalue = "Rising"
    else:
        bptrendvalue = "Falling"
   
    currentTime = time.time()

    print("api_key:", state.WeatherSTEMHash)
    data = {
                "SmartGardenSystemVersion": config.SGSVERSION,
                "SkyWeatherHardware": config.STATIONHARDWARE,
                "api_key": state.WeatherSTEMHash,

	"device":{
                "key":  config.STATIONKEY,
                "MAC":config.STATIONMAC,
	},
	"utc":currentTime,
	"sensors":[


		{
			"name":"OutsideTemperature",
			"value": state.OutdoorTemperature,
                        "units" : "C"

		},
		{
			"name":"OutsideHumidity",
			"value": state.OutdoorHumidity,
                        "units" : "%"

		},
		{
			"name":"InsideTemperature",
			"value": state.IndoorTemperature,
                        "units" : "C"
		},
		{
			"name":"InsideHumidity",
			"value": state.IndoorHumidity,
                        "units" : "%"

		},
		#{
		#	"name":"RainInLast60Minutes",
		#	"value": state.currentRain60Minutes,
        #                "units" : "mm/h"
		#},
		{
			"name":"VisibleSunlight",
			"value": state.SunlightVisible,
                        "units" : "lux"
		},
		#{
	    #		"name":"IRSunlight",
		#	"value": state.SunlightIR,
        #                "units" : "lux"
		#},
		{
			"name":"UVSunlightIndex",
			"value": state.SunlightUVIndex,
                        "units" : ""

		},
		{
			"name":"WindSpeed",
			"value": state.WindSpeed,
                        "units" : "m/s"
		},
		{
			"name":"WindGust",
			"value": state.WindGust,
                        "units" : "m/s"
		},
		{
			"name":"WindDirection",
			"value": state.WindDirection,
                        "units" : "degrees"
		},
		{
			"name":"totalRain",
			"value": state.TotalRain,
                        "units" : "mm"

		},
		{
			"name":"BarometricPressure",
			"value": state.BarometricPressure,
                        "units" : "hPa"

		},
		{
			"name":"Altitude",
			"value": state.Altitude,
                        "units" : "m"
		},
		{
			"name":"SeaLevelPressure",
			"value": state.BarometricPressureSeaLevel,
                        "units" : "hPa"
		},
		{
			"name":"BarometricTrend",
			"value": bptrendvalue,
                        "units" : ""


		},
		{
			"name":"OutdoorAirQuality",
			"value": state.AQI,
                        "units" : "AQI"
		},
		#{
		#	"name":"IndoorAirQuality",
		#	"value": state.Indoor_AirQuality_Sensor_Value,
        #                "units" : "AQI"
		#},
		#{
		#	"name":"LastLightningDistance",
		#	"value": state.currentAs3935LastDistance,
        #                "units" : "km"

		#},
		#{
		#	"name":"LastLightningTimeStamp",
		#	"value": state.currentAs3935LastLightningTimeStamp,
        #                "units" : ""
		#}
                ],
	"solarpower":[
		{
			"name":"BatteryVoltage",
			"value": state.batteryVoltage,
                        "units" : "V"


		},
		{
			"name":"BatteryCurrent",
			"value": state.batteryCurrent,
                        "units" : "ma"
		},
		{ 
                        "name":"SolarVoltage", 
                        "value": state.solarVoltage,
                        "units" : "V"
                },
		{
			"name":"SolarCurrent",
			"value": state.solarCurrent,
                        "units" : "ma"

		}, 
                {
			"name":"LoadVoltage",
			"value": state.loadVoltage,
                        "units" : "V"
		},
		{
			"name":"LoadCurrent",
			"value": state.loadCurrent,
                        "units" : "ma"
		},
		{
			"name":"BatteryPower",
			"value": state.batteryPower,
                        "units" : "W"
		},
		{
			"name":"SolarPower",
			"value": state.solarPower,
                        "units" : "W"
		},
		{
			"name":"LoadPower",
			"value": state.loadPower,
                        "units" : "W"
		},
		{
			"name":"BatteryCharge",
			"value": state.batteryCharge,
                        "units" : "%"

		},
		
	],
	"cameras":[
		{
			"name":"Sky Camera",
                        "image": encoded_string
		}
		
	]
    }


  
    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, json = data) 
    #print data 
    # extracting response text  
    pastebin_url = r.text 
    if (config.SWDEBUG):
        print("The pastebin URL is (r.text):%s"%pastebin_url) 



        
