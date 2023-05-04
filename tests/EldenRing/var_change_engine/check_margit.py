"""

This requires Elden Ring open with EasyAntiCheat disabled

"""

from src.EldenRing.var_change_engine.engine import MemoryAuthor
from src.EldenRing.restart_fight.config import boss_addr, boss_flag_pointer

import time


def main():
    base_address = boss_flag_pointer
    # The offset from the base of the static address of the pointer chain
    process_name = 'eldenring.exe'
    offsets = boss_addr["Margit, the Fell Omen"]["flag_offsets"]
    flags = boss_addr["Margit, the Fell Omen"]["flag"]
    boss_alive = flags["alive"]
    boss_dead = flags["dead"]

    author = MemoryAuthor(base_address, offsets)

    author.write(boss_alive)
    print(list(flags.keys())[list(flags.values()).index(author.read())])
    time.sleep(2)
    author.write(boss_dead)
    print(list(flags.keys())[list(flags.values()).index(author.read())])
    time.sleep(2)
    author.write(boss_alive)
    print(list(flags.keys())[list(flags.values()).index(author.read())])


if __name__ == "__main__":
    print("Expect Results of 'alive', 'dead', 'alive' in that order with 2 second delay between result display.")
    print("The results are read from memory.")
    main()
