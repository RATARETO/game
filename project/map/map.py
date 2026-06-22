from project.settings import MAP_WEIGHT, MAP_HEIGHT
from project.entities.entity import Entity


class Map:
    def __init__(self):
        self._points = [[0 for _ in range(MAP_WEIGHT)] for _ in range(MAP_HEIGHT)]
        self._enemies = []   # только враги (не игрок)

    def set_point(self, x: int, y: int, entity):
        if not self.in_map(x, y):
            return
        old = self._points[y][x]
        if not isinstance(old, int) and old in self._enemies:
            self._enemies.remove(old)
        if not isinstance(entity, int):
            if entity.model.is_player is False and entity not in self._enemies:
                self._enemies.append(entity)
        self._points[y][x] = entity

    def get_point(self, x, y):
        if self.in_map(x, y):
            return self._points[y][x]
        return 1

    def remove_entity(self, entity):
        """Удаляет сущность с карты и из списка врагов."""
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WEIGHT):
                if self._points[y][x] is entity:
                    self._points[y][x] = 0
                    if entity in self._enemies:
                        self._enemies.remove(entity)
                    return

    def get_enemies(self):
        """Возвращает копию списка врагов."""
        return self._enemies[:]

    @staticmethod
    def in_map(x, y):
        return 0 <= x < MAP_WEIGHT and 0 <= y < MAP_HEIGHT
