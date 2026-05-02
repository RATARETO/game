from os import getcwd

base_path = getcwd()

# временные константы
BACKGROUND_COLOR = (0, 0, 0)


# класс настроек проекта
class ConfigurationProject:
    def __init__(self):
        # константы окна
        self.FPS = 60

        self.WINDOW_SIZE = (800, 600)
