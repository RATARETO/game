import unittest
from project.map.map import Map
from project.core.turn_manager import TurnManager
from project.command.move_command import MoveCommand, RightTurnCommand
from project.command.attack_command import AttackCommand
from project.tests.test_utils import create_test_player, create_test_enemy


class TestIntegration(unittest.TestCase):
    def test_simple_battle(self):
        game_map = Map()
        player = create_test_player(2, 2)
        enemy = create_test_enemy(3, 2, health=3)
        game_map.set_point(2, 2, player)
        game_map.set_point(3, 2, enemy)
        all_entities = [player, enemy]
        turn_manager = TurnManager(all_entities)

        player.controller.right_turn()
        self.assertEqual(player.model.direction_of_view, "right")
        cmd_attack = AttackCommand(player, game_map)
        cmd_attack.execute()

        self.assertEqual(enemy.model.health, 1)  # урон 2, было 3 → 1
        # Враг может остаться на (3,2) или быть отброшен на (4,2)
        self.assertTrue(
            game_map.get_point(3, 2) == enemy or game_map.get_point(4, 2) == enemy,
            "Враг не найден на карте"
        )
        self.assertEqual(player.model.tile_x, 2)  # игрок не двигался
        self.assertEqual(player.model.tile_y, 2)
