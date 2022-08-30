from .utilities import tupleToDictRGB
from .constants.color_constants import *
from .constants.constants import MAX_BRIGHTNESS
from .request_handler import *
from .state_changer import fadeBrightnessLED


def wakeUpRoutine() -> None:
    """
    Set LED to color red for 10 minutes, then reverts to previous color
    This feature is based on this study: https://www.nature.com/articles/s41598-021-02311-1
    """
    while getPowerStateLED() is False:
        sleep(5)

    # Set and Keep the LED set to color red for 10 mins
    print("Running wake up routine...")
    curr_color = getColorStateLED()
    setLED("color", tupleToDictRGB(RED1))
    sleep(10 * 60)
    setLED("color", curr_color)


def dayToNightRoutine() -> None:
    """
    Changes the LED brightness depending on the time of day
    """
    print("Running day to night routine...")
    if getPowerStateLED() is False:
        setLED("brightness", MIN_BRIGHTNESS)
        setLED("turn", "off")
    else:
        fadeBrightnessLED(MIN_BRIGHTNESS, 20)


def nightToDayRoutine() -> None:
    """
    Changes the LED brightness depending on the time of day
    """
    print("Running night to day routine...")
    if getPowerStateLED() is False:
        setLED("brightness", MAX_BRIGHTNESS)
        setLED("turn", "off")
    else:
        fadeBrightnessLED(MAX_BRIGHTNESS, 20)
