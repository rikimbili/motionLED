import modules.constants.color_constants as color  # Stores different color constants as tuples
import datetime
import sys
import threading
from modules.request_handler import *  # Local module file
from modules.state_changer import *  # Local module file
from gpiozero import MotionSensor
from time import sleep


# Set up the motion sensor on GPIO_PIN
pir: MotionSensor = MotionSensor(constants.GPIO_PIN)

# LED Power state: This global variable is used to keep track of the LED power state
led_on: bool = getStateLED().json()["data"]["properties"][1]["powerState"] == "on"


def setStateFromMotionLED() -> None:
    """
    Sets the LED "on" or "off" state based on the pir sensor reading

    :return: None
    """
    global led_on

    while True:
        # False positive threshold: Check each second in range if motion is detected
        for i in range(constants.MOTION_DETECT_THRESHOLD):
            if pir.motion_detected:
                break
            sleep(1)

        if pir.motion_detected:
            print(datetime.datetime.now().strftime("%X"), ": Motion detected!")
            if not led_on:
                setLED("turn", "on")
                led_on = True
            pir.wait_for_no_motion()
        else:
            print(datetime.datetime.now().strftime("%X"), ": No motion detected!")
            if led_on:
                setLED("turn", "off")
                led_on = False
            pir.wait_for_motion()


def main():
    motion_state_t = threading.Thread(target=setStateFromMotionLED, daemon=True)
    motion_state_t.start()
    motion_state_t.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting...")
        sys.exit(0)
