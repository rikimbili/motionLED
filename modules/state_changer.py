"""
LED state changer module
"""
import requests
from .request_handler import setLED, getStateLED  # Local module file
from .utilities import rgbToJson  # Local module file
from time import sleep

# TODO: Fix 'colorTemInKelvin' property being replaced for 'color' on specific color changes
def fadeColorLED(
    rgb_value: tuple, led_data: dict, delay: float = 0.2
) -> requests.Response or None:
    """
    Fades the LED from current color into the passed color
    :param tuple rgb_value: RGB value to change color to
    :param dict led_data: JSON object of the LED state
    :param float delay: delay between API requests in seconds (Recommended: 0.2 or higher)
    :return: request response object from last request or None if no request is made
    """
    new_color = [rgb_value[0], rgb_value[1], rgb_value[2]]
    curr_color = led_data["data"]["properties"][3]["color"]
    curr_color = [curr_color["r"], curr_color["g"], curr_color["b"]]

    if new_color == curr_color:
        return None

    if led_data["data"]["properties"][1]["powerState"] == "off":
        return setLED("color", rgbToJson(new_color))

    # Calculate the maximum R, G, or B difference between the current and new color
    max_diff = max(
        abs(new_color[0] - curr_color[0]),
        abs(new_color[1] - curr_color[1]),
        abs(new_color[2] - curr_color[2]),
    )
    # Change the current color values by a stepping of 2 at a time until curr_color == new_color
    for i in range(max_diff):
        for j in range(3):
            if curr_color[j] > new_color[j]:
                curr_color[j] -= 1
            elif curr_color[j] < new_color[j]:
                curr_color[j] += 1

        last_r = setLED("color", rgbToJson(curr_color))
        sleep(delay)

    return last_r


def fadeBrightnessLED(
    value: int, led_data: dict, delay: float = 0.2
) -> requests.Response or None:
    """
    Fades the LED from current brightness into the passed one
    :param int value: brightness value to change to
    :param dict led_data: JSON object of the LED state
    :param float delay: delay between API requests in seconds (Recommended: 0.2 or higher)
    :return: request response object from last request or None if no request is made
    """
    initial = led_data["data"]["properties"][2]["brightness"]
    final = value

    if initial == final:
        return None

    if led_data["data"]["properties"][1]["powerState"] == "off":
        return setLED("brightness", final)

    if final > initial:
        for i in range(initial, final):
            setLED("brightness", i)
            sleep(delay)
    else:
        for i in range(initial, final, -1):
            setLED("brightness", i)
            sleep(delay)


# TODO: Fix sudden brightness change when turn command is used
def fadeLED(name: str, value, delay: float = 0.2) -> requests.Response or None:
    """
    Attempts to animate the LED as it transitions from one state to another
    :param str name: name of the command (turn, brightness, color)
    :param value: value of the command or RGB value as a tuple
    :param float delay: delay between API requests in seconds (Recommended: 0.2 or higher)
    :return: request response object or None if no request is made
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
            return fadeBrightnessLED(curr_brightness, led_data, delay)
        elif value == "off" and power_state == "on":
            fadeBrightnessLED(1, led_data, delay)
            setLED("turn", "off")
            sleep(delay)
            return setLED("brightness", curr_brightness)

    elif name == "brightness":
        return fadeBrightnessLED(value, led_data, delay)

    elif name == "color":
        return fadeColorLED(value, led_data, delay)

    else:
        return None
