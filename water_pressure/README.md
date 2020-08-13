The Water Pressure in our flat seemed to be a bit low from time to time.

To put measurements to feelings I decided to add a pressure sensor to our water installation and log the pressure over time.

![Setup](pics/sensor.png)

Because the Wemos only supports analog input up to 3.3V I needed an arduino that reads the pressure transducer.

The Arduino reads the voltage coming from the transducer, sends it via Serial Console to the ESP which is then publishing the measurement on a MQTT broker. 

# Parts List

## Electronics
* [Wemos D1 Mini](https://www.amazon.de/dp/B01N9RXGHY)
* [Arduino Nano v3](https://www.amazon.de/dp/B01MS7DUEM)
* [Pressure Transducer 1/4"](https://www.amazon.de/gp/product/B07GLHFCHR)

## Pipe Fittings
* [T-Piece 3/8"](https://www.db-shop24.de/T-Stueck-mit-Aussen-/Innen-/Innengewinde-Messing-vernickelt-3/8-Zoll)
* [Ball Valve](https://www.db-shop24.de/Minikugelhahn-langer-Griff-Innen-Aussengewinde-G-1-4-PN-15)
* Reducer piece 3/8" → 1/4"


