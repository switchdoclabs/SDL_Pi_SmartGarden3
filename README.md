SmartGarden3<BR>
SwitchDoc Labs<BR>
June 2022<BR>

Version 058 - June 20, 2022 - Fixed reboot of extender - restore valve state on reboot<BR>
Version 057 - March 28, 2022 - Fixed Type in SG3Configure.py<BR>
Version 056 - March 10, 2022 - Fixed Merge Error in scanBluetooth.py<BR>
Version 055 - February 27, 2022 - Minor bug fixes and removal of unused code <BR>
Version 054 - February 25, 2022 - Added scanAndFixExtenders.py utility for when IP numbers change due to Access Point reset<BR>
Version 053 - February 11, 2022 - Added Hydoponics pH Meter and 24 Hour averages<BR>
Version 052 - January 31, 2022 - Fixed Bluetooth<BR>
Version 051 - January 30, 2022 - Initial Released Version<BR>

To see what is happening on the MQTT channels:<BR>
mosquitto_sub -d -t SGS/#

To Install Yourself: (Note:  This is a complicated install.   For beginners and advanced beginners, you are better off buying a configured SD Card from shop.switchdoc.com)<BR>
This is a Python3 program.  All libraries need to be in python3.<BR>


Installation

1) Install MariaDB on Raspberry Pi

2) Read in the SmartGarden3.sql file into the database
sudo mysql -u root < SmartGarden3.sql
    
3) Install python apscheduler<BR>

 sudo pip3 install apscheduler

4) Install dash libraries (there are a bunch of them).

sudo pip3 install dash<BR>
sudo pip3 install dash-bootstrap-components<BR>
sudo pip3 install plotly<BR>

5) Install remi libraries<BR>

sudo pip3 install remi<BR>

6) Install SG3
git clone github.com/switchdoclabs/SDL_Pi_SmartGarden3

Depending on your system, you may have other missing files.   See the information printed out when your SG3.py software starts and install the missing librarys.
<BR>

Note: Why don't we supply exact installation procedures?  The reason is is they are different for every distribution on the Raspberry Pi and developers are continuously changing them.  

From our customer frenchi, he has summarized installation instructions:

<pre>

I just followed the instructions from Raspberry using the Raspberry Pi imager App -- it reformats the SD Card which simply allow the Pi4 to reload its boot sw.

After sudo apt-get -y update && apt-get -u dist-upgrade

Note I placed all the SDL software in a directory called SwitchDoc :-)

- sudo apt-get clean
- sudo apt-get autoremove
- sudo apt-get install build-essential python3 python3-pip python3-dev python3-smbus git python3-apscheduler
- sudo apt-get install pigpio python3-pigpio i2c-tools
- sudo apt-get install mariadb-server
- sudo apt-get install mosquitto mosquitto-clients
- sudo apt-get install python-imaging-tk libjpeg-dev zlib1g-dev libfreetype6-dev liblcms1-dev libopenjp2-7 libtiff5sudo mysql_secure_installation
- sudo apt-get install scons swig
- sudo raspi-config to enable I2C
- sudo i2cdetect -y 1
- sudo pip3 install --upgrade setuptools pip
- sudo pip3 install setuptools --upgrade
- sudo pip3 install i2cdevice
- sudo pip3 install apscheduler adafruit-blinka picamera
- sudo pip3 install mysqlclient paho-mqtt pillow
- sudo pip3 install dash dash-bootstrap-components plotly remi pandas dash_daq
-
- mkdir SwitchDoc
- cd SwitcDoc
- git clone github.com/adafruit/Adafruit_Python_GPIO.git
- cd Adafruit_Python_GPIO
- sudo python3 setup.py install
- cd ~/SwitchDoc
- git clone github.com/switchdoclabs/SDL_Pi_8PixelStrip.git
- cd SDL_Pi_8PixelStrip
- scons
- cd python
- sudo python3 ./setup.py build
- sudo python3 ./setup.py install
- git clone github.com/switchdoclabs/SDL_Pi_SmartGarden3
- cd ~/SwitchDoc
- cd SDL_Pi_SmartGarden3
- sudo mysql -u root < SmartGarden3.sql
- sudo python3 SG3Configure.py
- sudo python3 SG3.py

</pre>


