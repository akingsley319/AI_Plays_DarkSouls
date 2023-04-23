import os

# path to pytesseract file for purpose of loading module to perform text extraction from image
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PATH_TO_TESSERACT = (str(ROOT_DIR) + "/resources/pytesseract/Tesseract-OCR/tesseract.exe").replace("\\", "/")
print(PATH_TO_TESSERACT)

# Message displayed when player-character dies; individual words included
youdied_words = ["YOU DIED", "YOU", "DIED"]
# Messages displayed when player-character is victorious; individual words included
victory_words = ["FOE VANQUISHED", "GREAT FOE VANQUISHED", "ENEMY FELLED", "GREAT ENEMY FELLED",
                 "LEGEND FELLED", "GOD SLAIN", "FOE", "VANQUISHED", "GREAT", "ENEMY", "FELLED",
                 "LEGEND", "FELLED", "FELUED"]
# Boss name displayed when boss appears
bossname_words = ["MARGIT, THE FELL OMEN", "MARGIT", "MARGIT,", "THE", "FELL", "OMEN"]

# dimensions to retrieve; assumes (1920,1080) image
# crop region: (left, upper, right, lower)
youdied_crop = (750, 510, 1170, 590)
victory_crop = (450, 510, 1470, 590)
bossname_crop = (460, 840, 800, 867)

youdied_thresh_min = (100, 0, 0)
youdied_thresh_max = (150, 30, 30)
victory_thresh_min = (200, 170, 40)
victory_thresh_max = (250, 200, 70)
bossname_thresh_min = (90, 90, 90)
bossname_thresh_max = (150, 150, 150)

youdied_thresh = 30
victory_thresh = 170
bossname_thresh = 140
