# test for Weather Sensors
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
import sys
from subprocess import PIPE, Popen, STDOUT
from threading  import Thread
#import json
import datetime
import config
import traceback

import MySQLdb as mdb

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
print("Starting Bluetooth Read")
cmd = [ '/usr/bin/hcitool', 'lescan']


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#  database update functions


def addBluetooth(sLine):
       print("Found Sensor: ", sLine) 

       splitline = sLine.split(" ")
       # find out if address exists in data base
       print("splitline = ", splitline)
       try:
                #print("trying database")
                con = mdb.connect('localhost', 'root', config.MySQL_Password, 'SmartGardenSystem');
                cur = con.cursor()
                query = "SELECT *  WHERE fulladdress = '%s'" % (splitline[0])

                print("query=", query)
                cur.execute(query)
                myRecords = cur.fetchall()
                print("myRecords = ", myRecords)
       except mdb.Error as e:
                traceback.print_exc()
                print("Error %d: %s" % (e.args[0],e.args[1]))
                myRecords = [];
       finally:
                cur.close()
                con.close()

                del cur
                del con



       # add it if it doesnt exist
       if (len(myRecords) == 0):
            print("add new record")
     
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#   A few helper functions...

def nowStr():
    return( datetime.datetime.now().strftime( '%Y-%m-%d %H:%M:%S'))

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#stripped = lambda s: "".join(i for i in s if 31 < ord(i) < 127)


#   We're using a queue to capture output as it occurs
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x
ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(src, out, queue):
    for line in iter(out.readline, b''):
        queue.put(( src, line))
    out.close()

#   Create our sub-process...
#   Note that we need to either ignore output from STDERR or merge it with STDOUT due to a limitation/bug somewhere under the covers of "subprocess"
#   > this took awhile to figure out a reliable approach for handling it...
p = Popen( cmd, stdout=PIPE, stderr=STDOUT, bufsize=1, close_fds=ON_POSIX)
q = Queue()

t = Thread(target=enqueue_output, args=('stdout', p.stdout, q))

t.daemon = True # thread dies with the program
t.start()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

pulse = 0
while True:
    #   Other processing can occur here as needed...
    #sys.stdout.write('Made it to processing step. \n')

    try:
        src, line = q.get(timeout = 1)
        #print(line.decode())
    except Empty:
        pulse += 1
    else: # got line
        pulse -= 1
        sLine = line.decode()
        print(sLine)
        #   See if the data is something we need to act on...
        if ( sLine.find('Flower') != -1): 
            sys.stdout.write('This is the raw data: ' + sLine + '\n')
            action = addBluetooth(sLine) 
            print("action=", action)

    sys.stdout.flush()

