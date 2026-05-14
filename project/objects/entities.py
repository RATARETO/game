# встроенные модули
import time
# импортируемые модули
import pygame
from pygame.rect import Rect
# собственные модули


class BaseEntity:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size


class User(BaseEntity):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)

        self.color = (0, 255, 100)

        self.health = 100
        self.speed = 10

        self.last_time = time.time()
        self.movement_flag = False

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            (self.x * self.size, self.y * self.size, self.size, self.size)
        )

    def move(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_event = pygame.mouse.get_pressed()

        # FIXME: хитбокс справа не правильный
        mouse_rect = Rect(mouse_pos[0], mouse_pos[1], 25, 25)

        rect = pygame.Rect(self.x * self.size, self.y * self.size, self.size, self.size)

        # FIXME: работает не стабильно, бывает, появляется возможность ходить несколько раз
        # FIXME: переделать movement_flag
        if time.time() - self.last_time > 0.15:
            if self.movement_flag:
                if mouse_event[0]:
                    self.x = mouse_pos[0] // self.size
                    self.y = mouse_pos[1] // self.size

                    self.movement_flag = False

            if mouse_rect.colliderect(rect):
                self.color = (0, 100, 255)
                if mouse_event[0]:
                    self.movement_flag = not self.movement_flag
            elif not self.movement_flag:
                self.color = (25, 255, 10)
            self.last_time = time.time()

