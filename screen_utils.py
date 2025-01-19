import pyautogui
from PIL import Image, ImageOps
import pytesseract
from fuzzywuzzy import fuzz

def capture_fish_message(output_path="fish_message_screenshot.png"):
    """
    Captures a screenshot of the area where the fishing message appears
    and saves it to the specified output path.

    :param output_path: The file path where the screenshot will be saved.
    :return: The text detected in the message area.
    """
    # Valid region format: (x_start, y_start, x_end, y_end)
    region = (800, 250, 1500, 400)  # Example coordinates, adjust as needed
    
    print(f"Cropping fishing message region: {region}")

    # Take a full-screen screenshot
    screenshot = pyautogui.screenshot()

    # Crop the screenshot to the specified region
    cropped = screenshot.crop(region)

    # Save the cropped image
    cropped.save(output_path)
    print(f"Fish message screenshot saved to: {output_path}")

    # Extract text using Tesseract
    text = pytesseract.image_to_string(cropped).strip()
    print(f"Detected fish message: {text}")
    return text


def capture_pokemon_name(output_path="pokemon_name_screenshot.png"):
    """
    Captures a screenshot of the area where the Pokémon name appears,
    preprocesses it for better OCR, and saves it to the specified output path.

    :param output_path: The file path where the screenshot will be saved.
    :return: The text detected in the Pokémon name area.
    """
    # Valid region format: (x_start, y_start, x_end, y_end)
    region = (500, 370, 710, 430)  # Example coordinates, adjust as needed
    print(f"Cropping Pokémon name region: {region}")

    # Take a full-screen screenshot
    screenshot = pyautogui.screenshot()

    # Crop the screenshot to the specified region
    cropped = screenshot.crop(region)

    # Preprocess the image: Convert to grayscale
    grayscale = cropped.convert("L")  # Convert to grayscale

    # Increase contrast by binarizing
    binarized = grayscale.point(lambda x: 0 if x < 128 else 255, '1')  # Binarize image

    # Invert colors to make text black on white
    inverted = ImageOps.invert(binarized.convert("RGB")).convert("L")

    # Save the preprocessed image
    inverted.save(output_path)
    print(f"Pokémon name screenshot saved to: {output_path}")

    # Extract text using Tesseract
    text = pytesseract.image_to_string(inverted).strip()
    print(f"Detected Pokémon name: {text}")
    return text



def fuzzy_match(actual, expected, threshold=90):
    """
    Performs fuzzy string matching to handle OCR inaccuracies.

    :param actual: The text detected from the screen.
    :param expected: The expected text (e.g., "Feebas").
    :param threshold: The minimum match score to consider it a match (default: 90).
    :return: True if the match score is above the threshold, False otherwise.
    """
    score = fuzz.ratio(actual.lower(), expected.lower())
    print(f"Fuzzy Match Score: {score} (Actual: {actual}, Expected: {expected})")
    return score >= threshold
