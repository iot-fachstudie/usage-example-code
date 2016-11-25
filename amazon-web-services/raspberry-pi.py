from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
from gpiozero import LightSensor, Buzzer
import sys
import json
import time

host = "<Host URL with region>"
rootCAPath = "<Path to root CA certificate file>"
certificatePath = "<Path to the certificate file>"
privateKeyPath = "<Path to the private key file>"

# Thing shadow callback
def update_callback(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Update request timed out!")
    if responseStatus == "rejected":
        print("Update request rejected!")

# Client initialization
client = AWSIoTMQTTShadowClient("RaspberryPi")
client.configureEndpoint(host, 8883)
client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# Connection configuration
client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)

# Connect to the AWS IoT platform
client.connect()

# Create a device shadow handler
handler = client.createShadowHandlerWithName("RaspberryPi", True)

# Create a light sensor to fetch brightness data from the GPIO pins
light_sensor = LightSensor(4)

try:
    while True:
        payload = '{{"state":{{"desired":{{"brightness":{0}}}}}}}'.format(light_sensor.value)
        handler.shadowUpdate(payload, update_callback, 5)
        time.sleep(0.5)
    pass
except KeyboardInterrupt:
    print("Interrupted by user, shutting down.")
    sys.exit(0)
