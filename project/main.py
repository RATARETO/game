# встроенные модули
# импортируемые модули
import pygame
# собственные модули
from settings import ConfigurationProject
from settings import (
    BACKGROUND_COLOR,
)
config = ConfigurationProject()

display = pygame.display.set_mode(config.WINDOW_SIZE)

clock = pygame.time.Clock()

while True:
    display.fill(BACKGROUND_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    clock.tick(60)
    pygame.display.update()
