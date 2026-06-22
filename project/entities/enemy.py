from project.algorithms.minimax import find_best_action
from project.command.move_command import MoveCommand
from project.command.attack_command import AttackCommand


class EnemyAI:
    def __init__(self, entity, game_map, player, enemies, turn_order):
        self.entity = entity
        self.game_map = game_map
        self.player = player
        self.enemies = enemies
        self.turn_order = turn_order

    def take_turn(self, turn_index, depth=3):
        result = find_best_action(
            self.entity, self.game_map, self.player,
            self.enemies, self.turn_order, turn_index, depth
        )
        if result is None:
            return None
        direction, command_cls = result
        model = self.entity.model
        model.direction_of_view = direction
        model.start_index_direction_of_view = model.directions_of_view.index(direction)

        return command_cls(self.entity, self.game_map)