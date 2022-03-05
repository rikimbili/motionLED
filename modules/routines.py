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
    fadeLED("color", tupleToDictRGB(RED1), 0.5)
    fadeLED("brightness", MAX_BRIGHTNESS, 0.5)
    sleep(5 * 60)
    fadeLED("brightness", curr_brightness, 0.5)
    fadeLED("color", curr_color, 0.5)