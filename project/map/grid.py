from project.settings import *
import pygame


class Grid:
    def __init__(self, window):
        self.window = window

    def draw(self):
        # оптимизировал
        wight_grid, height_grid = MAP_WEIGHT, MAP_HEIGHT  # в клетках

        start_width, end_width = MAP_START_X, wight_grid  # в клетках
        start_height, end_height = MAP_START_Y, height_grid  # в клетках

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
