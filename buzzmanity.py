#!/usr/bin/env python3

from frames.DevFrame import DevFrame
from frames.AddCardFrame import AddCardFrame
from frames.HomeFrame import HomeFrame
from csv2dict import csv2dict
import serial
import time
import sys
import requests
import os

import importlib
from tkinter import *

humanity = __import__('humanity')

# Dev mode flag
DEVMODE = ('-dev' in sys.argv)
if DEVMODE:
    print('Dev mode enabled')

if os.environ.get('DISPLAY', '') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

# Import local config file
__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))
k = csv2dict(os.path.join(__location__, '.keys.txt'))

SERIAL_PORT = k.get('SERIAL_PORT')
SERIAL_RATE = 9600

FETCH_PERIOD_SECONDS = 60

# Credentials
user_id = k.get('user_id')
passwd = k.get('passwd')
client_id = k.get('client_id')
client_secret = k.get('client_secret')

h = None

while h == None:
    try:
        h = humanity.Humanity(user_id, passwd, client_id, client_secret)
    except requests.exceptions.ConnectionError:
        print('failed to connect to internet, retrying in 3s...')
        time.sleep(3)


# Open serial port
ser = None
serConnected = None


def connectToBuzzcardReader(SERIAL_PORT, SERIAL_RATE):
    global ser, serConnected
    try:
        ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)

        serConnected = True  # indicate success
    except serial.serialutil.SerialException:
        if serConnected is None:
            # First failure
            print('Unable to open serial port -  will retry in background')
            serConnected = False


window = Tk()

homeFrame = HomeFrame(window, h)

devWindow = None
devFrame = None

lastFetchTime = 0

if DEVMODE:
    devWindow = Tk()
    devFrame = DevFrame(devWindow, h, homeFrame)

while True:
    if(time.time() - lastFetchTime > FETCH_PERIOD_SECONDS):
        print('Automatically fetching onNow PIs')
        homeFrame.fetchOnNow()
        homeFrame.updateOnNowFrame()
        lastFetchTime = time.time()

    window.update_idletasks()
    window.update()

    # if incoming bytes are waiting to be read from the serial input buffer
    if ser is not None and (ser.inWaiting() > 0):
        # read the bytes and convert from binary array to ASCII
        data_str = ser.read(ser.inWaiting()).decode('ascii')

        print('Scanned card ' + data_str, end='\n')

        # Runs on each card scan
        try:
            homeFrame.processBuzzcardScan(data_str.strip())
        except requests.exceptions.ConnectionError:
            print('Failed to process buzzcard scan due to Connection Error')
    else:
        connectToBuzzcardReader(SERIAL_PORT, SERIAL_RATE)

    time.sleep(0.01)
