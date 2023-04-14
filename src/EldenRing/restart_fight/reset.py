import os
import shutil
import pydirectinput
import time


class Reset:
    def __init__(self, source_directory, destination_directory, state_name, state_number):
        self.SOURCE_STATE = os.path.join(source_directory, state_name).replace('\\', '/')
        self.DESTINATION_STATE = os.path.join(destination_directory, state_name).replace('\\', '/')
        self.STATE_NUMBER = state_number

    # exits to main menu, so that we can reload at desired save state
    @staticmethod
    def exit_to_main_menu():
        pydirectinput.press('esc')
        pydirectinput.press('up')
        pydirectinput.press('e')
        pydirectinput.press('z')
        pydirectinput.press('e')
        pydirectinput.press('left')
        pydirectinput.press('e')

    # replaces save state with desired state
    def reset_save(self):
        shutil.copyfile(self.SOURCE_STATE, self.DESTINATION_STATE)

    # loads up replaced state; For Elden Ring, we simply click continue
    def load_save(self):
        pydirectinput.press('enter')
        time.sleep(1)
        pydirectinput.press('e')
        """
        pydirectinput.press('down')
        pydirectinput.press('enter')
        time.sleep(1)
        for i in range(self.STATE_NUMBER):
            pydirectinput.press('down')
        pydirectinput.press('enter')
        """

    # enter boss fog, open door, etc.
    @staticmethod
    def start_boss():
        pydirectinput.keyDown('w')
        time.sleep(2)
        pydirectinput.keyUp('w')
        pydirectinput.press('up')
