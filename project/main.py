import pygame

from core.game import Game
from project.menu.button import Button
from project.menu.main_menu import MainMenu
from core.input_handler import InputHandler
from project.settings import *
from project.core.status_controller import Controller

from project.map.grid import Grid

from project.command.move_command import RightTurnCommand, LeftTurnCommand

from project.entities.controlled_entity import (ControllerControlledEntity,
                                                RenderControlledEntity,
                                                ModelControlledEntity,
                                                ControlledEntity)

from project.command.history import History


def main():
    pygame.init()
    pygame.font.init()

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    history = History()
    input_handler = InputHandler(history)

    # инициализация управляемых сущностей
    controlled_entities = []

    controlled_entity_model = ModelControlledEntity(10, 10, TILE_SIZE, (100, 200, 0), 3, 1)
    controlled_entity_render = RenderControlledEntity(window)
    controlled_entity_controller = ControllerControlledEntity(controlled_entity_model)

    controlled_entity = ControlledEntity(
        controlled_entity_model,
        controlled_entity_render,
        controlled_entity_controller)

    controlled_entities.append(controlled_entity)
    # привязка команд к кнопкам
    input_handler.bind(pygame.K_d, RightTurnCommand(controlled_entity_controller))
    input_handler.bind(pygame.K_a, LeftTurnCommand(controlled_entity_controller))

    input_handler.bind(pygame.K_z, history.undo())
    input_handler.bind(pygame.K_y, history.redo())

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
        "кто придумал эту хуйню ?",
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

    menu = MainMenu(start_button, load_button, author_button, exit_button)

    grid = Grid(window)
    game = Game(window, input_handler, menu, controller, grid, controlled_entities)

    game.run()


if __name__ == '__main__':
    main()
