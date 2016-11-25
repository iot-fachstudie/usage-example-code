from google.cloud import pubsub
import sys
import time

topic_name = '<Name of the Pub/Sub topic to write to>'

def publish_message(data):
  pubsub_client = pubsub.Client()
  topic = pubsub_client.topic(topic_name)
  data = data.encode('utf-8')
  message_id = topic.publish(data)
  print('Message {0} published.'.format(message_id))

# Create a light sensor to fetch brightness data from the GPIO pins
light_sensor = LightSensor(4)

try:
  while True:
    payload = '{{"brightness":{0}}}'.format(light_sensor.value)
    publish_message(payload)
    time.sleep(1)
except KeyboardInterrupt:
  print("Interrupted by user, shutting down.")
  sys.exit(0)
