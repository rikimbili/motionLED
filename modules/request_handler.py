"""
Govee API requests handling module
"""
import requests
from .constants.constants import *  # Local constants file
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


def getPowerStateLED() -> bool:
    """
    Gets the power state of the LED

    :return: True if the LED is on, False if the LED is off
    """
    return getStateLED().json()["data"]["properties"][1]["powerState"] == "on"
