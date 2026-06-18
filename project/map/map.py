from project.settings import MAP_WEIGHT, MAP_HEIGHT, MAP_START_X, MAP_START_Y, TILE_SIZE


class Map:
    def __init__(self):
        # Создаем сетку размером MAP_WEIGHT x MAP_HEIGHT
        self.points = [
            [0 for _ in range(MAP_WEIGHT)] for _ in range(MAP_HEIGHT)
        ]

    def set_point(self, x, y, value=1):
        """x, y - координаты внутри сетки (0..MAP_WEIGHT-1, 0..MAP_HEIGHT-1)"""
        if self.in_map(x, y):
            self.points[y][x] = value

    def get_point(self, x, y):
        """x, y - координаты внутри сетки (0..MAP_WEIGHT-1, 0..MAP_HEIGHT-1)"""
        if self.in_map(x, y):
            return self.points[y][x]
        return 1  # Возвращаем 1 (стена) для точек вне карты

    @staticmethod
    def in_map(x, y):
        """Проверяет, находятся ли координаты в пределах сетки"""
        return 0 <= x < MAP_WEIGHT and 0 <= y < MAP_HEIGHT

    def get_pixel_offset(self):
        """Возвращает смещение сетки в пикселях"""
        return MAP_START_X * TILE_SIZE, MAP_START_Y * TILE_SIZE

