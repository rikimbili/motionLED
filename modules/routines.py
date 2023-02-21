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
        sleep(15)

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
    time_asleep = 0  # Minutes
    while getPowerStateLED() is False:
        sleep(60)
        time_asleep += 1

    # If more than 6 hours pass from the end of day, don't change the brightness
    if time_asleep > 6 * 60:
        return

    print("Running day to night routine...")
    fadeBrightnessLED(MIN_BRIGHTNESS, 20)


def nightToDayRoutine() -> None:
    """
    Changes the LED brightness depending on the time of day
    """
    time_asleep = 0  # Minutes
    while getPowerStateLED() is False:
        sleep(60)
        time_asleep += 1

    # If more than 6 hours pass from the start of day, don't change the brightness
    if time_asleep > 6 * 60:
        return

    print("Running night to day routine...")
    fadeBrightnessLED(MAX_BRIGHTNESS, 20)
