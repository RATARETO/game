# встроенные модули
import time
# импортируемые модули
import pygame
from pygame.rect import Rect
# собственные модули
from project.settings import ConfigurationProject


config = ConfigurationProject()


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
        self.last_time_to_move = time.time()

        self.movement_flag = False

    def draw(self, screen):
        # mops
        image = pygame.image.load("123.png")
        scaled_image = pygame.transform.scale(image, (self.size - 3, self.size - 3))

        pygame.draw.rect(
            screen,
            self.color,
            (self.x * self.size, self.y * self.size, self.size, self.size)
        )

        screen.blit(scaled_image, (self.x * self.size + 2, self.y * self.size + 2))

    def move(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_event = pygame.mouse.get_pressed()

        # FIXME: хитбокс справа не правильный
        mouse_rect = Rect(mouse_pos[0], mouse_pos[1], 25, 25)

        rect = pygame.Rect(self.x * self.size, self.y * self.size, self.size, self.size)

        rect_grid = pygame.Rect(
            config.MAP_START_X * config.TILE_SIZE,
            config.MAP_START_Y * config.TILE_SIZE,
            config.MAP_WEIGHT * config.TILE_SIZE,
            config.MAP_HEIGHT * config.TILE_SIZE
        )

        # FIXME: работает не стабильно, бывает, появляется возможность ходить несколько раз
        # FIXME: переделать movement_flag
        if time.time() - self.last_time > 0.15:
            if self.movement_flag:
                if mouse_event[0] and mouse_rect.colliderect(rect_grid):
                    self.x = mouse_pos[0] // self.size
                    self.y = mouse_pos[1] // self.size

                    self.movement_flag = False
            self.last_time = time.time()

        if time.time() - self.last_time_to_move > 0.15:
            if mouse_rect.colliderect(rect):
                self.color = (0, 100, 255)
                if mouse_event[0] and mouse_rect.colliderect(rect_grid):
                    self.movement_flag = (lambda x: not x)(self.movement_flag)
            elif not self.movement_flag:
                self.color = (25, 255, 10)

            self.last_time_to_move = time.time()


