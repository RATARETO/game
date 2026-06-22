import unittest
from project.core.history import History
from project.command.move_command import MoveCommand, RightTurnCommand, LeftTurnCommand
from project.tests.test_utils import create_test_entity, create_test_map

class TestHistory(unittest.TestCase):
    def test_undo_redo_move(self):
        game_map = create_test_map()
        entity = create_test_entity("test", 2, 2)
        game_map.set_point(2, 2, entity)
        # повернём вправо, чтобы двигаться
        turn_cmd = RightTurnCommand(entity.controller)
        turn_cmd.execute()  # теперь направление "right"
        cmd = MoveCommand(entity, game_map)
        history = History()
        history.execute(cmd)
        self.assertEqual(entity.model.tile_x, 3)  # сместился вправо
        self.assertEqual(entity.model.tile_y, 2)
        history.undo()
        self.assertEqual(entity.model.tile_x, 2)
        self.assertEqual(entity.model.tile_y, 2)
        history.redo()
        self.assertEqual(entity.model.tile_x, 3)
        self.assertEqual(entity.model.tile_y, 2)

    def test_undo_redo_turn(self):
        entity = create_test_entity("test", 0, 0)
        controller = entity.controller
        cmd = RightTurnCommand(controller)
        history = History()
        history.execute(cmd)
        self.assertEqual(entity.model.direction_of_view, "right")
        history.undo()
        self.assertEqual(entity.model.direction_of_view, "up")
        history.redo()
        self.assertEqual(entity.model.direction_of_view, "right")
