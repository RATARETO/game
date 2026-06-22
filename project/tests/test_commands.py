import unittest
from project.command.move_command import MoveCommand, RightTurnCommand, LeftTurnCommand
from project.command.attack_command import AttackCommand
from project.tests.test_utils import create_test_map, create_test_player, create_test_enemy


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.map = create_test_map()
        self.player = create_test_player(2, 2)
        self.map.set_point(2, 2, self.player)
        # повернём игрока вправо, чтобы двигаться/атаковать
        RightTurnCommand(self.player.controller).execute()

    def test_move_command(self):
        cmd = MoveCommand(self.player, self.map)
        cmd.execute()
        self.assertEqual(self.player.model.tile_x, 3)
        self.assertEqual(self.player.model.tile_y, 2)
        self.assertEqual(self.map.get_point(2, 2), 0)
        self.assertEqual(self.map.get_point(3, 2), self.player)
        # отмена
        cmd.undo()
        self.assertEqual(self.player.model.tile_x, 2)
        self.assertEqual(self.player.model.tile_y, 2)
        self.assertEqual(self.map.get_point(2, 2), self.player)
        self.assertEqual(self.map.get_point(3, 2), 0)

    def test_attack_command(self):
        enemy = create_test_enemy(3, 2, health=3)
        self.map.set_point(3, 2, enemy)
        cmd = AttackCommand(self.player, self.map)
        cmd.execute()
        self.assertEqual(enemy.model.health, 1)  # damage=2, было 3
        self.assertEqual(self.player.model.tile_x, 2)  # не двигается
        # отмена
        cmd.undo()
        self.assertEqual(enemy.model.health, 3)
        self.assertEqual(self.map.get_point(3, 2), enemy)

    def test_attack_kills_and_restore(self):
        enemy = create_test_enemy(3, 2, health=1)
        self.map.set_point(3, 2, enemy)
        cmd = AttackCommand(self.player, self.map)
        cmd.execute()
        self.assertEqual(enemy.model.health, -1)  # damage=2
        self.assertNotIn(enemy, self.map.get_enemies())
        self.assertEqual(self.map.get_point(3, 2), 0)  # мёртвый убран с карты
        # отмена
        cmd.undo()
        self.assertEqual(enemy.model.health, 1)  # восстановлено
        self.assertIn(enemy, self.map.get_enemies())
        self.assertEqual(self.map.get_point(3, 2), enemy)