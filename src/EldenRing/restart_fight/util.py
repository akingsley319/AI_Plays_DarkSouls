import time
import pydirectinput


def press_and_release(button):
    time.sleep(0.1)
    pydirectinput.press(button)
    time.sleep(0.1)
