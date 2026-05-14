"""
Здесь реализуется логика перехода от координат в pagame в координаты тайлов
и реализуется логика перехода от координат тайлов в координаты pagame
"""


from project.settings import ConfigurationProject


config = ConfigurationProject()


class Serializer:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def straight_running(self):
        new_coordinates = self.coordinates[0] // config.TILE_SIZE, self.coordinates[1] // config.TILE_SIZE
        return new_coordinates

    def reverse_gear(self):
        new_coordinates = self.coordinates[0] * config.TILE_SIZE, self.coordinates[1] * config.TILE_SIZE
        return new_coordinates
