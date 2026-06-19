from project.command.base_command import BaseCommand


class RightTurnCommand(BaseCommand):
    def __init__(self, entity_controller):
        self.entity_controller = entity_controller

        self._last_direction_of_view = entity_controller

        self.applied = True

    def execute(self):
        self.entity_controller.right_turn()

    def undo(self):
        self.entity_controller.left_turn()

    def redo(self):
        self.execute()


class LeftTurnCommand(BaseCommand):
    def __init__(self, entity_controller):
        self.entity_controller = entity_controller

        self.applied = True

    def execute(self):
        self.entity_controller.left_turn()

    def undo(self):
        self.entity_controller.right_turn()

    def redo(self):
        self.execute()


class MoveCommand:
    def __init__(self, entity, game_map):
        self.entity = entity

        self.entity_controller = self.entity.controller
        self.entity_model = self.entity.model
        self.game_map = game_map

        self.old_x = self.entity_model.tile_x
        self.old_y = self.entity_model.tile_y

        self.new_x = self.entity_model.tile_x
        self.new_y = self.entity_model.tile_y

        self.applied = False

    def execute(self):
        if self.applied:
            return

        direction_map = {
            "up": (0, -1), "right": (1, 0),
            "down": (0, 1), "left": (-1, 0)
        }
        dx, dy = direction_map[self.entity_model.direction_of_view]
        new_x = self.entity_model.tile_x + dx
        new_y = self.entity_model.tile_y + dy

        if (self.game_map.in_map(new_x, new_y) and
                self.game_map.get_point(new_x, new_y) == 0):
            self.game_map.set_point(self.old_x, self.old_y, 0)
            self.entity_controller.move(new_x, new_y)
            self.game_map.set_point(new_x, new_y, self.entity)

            self.new_x, self.new_y = new_x, new_y

            self.applied = True

    def undo(self):
        if not self.applied:
            return

        self.game_map.set_point(self.new_x, self.new_y, 0)
        self.entity_controller.move(self.old_x, self.old_y)
        self.game_map.set_point(self.old_x, self.old_y, self.entity)

    def redo(self):
        if not self.applied:
            return

        self.game_map.set_point(self.old_x, self.old_y, 0)
        self.entity_controller.move(self.new_x, self.new_y)
        self.game_map.set_point(self.new_x, self.new_y, self.entity)


class PathFinding:
    def __init__(self):
        pass

    def execute(self):
        # Вызов алгоритма A*
        pass
