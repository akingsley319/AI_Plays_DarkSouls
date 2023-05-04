import time
import pydirectinput

from src.EldenRing.var_change_engine.engine import MemoryAuthor
from src.EldenRing.restart_fight.config import warp_pointer, camera_pointer


def press_and_release(button):
    time.sleep(0.1)
    pydirectinput.press(button)
    time.sleep(0.1)


def teleport(base_address, location_dict):
    # Orders the coordinates and the offsets which they are stored from
    coordinates = [[location_dict["map_id"]], location_dict["chunk"],
                   location_dict["character"], location_dict["camera"]]
    offsets = [[location_dict["map_id_offsets"]], location_dict["chunk_offsets"],
               location_dict["character_offsets"], location_dict["camera_offsets"]]
    coordinates = [coord for grouping in coordinates for coord in grouping]
    offsets = [offset_list for grouping in offsets for offset_list in grouping]

    # Camera is on different base pointer address, so we add the length of the coords that appear prior
    not_camera_index = len([location_dict["map_id"]]) + len(location_dict["chunk"]) + len(location_dict["character"])

    for i in range(len(coordinates)):
        # if i == 1 or (i == len(location_dict["chunk"]) + 1):
        #     time.sleep(2.0)
        # if i == 0:
        #     continue
        if i < not_camera_index:
            time.sleep(0.1)
            author = MemoryAuthor(warp_pointer, offsets[i])
        else:
            author = MemoryAuthor(camera_pointer, offsets[i])
        author.write(coordinates[i])
