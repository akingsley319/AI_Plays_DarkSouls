import os

# path to pytesseract file for purpose of loading module to perform text extraction from image
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PATH_TO_TESSERACT = (str(ROOT_DIR) + "/resources/pytesseract/Tesseract-OCR/tesseract.exe").replace("\\", "/")
print(PATH_TO_TESSERACT)

# dimensions to retrieve; assumes (1920,1080) image
# crop region: (left, upper, right, lower)
damage_value_crop = (1400, 840, 1470, 860)

# Threshold on sensitivity of monochrome conversion of image
threshold = 150

# Game base address
process_name = "eldenring.exe"
