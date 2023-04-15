import numpy as np
from PIL import Image

from src.EldenRing.player_damaged.config import player_health_crop
from src.EldenRing.player_damaged.util import region_extraction


class PlayerHealthTracker:
    def __init__(self):
        self.max_health_crop = player_health_crop
        self.current_health_crop = player_health_crop
        self.health_bin_size = self.max_health_crop[3] - self.max_health_crop[1]

    def health_loss_check(self, image):
        # find region of health bar
        left, top, right, bottom, _ = region_extraction(image, self.current_health_crop)
        # update health
        if right - left < self.current_health_crop[2] - self.current_health_crop[0]:
            new_left = self.current_health_crop[0] + left
            new_upper = self.current_health_crop[1]
            new_right = self.current_health_crop[0] + right + left
            new_lower = self.current_health_crop[3]
            self.current_health_crop = (new_left, new_upper, new_right, new_lower)
        return image.crop(self.current_health_crop), right - left
        #return Image.fromarray(ROI), right - left

    def max_health(self, image):
        # find region of health bar
        left, top, right, bottom, _ = region_extraction(image, self.max_health_crop)
        # redefine the pixels describing player health
        new_left = self.max_health_crop[0] + left
        new_upper = self.max_health_crop[1] + top
        new_right = self.max_health_crop[0] + right + left
        new_lower = self.max_health_crop[1] + top + bottom
        self.max_health_crop = (new_left, new_upper, new_right, new_lower)
        self.current_health_crop = self.max_health_crop
        return image.crop(self.max_health_crop), right - left

    def reset_health(self):
        self.current_health_crop = self.max_health_crop



