from project.command.base_command import BaseCommand


class RightTurnCommand(BaseCommand):
    def __init__(self, entity_controller):
        self.entity_controller = entity_controller

        self._last_direction_of_view = entity_controller

    def undo(self):
        self.entity_controller.left_turn()

    def execute(self):
        self.entity_controller.right_turn()


class LeftTurnCommand(BaseCommand):
    def __init__(self, entity_controller):
        self.entity_controller = entity_controller

    def undo(self):
        self.entity_controller.right_turn()

    def execute(self):
        self.entity_controller.left_turn()


class SetMoveStateCommand(BaseCommand):
    def __init__(self, entity_controller):
        self.entity_controller = entity_controller

    def execute(self):
        self.entity_controller.set_is_moving()

    def undo(self):
        self.entity_controller.set_is_moving()


class MoveCommand(BaseCommand):
    def __init__(self, entity_model):
        self.entity_model = entity_model

        self._last_tile_x = entity_model.tile_x
        self._last_tile_y = entity_model.tile_y

    def execute(self):
        self.entity_model.is_moving = False

        # TODO: вынести метод в контроллер

        # TODO: проверки на возможность перемещения

        # TODO: A* -> self.entity_model.tile_x, self.entity_model.tile_y

    def undo(self):
        # TODO: вынести метод в контроллер
        self.entity_model.tile_x = self._last_tile_x
        self.entity_model.tile_y = self._last_tile_y


class PathFinding:
    def __init__(self):
        pass

    def execute(self):
        # Вызов алгоритма A*
        pass
