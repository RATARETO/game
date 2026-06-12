# встроенные модули
from random import randint
# импортируемые модули
import pygame
# собственные модули
from settings import ConfigurationProject
from settings import (
    BACKGROUND_COLOR,
)
from objects.entities import User
from objects.entities_deque import EntitiesDeque

from utils.debugging_tools import DebuggingTools

from project.algoritms.priority_queue import PriorityQueue

config = ConfigurationProject()

display = pygame.display.set_mode(config.WINDOW_SIZE)
pygame.display.set_caption("мопсGAMING")

debug_tools = DebuggingTools(display)
clock = pygame.time.Clock()

users = []
for i in range(10):
    number = randint(1, 5)
    print(number)
    users.append(User(4 + i, 5, config.TILE_SIZE, i + 1, number))

for i in range(5):
    users[i].color = (255, 0, 0)
entities_deque = EntitiesDeque(users)

print([user.movement_count for number, user in enumerate(users) if number > 5])
priority_queue = PriorityQueue()

for user in users:
    priority_queue.push(user, user.movement_count)

top_user = None
while True:
    display.fill(BACKGROUND_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(909)
        # часть для перемещения
        if event.type == pygame.MOUSEBUTTONDOWN and top_user is not None:
            if top_user.is_move:
                top_user.move()

    # отрисовка
    if top_user is None:
        top_user = priority_queue.pop()

    if not priority_queue.is_empty():
        if not top_user.is_move:
            top_user = priority_queue.pop()
    else:
        # ход врага
        for user in users:
            user.is_move = True
            priority_queue.push(user, user.movement_count)

    for user in users:
        user.draw(display)

    # debug
    debug_tools.grid.draw()
    entities_deque.draw(display)
    # debug_tools.graph.draw_edges()
    # debug_tools.graph.draw_vertexes()

    clock.tick(60)
    pygame.display.update()
