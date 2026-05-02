# встроенные модули
# импортируемые модули
import pygame
# собственные модули


class BaseEntity:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

