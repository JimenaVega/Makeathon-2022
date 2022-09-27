import machine
import math
import network
import os
import time
import utime
import gc
import pycom
from machine import RTC
from machine import SD
from L76GNSS import L76GNSS
from pytrack import Pytrack
from network import WLAN
 
pycom.heartbeat(False)
pycom.rgbled(0x0A0A08) # white
 
time.sleep(2)
gc.enable()
 
py = Pytrack()
 
time.sleep(1)
l76 = L76GNSS(py, timeout=30, buffer=512)
 
# Load SD card
sd = SD()
os.mount(sd, '/sd')
os.listdir('/sd')
 
# Read SD card
print('Reading from file:')
f = open('/sd/test.txt', 'r')
print(f.readlines())
f.close()
print("Read from file.")
 
time.sleep(1)
 
while (True):
    coord = l76.coordinates()
    print("{} - {}".format(coord, gc.mem_free()))
    f = open('/sd/test.txt', 'a') # Append
    f.write("{}".format(coord[1]))
    f.write(' ')
    f.write("{}".format(coord[0]))
    f.write(',\n')
    f.close()
    print('Sleep for 1 minute.')
    time.sleep(60)
