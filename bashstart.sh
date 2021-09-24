#!/bin/bash

######################################################
# Smart Garden System V2 Autostart Script v1.0
# author : cciecanuck
# script based upon following works
# 1) https://gist.github.com/todgru/6224848#
# 2) https://gist.github.com/Jofkos/a736e40ea701a0d705c1
# Notes: This script assumes you have done the inital
# setup and configuration.
######################################################

#####<Variables Start>#####

# Create our application base
app_base=/home/pi/SDL_Pi_SmartGarden3

# base directory is this script's parent dir
cd $app_base

# dir which contains the server/proxy directories (`pwd` -> current dir)
basedir="`pwd`"

# tmux session name (`basename \"$basedir\"` -> basedir's name)
session="`basename \"$basedir\"`"

# txmux window name
window_name="SmartGardenSystemv2"

# Smart Garden System web app directory
web_app_dir=dash_app

# Smart Garden System web app name
web_app_name="index.py"

# Smart Garden System web app tcp port
web_app_tcp=8050

# Smart Garden System web app name
config_app_name="SG3Configure.py"

# Smart Garden System web app tcp port
config_app_tcp=8001

# Smart Garden System Core application
core_app_name="SG3.py"

#####<</Variables End>#####

# Make sure we start in our correct directory
if [[ basedir != */ ]]
then
   basedir+="/"
fi

#####<Functions Start>#####

start() {

# Check to see if there is currently a session running
    tmux has-session -t $session 2>/dev/null

# If the Smart Garden system is not running lets start it!
if [ $? != 0 ]; then

# This code ensures tmux process will not collide with another SmartGarden Service
# Check to see if any of the Smart Garden System Web App Components are running, if so exit out of the script
     check_app_running=$(sudo lsof -i:$web_app_tcp | egrep LISTEN | cut -d" " -f2)
     # Process cannot be empty
     if [ ! -z "$check_app_running" ]; then
      echo "[ERROR] - SG3 Web App is currently running on TCP Port $web_app_tcp, run command 'sudo kill -9 $(sudo lsof -i:$web_app_tcp | egrep LISTEN | cut -d" " -f2)' to stop server"
      exit
     else
# Check to see if any of the Smart Garden System Config Components are running, if so exit out of the script
     check_config_running=$(sudo lsof -i:$config_app_tcp | egrep LISTEN | cut -d" " -f2)
     # Process cannot be empty
      if [ ! -z "$check_config_running" ]; then
       echo "[ERROR] - SG3 Config App is currently running on TCP Port $config_app_tcp, run command 'sudo kill -9 $(sudo lsof -i:$config_app_tcp | egrep LISTEN | cut -d" " -f2)' to stop server"
       exit
      else
       check_core_running=$(ps aux | egrep "$core_app_name" | egrep -v "grep|sudo" | awk '{print $2}')
       # Process cannot be empty
       if [ ! -z "$check_core_running" ]; then
        echo "[ERROR] - SG3 Core App is currently running, run command 'sudo kill -9 $(ps aux | egrep "$core_app_name" | egrep -v "grep|sudo" | awk '{print $2}')' to stop server"
        exit
       fi
     fi
   fi


# Create tmux session and assign names to these
    tmux new-session -d -s $session -n $window_name
# Select pane 1 and start Smart Garden System Application
    tmux send-keys "sudo /usr/bin/python3 $core_app_name" C-m

# Split pane 1 horizontal by 65%, start redis-server
    tmux splitw -h -p 35

# Start Smart Garden System - core application
    tmux send-keys "sudo /usr/bin/python3 $config_app_name" C-m

# Split pane 2 vertiacally by 25%
    tmux splitw -v -p 75

# select pane 3, start Smart Garden System web app
    tmux send-keys "cd $web_app_dir && sudo /usr/bin/python3 $web_app_name" C-m

# Select pane 1
    tmux selectp -t 1


    echo "Server started. Attaching session..."
    sleep 0.5
    tmux attach-session -t $session:0
else
    echo "[INFO] - Tmux service for $window_name is currently already running, use 'sgsctl attach' to connect to session"
fi
}

stop() {

# Check to see if there is currently a session running
    tmux has-session -t $session 2>/dev/null

# If the Smart Garden system is running lets stop it!
if [ $? = 0 ]; then

    echo "[INFO] - Stopping $window_name tmux session"
    tmux kill-session -t $session
else
   echo "[INFO] - Tmux session $window_name is currently not running"
fi
}

status() {
# Check to see if there is currently a session running
    tmux has-session -t $session 2>/dev/null

# If the Smart Garden system is running lets display some info
if [ $? = 0 ]; then
    echo "[INFO] - $window_name is currently running, use 'sgsctl attach' to connect to session"
else
    echo "[INFO] - $window_name is currently not running, use 'sgsctl start' to start service"
fi
}

cron() {
# Check to see if there is currently a session running
    tmux has-session -t $session 2>/dev/null

# If the Smart Garden system is running lets display some info
if [ $? = 0 ]; then
    echo "[INFO] - $window_name is currently running, use 'sgsctl attach' to connect to session"
else
    echo "[INFO] - $window_name is currently not running, starting service"
    start
fi
}

restart() {
# Stop the service then restart it
    stop
    sleep 0.8
    echo "[INFO] - Tmux session $window_name is now being restarted"
    sleep 0.8
    start
}

#####</End Functions>#####

case "$1" in
start)
    start
;;
stop)
    stop
;;
attach)
    tmux attach -t $session
;;
status)
    status
;;
cron)
    cron
;;
restart)
    restart
;;
*)
echo "Usage: sgsctl (start|stop|restart|attach|cron|status)"
;;
esac
