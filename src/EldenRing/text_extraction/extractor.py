from pytesseract import pytesseract
from src.EldenRing.text_extraction.config import PATH_TO_TESSERACT


class TextExtractor:
    def __init__(self, words):
        # sets path to pytesseract module
        pytesseract.tesseract_cmd = PATH_TO_TESSERACT
        # determines the words being searched for
        self.words = words

    # noinspection PyMethodMayBeStatic
    def extract_text(self, image):
        return pytesseract.image_to_string(image)

    def determine_state(self, image):
        text = self.extract_text(image)
        if text in self.words:
            return True
        else:
            return False
