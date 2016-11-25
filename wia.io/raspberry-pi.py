import sys
import wia
from gpiozero import LightSensor, Buzzer
import logging

logging.getLogger("requests").setLevel(logging.WARNING)

# API endpoints and keys
wia.secret_key = "<Secret API key>"
wia_sensor_name = "brightness_sensor"

# Initialize a new light sensor connected to the fourth GPIO pin
light_sensor = LightSensor(4)

try:
    while True:
        # Identify as the light sensor and publish the current value to the IoT platform
        wia.Sensor.publish(
            name = wia_sensor_name,
            data = "{0}".format(1 - light_sensor.value)
        )
except KeyboardInterrupt:
    print("Interrupted by user, shutting down.")
    sys.exit(0)
