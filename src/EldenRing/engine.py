import time

from restart_fight.reset import Reset
from config import SOURCE_DIRECTORY, DESTINATION_DIRECTORY, STATE_NAME, STATE_NUMBER

if __name__ == '__main__':
    time.sleep(10)
    reset_boss = Reset(SOURCE_DIRECTORY, DESTINATION_DIRECTORY, STATE_NAME, STATE_NUMBER)
    reset_boss.exit_to_main_menu()
    time.sleep(5)  # waits for game to get to menu before replacing state
    reset_boss.reset_save()
    time.sleep(8)
    reset_boss.load_save()
    time.sleep(8)
    reset_boss.start_boss()
