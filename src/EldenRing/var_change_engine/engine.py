from pymem import *
from pymem.ptypes import RemotePointer


class MemoryAuthor:
    def __init__(self, base_address, offsets, process_name='eldenring.exe', handle=None):
        self.base_address = base_address
        self.mem = Pymem(process_name)  # Opens process and address
        self.address = None
        _ = self.get_pointer_addr(offsets)  # Retrieves Static Address of desired function

    # This takes care of all steps for finding variable in memory; assumes 64 bit
    def get_pointer_addr(self, offsets):
        addr = RemotePointer(self.mem.process_handle, self.base_address)
        for offset in offsets:
            if offset != offsets[-1]:
                addr = RemotePointer(self.mem.process_handle, addr + offset)
        addr = addr.value + offsets[-1]
        self.address = addr
        return addr

    # Reads value of designated variable in memory
    def read(self):
        out = self.mem.read_int(self.address)
        return out

    # Writes value to designated variable in memory; must typecast prior to being input; c_uint32() works in tutorial
    def write(self, value):
        if isinstance(value, int):
            self.mem.write_int(self.address, value)
        elif isinstance(value, float):
            self.mem.write_float(self.address, value)


if __name__ == "__main__":
    from src.EldenRing.restart_fight.config import boss_flag_pointer, boss_addr

    base_address = boss_flag_pointer
    # The offset from the base of the static address of the pointer chain
    process_name = 'eldenring.exe'
    offsets = boss_addr["Margit, the Fell Omen"]["flag_offsets"]
    flags = boss_addr["Margit, the Fell Omen"]["flag"]
    boss_alive = flags["alive"]
    boss_dead = flags["dead"]

    author = MemoryAuthor(base_address, offsets)

    print(author.read())
