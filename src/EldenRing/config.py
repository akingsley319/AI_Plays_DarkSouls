"""
Config file for all Elden Ring
"""

# Directory for boss save states and current save state location
SOURCE_DIRECTORY = "D:/Documents/ai_plays_ds/resources/EldenRing/SaveStates"
DESTINATION_DIRECTORY = "C:/Users/cubs1/AppData/Roaming/EldenRing/76561198099506921"

# Name of save in directory
# Elden RIng has a backup copy of the same name with ".bak" attached to it; This file is not called when game is loaded
STATE_NAME = "ER0000.sl2"

# Location of save character in load menu: 0 is the topmost spot
STATE_NUMBER = 6

# Messages displayed when a boss is defeated
victory_messages = ['ENEMY FELLED', 'GREAT ENEMY FELLED', 'LEGEND FELLED', 'GOD SLAIN']
