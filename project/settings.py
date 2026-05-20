from os import getcwd

base_path = getcwd()

# временные константы
BACKGROUND_COLOR = (0, 0, 0)

# TILE_SIZE = 75


# класс настроек проекта
class ConfigurationProject:
    def __init__(self):
        # константы окна
        self.FPS = 60

        self.WINDOW_SIZE = (1200, 900)

        self.TILE_SIZE = 50

        self.MAP_START_X, self.MAP_START_Y = 3, 2
        self.MAP_WEIGHT, self.MAP_HEIGHT = 20, 15
