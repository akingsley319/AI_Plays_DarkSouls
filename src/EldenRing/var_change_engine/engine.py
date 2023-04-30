from src.EldenRing.var_change_engine.read_write import ProcessInterface
from ctypes import *


class MemoryAuthor:
    def __init__(self, process_name, base_address, static_address_offset, offsets=[]):
        self.base_address = base_address
        self.static_address_offset = static_address_offset
        # Opens the interface for this particular task
        self.process_interface = ProcessInterface()
        self.process_interface.open(process_name)
        # Offsets from base program address
        self.offsets = offsets
        # This is the final static address of the sought variable in memory
        self.final_step_address = self.find_final_step_address(self.base_address, self.static_address_offset)

    # This takes care of all steps for finding variable in memory; assumes 64 bit
    def find_final_step_address(self, base_address, static_address_offset):
        pointer_static_address = c_uint64(base_address + static_address_offset)
        step_pointer = c_uint64.from_buffer(
                self.process_interface.read_memory(
                    pointer_static_address, buffer_size=8
                )
            )
        highest_index = len(self.offsets) - 1
        for i in range(len(self.offsets)):
            if i < highest_index:
                step_pointer = c_uint64.from_buffer(
                    self.process_interface.read_memory(
                        (step_pointer.value + self.offsets[i]), buffer_size=8
                    )
                )
            else:
                step_pointer = step_pointer.value + self.offsets[i]
        return step_pointer

    # Reads value of designated variable in memory
    def read(self):
        out = c_uint32.from_buffer((self.process_interface.read_memory(self.final_step_address))).value
        return out

    # Writes value to designated variable in memory; must typecast prior to being input; c_uint32() works in tutorial
    def write(self, value):
        self.final_step_address = self.find_final_step_address(self.base_address, self.static_address_offset)
        self.process_interface.write_memory(self.final_step_address, value)


