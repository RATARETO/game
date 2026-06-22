import unittest
from project.algorithms.minimax import evaluate, generate_legal_actions, minimax, find_best_action
from project.utils.constants import DIRECTIONS
from project.tests.test_utils import create_test_map, create_test_player, create_test_enemy, create_test_entity

class TestMinimax(unittest.TestCase):
    def test_evaluate(self):
        player = create_test_player(0, 0)
        enemies = [create_test_enemy(3, 0, health=3), create_test_enemy(0, 3, health=2)]
        score = evaluate(player, enemies)
        # просто проверяем, что возвращается число
        self.assertIsInstance(score, float)

    def test_generate_legal_actions(self):
        game_map = create_test_map()
        player = create_test_player(2, 2)
        enemy = create_test_enemy(3, 2)
        game_map.set_point(2, 2, player)
        game_map.set_point(3, 2, enemy)
        # повернём вправо – атака
        player.controller.right_turn()
        actions = generate_legal_actions(player, game_map, [enemy])
        # должно быть действие атаки (вправо) и, возможно, движение в другие стороны
        self.assertGreater(len(actions), 0)
        # проверяем, что есть атака
        attack_actions = [a for a in actions if a.command_cls.__name__ == "AttackCommand"]
        self.assertEqual(len(attack_actions), 1)
        # также есть движения в пустые клетки, если они свободны

    def test_minimax(self):
        # простой сценарий: игрок и враг рядом, игрок ходит первым
        game_map = create_test_map()
        player = create_test_player(2, 2)
        enemy = create_test_enemy(3, 2)
        game_map.set_point(2, 2, player)
        game_map.set_point(3, 2, enemy)
        player.controller.right_turn()  # смотрит на врага
        turn_order = [player, enemy]
        score = minimax(game_map, player, [enemy], turn_order, 0, depth=2, alpha=float("-inf"), beta=float("inf"))
        self.assertIsInstance(score, float)

    def test_find_best_action(self):
        game_map = create_test_map()
        player = create_test_player(2, 2)
        enemy = create_test_enemy(3, 2)
        game_map.set_point(2, 2, player)
        game_map.set_point(3, 2, enemy)
        player.controller.right_turn()
        turn_order = [player, enemy]
        action = find_best_action(player, game_map, player, [enemy], turn_order, 0, depth=2)
        self.assertIsNotNone(action)
        direction, command_cls = action
        self.assertEqual(direction, "right")  # должна атаковать
        self.assertEqual(command_cls.__name__, "AttackCommand")