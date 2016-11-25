import requests
import sys
import wia
import json
import logging

logging.getLogger("requests").setLevel(logging.WARNING)

# API endpoints and keys
philips_hue_local_url = "<Local URL with username to the lamp>"
wia.secret_key = "<Secret user key>"
wia_sensor_device_uid = "<Device UID>"
wia_sensor_name = "brightness_sensor"

wia.Stream.connect()

def hue_post(data):
    '''Post some JSON data to the Philips Hue light.'''
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    requests.put(philips_hue_local_url, data=json.dumps(data), headers=headers)

def set_light(value):
    '''Given a value between 0 and 1, set the light to an appropriate color between bright white and dark orange'''
    hue_post({'on': True, 'sat': int(min(255, value * 400)), 'bri': int(max(0, min(255, 555 - value * 600))), 'hue': 6000})

def handle_brightness_update(payload):
    '''Handle a data payload from a sensor event'''
    set_light(float(payload['data']))

def subscribe_to_sensor():
    '''Subscribe to all events from a specific sensor on the Wia IoT platform.'''
    wia.Sensor.subscribe(
        device = wia_sensor_device_uid,
        name = wia_sensor_name,
        func = handle_brightness_update
    )

try:
    subscribe_to_sensor()
    hue_post({'on': True, 'sat': 0, 'bri': 255, 'hue': 0})
    while True:
        pass
except KeyboardInterrupt:
    print("Interrupted by user, shutting down.")
    wia.Stream.disconnect()
    hue_post({'on': False})
    sys.exit(0)
