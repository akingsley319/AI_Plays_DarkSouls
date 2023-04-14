# Import text extraction module
from src.EldenRing.retrieve_damage_values.extractor import DamageValueExtractor
# Import values
from src.EldenRing.retrieve_damage_values.config import damage_value_crop, threshold
# File traversal
import os
# For image retrieval and manipulation
from PIL import Image, ImageOps
# For image color
import cv2


# Instantiate Text Extractor objects
damage_extractor = DamageValueExtractor()

# Where the calibration images were saved
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
IMAGE_CALIBRATION_PATH = "../resources/EldenRing/BossImages/margityolo/train/images"
IMAGE_CALIBRATION_PATH = os.path.join(project_root, IMAGE_CALIBRATION_PATH).replace("\\", "/")

# This fully reaches out to the necessary image for calibration
image_names = ["0b078464-215.png", "0bfd9462-86.png", "0bc1828a-463.png", "1fca124b-198.png", "3d77a205-429.png"]
image_paths = [os.path.join(IMAGE_CALIBRATION_PATH, image_name).replace("\\", "/") for image_name in image_names]
image_list = [Image.open(path) for path in image_paths]
# Damage values displayed in image
image_values = [60, 49, 121, 0, 172]

# The test is run
damage_value = 0
for i in range(len(image_list)):
    image = image_list[i]
    display = ImageOps.invert(image.convert('L').crop((1400, 840, 1470, 860)).point(lambda p: 255 if p > threshold else 0).convert('1'))
    display.show()
    reward_value = damage_extractor.determine_state(image, damage_value_crop)
    damage_text = damage_extractor.extract_text(image, damage_value_crop)
    damage_text = 0 if len(damage_text) == 0 else damage_text
    expected_damage_text = image_values[i]
    expected_reward_value = abs(int(damage_text) - damage_value) if (int(damage_text) > damage_value) else int(damage_text)
    text_outcome = "Success" if str(expected_damage_text) == str(damage_text) else "Failure"
    reward_outcome = "Success" if str(expected_reward_value) == str(reward_value) else "Failure"
    print("Text Displayed Resulted in {}: Expected {}, Retrieved {}".format(text_outcome,
                                                                            str(expected_damage_text),
                                                                            str(damage_text)))
    print("Reward Received Resulted in {}: Expected {}, Retrieved {}".format(reward_outcome,
                                                                             str(expected_reward_value),
                                                                             str(reward_value)))
    damage_value = expected_damage_text

