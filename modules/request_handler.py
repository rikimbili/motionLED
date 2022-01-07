"""
Govee API requests handling module
"""
import requests
from .constants import constants  # Local constants file
from time import sleep


def handleRateLimit(r: requests.Response) -> None:
    """
    Handles the rate limit for the Govee API by sleeping for the time remaining
    :param response r: request response object
    :return: None
    """
    if r.status_code == 429:
        sleep_time = ""
        for s in r.text:
            if s.isdigit():
                sleep_time += s
        sleep(int(sleep_time) + 1)


def setLED(name: str, value) -> requests.Response:
    """
    Sets the LED state based on the name and value parameters passed
    :param str name: name of the command (Eg. turn, brightness, color, colorTem)
    :param value: value of the command
    :return: request response object
    :raises RequestException: If the request fails for any reason
    """
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
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Request Exception:", e)
        handleRateLimit(r)

    return r


def getStateLED() -> requests.Response:
    """
    Returns the state of the LED
    :return: request response object
    :raises RequestException: If the request fails for any reason
    """
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
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Request Exception:", e)
        handleRateLimit(r)

    return r
