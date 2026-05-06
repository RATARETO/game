import pygame

from project.settings import ConfigurationProject


config = ConfigurationProject()


class Grid:
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        for i in range(config.WINDOW_SIZE[1] // config.TILE_SIZE):
            for j in range(config.WINDOW_SIZE[0] // config.TILE_SIZE):
                pygame.draw.line(
                    self.screen,
                    (255, 255, 255),
                    (config.TILE_SIZE * j, 0),
                    (config.TILE_SIZE * j, config.WINDOW_SIZE[1])
                )
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                (0, config.TILE_SIZE * i),
                (config.WINDOW_SIZE[0], config.TILE_SIZE * i)
            )


class GraphPoints:
    def __init__(self, screen):
        self.graph = [
            [x for x in range(config.WINDOW_SIZE[0] // config.TILE_SIZE)] for _ in range(config.WINDOW_SIZE[1] // config.TILE_SIZE)
        ]
        self.screen = screen

    def draw(self):
        for x in range(config.WINDOW_SIZE[0] // config.TILE_SIZE):
            for y in range(config.WINDOW_SIZE[1] // config.TILE_SIZE):
                pygame.draw.circle(
                    self.screen,
                    (255, 0, 0),
                    (x * config.TILE_SIZE + config.TILE_SIZE // 2, y * config.TILE_SIZE + config.TILE_SIZE // 2),
                    5
                )


class DebuggingTools:
    def __init__(self, screen):
        self.grid = Grid(screen)
        self.dots = GraphPoints(screen)
