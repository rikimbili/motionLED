# motionLED
motionLED is a small program that aims to automate the control of Govee LEDs(Light strips) through motion detection using a PIR sensor attached to a Raspberry Pi 4
![alt text](https://i.imgur.com/PRnKKXI.jpeg)
## Features
So far, only a handful of features are implemented:
* Automatically turn off/on LED based on readings from the PIR sensor
* Functions that make http requests to GoveeAPI in order to control/get data from the LEDs
* Functions that change the state of the LEDs(power on or off, brightness and rgb color) using a fade/merge animation

Currently, the functions that add animation are not used in the main function as I'm still thinking on ways to use those 
(like changing color at a certain hour or when a certain condition is met)

## Usage
### Requirements before you set it up
* Your LED strip must be on and connected to a wifi router (it doesn't have to be the same wifi as the raspberry pi)
* Make sure you have the latest Python 3 version and are running Raspbian 10 or 11 (not necessary but that is what I'm running)
* You will also need a Govee API key. You can get it through the mobile app as shown [here](https://twitter.com/goveeofficial/status/1383962664217444353)

### Steps to setup the constants file
1. Create a constants.py file in ./modules/constants/
2. Add these constants and fill out the rest based on your specific LED strip
```
SERVER_URL_PUT = "https://developer-api.govee.com/v1/devices/control"
SERVER_URL_GET = "https://developer-api.govee.com/v1/devices"
SERVER_URL_STATE = "https://developer-api.govee.com/v1/devices/state"
GOVEE_API_KEY = "YOUR API KEY HERE"
LED_DEVICE = "YOUR DEVICE ID HERE"
LED_MODEL = "YOUR DEVICE MODEL HERE"
```

Lastly, just run the python script by running the main file
> python motion_led.py
