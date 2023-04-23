import os
from gym.spaces import Discrete, Box
import numpy as np

# camera: (x,y)
camera = Box(low=-1, high=1, shape=(2,), dtype=float)
# movement: (x,y)
movement_x = Discrete(3)
movement_y = Discrete(3)
# action: nothing, light attack, heavy attack, jump, dodge, consumable
action = Discrete(6)
# Full action space
action_space = Box(low=np.array([-1., -1., 0., 0., 0.]), high=np.array([1., 1., 3., 3., 7.]), dtype=np.float32)

# Path to the model used for boss detection
project_root = str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))).\
                                                                                                      replace("\\", "/")
MODEL_PATH = project_root + "/resources/EldenRing/BossImages/margityolo/outputs/model100.pth"

# Threshold of confidence score in boss detection model
boss_score_threshold = 0.8
# Maximum reward available from boss detection
max_boss_reward = 1
min_boss_reward = 0

# damage value division
damage_divider_config = 0.1

# how much penalty should be attributed per pixel of health lost
penalty_per_pixel = -1

# victory and defeat rewards
victory_reward_value = 1000
defeat_penalty_value = -1000

# Monitor size; standard is 1920x1080; if this is changed, all screen grab values should be reconfigured
monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
n_channels = 3
n_height = monitor['height'] - monitor['top']
n_width = monitor['width'] - monitor['left']
RESIZE_HEIGHT = 540
RESIZE_WIDTH = 960

# Number of screen grabs stored in the state
number_observations = 3

# Model Paths
MODEL_PLAYS_PATH = project_root + "/resources/EldenRing/Models/AI_Plays"
LOGS_PLAYS_PATH = project_root + "/resources/EldenRing/Logs/AI_Plays"
