import modules.constants.color_constants as color  # Stores different color constants as tuples
import datetime
import sys
from modules.request_handler import *  # Local module file
from modules.state_changer import *  # Local module file
from gpiozero import MotionSensor
from time import sleep


def setStateFromMotionLED(pir: MotionSensor, led_on: bool) -> None:
    """
    Sets the LED state based on the motion sensor state
    :param MotionSensor pir: motion sensor object
    :param bool led_on: current state of the LED
    :return: None
    """
    while True:
        # False positive threshold: Check each second in range if motion is detected
        for i in range(180):
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
    # Set up the motion sensor on GPIO_PIN and get current power state of the LED
    pir: MotionSensor = MotionSensor(constants.GPIO_PIN)
    led_on: bool = getStateLED().json()["data"]["properties"][1]["powerState"] == "on"

    setStateFromMotionLED(pir, led_on)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting...")
        sys.exit(0)
