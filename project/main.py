import pygame
from project.settings import WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE
from project.core.game_engine import GameEngine
from project.core.input_handler import InputHandler
from project.core.turn_manager import TurnManager
from project.core.history import History
from project.core.status_controller import Controller
from project.map.map import Map
from project.map.grid import Grid
from project.ui.ui import UI
from project.ui.button import Button
from project.ui.menu import MainMenu
from project.entities.entity import ModelEntity, RenderEntity, ControllerEntity, Entity
from project.command.move_command import RightTurnCommand, LeftTurnCommand, MoveCommand
from project.command.attack_command import AttackCommand
from project.command.end_turn_command import EndTurnCommand
from project.save_manager import SaveManager


def main():
    pygame.init()
    pygame.font.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Ядро
    history = History()
    input_handler = InputHandler(history)
    game_map = Map()
    state_controller = Controller()

    # Создание игрока
    player_model = ModelEntity(10, 10, health=3, damage=1, name="player", initiative=10, is_player=True)
    player_render = RenderEntity(window, color=(100, 200, 0))
    player_controller = ControllerEntity(player_model)
    player = Entity(player_model, player_render, player_controller)
    game_map.set_point(10, 10, player)

    # Создание врага
    enemy_model = ModelEntity(14, 13, health=3, damage=1, name="enemy", initiative=0, is_player=False)
    enemy_render = RenderEntity(window, color=(255, 200, 0))
    enemy_controller = ControllerEntity(enemy_model)
    enemy = Entity(enemy_model, enemy_render, enemy_controller)
    game_map.set_point(14, 13, enemy)

    all_entities = [player, enemy]

    # Очередь ходов
    turn_manager = TurnManager(all_entities)

    # UI и меню
    font = pygame.font.SysFont(None, 36)
    ui = UI(font, f"Ходит: {turn_manager.get_current().model.name}")

    start_button = Button(100, 100, 300, 100, "Начать игру", font,
                          (124, 182, 247), (20, 114, 220), (69, 151, 244),
                          state_controller.set_game_state)
    load_button = Button(100, 210, 300, 100, "Загрузить игру", font,
                         (124, 182, 247), (20, 114, 220), (69, 151, 244),
                         None)
    save_button = Button(100, 320, 300, 100, "Сохранить", font,
                         (124, 182, 247), (20, 114, 220), (69, 151, 244),
                         None)
    exit_button = Button(100, 430, 300, 100, "Выход", font,
                         (124, 182, 247), (20, 114, 220), (69, 151, 244),
                         state_controller.set_exit_state)
    menu = MainMenu(start_button, load_button, save_button, exit_button)

    grid = Grid(window)

    # Игровой движок
    engine = GameEngine(window, input_handler, menu, state_controller,
                        grid, ui, game_map, turn_manager, history,
                        all_entities, player)

    # Функция для обновления привязок клавиш (используется после загрузки)
    def refresh_bindings():
        # Очищаем старые привязки команд
        input_handler.commands.clear()
        input_handler.bind(pygame.K_d, RightTurnCommand, entity_controller=engine.player.controller)
        input_handler.bind(pygame.K_a, LeftTurnCommand, entity_controller=engine.player.controller)
        input_handler.bind(pygame.K_SPACE, AttackCommand, entity=engine.player, game_map=game_map)
        # Привязка EndTurn уже есть через bind_action, её не трогаем

    # Первоначальная привязка
    refresh_bindings()

    # Привязка действий сохранения/загрузки
    def save_game():
        data = engine.get_save_data()
        SaveManager.save(data)
        print("Игра сохранена")

    def load_game():
        data = SaveManager.load()
        if data:
            engine.load_state(data)
            refresh_bindings()  # обновляем привязки после загрузки
            ui.set_text(f"Ходит: {engine.turn_manager.get_current().model.name}")
            print("Игра загружена")
        else:
            print("Нет сохранения")

    save_button.action = save_game
    load_button.action = load_game
    input_handler.bind_action(pygame.K_s, save_game)
    input_handler.bind_action(pygame.K_l, load_game)

    def end_turn_action():
        current = turn_manager.get_current()
        if current and current.model.is_player:
            cmd = EndTurnCommand(turn_manager, engine, current)
            engine.history.execute(cmd)
    input_handler.bind_action(pygame.K_RETURN, end_turn_action)

    engine.run()


if __name__ == '__main__':
    main()