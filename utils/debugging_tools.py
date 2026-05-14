import pygame

from project.objects.map import Map
from project.settings import ConfigurationProject

config = ConfigurationProject()
map = Map()


class Grid:
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        for i in range(config.WINDOW_SIZE[1] // config.TILE_SIZE):
            for j in range(config.WINDOW_SIZE[0] // config.TILE_SIZE):
                pygame.draw.line(
                    self.screen,
                    (40, 40, 40),
                    (config.TILE_SIZE * j, 0),
                    (config.TILE_SIZE * j, config.WINDOW_SIZE[1])
                )
            pygame.draw.line(
                self.screen,
                (40, 40, 40),
                (0, config.TILE_SIZE * i),
                (config.WINDOW_SIZE[0], config.TILE_SIZE * i)
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
