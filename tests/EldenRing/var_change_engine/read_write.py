"""

This requires the use of the cheat engine tutorial, step 8.

"""

from src.EldenRing.var_change_engine.engine import MemoryAuthor
from ctypes import *
import time


def main():
    base_address = 0x100000000  # "Tutorial-i386.exe"
    static_address_offset = 0x325B00  # The offset from the base of the static address of the pointer chain
    process_name = 'Tutorial-x86_64.exe'
    offsets = [0x10, 0x18, 0x00, 0x18]

    author = MemoryAuthor(process_name, base_address, static_address_offset, offsets)
    print(author.read())

    while True:
        author.write(c_uint32(5000))
        time.sleep(0.01)


if __name__ == "__main__":
    main()
