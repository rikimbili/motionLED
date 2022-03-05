import modules.constants.color_constants as color  # Contains different color constants as tuples
import datetime
import schedule
import sys
import threading
from modules.constants.constants import *  # Local constants file
from modules.request_handler import *  # Local module file
from modules.routines import *  # Local module file
from modules.state_changer import *  # Local module file
from gpiozero import MotionSensor
from time import sleep


# Set up the motion sensor on GPIO_PIN
pir: MotionSensor = MotionSensor(GPIO_PIN)


def setStateFromMotionLED() -> None:
    """
    Sets the LED "on" or "off" state based on the pir sensor reading

    :return: None
    """
    lastState: bool = False  # Last state of the motion sensor, on or off

    while True:
        # False positive threshold: Check each second in range if motion is detected
        for i in range(MOTION_DETECT_THRESHOLD):
            if pir.motion_detected:
                break
            sleep(1)

        if pir.motion_detected:
            # If the last motion sensor state was no motion detected, display the motion detected message
            if lastState is False:
                print(datetime.datetime.now().strftime("%X"), ": Motion detected!")

            lastState = True
            setLED("turn", "on")
            pir.wait_for_no_motion()
        elif not pir.motion_detected:
            print(datetime.datetime.now().strftime("%X"), ": No motion detected!")
            lastState = False
            setLED("turn", "off")
            pir.wait_for_motion()


def setStateFromRoutineLED() -> None:
    """
    Sets the LED state based on a schedule/routine

    :return: None
    """
    schedule.every().day.at(WAKE_UP_TIME).do(wakeUpRoutine)

    while True:
        schedule.run_pending()
        sleep(1)


def main():
    motion_state_t = threading.Thread(target=setStateFromMotionLED, daemon=True)
    motion_state_t.start()
    routine_t = threading.Thread(target=setStateFromRoutineLED, daemon=True)
    routine_t.start()
    routine_t.join()
    motion_state_t.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting...")
        sys.exit(0)
