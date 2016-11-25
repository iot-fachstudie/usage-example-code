#!/usr/bin/python

import time
import sys
import os, json
import ibmiotf.application
import uuid
from gpiozero import LightSensor

def sample():
    value = 0
    for i in range(0,5):
        value += light_sensor.value / 5.0
    return value

try:
    light_sensor = LightSensor(21)
    client = None
    lightStatus = None
    
    options = {
		"org": "my-organisation-id",
		"type": "Raspberry Pi",
		"id": "my-id",
		"auth-method": "token",
		"auth-token": "my-token"
	}
    client = ibmiotf.application.Client(options)
    client.connect()
    print "connected"
    
    while True:
        data = {"light": sample()}
        print data
        client.publishEvent(options["type"], options["id"], "status", "json", data)

        time.sleep(0.1)

except ibmiotf.ConnectionException as e:
    print e
except KeyboardInterrupt:
    print "Interrupted by user, shutting down."
    sys.exit(0)
