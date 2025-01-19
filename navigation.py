import pyautogui
import time
from fishing import fish_on_tile

# Directions and corresponding movements
DIRECTIONS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0)
}

# Current facing direction (start facing down by default)
facing_direction = "down"

def move_to_tile(current_tile, next_tile):
    """
    Move the player from the current tile to the next tile.

    :param current_tile: (x, y) coordinates of the current tile.
    :param next_tile: (x, y) coordinates of the next tile.
    """
    global facing_direction
    x_diff = next_tile[0] - current_tile[0]
    y_diff = next_tile[1] - current_tile[1]

    # Determine the direction to move and update facing direction
    if x_diff > 0:
        pyautogui.press('d')  # Move right
        facing_direction = "right"
    elif x_diff < 0:
        pyautogui.press('a')  # Move left
        facing_direction = "left"

    if y_diff > 0:
        pyautogui.press('s')  # Move down
        facing_direction = "down"
    elif y_diff < 0:
        pyautogui.press('w')  # Move up
        facing_direction = "up"

    time.sleep(1)  # Allow time for the movement to complete


def is_water_tile(tile_position, screenshot):
    """
    Check if a given tile is water based on its color in the screenshot.

    :param tile_position: (x, y) position of the tile on the screen.
    :param screenshot: Screenshot of the game screen.
    :return: True if the tile is water, False otherwise.
    """
    # Get pixel color at the given position
    pixel_color = screenshot.getpixel(tile_position)
    

    # Example: Check if the pixel color matches water (adjust as needed)
    water_color = (52, 104, 162)  # Replace with the RGB value of water tiles
    return pixel_color == water_color


def explore_water_dynamic(start_tile):
    """
    Dynamically explore all water tiles starting from the given tile.

    :param start_tile: (x, y) coordinates of the starting tile.
    """
    global facing_direction

    visited = set()  # Track visited tiles
    stack = [start_tile]  # Stack for depth-first search

    while stack:
        current_tile = stack.pop()

        if current_tile in visited:
            continue

        # Take a screenshot and fish on the current tile
        screenshot = pyautogui.screenshot()
        print(f"Fishing on tile {current_tile}")
        fish_on_tile()

        visited.add(current_tile)

        # Check neighboring tiles (up, down, left, right)
        for direction, (dx, dy) in DIRECTIONS.items():
            next_tile = (current_tile[0] + dx, current_tile[1] + dy)

            # Move in the direction and check if the tile is water
            if is_water_tile(next_tile, screenshot) and next_tile not in visited:
                move_to_tile(current_tile, next_tile)
                stack.append(next_tile)

        # Backtrack to the previous tile (if needed)
        if stack:
            backtrack_tile = stack[-1]
            move_to_tile(current_tile, backtrack_tile)
