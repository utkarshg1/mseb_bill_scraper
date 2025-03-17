import pytesseract
from PIL import Image
from dotenv import load_dotenv
import os
from playwright.sync_api import sync_playwright
from io import BytesIO
import base64

# Load env variables
load_dotenv()
tes_path = os.getenv("TES_PATH")
pytesseract.pytesseract.tesseract_cmd = tes_path


def extract_captcha(image_data):
    # Convert base64 to PIL Image
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    # Run Tesseract OCR
    custom_config = r"--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    captcha_text = pytesseract.image_to_string(image, config=custom_config).strip()
    return captcha_text


def scrape_website(url="https://wss.mahadiscom.in/wss/wss?uiActionName=getViewPayBill"):
    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    print(page.title())
    page.screenshot(path="screenshot.png")
    # Extract base64 image data from the canvas
    image_data = page.evaluate(
        """
        () => {
            const canvas = document.getElementById('captcha');
            return canvas.toDataURL('image/png').split(',')[1];  // Extract base64 data
        }
    """
    )
    captcha = extract_captcha(image_data)
    print(f"Extracted captcha : {captcha}")
    browser.close()


if __name__ == "__main__":
    scrape_website()
