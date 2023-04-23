import time

import gym

from gym.spaces import Box, MultiDiscrete


import numpy as np
import mss
from PIL import Image

from src.EldenRing.ai_plays.config import action_space, monitor, RESIZE_HEIGHT, RESIZE_WIDTH
from src.EldenRing.ai_plays.util import resize_observation, movement, camera, take_action, reset_keys
from src.EldenRing.ai_plays.reward import RewardSystem

from src.EldenRing.restart_fight.reset import Reset

from src.EldenRing.text_extraction.extractor import TextExtractor
from src.EldenRing.text_extraction.config import bossname_words, bossname_crop
from src.EldenRing.text_extraction.config import victory_words, youdied_words, victory_crop, youdied_crop
from src.EldenRing.text_extraction.config import victory_thresh, youdied_thresh, bossname_thresh


class CustomEnv(gym.Env):
    def __init__(self):
        super(CustomEnv, self).__init__()
        # Define action and observation space
        self.action_space = action_space  # (x,y) movement; (x,y) camera; camera speed; actions
        self.observation_space = Box(low=0, high=255, shape=(RESIZE_HEIGHT, RESIZE_WIDTH, 1), dtype=np.uint8)
        # Text Check for done or not
        #self.victory_checker = TextExtractor(victory_words, victory_thresh)
        #self.defeat_checker = TextExtractor(youdied_words, youdied_thresh)
        # Calculates Reward
        self.reward_system = RewardSystem()
        # Checks for boss name to signify start of boss fight
        self.boss_start_check = TextExtractor(bossname_words, bossname_thresh)
        # creates queue for check if boss is done
        self.boss_checklist = 0
        # queued reward: if checking for 'game_over' store reward while verifying
        self.stored_reward = 0

    def step(self, action):
        reset_keys()
        # Performs the specific action
        camera(action[0], action[1])
        movement(int(action[2]), int(action[3]))
        take_action(int(action[4]))  # light attack, heavy attack, jump, dodge, consumable, block
        # Nothing to really put into info
        info = {}
        # Wait a moment for the next information
        time.sleep(0.05)
        # Gather new observation
        img = mss.mss().grab(monitor)  # grabs screenshot
        img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")  # transforms screenshot to usable form
        # Calculate reward
        reward = self.reward_system.calculate_reward(img.copy())  # Reward
        reward += self.reward_system.calculate_penalty(img.copy())  # Penalty
        # Check if done
        #victory = self.victory_checker.determine_state(img.copy(), victory_crop)
        #defeat = self.defeat_checker.determine_state(img.copy(), youdied_crop)
        boss_present = self.boss_start_check.determine_state(img.copy(), bossname_crop)
        #if (victory is True) or (defeat is True) or (boss_present is False):
        done = False
        if boss_present is False:
            self.boss_checklist += 1
            self.stored_reward += reward
            reward = 0
            if self.boss_checklist > 5:
                done = True
                self.stored_reward = 0
        #    reward += self.reward_system.game_over(img)
        else:
            self.boss_checklist = 0
            reward += self.stored_reward
            self.stored_reward = 0
        # Prepare observation
        observation = resize_observation(img)
        return observation, reward, done, info

    def reset(self):
        reset_keys()
        time.sleep(12)
        # Load the designated save state
        reset_object = Reset()
        start_time = reset_object.restart_boss()
        # The fight doesn't start until the boss is introduced; this checks for this to signify the start of new attempt
        boss_start = False
        while boss_start is False:
            if time.time() - start_time > 130:
                raise EnvironmentError("Load time too long")
            elif int(time.time()) % 100 == 0:
                reset_object.restart_boss()
            elif int(time.time()) % 10 == 0:
                reset_object.start_boss()
            img = mss.mss().grab(monitor)  # grabs screenshot
            img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")  # transforms screenshot to usable form
            boss_start = self.boss_start_check.determine_state(img.copy(), bossname_crop)  # checks if boss started; ends loop
        observation = resize_observation(img)
        self.reward_system.reset()
        return observation  # reward and done and info not included

    def render(self, mode='human'):
        pass

    def close(self):
        pass
