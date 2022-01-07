import modules.constants.color_constants as color  # Stores different color constants as tuples
import datetime
import sys
from modules.request_handler import *  # Local module file
from modules.state_changer import *  # Local module file
from gpiozero import MotionSensor
from time import sleep

# Set up the motion sensor on GPIO 17
pir = MotionSensor(17)


def main():
    while True:
        if pir.motion_detected:
            print(datetime.datetime.now().strftime("%X"), ": Motion detected!")
            setLED("turn", "on")
            fadeLED("color", color.AQUAMARINE1)
            pir.wait_for_no_motion()
        else:
            # False positive threshold: Check each second in range if motion is detected,
            # if so, continue and dont turn off the LED
            for i in range(100):
                if pir.motion_detected:
                    break
                sleep(1)
            if i < 99:
                continue

            print(datetime.datetime.now().strftime("%X"), ": No motion detected!")
            setLED("turn", "off")
            pir.wait_for_motion()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting...")
        sys.exit(0)
