import time
import numpy as np

from src.EldenRing.retrieve_damage_values.extractor import DamageValueExtractor
from src.EldenRing.boss_detection.inference import BossDetectionReturn
from src.EldenRing.ai_plays.config import MODEL_PATH, boss_score_threshold, damage_divider_config
from src.EldenRing.ai_plays.util import calculate_boss_reward

from src.EldenRing.player_damaged.player_health_tracker import PlayerHealthTracker
from src.EldenRing.ai_plays.config import penalty_per_pixel

from src.EldenRing.text_extraction.extractor import TextExtractor
from src.EldenRing.text_extraction.config import youdied_words, victory_words
from src.EldenRing.ai_plays.config import victory_reward_value, defeat_penalty_value


class RewardSystem:
    def __init__(self):
        # Reward class objects
        self.damage_value_extractor = DamageValueExtractor()  # Reward: determines damage done to boss
        self.boss_detection_model = BossDetectionReturn(MODEL_PATH)  # Reward: detect boss on screen
        self.victory_detection_model = TextExtractor(victory_words)
        # Penalty class objects
        self.player_hit_detector = PlayerHealthTracker()  # Tracks player current health
        self.max_health_set = False
        self.player_current_health = 0
        self.defeat_detection_model = TextExtractor(youdied_words)

    def calculate_reward(self, image, boss_threshold=boss_score_threshold, damage_divider=damage_divider_config):
        # This pulls the value of any damage done to a boss, and tracks differences in damage displayed
        damage_reward = self.damage_value_extractor.determine_state(image)
        damage_reward = damage_reward / damage_divider
        # time based reward to the agent for staying alive
        time_reward = 0.1
        # reward for keeping the boss or bosses on screen to receive information; reduced reward for lower confidence
        _, boss_detection_scores = self.boss_detection_model.boss_detection(np.array(image))
        boss_detection_score_sum = sum([score for score in boss_detection_scores[0]['scores'] if score > boss_threshold])
        boss_detection_reward = calculate_boss_reward(boss_detection_score_sum)
        # Add boss detection reward to model in place of time, if it is a higher score
        reward = time_reward + damage_reward + boss_detection_reward
        return reward

    def calculate_penalty(self, image):
        if self.max_health_set is False:
            _, health_value = self.player_hit_detector.max_health(image)
            self.max_health_set = True
            self.player_current_health = health_value
            return 0
        # player hit
        elif self.max_health_set is True:
            _, health_value = self.player_hit_detector.health_loss_check(image)
            penalty = self.player_current_health - health_value
            penalty = penalty * penalty_per_pixel
            self.player_current_health = health_value
            return penalty

    def game_over(self, image):
        # First checks if victory is achieved
        if self.victory_detection_model.determine_state(image):
            return victory_reward_value
        elif self.defeat_detection_model.determine_state(image):
            return defeat_penalty_value

    def reset(self):
        self.player_current_health = 0
        self.max_health_set = False
