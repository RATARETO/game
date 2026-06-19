from project.settings import MAP_WEIGHT, MAP_HEIGHT, MAP_START_X, MAP_START_Y, TILE_SIZE

from pprint import pprint


class Map:
    def __init__(self):
        self.points = [
            [0 for _ in range(MAP_WEIGHT)] for _ in range(MAP_HEIGHT)
        ]

        self.enemies = []

    def set_point(self, x, y, value=1):
        if self.in_map(x, y):

            if not isinstance(value, int) and value not in self.enemies:
                self.enemies.append(value)

            if isinstance(value, int) and self.points[y][x] in self.enemies:
                self.enemies.remove(self.points[y][x])

            self.points[y][x] = value

    def get_point(self, x, y):
        if self.in_map(x, y):
            return self.points[y][x]
        return 1

    @staticmethod
    def in_map(x, y):
        return 0 <= x < MAP_WEIGHT and 0 <= y < MAP_HEIGHT
