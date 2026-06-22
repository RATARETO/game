from project.command.base_command import BaseCommand
from project.utils.constants import DIRECTION_VECTORS


class RightTurnCommand(BaseCommand):
    def __init__(self, entity_controller):
        self.controller = entity_controller
        self.applied = True

    def execute(self):
        self.controller.right_turn()

    def undo(self):
        self.controller.left_turn()

    def redo(self):
        self.execute()


class LeftTurnCommand(BaseCommand):
    def __init__(self, entity_controller):
        self.controller = entity_controller
        self.applied = True

    def execute(self):
        self.controller.left_turn()

    def undo(self):
        self.controller.right_turn()

    def redo(self):
        self.execute()


class MoveCommand(BaseCommand):
    def __init__(self, entity, game_map):
        self.entity = entity
        self.game_map = game_map
        self.controller = entity.controller
        self.model = entity.model
        self.old_x = self.model.tile_x
        self.old_y = self.model.tile_y
        self.new_x = self.model.tile_x
        self.new_y = self.model.tile_y
        self.applied = False

    def execute(self):
        if self.applied or not self.controller.has_moves():
            return

        dx, dy = DIRECTION_VECTORS[self.model.direction_of_view]
        new_x = self.model.tile_x + dx
        new_y = self.model.tile_y + dy

        if self.game_map.in_map(new_x, new_y) and self.game_map.get_point(new_x, new_y) == 0:
            self.game_map.set_point(self.old_x, self.old_y, 0)
            self.controller.move(new_x, new_y)
            self.game_map.set_point(new_x, new_y, self.entity)
            self.new_x, self.new_y = new_x, new_y
            self.controller.use_move()
            self.applied = True

    def undo(self):
        if not self.applied:
            return
        self.game_map.set_point(self.new_x, self.new_y, 0)
        self.controller.move(self.old_x, self.old_y)
        self.game_map.set_point(self.old_x, self.old_y, self.entity)
        self.controller.restore_move()
        self.applied = False

    def redo(self):
        if self.applied:
            return
        self.game_map.set_point(self.old_x, self.old_y, 0)
        self.controller.move(self.new_x, self.new_y)
        self.game_map.set_point(self.new_x, self.new_y, self.entity)
        self.controller.use_move()
        self.applied = True
