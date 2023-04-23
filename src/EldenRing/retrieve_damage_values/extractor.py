from pytesseract import pytesseract
from src.EldenRing.retrieve_damage_values.config import PATH_TO_TESSERACT, threshold, damage_value_crop
from PIL import ImageOps


class DamageValueExtractor:
    def __init__(self):
        # sets path to pytesseract module
        pytesseract.tesseract_cmd = PATH_TO_TESSERACT
        # stores damage value
        self.damage_value = 0

    # noinspection PyMethodMayBeStatic
    def extract_text(self, image, crop=damage_value_crop, thresh=threshold):
        # Crops image if coordinates are supplied
        if crop is not None:
            image = image.crop(crop)
            image = image.point(lambda p: 255 if p > thresh else 0)
            image = image.convert('1')
            image = ImageOps.invert(image)
        out_text = pytesseract.image_to_string(image, config="--psm 7 digits")
        return out_text.strip()

    def determine_state(self, image, crop=damage_value_crop, thresh=threshold):
        text = self.extract_text(image.convert('L'), crop, thresh)
        # if text is empty, no damage is being done
        if len(text) == 0:
            self.damage_value = 0
            return self.damage_value
        # Check if text is a numerical value, update damage value for reward purposes
        elif text.isdigit():
            output = self.handle_digit(int(text))
            return output
        # if text cannot be converted to int, we assume damage does not track and wait to try again
        else:
            return 0

    def handle_digit(self, value):
        # if the new value is greater than the previous value, we track the difference for reward
        if value > self.damage_value:
            base_value = self.damage_value
            self.damage_value = value
            return self.damage_value - base_value
        # if the damage is the same, no new damage was applied, keeping value the same and 0 reward
        elif value == self.damage_value:
            return 0
        # if the damage value is less, we assume the update occurred rapidly after previous value disappeared
        elif value < self.damage_value:
            self.damage_value = value
            return self.damage_value

