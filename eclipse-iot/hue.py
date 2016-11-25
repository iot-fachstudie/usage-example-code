#!/usr/bin/python

import paho.mqtt.client as mqtt
import json
import sys
import requests

hue_url = "http://192.168.178.46/api/my-api-key/lights/1/state"

def hue_post(sat=0, bri=0, hue=0, on=True):
	'''Post some JSON data to the Philips Hue light.'''
	headers = {"Content-type": "application/json", "Accept": "text/plain"}
	payload = {"on": on, "sat": int(sat), "bri": int(bri), "hue": int(hue)}
	requests.put(hue_url, data=json.dumps(payload), headers=headers)

def on_message(client, userdata, msg):
	payload = json.loads(msg.payload)
	print "Received new light: " + msg.payload
	hue_post(payload["sat"], payload["bri"], payload["hue"])
    
def on_connect(client, userdata, rc):
	print "Connected. Status: " + str(rc)
	client.subscribe("fachstudie-us/light-cmd")
    
try:
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message

	client.connect("iot.eclipse.org", 1883, 60)
	client.loop_forever()
except KeyboardInterrupt:
	print("Interrupted by user, shutting down.")
	hue_post(on=False)
	client.disconnect()
	sys.exit(0)

