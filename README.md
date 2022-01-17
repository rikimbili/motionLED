# motionLED
motionLED is a small program that aims to automate the control of Govee LEDs (Light strips) through motion detection using a PIR sensor attached to a Raspberry Pi 4
![alt text](https://i.imgur.com/BCDY754.png)
## Features
So far, a handful of features are implemented:
* Automatically turn off/on LED based on readings from the PIR sensor
* Routines to change the LED state at specified intervals/times/dates
* Functions that make http requests to GoveeAPI in order to control/get data from the LEDs
* Functions that change the state of the LEDs (power on or off, brightness and rgb color) using a fade/merge animation

## Usage
### Requirements before you set it up
* The LED strip must be powered and connected to a wifi router. Note: It doesn't have to be the same router as the raspberry pi, as long as both are connected to the internet, the request will go through
* Raspbian 10 (Buster) or 11 (Bullseye) and at least Python 3.9 
* A Govee API key. You can get it through the mobile app as shown [here](https://twitter.com/goveeofficial/status/1383962664217444353)
* Know the GPIO Pin you connected your pir sensor to (I recommend GPIO 17). If you are not sure take a look at the [pinout](https://pinout.xyz)
* Install every module dependency in requirements.txt 

### Steps to setup the constants file
1. Create a constants.py file in ./modules/constants/
2. Add these constants and fill out the rest based on your specific setup
```
SERVER_URL_PUT = "https://developer-api.govee.com/v1/devices/control"
SERVER_URL_GET = "https://developer-api.govee.com/v1/devices"
SERVER_URL_STATE = "https://developer-api.govee.com/v1/devices/state"
GOVEE_API_KEY = "[YOUR_API_KEY_HERE]"
LED_DEVICE = "[YOUR_DEVICE_ID_HERE]"
LED_MODEL = "[YOUR_DEVICE_MODEL_HERE]"
GPIO_PIN = [YOUR_GPIO_PIN_HERE]
MOTION_DETECT_THRESHOLD = 180  # Seconds to wait to avoid false positives
REQUEST_ERROR_SLEEP_TIME = 15  # Seconds to wait if an API error occurs
WAKE_UP_TIME = "08:00"  # Your personal wake up time for the routines
MAX_BRIGHTNESS = 90  # Max brightness (Percentage) that the LED can reach
```
Lastly, just run the python script by running the main file on your terminal ```python motion_led.py```
