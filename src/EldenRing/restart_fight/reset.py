import os
import shutil
import pydirectinput
import time
from src.EldenRing.restart_fight.config import SOURCE_DIR, DESTINATION_DIR, STATE_NAME
from src.EldenRing.restart_fight.util import press_and_release


class Reset:
    def __init__(self, source_directory=SOURCE_DIR,
                        destination_directory=DESTINATION_DIR, state_name=STATE_NAME):
        self.SOURCE_STATE = os.path.join(source_directory, state_name).replace('\\', '/')
        self.DESTINATION_STATE = os.path.join(destination_directory, state_name).replace('\\', '/')

    def restart_boss(self):
        self.exit_to_main_menu()
        time.sleep(20)
        self.reset_save()
        self.load_save()
        return time.time()

    # exits to main menu, so that we can reload at desired save state
    def exit_to_main_menu(self):
        press_and_release('esc')
        time.sleep(0.5)
        press_and_release('up')
        time.sleep(0.5)
        press_and_release('e')
        time.sleep(0.5)
        press_and_release('z')
        time.sleep(0.5)
        press_and_release('e')
        time.sleep(0.5)
        press_and_release('left')
        time.sleep(0.5)
        press_and_release('e')
        time.sleep(0.5)

    # replaces save state with desired state
    def reset_save(self):
        shutil.copyfile(self.SOURCE_STATE, self.DESTINATION_STATE)

    # loads up replaced state; For Elden Ring, we simply click continue
    def load_save(self):
        press_and_release('enter')
        time.sleep(2)
        press_and_release('e')

    # enter boss fog, open door, etc.
    def start_boss(self):
        pydirectinput.keyDown('w')
        time.sleep(1.8)
        pydirectinput.keyUp('w')
        press_and_release('e')
