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


    def bellman_ford(self, graph, vertices, source):
        distance = [float('inf')] * vertices
        distance[source] = 0

        for _ in range(vertices - 1):
            for u, v, weight in graph:
                if distance[u] != float('inf') and distance[u] + weight < distance[v]:
                    distance[v] = distance[u] + weight

        for u, v, weight in graph:
            if distance[u] != float('inf') and distance[u] + weight < distance[v]:
                raise ValueError("Graph contains negative weight cycle")

        return distance

    def move(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_event = pygame.mouse.get_pressed()

        mouse_rect = Rect(mouse_pos[0], mouse_pos[1], 25, 25)

        rect = pygame.Rect(self.x * self.size, self.y * self.size, self.size, self.size)

        if time.time() - self.last_time > 0.1:
            if self.movement_flag:
                if mouse_event[0]:
                    self.x = mouse_pos[0] // self.size
                    self.y = mouse_pos[1] // self.size

                    self.movement_flag = False

            if mouse_rect.colliderect(rect):
                self.color = (0, 100, 255)
                if mouse_event[0]:
                    self.movement_flag = not self.movement_flag
            else:
                self.color = (0, 255, 100)
            self.last_time = time.time()


