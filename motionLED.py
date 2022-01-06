from gpiozero import MotionSensor
from time import sleep
import requests
import datetime

import constants

# Set up the motion sensor on GPIO 17
pir = MotionSensor(17)

# Turns on or off LED when called
## :param str name: name of the command (Eg. turn, brightness, color, colorTem)
## :param value: value of the command
## :return: request response object
def setLED(name: str, value) -> requests.Response:
    try:
        r = requests.put(
            constants.SERVER_URL_PUT,
            headers={
                "Govee-API-Key": constants.GOVEE_API_KEY,
            },
            json={
                "device": constants.LED_DEVICE,
                "model": constants.LED_MODEL,
                "cmd": {"name": name, "value": value},
            },
        )
    except requests.exceptions.RequestException as e:
        print(e)
        return None

    return r


# Returns the state of the LED
## :return: request response object
def getStateLED() -> requests.Response:
    try:
        r = requests.get(
            constants.SERVER_URL_STATE,
            headers={
                "Govee-API-Key": constants.GOVEE_API_KEY,
            },
            params={
                "device": constants.LED_DEVICE,
                "model": constants.LED_MODEL,
            },
        )
    except requests.exceptions.RequestException as e:
        print(e)
        return None

    return r


# Attempts to animate the LED from on to off to on or from one level of brightness to another
# The brightness stepping is 1 for every api_delay seconds
## :param str name: name of the command (turn, brightness)
## :param value: value of the command
## :param float api_delay: delay between API requests in seconds (Recommended: 0.1 or higher)
## :return: None if an invalid name parameter is passed
def fadeLED(name, value, api_delay: float):
    led_data = getStateLED().json()
    initial = led_data["data"]["properties"][2]["brightness"]

    if led_data["data"]["properties"][1]["powerState"] == "off" and (
        value == "on" or value > 0
    ):
        setLED("brightness", 1)
        setLED("turn", "on")

    if name == "turn":
        if value == "on":
            final = 0
        elif value == "off":
            final = initial
            initial = 0
    elif name == "brightness":
        final = value
    else:
        return None

    if final >= initial:
        for i in range(initial, final):
            setLED(name, i)
            print("Brightness: " + str(i))
            sleep(api_delay)
    else:
        for i in range(initial, final, -1):
            setLED(name, i)
            print("Brightness: " + str(i))

    if value == 0:
        setLED("turn", "off")


if __name__ == "__main__":
    while True:
        if pir.motion_detected:
            print(datetime.datetime.now().strftime("%X"), ": Motion detected!")
            setLED("turn", "on")
            pir.wait_for_no_motion()
        else:
            # False positive threshold: Check each second in range if motion is detected,
            # if so, continue and dont turn off the LED
            FP_flag = False
            for i in range(60):
                if pir.motion_detected:
                    print("False positive at " + str(i) + " seconds")
                    FP_flag = True  # Debugging
                    break
                sleep(1)
            if FP_flag:
                continue

            print(datetime.datetime.now().strftime("%X"), ": No motion detected!")
            setLED("turn", "off")
            pir.wait_for_motion()
