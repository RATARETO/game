import unittest
from project.map.map import Map
from project.tests.test_utils import create_test_entity

class TestMap(unittest.TestCase):
    def test_set_get_point(self):
        m = Map()
        e = create_test_entity("e", 0, 0)
        m.set_point(3, 4, e)
        self.assertEqual(m.get_point(3, 4), e)

    def test_enemies_list(self):
        m = Map()
        player = create_test_entity("player", 0, 0, is_player=True)
        enemy1 = create_test_entity("enemy1", 1, 1, is_player=False)
        enemy2 = create_test_entity("enemy2", 2, 2, is_player=False)
        m.set_point(0, 0, player)
        m.set_point(1, 1, enemy1)
        m.set_point(2, 2, enemy2)
        enemies = m.get_enemies()
        self.assertEqual(len(enemies), 2)
        self.assertIn(enemy1, enemies)
        self.assertIn(enemy2, enemies)
        # удаление
        m.remove_entity(enemy1)
        self.assertNotIn(enemy1, m.get_enemies())
        self.assertEqual(m.get_point(1, 1), 0)

    def test_in_map(self):
        m = Map()
        self.assertTrue(m.in_map(0, 0))
        self.assertFalse(m.in_map(-1, 0))
        self.assertFalse(m.in_map(100, 100))