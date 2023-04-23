# Import text extraction module
from src.EldenRing.text_extraction.extractor import TextExtractor
# Import values
from src.EldenRing.text_extraction.config import youdied_words, victory_words, bossname_words,\
                                                    youdied_crop, victory_crop, bossname_crop,\
                                                    youdied_thresh, victory_thresh, bossname_thresh
# File traversal
import os
# For image retrieval and manipulation
from PIL import Image


# Instantiate Text Extractor objects
youdied_extractor = TextExtractor(youdied_words, youdied_thresh)
victory_extractor = TextExtractor(victory_words, victory_thresh)
bossname_extractor = TextExtractor(bossname_words, bossname_thresh)

# Where the calibration images were saved
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
IMAGE_CALIBRATION_PATH = "../resources/EldenRing/CalibrateScreenGrabs"
IMAGE_CALIBRATION_PATH = os.path.join(project_root, IMAGE_CALIBRATION_PATH).replace("\\", "/")

# This fully reaches out to the necessary image for calibration
BOSS_DAMAGED_PATH = os.path.join(IMAGE_CALIBRATION_PATH, 'BossDamaged.png').replace('\\', '/')
BOSS_DEFEATED_PATH = os.path.join(IMAGE_CALIBRATION_PATH, 'GreatEnemyFelled.png').replace('\\', '/')
YOU_DIED_PATH = os.path.join(IMAGE_CALIBRATION_PATH, 'YouDied.png').replace('\\', '/')
path_list = [BOSS_DAMAGED_PATH, BOSS_DEFEATED_PATH, YOU_DIED_PATH]
image_list = [Image.open(path) for path in path_list]
expected_texts = [None, "GREAT ENEMY FELLED", "YOU DIED"]

# Run checker for You Died Text Extractor
expected_outcome = [False, False, True]
print("Text Extractor: You Died Message")
for i in range(len(image_list)):
    image = image_list[i]
    expected_text = expected_texts[i]
    retrieved_text = youdied_extractor.extract_text(image, youdied_crop)
    outcome = youdied_extractor.determine_state(image, youdied_crop)
    result = "Success" if outcome == expected_outcome[i] else "Failure"
    print("     Result: " + str(result))

# Run checker for Victory Text Extractor
expected_outcome = [False, True, False]
print("Text Extractor: Victory Message")
for i in range(len(image_list)):
    image = image_list[i]
    expected_text = expected_texts[i]
    retrieved_text = victory_extractor.extract_text(image, victory_crop)
    outcome = victory_extractor.determine_state(image, victory_crop)
    result = "Success" if outcome == expected_outcome[i] else "Failure"
    print("     Result: " + str(result))

# Run checker for Boss Name Extractor
expected_outcome = [True, False, True]
print("Text Extractor: Boss Name")
for i in range(len(image_list)):
    image = image_list[i]
    retrieved_text = bossname_extractor.extract_text(image, bossname_crop)
    outcome = bossname_extractor.determine_state(image, bossname_crop)
    result = "Success" if outcome == expected_outcome[i] else "Failure"
    print("     Result: " + str(result))
