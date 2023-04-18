import time
from src.EldenRing.restart_fight.reset import Reset
from src.EldenRing.restart_fight.config import SOURCE_DIR, DESTINATION_DIR, STATE_NAME, STATE_NUMBER

import vgamepad as vg

gamepad = vg.VX360Gamepad()

# Make sure Elden Ring is open in a state different from the replacing save state
restart_object = Reset(SOURCE_DIR, DESTINATION_DIR, STATE_NAME, gamepad)
time.sleep(15)  # Gives time to reopen EldenRing
restart_object.restart_boss()
