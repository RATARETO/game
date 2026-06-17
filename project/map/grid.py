from project.settings import *
import pygame


class Grid:
    def __init__(self, window):
        self.window = window

        self.cols = MAP_WEIGHT
        self.rows = MAP_HEIGHT

        self.tiles = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        # =========================================

    def draw(self):
        wight_grid, height_grid = MAP_WEIGHT, MAP_HEIGHT

        start_width, end_width = MAP_START_X, wight_grid
        start_height, end_height = MAP_START_Y, height_grid

        # горизонтальные линии
        for i in range(0, end_width + 1):
            pygame.draw.line(
                self.window,
                (40, 40, 40),
                (start_width * TILE_SIZE, (start_height + i) * TILE_SIZE),
                ((start_width + end_width) * TILE_SIZE, (start_height + i) * TILE_SIZE)
            )

        # вертикальные линии
        for i in range(0, end_width + 1):
            pygame.draw.line(
                self.window,
                (40, 40, 40),
                ((start_width + i) * TILE_SIZE, TILE_SIZE * start_height),
                ((start_width + i) * TILE_SIZE, TILE_SIZE * (start_height + end_height))
            )

    def is_walkable(self, col, row):
        if 0 <= col < self.cols and 0 <= row < self.rows:
            return self.tiles[row][col] == 0
        return False

    def set_tile(self, col, row, value):
        if 0 <= col < self.cols and 0 <= row < self.rows:
            self.tiles[row][col] = value

    def get_tile(self, col, row):
        if 0 <= col < self.cols and 0 <= row < self.rows:
            return self.tiles[row][col]
        return 1  # За пределами = стена

    def pixel_to_grid(self, pixel_x, pixel_y):
        col = (pixel_x - MAP_START_X * TILE_SIZE) // TILE_SIZE
        row = (pixel_y - MAP_START_Y * TILE_SIZE) // TILE_SIZE
        return int(col), int(row)

    def grid_to_pixel(self, col, row):
        x = (MAP_START_X + col) * TILE_SIZE
        y = (MAP_START_Y + row) * TILE_SIZE
        return x, y

    def set_wall(self, col, row):
        self.set_tile(col, row, 1)

    def clear_wall(self, col, row):
        self.set_tile(col, row, 0)
