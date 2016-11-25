#!/usr/bin/python

import paho.mqtt.client as mqtt
import json
import time
import sys
from gpiozero import LightSensor

def sample():
    value = 0
    for i in range(0,5):
        value += light_sensor.value / 5.0
    return value

try:
    client = mqtt.Client()
    light_sensor = LightSensor(21)
    
    client.connect("iot.eclipse.org", 1883, 60)
    print "connected"
    client.loop_start()
    
    while True:
        data = {"light": sample()}
        print data
        client.publish("fachstudie-us/light-val", payload=json.dumps(data))

        time.sleep(0.1)

except KeyboardInterrupt:
    print "Interrupted by user, shutting down."
    client.loop_stop(True)
    client.disconnect()
    sys.exit(0)
