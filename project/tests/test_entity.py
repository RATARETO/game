import unittest
from project.entities.entity import ModelEntity, ControllerEntity
from project.utils.constants import DIRECTIONS

class TestEntity(unittest.TestCase):
    def test_model_init(self):
        model = ModelEntity(10, 20, 5, 2, "test", is_player=True)
        self.assertEqual(model.tile_x, 10)
        self.assertEqual(model.tile_y, 20)
        self.assertEqual(model.health, 5)
        self.assertEqual(model.damage, 2)
        self.assertEqual(model.name, "test")
        self.assertTrue(model.is_player)

    def test_controller_turn(self):
        model = ModelEntity(0, 0, 3, 1, "test")
        controller = ControllerEntity(model)
        self.assertEqual(model.direction_of_view, "up")
        controller.right_turn()
        self.assertEqual(model.direction_of_view, "right")
        controller.right_turn()
        self.assertEqual(model.direction_of_view, "down")
        controller.left_turn()
        self.assertEqual(model.direction_of_view, "right")
        controller.left_turn()
        self.assertEqual(model.direction_of_view, "up")

    def test_controller_move(self):
        model = ModelEntity(2, 3, 3, 1, "test")
        controller = ControllerEntity(model)
        controller.move(5, 7)
        self.assertEqual(model.tile_x, 5)
        self.assertEqual(model.tile_y, 7)

    def test_controller_damage(self):
        model = ModelEntity(0, 0, 10, 2, "test")
        controller = ControllerEntity(model)
        controller.get_damage(3)
        self.assertEqual(model.health, 7)

    def test_controller_moves(self):
        model = ModelEntity(0, 0, 3, 1, "test")
        controller = ControllerEntity(model)
        self.assertTrue(controller.has_moves())
        controller.use_move()
        self.assertEqual(controller.model.count_move, 0)
        self.assertFalse(controller.has_moves())
        controller.restore_move()
        self.assertTrue(controller.has_moves())