import os
import shutil
# import pydirectinput
import time
import vgamepad as vg
# from src.EldenRing.restart_fight.util import press_and_release


class Reset:
    def __init__(self, source_directory, destination_directory, state_name, controller):
        self.SOURCE_STATE = os.path.join(source_directory, state_name).replace('\\', '/')
        self.DESTINATION_STATE = os.path.join(destination_directory, state_name).replace('\\', '/')
        self.gamepad = controller

    def restart_boss(self):
        self.exit_to_main_menu()
        time.sleep(20)
        self.reset_save()
        self.load_save()
        time.sleep(15)
        self.start_boss()

    # exits to main menu, so that we can reload at desired save state
    def exit_to_main_menu(self):
        self.press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        self.press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        self.press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        self.press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        self.press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        self.press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)

    # replaces save state with desired state
    def reset_save(self):
        shutil.copyfile(self.SOURCE_STATE, self.DESTINATION_STATE)

    # loads up replaced state; For Elden Ring, we simply click continue
    def load_save(self):
        self.press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        time.sleep(2)
        self.press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)

    # enter boss fog, open door, etc.
    def start_boss(self):
        self.gamepad.left_joystick_float(x_value_float=0, y_value_float=1.0)
        self.gamepad.update()
        time.sleep(2)
        self.gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        self.gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
        self.gamepad.update()
        time.sleep(0.1)
        self.gamepad.reset()

    def press_and_release(self, button):
        time.sleep(0.1)
        self.gamepad.press_button(button=button)
        self.gamepad.update()
        time.sleep(0.1)
        self.gamepad.release_button(button=button)
        self.gamepad.update()
