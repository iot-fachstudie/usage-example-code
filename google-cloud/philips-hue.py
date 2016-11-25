from google.cloud import pubsub
import requests
import sys
import time

philips_hue_local_url = '<Local URL with username to the lamp>'
topic_name = '<Name of the Pub/Sub topic to subscribe to>'
subscription_name = '<Name of the subscription to use>'

def hue_post(data):
  '''Post some JSON data to the Philips Hue light.'''
  headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
  requests.put(philips_hue_local_url, data=data, headers=headers)

def create_subscription():
  '''Create the subscription topic used to listen for Hue commands.'''
  pubsub_client = pubsub.Client()
  topic = pubsub_client.topic(topic_name)

  subscription = topic.subscription(subscription_name)
  if not subscription.exists():
    subscription.create()

def receive_message():
  '''Checks for a new message on the Pub/Sub topic.'''
  pubsub_client = pubsub.Client()
  topic = pubsub_client.topic(topic_name)
  subscription = topic.subscription(subscription_name)
  results = subscription.pull(return_immediately = True)

  # Acknowledge that the message was received if one was received.
  if results:
    subscription.acknowledge([ack_id for ack_id, message in results])

  # Extract the message payload from the messages
  return [message.data.decode('utf-8') for ack_id, message in results]

create_subscription()

try:
  while True:
    for command in receive_message():
      hue_post(command)
except KeyboardInterrupt:
  print('Interrupted by user, shutting down.')
  hue_post({'on': False})
  sys.exit(0)
