"""
LED state changer module
"""
import requests
from .request_handler import *  # Local module file
from .utilities import tupleToDictRGB  # Local module file
from time import sleep


def fadeColorLED(rgb_value: tuple, delay: float = 0.2) -> requests.Response or None:
    """
    Fades the LED from current color into the passed color

    :param tuple rgb_value: RGB value to change color to
    :param float delay: delay between API requests in seconds (Recommended: 0.2 or higher)
    :return: request response object from last request or None if no request is made
    """
    curr_color = getColorStateLED()
    curr_color = [curr_color["r"], curr_color["g"], curr_color["b"]]
    new_color = [rgb_value["r"], rgb_value["g"], rgb_value["b"]]

    if new_color == curr_color:
        return None

    # If the LED is off, just set the color without fading
    if not getPowerStateLED():
        return setLED("color", tupleToDictRGB(new_color))

    # Calculate the maximum R, G, or B difference between the current and new color
    max_diff = max(
        abs(new_color[0] - curr_color[0]),
        abs(new_color[1] - curr_color[1]),
        abs(new_color[2] - curr_color[2]),
    )
    # Change the current color values by a stepping of 1 at a time until curr_color == new_color
    for i in range(max_diff):
        for j in range(3):
            if curr_color[j] > new_color[j]:
                curr_color[j] -= 1
            elif curr_color[j] < new_color[j]:
                curr_color[j] += 1

        last_r = setLED("color", tupleToDictRGB(curr_color))
        sleep(delay)

    return last_r


def fadeBrightnessLED(value: int, delay: float = 0.2) -> requests.Response or None:
    """
    Fades the LED from current brightness into the passed one

    :param int value: Brightness value to change to
    :param float delay: Delay between API requests in seconds (Recommended: 0.2 or higher)
    :return: Request response object from last request or None if no request is made
    """
    initial = getBrightnessStateLED()
    final = value

    if initial == final:
        return None

    # If the LED is off, just set the brightness without fading
    if not getPowerStateLED():
        return setLED("brightness", final)

    if final > initial:
        for i in range(initial, final + 1):
            setLED("brightness", i)
            sleep(delay)
    else:
        for i in range(initial, final - 1, -1):
            setLED("brightness", i)
            sleep(delay)


# TODO: Fix sudden brightness change when turn command is used
def fadeLED(name: str, value, delay: float = 0.2) -> requests.Response or None:
    """
    Attempts to animate the LED as it transitions from one state to another

    :param str name: Name of the command (turn, brightness, color)
    :param value: Value of the command or RGB value as a tuple
    :param float delay: Delay between API requests in seconds (Recommended: 0.2 or higher)
    :return: Request response object or None if no request is made
    """
    led_data = getStateLED().json()
    power_state = led_data["data"]["properties"][1]["powerState"]
    curr_brightness = led_data["data"]["properties"][2]["brightness"]

    if name == "turn":
        if value == "on" and power_state == "off":
            setLED("brightness", 1)
            sleep(delay)
            led_data["data"]["properties"][2]["brightness"] = 1
            setLED("turn", "on")
            sleep(delay)
            led_data["data"]["properties"][1]["powerState"] = "on"
            return fadeBrightnessLED(curr_brightness, delay)
        elif value == "off" and power_state == "on":
            fadeBrightnessLED(1, delay)
            setLED("turn", "off")
            sleep(delay)
            return setLED("brightness", curr_brightness)

    elif name == "brightness":
        return fadeBrightnessLED(value, delay)

    elif name == "color":
        return fadeColorLED(value, delay)

    else:
        return None
