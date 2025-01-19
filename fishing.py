import pyautogui
import time
from screen_utils import capture_fish_message, capture_pokemon_name, fuzzy_match

def fish_on_tile():
    """Fish on the current tile and check for Feebas."""
    time.sleep(3)
    while True:
        pyautogui.press('3') 
        time.sleep(6)  



        fish_message = capture_fish_message(output_path="fish_message_screenshot.png")
        print(f"Fishing Message Detected: {fish_message}")

        if "nibble" in fish_message:
            pyautogui.press('x')
            continue  
        elif "Landed" in fish_message:
            pyautogui.press('z') 
            time.sleep(12)


            pokemon_name = capture_pokemon_name(output_path="pokemon_name_screenshot.png")
            print(f"Pokémon Name Detected: {pokemon_name}")


            if "Tentac" not in pokemon_name and "Magi" not in pokemon_name:

                if fuzzy_match(pokemon_name, "Feebas"):
                    print("Feebas found! Stopping program.")
                    return True  
                else:
                    print(f"Unidentified Pokémon: {pokemon_name}. Stopping Bot.")
                    return True
            else:

                print(f"Encountered {pokemon_name}. Fleeing from battle.")
                run_from_battle()
                return False


def run_from_battle():
    """Run from the current battle."""
    print("Running from battle")
    pyautogui.press('s')  # Move to "Run" option
    pyautogui.press('d')
    pyautogui.press('z')  # Confirm
    time.sleep(10)
