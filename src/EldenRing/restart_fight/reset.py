import os
import shutil
import pydirectinput
import time
from src.EldenRing.restart_fight.config import SOURCE_DIR, DESTINATION_DIR, STATE_NAME
from src.EldenRing.restart_fight.util import press_and_release, teleport

from src.EldenRing.var_change_engine.engine import MemoryAuthor
from src.EldenRing.restart_fight.config import boss_addr, boss_flag_pointer


class Reset:
    def __init__(self, boss_name,  source_directory=SOURCE_DIR,
                        destination_directory=DESTINATION_DIR, state_name=STATE_NAME):
        self.SOURCE_STATE = os.path.join(source_directory, state_name).replace('\\', '/')
        self.DESTINATION_STATE = os.path.join(destination_directory, state_name).replace('\\', '/')

        self.boss_name = boss_name
        self.author = MemoryAuthor(boss_flag_pointer, boss_addr[self.boss_name]["flag_offsets"])

    # checks if boss is dead
    def is_game_over(self):
        death_flag = boss_addr[self.boss_name]["flag"]["dead"]
        return self.author.read() == death_flag

    # Fully resets desired boss: reset flag, reset area, teleport to boss, enter fight
    def restart_boss(self):
        self.reset_boss_flag()
        time.sleep(1.0)
        self.reset_area()
        time.sleep(1.0)
        self.start_boss()

    # Will set the boss flag to "alive", resetting the boss if dead (requires area reset to take effect
    def reset_boss_flag(self):
        alive_flag = boss_addr[self.boss_name]["flag"]["alive"]
        self.author.write(alive_flag)

    # Reloads the area, allowing boss to spawn back in if dead
    def reset_area(self):
        # Teleport to site of grace
        grace_location = boss_addr[self.boss_name]["grace_location"]
        teleport(boss_flag_pointer, grace_location)
        # Sits at sight of grace and then gets up
        time.sleep(5.0)
        pydirectinput.keyDown("w")
        time.sleep(0.5)
        pydirectinput.keyUp("w")
        press_and_release("e")
        time.sleep(3.0)
        press_and_release("q")

    # Teleports to fog wall and enters the boss fight
    def start_boss(self):
        # Teleports to Fog Wall
        fog_wall_location = boss_addr[self.boss_name]["fog_wall_location"]
        teleport(boss_flag_pointer, fog_wall_location)
        # Enters boss arena
        time.sleep(1.0)
        pydirectinput.keyDown("w")
        time.sleep(1.0)
        pydirectinput.keyUp("w")
        press_and_release("e")

    """
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
    """