import pygame
from project.settings import WINDOW_WIDTH, WINDOW_HEIGHT, MAP_WEIGHT, MAP_HEIGHT
from project.entities.enemy import EnemyAI
from project.entities.entity import ModelEntity, RenderEntity, ControllerEntity, Entity


class GameEngine:
    def __init__(self, window, input_handler, menu, controller_state,
                 grid, ui, game_map, turn_manager, history, all_entities,
                 player):
        self.window = window
        self.clock = pygame.time.Clock()
        self.input_handler = input_handler
        self.menu = menu
        self.state_controller = controller_state
        self.grid = grid
        self.ui = ui
        self.game_map = game_map
        self.turn_manager = turn_manager
        self.history = history
        self.all_entities = all_entities
        self.player = player

    def run(self):
        while True:
            self.window.fill((0, 0, 0))
            state = self.state_controller.state

            if state == "menu":
                self._handle_menu()
            elif state == "game":
                self._handle_game()
            elif state == "vin":
                self._handle_win()
            elif state == "game_over":
                self._handle_game_over()
            elif state == "exit":
                pygame.quit()
                exit()

            pygame.display.update()
            self.clock.tick(60)

    def _handle_menu(self):
        self.input_handler.update()
        self.menu.update(self.input_handler, self.input_handler.mouse_position)
        if self.input_handler.escape:
            self.state_controller.state = "exit"
        self.menu.draw(self.window)

    def _handle_game(self):
        self.input_handler.update()
        self.ui.update(self.input_handler, self.input_handler.mouse_position)

        current = self.turn_manager.get_current()
        if current and current.model.health <= 0:
            self.turn_manager.advance()
            current = self.turn_manager.get_current()

        if current and not current.model.is_player:
            self._execute_enemy_turn(current)

        self.ui.set_text(f"Ходит: {current.model.name}" if current else "Очередь пуста")

        if self.player.model.health <= 0:
            self.state_controller.state = "game_over"
        elif not self.game_map.get_enemies():
            self.state_controller.state = "vin"

        if self.input_handler.escape:
            self.state_controller.state = "menu"

        self.grid.draw()
        self.ui.draw(self.window)
        for enemy in self.game_map.get_enemies():
            if enemy.model.health > 0:
                enemy.renderer.render(enemy.model)
        if current and current.model.is_player and current.model.health > 0:
            current.renderer.render(current.model)

    def _execute_enemy_turn(self, enemy):
        if enemy.model.health <= 0 or not self.player or self.player.model.health <= 0:
            self.turn_manager.advance()
            return

        turn_order = [e for e in self.all_entities if e.model.health > 0]
        if enemy not in turn_order:
            turn_order.append(enemy)
        turn_index = turn_order.index(enemy)

        ai = EnemyAI(enemy, self.game_map, self.player,
                     self.game_map.get_enemies(), turn_order)
        command = ai.take_turn(turn_index, depth=3)

        if command:
            self.history.execute(command)
            # command.execute()

        self.turn_manager.advance()
        current = self.turn_manager.get_current()
        self.ui.set_text(f"Ходит: {current.model.name}" if current else "Очередь пуста")

    def _handle_win(self):
        self.input_handler.update()
        font = pygame.font.Font(None, 250)
        text = font.render("Вы победили!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.window.blit(text, text_rect)
        if self.input_handler.escape:
            self.state_controller.state = "exit"

    def _handle_game_over(self):
        self.input_handler.update()
        font = pygame.font.Font(None, 200)
        text = font.render("Вы проиграли!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.window.blit(text, text_rect)
        if self.input_handler.escape:
            self.state_controller.state = "exit"

    def get_save_data(self):
        entities_data = []
        for entity in self.all_entities:
            model = entity.model
            entities_data.append({
                'name': model.name,
                'tile_x': model.tile_x,
                'tile_y': model.tile_y,
                'health': model.health,
                'damage': model.damage,
                'direction_of_view': model.direction_of_view,
                'start_index_direction_of_view': model.start_index_direction_of_view,
                'count_move': model.count_move,
                'max_count_move': model.max_count_move,
                'is_moving': model.is_moving,
                'initiative': model.initiative,
                'maximum_initiative': model.maximum_initiative,
                'is_player': model.is_player,
            })
        map_data = []
        for y in range(MAP_HEIGHT):
            row = []
            for x in range(MAP_WEIGHT):
                cell = self.game_map.get_point(x, y)
                row.append(cell.model.name if cell != 0 else 0)
            map_data.append(row)
        queue_data = [e.model.name for e in self.turn_manager.queue._queue]
        return {
            'entities': entities_data,
            'map': map_data,
            'queue': queue_data,
            'player_name': self.player.model.name,
        }

    def load_state(self, data):
        # Очищаем старые сущности и карту
        self.all_entities.clear()
        self.game_map._points = [[0 for _ in range(MAP_WEIGHT)] for _ in range(MAP_HEIGHT)]
        self.game_map._enemies.clear()

        entity_map = {}
        for edata in data['entities']:
            model = ModelEntity(
                edata['tile_x'], edata['tile_y'],
                edata['health'], edata['damage'],
                edata['name'],
                initiative=edata.get('initiative', 0),
                is_player=edata['is_player']
            )
            # Восстанавливаем направление через индекс
            model.start_index_direction_of_view = edata['start_index_direction_of_view']
            model.direction_of_view = model.directions_of_view[model.start_index_direction_of_view]
            model.count_move = edata['count_move']
            model.max_count_move = edata['max_count_move']
            model.is_moving = edata['is_moving']
            model.initiative = edata['initiative']
            model.maximum_initiative = edata['maximum_initiative']

            color = (100, 200, 0) if edata['is_player'] else (255, 200, 0)
            renderer = RenderEntity(self.window, color)
            controller = ControllerEntity(model)
            entity = Entity(model, renderer, controller)
            entity_map[edata['name']] = entity
            self.all_entities.append(entity)

        # Сбрасываем ходы для всех сущностей (чтобы они могли ходить)
        for entity in self.all_entities:
            entity.controller.reset_moves()
            entity.model.is_moving = False

        # Восстанавливаем карту
        for y, row in enumerate(data['map']):
            for x, name in enumerate(row):
                if name != 0 and name in entity_map:
                    entity = entity_map[name]
                    self.game_map.set_point(x, y, entity)
                    entity.model.tile_x = x
                    entity.model.tile_y = y

        # Восстанавливаем очередь
        self.turn_manager.queue._queue = []
        for name in data['queue']:
            if name in entity_map:
                self.turn_manager.queue.push(entity_map[name])

        # Устанавливаем игрока
        if data['player_name'] in entity_map:
            self.player = entity_map[data['player_name']]
        else:
            self.player = next((e for e in self.all_entities if e.model.is_player), None)

        self.turn_manager.current_entity = self.turn_manager.queue.first_motion()