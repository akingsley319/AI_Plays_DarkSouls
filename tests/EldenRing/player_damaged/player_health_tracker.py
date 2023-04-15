# Import text extraction module
from src.EldenRing.player_damaged.player_health_tracker import PlayerHealthTracker
# Import values
from src.EldenRing.player_damaged.config import player_health_crop
# File traversal
import os
# For image retrieval and manipulation
from PIL import Image
# For image color
import cv2


# Instantiate Text Extractor objects
player_health = PlayerHealthTracker()

# Where the calibration images were saved
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
IMAGE_CALIBRATION_PATH = "../resources/EldenRing/BossImages/margityolo/train/images"
IMAGE_CALIBRATION_PATH = os.path.join(project_root, IMAGE_CALIBRATION_PATH).replace("\\", "/")

# This fully reaches out to the necessary image for calibration
image_names = ["43fc0ba6-411.png", "0b078464-215.png", "0bfd9462-86.png", "0bc1828a-463.png", "1fca124b-198.png",
               "3d77a205-429.png", "4c882f2d-482.png"]
image_paths = [os.path.join(IMAGE_CALIBRATION_PATH, image_name).replace("\\", "/") for image_name in image_names]
image_list = [Image.open(path) for path in image_paths]

image_list[0].crop(player_health.max_health_crop).show()
for i in range(len(image_names)):
    image = image_list[i]
    if i == 0:
        img, value = player_health.max_health(image)
        print("Max Health Value: {}".format(value))
    else:
        img, value = player_health.health_loss_check(image)
        print("Health Bar Value: {}".format(value))
    img.show()
    player_health.reset_health()

