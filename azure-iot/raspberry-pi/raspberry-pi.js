'use strict'

const Protocol = require('azure-iot-device-amqp').Amqp
const { Client, Message } = require('azure-iot-device')
const { measureBrightness } = require('./light-sensor')

// Connection string for Azure
const connectionString = '[IoT Hub device connection string]'

// Create a client and open a connection to Azure's IoT Hub
const client = Client.fromConnectionString(connectionString, Protocol)
client.open()
  .then(() => {
    console.log('Client connected')

    // Log incoming messages
    client.on('message', msg => {
      console.log(`ID: ${msg.messageId} Body: ${msg.data}`)
      client.complete(msg, printResultFor('completed'))
    })

    // Log errors
    client.on('error', err => {
      console.error(err.message)
    })

    // Every second, measure the brightness and send the result to the Cloud
    setInterval(() => {
      measureBrightness(4)
        .then(brightness => {
          const message = new Message(JSON.stringify({ brightness: value }))
          console.log(`Sending message: ${message.getData()}`)
          client.sendEvent(message, printResultFor('send'))
        })
    }, 1000)
  })
  .catch(err => console.error(`Could not connect: ${err}`))

function printResultFor(op) {
  return function printResult(err, res) {
    if (err) console.log(`${op} error: ${err}`)
    if (res) console.log(`${op} status: ${res.constructor.name}`)
  }
}
