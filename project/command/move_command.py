from project.command.base_command import BaseCommand


class MoveCommand(BaseCommand):
    def __init__(self, direction):
        pass

    def execute(self):
        # Вызов алгоритма A*
        pass


class RightTurnCommand(BaseCommand):
    def __init__(self, entity_controller):
        self.entity_controller = entity_controller

    def execute(self):
        self.entity_controller.right_turn()


class LeftTurnCommand(BaseCommand):
    def __init__(self, entity_controller):
        self.entity_controller = entity_controller

    def execute(self):
        self.entity_controller.left_turn()


class PathFinding:
    def __init__(self):
        pass

    def execute(self):
        # Вызов алгоритма A*
        pass
