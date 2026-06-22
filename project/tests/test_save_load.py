import unittest
import os
import tempfile
from project.save_manager import SaveManager
from project.map.map import Map
from project.core.turn_manager import TurnManager
from project.tests.test_utils import create_test_player, create_test_enemy
from project.settings import MAP_WEIGHT, MAP_HEIGHT


class TestSaveLoad(unittest.TestCase):
    def setUp(self):
        # Создаём тестовую среду
        self.game_map = Map()
        self.player = create_test_player(5, 5)
        self.enemy1 = create_test_enemy(6, 5, health=3)
        self.enemy2 = create_test_enemy(7, 6, health=2)
        self.game_map.set_point(5, 5, self.player)
        self.game_map.set_point(6, 5, self.enemy1)
        self.game_map.set_point(7, 6, self.enemy2)
        self.all_entities = [self.player, self.enemy1, self.enemy2]
        self.turn_manager = TurnManager(self.all_entities)

        # Сохраняем в временный файл, чтобы не мешать основному сохранению
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        SaveManager.SAVE_FILE = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        os.unlink(SaveManager.SAVE_FILE)
        SaveManager.SAVE_FILE = "savegame.dat"  # восстанавливаем стандартное имя

    def test_save_and_load_data(self):
        # Подготовка данных как в get_save_data
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

        data = {
            'entities': entities_data,
            'map': map_data,
            'queue': queue_data,
            'player_name': self.player.model.name,
        }

        # Сохраняем
        SaveManager.save(data)

        # Загружаем
        loaded = SaveManager.load()
        self.assertIsNotNone(loaded)

        # Проверяем, что загруженные данные совпадают с исходными
        self.assertEqual(len(loaded['entities']), len(entities_data))
        self.assertEqual(loaded['map'], map_data)
        self.assertEqual(loaded['queue'], queue_data)
        self.assertEqual(loaded['player_name'], self.player.model.name)

    def test_save_and_load_entity_attributes(self):
        # Меняем здоровье врага, чтобы проверить сохранение
        self.enemy1.model.health = 1
        data = {
            'entities': [
                {
                    'name': e.model.name,
                    'tile_x': e.model.tile_x,
                    'tile_y': e.model.tile_y,
                    'health': e.model.health,
                    'damage': e.model.damage,
                    'direction_of_view': e.model.direction_of_view,
                    'start_index_direction_of_view': e.model.start_index_direction_of_view,
                    'count_move': e.model.count_move,
                    'max_count_move': e.model.max_count_move,
                    'is_moving': e.model.is_moving,
                    'initiative': e.model.initiative,
                    'maximum_initiative': e.model.maximum_initiative,
                    'is_player': e.model.is_player,
                } for e in self.all_entities
            ],
            'map': [[0]*MAP_WEIGHT for _ in range(MAP_HEIGHT)],
            'queue': [],
            'player_name': self.player.model.name,
        }
        SaveManager.save(data)
        loaded = SaveManager.load()
        # Ищем врага по имени
        enemy_data = next((e for e in loaded['entities'] if e['name'] == 'enemy'), None)
        self.assertIsNotNone(enemy_data)
        self.assertEqual(enemy_data['health'], 1)


if __name__ == '__main__':
    unittest.main()
