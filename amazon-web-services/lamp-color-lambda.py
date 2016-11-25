import json
import boto3

client = boto3.client('iot-data', region_name='eu-central-1')

def lambda_handler(event, context):
    if event and 'brightness' in event:
        value = event['brightness']

        # Construct a Philips Hue request using the given brightness value
        saturation = int(min(255, value * 400))
        brightness = int(max(0, min(255, 555 - value * 600)))
        hue = 6000

        response = client.publish(
            topic = 'iot/raspberrypi/brightness/update',
            qos = 1,
            payload = json.dumps({'on': True, 'hue': hue, 'bri': brightness, 'sat': saturation})
        )
    return 0
