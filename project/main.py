# встроенные модули
# импортируемые модули
import pygame
# собственные модули
from settings import ConfigurationProject
from settings import (
    BACKGROUND_COLOR,
)
from objects.entities import User

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
    user.move()
    # debug
    debug_tools.grid.draw()
    debug_tools.graph.draw_edges()
    debug_tools.graph.draw_vertexes()

    clock.tick(60)
    pygame.display.update()
