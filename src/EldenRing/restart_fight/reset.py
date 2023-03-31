import os
import shutil
import pydirectinput

import time
from EldenRing.restart_fight.config import SOURCE_DIRECTORY, DESTINATION_DIRECTORY, STATE_NAME, STATE_NUMBER, \
                                           BACKUP_STATE_NAME


class Reset:
    def __init__(self, source_directory, destination_directory, state_name, state_number, backup_name):
        self.SOURCE_STATE = os.path.join(source_directory, state_name).replace('\\', '/')
        self.BACKUP_SOURCE = os.path.join(source_directory, backup_name).replace('\\', '/')
        if backup_name is not None:
            self.DESTINATION_STATE = os.path.join(destination_directory, state_name).replace('\\', '/')
            self.BACKUP_DESTINATION = os.path.join(destination_directory, backup_name).replace('\\', '/')
        self.STATE_NUMBER = state_number

    # exits to main menu, so that we can reload at desired save state
    @staticmethod
    def exit_to_main_menu():
        pydirectinput.press('end')
        pydirectinput.press('left')
        pydirectinput.press('enter')
        pydirectinput.press('up')
        pydirectinput.press('enter')
        pydirectinput.press('left')
        pydirectinput.press('enter')

    # replaces save state with desired state
    def reset_save(self):
        shutil.copy(self.SOURCE_STATE, self.DESTINATION_STATE)
        if self.BACKUP_SOURCE:
            shutil.copy(self.BACKUP_SOURCE, self.BACKUP_DESTINATION)

    # loads up replaced state
    def load_save(self):
        pydirectinput.press('enter')
        pydirectinput.press('enter')
        time.sleep(1)
        for i in range(self.STATE_NUMBER):
            pydirectinput.press('down')
        pydirectinput.press('enter')

    # enter boss fog, open door, etc.
    @staticmethod
    def start_boss():
        pydirectinput.press('enter')


if __name__ == '__main__':
    time.sleep(10)
    reset_boss = Reset(SOURCE_DIRECTORY, DESTINATION_DIRECTORY, STATE_NAME, STATE_NUMBER, BACKUP_STATE_NAME)
    reset_boss.exit_to_main_menu()
    time.sleep(2)  # waits for game to get to menu before replacing state
    reset_boss.reset_save()
    reset_boss.load_save()
    time.sleep(5)
    reset_boss.start_boss()
