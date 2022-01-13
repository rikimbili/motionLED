from .utilities import rgbToJson
from .request_handler import *  # Local module file
from .constants.color_constants import *  # Contains different color constants as tuples
from .constants.constants import MAX_BRIGHTNESS

# TODO: Awaiting fix in request_handler
def wakeUpRoutine() -> None:
    """
    Set LED to color red for 20 minutes, then revert to previous color
    This feature is based on this study: https://www.nature.com/articles/s41598-021-02311-1

    :return: None
    """
    curr_color = getColorStateLED()

    setLED("color", rgbToJson(RED1))
    sleep(20 * 60)  # Sleep for 20 minutes

    setLED("color", rgbToJson(curr_color))
