import pygame

from project.objects.map import Map
from project.settings import ConfigurationProject

config = ConfigurationProject()
map = Map()


class Grid:
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        # оптимизировал
        wight_grid, height_grid = config.MAP_WEIGHT, config.MAP_HEIGHT  # в клетках

        start_width, end_width = config.MAP_START_X, wight_grid  # в клетках
        start_height, end_height = config.MAP_START_Y, height_grid  # в клетках

        # горизонтальные линии
        for i in range(0, end_width + 1):
            pygame.draw.line(
                self.screen,
                (40, 40, 40),
                (start_width * config.TILE_SIZE, (start_height + i) * config.TILE_SIZE),
                ((start_width + end_width) * config.TILE_SIZE, (start_height + i) * config.TILE_SIZE)
            )

        # вертикальные линии
        for i in range(0, end_width + 1):
            pygame.draw.line(
                self.screen,
                (40, 40, 40),
                ((start_width + i) * config.TILE_SIZE, config.TILE_SIZE * start_height),
                ((start_width + i) * config.TILE_SIZE, config.TILE_SIZE * (start_height + end_height))
            )


class GraphPoints:
    def __init__(self, screen):
        self.graph = map.graph
        self.screen = screen

    def draw_vertexes(self):
        for x, y in self.graph[0]:
            pygame.draw.circle(
                self.screen,
                (216, 51, 75),
                (x * config.TILE_SIZE + config.TILE_SIZE // 2, y * config.TILE_SIZE + config.TILE_SIZE // 2),
                5
            )

    def draw_edges(self):
        for edgex_1, edges_2 in self.graph[1].items():
            for edgex_2 in edges_2:
                pygame.draw.line(
                    self.screen,
                    (0, 0, 255),
                    (edgex_1[0] * config.TILE_SIZE + config.TILE_SIZE // 2,
                     edgex_1[1] * config.TILE_SIZE + config.TILE_SIZE // 2),
                    (edgex_2[0] * config.TILE_SIZE + config.TILE_SIZE // 2,
                     edgex_2[1] * config.TILE_SIZE + config.TILE_SIZE // 2),
                )


class DebuggingTools:
    def __init__(self, screen):
        self.grid = Grid(screen)
        self.graph = GraphPoints(screen)
