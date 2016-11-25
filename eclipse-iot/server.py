#!/usr/bin/python

import paho.mqtt.client as mqtt
import json
import sys

def getNewLightValues(value):
    sat = int(min(255, value*400))
    bri = int(max(0, min(255, 555 - value * 600)))
    hue = 6000
    return {"sat":sat, "bri":bri, "hue": hue}

def on_connect(client, userdata, rc):
    print "Connected. Status: " + str(rc)
    client.subscribe("fachstudie-us/light-val")

def on_message(client, userdata, msg):
    global lastLightValue
    payload = json.loads(msg.payload)
    print "Received new light value: " + str(payload["light"])
    if abs(lastLightValue - payload["light"]) > 0.1:
        lastLightValue = payload["light"]
        cmd = getNewLightValues(1-payload["light"])
        client.publish("fachstudie-us/light-cmd", json.dumps(cmd)) 

try:
    lastLightValue = -1
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect("iot.eclipse.org", 1883, 60)
    client.loop_forever()
except KeyboardInterrupt:
    print "Interrupted by User... shutting down"
    client.disconnect()
    sys.exit(0)
