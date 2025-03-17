import cv2
import pytesseract
import numpy as np
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()
tes_path = os.getenv("TES_PATH")
pytesseract.pytesseract.tesseract_cmd = tes_path

# Load image
image_path = "download.png"

# Run Tesseract OCR
custom_config = r"--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
captcha_text = pytesseract.image_to_string(image_path, config=custom_config)

print("Extracted CAPTCHA:", captcha_text.strip())
