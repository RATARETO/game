# встроенные модули
# импортируемые модули
import pygame
# собственные модули
from settings import ConfigurationProject
from settings import (
    BACKGROUND_COLOR,
)
from objects.base_entity import User

from utils.debugging_tools import DebuggingTools


config = ConfigurationProject()

display = pygame.display.set_mode(config.WINDOW_SIZE)

debug_tools = DebuggingTools(display)

clock = pygame.time.Clock()

user = User(1, 3, 75)


while True:
    display.fill(BACKGROUND_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    user.draw(display)
    debug_tools.grid.draw()
    debug_tools.dots.draw()
    user.move()

    clock.tick(60)
    pygame.display.update()
