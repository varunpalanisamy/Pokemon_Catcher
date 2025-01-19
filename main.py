import time
from grid_generator import draw_grid_on_image, visualize_grid
from navigation import move_to_tile, DIRECTIONS, facing_direction
from fishing import fish_on_tile
from PIL import ImageGrab

def take_game_screenshot(output_path="game_screenshot.png"):
    """
    Takes a screenshot of the game and saves it to the specified path.

    :param output_path: Path to save the screenshot.
    """
    screenshot = ImageGrab.grab()
    screenshot.save(output_path)
    print(f"Screenshot saved to: {output_path}")

def generate_water_grid():
    """
    Takes a screenshot of the game and generates the water grid matrix.

    :return: The generated water grid matrix.
    """
    screenshot_path = "game_screenshot.png"
    take_game_screenshot(screenshot_path)  # Take a screenshot of the game

    # Generate the grid from the screenshot
    tile_size = 127  # Adjust based on your game tile size
    x_offset = 0  # Horizontal offset (adjust as needed)
    y_offset = 130  # Vertical offset (adjust as needed)
    water_grid = draw_grid_on_image(
        screenshot_path,
        tile_size=tile_size,
        x_offset=x_offset,
        y_offset=y_offset,
        output_path="grid_with_overlay.png"
    )

    # Visualize the grid
    visualize_grid(water_grid, tile_size=30)
    return water_grid

def find_path_to_fish(water_grid, start_tile):
    """
    Finds a path to fish on all water tiles based on the water grid matrix.

    :param water_grid: 2D list representing the water grid.
    :param start_tile: Starting position of the character in the grid.
    :return: A list of tiles to fish on.
    """
    rows = len(water_grid)
    cols = len(water_grid[0])
    visited = set()
    path = []

    def dfs(tile):
        if tile in visited:
            return
        visited.add(tile)

        # Add to path if it's a water tile
        if water_grid[tile[1]][tile[0]] == 1:  # (x, y) corresponds to (col, row)
            path.append(tile)

        # Explore neighboring tiles (up, down, left, right)
        for dx, dy in DIRECTIONS.values():
            next_tile = (tile[0] + dx, tile[1] + dy)
            if 0 <= next_tile[0] < cols and 0 <= next_tile[1] < rows:
                dfs(next_tile)

    dfs(start_tile)
    return path

def main():
    print("Starting Feebas fishing bot...")

    # Step 1: Generate water grid
    water_grid = generate_water_grid()

    # Step 2: Define starting position (character is always in the center of the grid)
    start_tile = (11, 6)  # (x, y) based on 12th column, 7th row (0-indexed)

    # Step 3: Find path to fish on all water tiles
    path_to_fish = find_path_to_fish(water_grid, start_tile)

    print(f"Path to fish on water tiles: {path_to_fish}")

    # Step 4: Traverse the path and fish on each tile
    for tile in path_to_fish:
        print(f"Moving to tile {tile} and fishing...")
        move_to_tile(start_tile, tile)  # Move to the next tile
        fish_on_tile()  # Fish on the current tile
        start_tile = tile  # Update the current position

    print("Finished! Either found Feebas or completed all tiles.")

if __name__ == "__main__":
    main()
