from pytesseract import pytesseract
from src.EldenRing.text_extraction.config import PATH_TO_TESSERACT


class DamageValueExtractor:
    def __init__(self):
        # sets path to pytesseract module
        pytesseract.tesseract_cmd = PATH_TO_TESSERACT
        # stores damage value
        self.damage_value = 0

    # noinspection PyMethodMayBeStatic
    def extract_text(self, image):
        return pytesseract.image_to_string(image)

    def determine_state(self, image):
        text = self.extract_text(image)
        # if text is empty, no damage is being done
        if len(text) == 0:
            self.damage_value = 0
            return self.damage_value
        # if text cannot be converted to int, we assume damage does not track and wait to try again
        elif text.isdigit():
            output = self.handle_digit(int(text))
            return output

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

