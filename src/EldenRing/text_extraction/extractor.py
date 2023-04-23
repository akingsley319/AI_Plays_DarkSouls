from pytesseract import pytesseract
from src.EldenRing.text_extraction.config import PATH_TO_TESSERACT
from PIL import ImageOps


class TextExtractor:
    def __init__(self, words, thresh=None):
        # sets path to pytesseract module
        pytesseract.tesseract_cmd = PATH_TO_TESSERACT
        # determines the words being searched for
        self.words = words
        self.thresh = thresh

    def extract_text(self, image, crop=None):
        # Crops image if coordinates are supplied
        if crop is not None:
            image = image.crop(crop)
            if self.thresh is not None:
                image = image.convert('L')
                image = image.point(lambda p: 255 if p > self.thresh else 0)
                image = image.convert('1')
                image = ImageOps.invert(image)
        return pytesseract.image_to_string(image), image

    def determine_state(self, image, crop=None):
        # Extract text and separate them by perceived word
        text, _ = self.extract_text(image, crop)
        text_seperated = text.strip().split(" ")
        # Check each retrieved word; if none found, return False, otherwise return True for any matches found
        for word in text_seperated:
            if word.upper() in self.words:
                return True
        return False
