from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import json
import requests
import logging

logging.getLogger("requests").setLevel(logging.WARNING)

# API endpoints, keys and certificates
philips_hue_local_url = "<Local URL with username to the lamp>"
host = "<Host URL with region>"
rootCAPath = "<Path to root CA certificate file>"
certificatePath = "<Path to the certificate file>"
privateKeyPath = "<Path to the private key file>"

def hue_post(data):
	'''Post some JSON data to the Philips Hue light.'''
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	requests.put(philips_hue_local_url, data=json.dumps(data), headers=headers)

def lampUpdateCallback(client, userdata, message):
	'''This method will be called whenever the lamp color needs to be updated.'''
	hue_post(json.loads(message.payload))

# Client initialization
client = AWSIoTMQTTClient("PhilipsHue")
client.configureEndpoint(host, 8883)
client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# Connection configuration
client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)

# Connect to the AWS IoT platform
client.connect()

# Subscribe to all lamp color update requests using their common MQTT topic
client.subscribe("iot/raspberrypi/brightness/update", 1, lampUpdateCallback)

# Initially, turn on the lamp and set it to white
hue_post({'on': True, 'sat': 0, 'bri': 255, 'hue': 0})

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Interrupted by user, shutting down.")
    hue_post({'on': False})
    sys.exit(0)
