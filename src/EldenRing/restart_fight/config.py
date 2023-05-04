

# The locations of the save states and where Elden Ring draws the save files from
SOURCE_DIR = "D:/Documents/ai_plays_ds//resources/EldenRing/SaveStates/Margit"
DESTINATION_DIR = "C:/Users/cubs1/AppData/Roaming/EldenRing/76561198099506921"

# Name of the save files
STATE_NAME = "ER0000.sl2"

# How many spots down in load menu the desired saved character is
STATE_NUMBER = 6

# Offsets for boss health
boss_flag_pointer = 0x7FF7204BF238
warp_pointer = 0x7FF7204BCDD8
camera_pointer = 0x7FF71C7C0023
boss_addr = {
    "Margit, the Fell Omen": {
        "flag_offsets": [0x28, 0x151C39],
        "flag": {
            "alive": 223,
            "dead": 255
        },
        "grace_location": {
            "character": [4.421589375, 6.639990902, -3.283481121],  # Local Co-ords: X, Y, Z
            "character_offsets": [[0x10EF8, 0x0, 0x190, 0x68, 0x70],
                                  [0x10EF8, 0x0, 0x190, 0x68, 0x78],
                                  [0x10EF8, 0x0, 0x190, 0x68, 0x74]],
            "chunk": [-32.0, 8.0, 0.0],  # Chunk Co-ords: X, Y, Z
            "chunk_offsets": [[0x10EF8, 0x0, 0x190, 0x68, 0xA8, 0x18, 0xD0],
                              [0x10EF8, 0x0, 0x190, 0x68, 0xA8, 0x18, 0xD4],
                              [0x10EF8, 0x0, 0x190, 0x68, 0xA8, 0x18, 0xD8]],
            "map_id": 0x4211AFB5,  # Map to load in
            "map_id_offsets": [0x10EF8, 0x0, 0x6C0],
            "camera": [4.613502026,-3.280267477, 7.726156712, -3.087848425, 0.6788654327],  # X, Y, Z, Yaw, Pitch
            "camera_offsets": [[0x0],
                               [0x4],
                               [0x8],
                               [0xB4],
                               [0xB8]],
        },
        "fog_wall_location": {
            "character": [-9.283949852, -11.65603352, 0.5131742954],  # Local Co-ords: X, Y, Z
            "character_offsets": [[0x10EF8, 0x0, 0x190, 0x68, 0x70],
                                  [0x10EF8, 0x0, 0x190, 0x68, 0x78],
                                  [0x10EF8, 0x0, 0x190, 0x68, 0x74]],
            "chunk": [-32.0, 8.0, 0.0],  # Chunk Co-ords: X, Y, Z
            "chunk_offsets": [[0x10EF8, 0x0, 0x190, 0x68, 0xA8, 0x18, 0xD0],
                              [0x10EF8, 0x0, 0x190, 0x68, 0xA8, 0x18, 0xD4],
                              [0x10EF8, 0x0, 0x190, 0x68, 0xA8, 0x18, 0xD8]],
            "map_id": 0x41B5BA78,  # Map to load in
            "map_id_offsets": [0x10EF8, 0x0, 0x6C0],
            "camera": [-5.443279266, -0.1501506418, -11.24659443, -1.642549396, 0.03692962974],  # X, Y, Z, Yaw, Pitch
            "camera_offsets": [[0x0],
                               [0x4],
                               [0x8],
                               [0xB4],
                               [0xB8]]
        },
    },
    "Godrick the Grafted": {
        "flag_offsets": [0x28, 0x151C33],
        "flag": {
            "alive": 127,
            "dead": 255
        },
        "grace_location": {
            "character": [],
            "character_offsets": [],
            "camera": [],
            "camera_offsets": []
        },
        "fog_wall_location": {
            "character": [],
            "character_offsets": [],
            "camera": [],
            "camera_offsets": []
        },
    }
}
