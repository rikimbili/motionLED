"""
Govee API requests handling module
"""
import requests

from .utilities import tupleToDictRGB
from .constants.constants import *  # Local constants file
from .constants.color_constants import *  # Local constants file
from time import sleep


def setLED(name: str, value, error_delay=REQUEST_ERROR_SLEEP_TIME) -> requests.Response:
    """
    Sets the LED state specified by command name and value

    :param str name: Name of the command (Eg. turn, brightness, color, colorTem)
    :param value: Value of the command
    :param float error_delay: Time to wait if a request error occurs
    :return: Request response object
    :raises RequestException: If the request fails for any reason
    """
    try:
        r = requests.put(
            SERVER_URL_PUT,
            headers={
                "Govee-API-Key": GOVEE_API_KEY,
            },
            json={
                "device": LED_DEVICE,
                "model": LED_MODEL,
                "cmd": {"name": name, "value": value},
            },
        )
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"{e}\n Sleeping for {error_delay} seconds and Retrying...")
        sleep(error_delay)
        return setLED(name, value, error_delay)

    return r


def getStateLED(error_delay=REQUEST_ERROR_SLEEP_TIME) -> requests.Response:
    """
    Returns the state of the LED

    :param float error_delay: Time to wait if a request error occurs
    :return: Request response object
    :raises RequestException: If the request fails for any reason
    """
    try:
        r = requests.get(
            SERVER_URL_STATE,
            headers={
                "Govee-API-Key": GOVEE_API_KEY,
            },
            params={
                "device": LED_DEVICE,
                "model": LED_MODEL,
            },
        )
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"{e}\n Sleeping for {error_delay} seconds and Retrying...")
        sleep(error_delay)
        return getStateLED(error_delay)

    return r


def getBrightnessStateLED() -> int:
    """
    Gets the current brightness of the LED

    :return: Brightness of the LED
    """
    return getStateLED().json()["data"]["properties"][2]["brightness"]


def getColorStateLED() -> dict:
    """
    Gets the current color RGB value of the LED

    :return: dict of rgb values for the current color
    """
    color = getStateLED().json()["data"]["properties"][3]

    if color.get("colorTemInKelvin") is not None:
        color = KELVIN_TABLE.get(color["colorTemInKelvin"])
        return tupleToDictRGB(color)
    elif color.get("color") is not None:
        return color["color"]
    else:
        print("Unknown LED color key")
        return None


def getPowerStateLED() -> bool:
    """
    Gets the power state of the LED

    :return: True if the LED is on, False if the LED is off
    """
    return getStateLED().json()["data"]["properties"][1]["powerState"] == "on"
