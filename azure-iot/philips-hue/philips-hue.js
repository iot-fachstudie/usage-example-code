// Ref. https://github.com/Azure/azure-event-hubs/tree/master/node/send_receive
'use strict'

const request = require('request')
const EventHubClient = require('azure-event-hubs').Client

// Connection string for Azure's Event Hub
const connectionString = '[Event Hub listener connection string]'
// URL pointing to hue's endpoint for one of the lights to use
const hueLightUrl = 'http://<bridge ip address>/api/<username>/lights/1'

// Create a client and open a connection to Azure's Event Hub
const client = EventHubClient.fromConnectionString(connectionString)
client.open()
  // Get all available partition IDs of the Event Hub
  .then(() => client.getPartitionIds())
  // Register receivers on all partitions to intercept every message sent by the Event Hub
  .then(partitions => partitions.forEach(
    partitionId => client.createReceiver('$Default', partitionId)
      .then(receiver => {
        console.log(`Created partition receiver for partition '${partitionId}'`)

        // Log errors
        receiver.on('errorReceived', err => console.error(err))

        // Set the light's color according to incoming messages
        receiver.on('message', message => {
          const { saturation, brightness, hue } = message.body
          request.put({
            url: hueLightUrl,
            json: true,
            body: {
              on: 'true',
              sat: saturation,
              bri: brightness,
              hue: hue
            }
          })
        })
      })
  ))
  .catch(err => console.error)
