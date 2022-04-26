from .utilities import tupleToDictRGB
from .constants.color_constants import *  # Local constants file
from .constants.constants import MAX_BRIGHTNESS  # Local constants file
from .request_handler import *  # Local module file
from .state_changer import fadeLED  # Local constants file


def wakeUpRoutine() -> None:
    """
    Set LED to color red for 10 minutes, then reverts to previous color
    This feature is based on this study: https://www.nature.com/articles/s41598-021-02311-1

    :return: None
    """
    while getPowerStateLED() is False:
        sleep(5)

    curr_color = getColorStateLED()
    curr_brightness = getBrightnessStateLED()

    # Set and Keep the LED set to color red for 10 mins
    setLED("color", tupleToDictRGB(RED1))
    setLED("brightness", MAX_BRIGHTNESS)
    sleep(5 * 60)
    setLED("brightness", curr_brightness)
    setLED("color", curr_color)
