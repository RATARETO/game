import pygame

from core.game import Game
from project.menu.button import Button
from project.menu.main_menu import MainMenu
from core.input_handler import InputHandler
from project.settings import *
from project.core.status_controller import Controller

from project.map.grid import Grid
from project.map.map import Map

from project.command.move_command import RightTurnCommand, LeftTurnCommand, SetMoveStateCommand

from project.entities.entity import ControllerEntity, RenderEntity, ModelEntity, ControlledEntity

from project.command.history import History

from project.map.ui import UI
from project.algorithms.queue import Queue

from project.command.attack_command import AttackCommand


def main():
    pygame.init()
    pygame.font.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    history = History()
    input_handler = InputHandler(history)

    map = Map()

    # инициализация управляемых сущностей
    controlled_entities = []

    controlled_entity_model = ModelEntity(10, 10, TILE_SIZE, (100, 200, 0), 3, 1, "player")
    controlled_entity_render = RenderEntity(window)
    controlled_entity_controller = ControllerEntity(controlled_entity_model)

    controlled_entity = ControlledEntity(
        controlled_entity_model,
        controlled_entity_render,
        controlled_entity_controller)

    controlled_entities.append(controlled_entity)
    map.set_point(10, 10)

    # враги
    enemies = []

    enemy_model = ModelEntity(12, 13, TILE_SIZE, (255, 200, 0), 3, 1, "enemy")
    enemy_render = RenderEntity(window)
    enemy_controller = ControllerEntity(controlled_entity_model)

    enemy = ControlledEntity(
        enemy_model,
        enemy_render,
        enemy_controller)

    enemies.append(enemy)
    map.set_point(12, 13)

    # привязка команд к кнопкам
    input_handler.bind(pygame.K_d, RightTurnCommand(controlled_entity_controller))
    input_handler.bind(pygame.K_a, LeftTurnCommand(controlled_entity_controller))

    # input_handler.bind(pygame.K_SPACE, SetMoveStateCommand(controlled_entity_controller))

    input_handler.bind(pygame.K_SPACE, AttackCommand(controlled_entity, map, [controlled_entity]))

    controller = Controller()

    font = pygame.font.SysFont(None, 36)

    # TODO: убрать нарушение DRY
    start_button = Button(
        100,
        100,
        300,
        100,
        "Начать игру",
        font,
        (124, 182, 247),
        (20, 114, 220),
        (69, 151, 244),
        controller.set_game_state
    )

    load_button = Button(
        100,
        210,
        300,
        100,
        "Загрузить игру",
        font,
        (124, 182, 247),
        (20, 114, 220),
        (69, 151, 244)
    )
    author_button = Button(
        100,
        320,
        300,
        100,
        "сохранить",
        font,
        (124, 182, 247),
        (20, 114, 220),
        (69, 151, 244)
    )
    exit_button = Button(
        100,
        430,
        300,
        100,
        "Выход",
        font,
        (124, 182, 247),
        (20, 114, 220),
        (69, 151, 244),
        controller.set_exit_state
    )

    queue = Queue(controlled_entities + enemies)

    ui = UI()

    next_button = Button(
        25,
        800,
        100,
        50,
        "Далее",
        font,
        (124, 182, 247),
        (20, 114, 220),
        (69, 151, 244),
        queue.next_motion
    )

    ui.add_button(next_button)

    menu = MainMenu(start_button, load_button, author_button, exit_button)

    grid = Grid(window)
    game = Game(window, input_handler, menu, controller, grid, controlled_entities, ui, queue, enemies, map)

    game.run()


if __name__ == '__main__':
    main()
