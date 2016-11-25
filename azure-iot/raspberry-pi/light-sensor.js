'use strict'

// Ref. https://www.scribd.com/document/193892647/RaspberryPi-Analogue-Input-with-Capacitor-node-js
// Ref. http://www.raspberrypi-spy.co.uk/2012/08/reading-analogue-sensors-with-one-gpio-pin/
// Ref. https://github.com/RPi-Distro/python-gpiozero/blob/f607a27c79404657f777687165ec4f6e2f205a11/gpiozero/input_devices.py
let test = 0
function measureBrightness(pin) {
  return new Promise((resolve, reject) => {
    test = (test + 1) % 11
    resolve(Math.min(1.0, Math.max(0.0, test / 10.0)))
  })

  // If the capacitor takes longer than this time (in ms) to charge, it is assumed to be dark.
  const chargeTimeLimit = 10

  return Promise((resolve, reject) => {
    // Open the sensor pin as output
    let sensor = new Gpio(pin, 'out')
    // Ground the sensor pin
    sensor.write(0)
    // Wait 0.1s to drain the capacitor
    sleep.usleep(100000)

    // Re-open the sensor pin as input port, enabling interrupts at rising edge
    sensor = new Gpio(pin, 'in', 'rising')

    function risingEdgeCallback(err, value) {
      // Calculate the time the capacitor needed to be charged
      const timeDiff = startTime - hrtime()
      // Clear the listener
      sensor.unwatch(risingEdgeCallback)
      // Map the charge time lineary onto the interval [0, 1]
      resolve(1.0 - Math.min(chargeTimeLimit, timeDiff) / chargeTimeLimit)
    }

    // Install a listener for the rising edge
    sensor.watch(risingEdgeCallback)
    // Store the timestamp at when we started waiting fot the rising edge
    const startTime = hrtime()
  })
}

module.exports = { measureBrightness }
