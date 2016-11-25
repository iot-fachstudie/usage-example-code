'use strict'

const { EventEmitter } = require('events')
const { measureBrightness } = require('./light-sensor')

class Connector extends EventEmitter {
  isOnline (callback) {
    callback(null, { running: true })
  }

  close (callback) {
    callback()
  }

  start (device, callback) {
    setInterval(() => measureBrightness(4)
      .then(brightness => this.emit('message', {
        devices: ['*'], // Send to all flows the device is in
        topic: 'value-changed',
        payload: {
          brightness
        }
      }))
    , 1000)

    callback()
  }
}

module.exports = Connector
