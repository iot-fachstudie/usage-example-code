import ibmiotf.device
import time
import json
import sys
import requests

hue_url = "http://192.168.178.46/api/my-api-key/lights/1/state"

def hue_post(sat=0, bri=0, hue=0, on=True):
	'''Post some JSON data to the Philips Hue light.'''
	headers = {"Content-type": "application/json", "Accept": "text/plain"}
	payload = {"on": on, "sat": int(sat), "bri": int(bri), "hue": int(hue)}
	requests.put(hue_url, data=json.dumps(payload), headers=headers)

def callback(cmd):
    if cmd.command != "changeLight":
        return
    print "received new values:"
    print cmd.data
    hue_post(cmd.data["sat"], cmd.data["bri"], cmd.data["hue"])

options = {
	"org": "my-organisation-id",
	"type": "Hue",
	"id": "test-pc",
	"auth-method": "token",
    "auth-token": "my-token"
}

client = ibmiotf.device.Client(options)
client.connect()

client.commandCallback = callback;

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Interrupted by user, shutting down.")
    hue_post(on=False)
    sys.exit(0)

