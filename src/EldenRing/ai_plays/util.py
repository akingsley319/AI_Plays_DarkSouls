import math
from src.EldenRing.ai_plays.config import boss_score_threshold, max_boss_reward, min_boss_reward
from src.EldenRing.ai_plays.config import RESIZE_WIDTH, RESIZE_HEIGHT
from PIL import ImageOps, Image
import pydirectinput
import numpy as np
import cv2


# Determines the reward from boss detection
# Exponential rewards with a configurable maximum and minimum; threshold dependent
def calculate_boss_reward(score, threshold=boss_score_threshold,
                                 max_reward=max_boss_reward,
                                 min_reward=min_boss_reward):
    a = (max_reward - min_reward) / (math.exp(threshold) * (math.e - 1))
    c = (max_reward - (min_reward * math.e)) / (1 - math.e)
    return a * math.exp(score + threshold) + c


# Resize the image to the desired size and channel number
def resize_observation(img, grayscale=True):
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    img = cv2.resize(img, (RESIZE_WIDTH, RESIZE_HEIGHT), interpolation=cv2.INTER_AREA)
    img = np.expand_dims(img, axis=-1)
    return img


# control discrete action in action space
# action: light attack, heavy attack, jump, dodge, consumable, parry/skill (not included, kept for future)
def take_action(action):
    if action == 1:
        pydirectinput.click()
    elif action == 2:
        pydirectinput.keyDown('shift')
        pydirectinput.leftClick()
        pydirectinput.keyUp('shift')
    elif action == 3:
        pydirectinput.press('f')
    elif action == 4:
        pydirectinput.press('space')
    elif action == 5:
        pydirectinput.press('r')
    elif action == 6:
        pydirectinput.keyDown('shift')
        pydirectinput.rightClick(duration=0.2)
        pydirectinput.keyUp('shift')


# This defines movement for the character:
# For both axes: 0 = no movement; 1 = positive movement (right/forward); 2 = negative movement (left/backward)
def movement(x, y):
    if x == 1:
        pydirectinput.keyDown('a')
    elif x == 2:
        pydirectinput.keyDown('d')
    if y == 1:
        pydirectinput.keyDown('w')
    elif y == 2:
        pydirectinput.keyDown('s')


# This defines the movement of the mouse, which affects the camera orientation
# subtract one from x and y so the spread is (-1, 0, 1)
# Multiplier will change the mouse speed, changing the speed at which the camera will change
def camera(x, y, multiplier=20):
    x = int((x-1) * multiplier)
    y = int((y-1) * multiplier)
    pydirectinput.move(x, y)


# resets all keys to up position
def reset_keys():
    pydirectinput.keyUp('shift')
    pydirectinput.keyUp('f')
    pydirectinput.keyUp('space')
    pydirectinput.keyUp('r')
    pydirectinput.keyUp('w')
    pydirectinput.keyUp('a')
    pydirectinput.keyUp('s')
    pydirectinput.keyUp('d')
