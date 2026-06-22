from project.utils.constants import DIRECTION_VECTORS
from project.utils.helpers import remove_dead_entities_from_map, restore_dead_entities
from project.command.move_command import MoveCommand
from project.command.attack_command import AttackCommand
from project.settings import AI_DEPTH, EVAL_ENEMY_HEALTH_WEIGHT, EVAL_PLAYER_HEALTH_WEIGHT, EVAL_DISTANCE_WEIGHT


class SimulatedAction:
    """Обёртка для симуляции хода без записи в историю."""
    def __init__(self, entity, game_map, direction, command_cls):
        self.entity = entity
        self.game_map = game_map
        self.direction = direction
        self.command_cls = command_cls

        self._old_direction = None
        self._old_index = None
        self._command = None
        self._removed_corpses = []

    def execute(self, all_entities):
        model = self.entity.model
        self._old_direction = model.direction_of_view
        self._old_index = model.start_index_direction_of_view

        model.direction_of_view = self.direction
        model.start_index_direction_of_view = model.directions_of_view.index(self.direction)

        self._command = self.command_cls(self.entity, self.game_map)
        self._command.execute()
        self._removed_corpses = remove_dead_entities_from_map(self.game_map, all_entities)

    def undo(self):
        restore_dead_entities(self.game_map, self._removed_corpses)
        if self._command:
            self._command.undo()

        model = self.entity.model
        model.direction_of_view = self._old_direction
        model.start_index_direction_of_view = self._old_index


def generate_legal_actions(actor, game_map, opponents):
    """Генерирует все допустимые действия (движение или атака)."""
    model = actor.model
    opponents_set = set(opponents)
    actions = []

    for direction, (dx, dy) in DIRECTION_VECTORS.items():
        tx, ty = model.tile_x + dx, model.tile_y + dy
        if not game_map.in_map(tx, ty):
            continue
        target = game_map.get_point(tx, ty)
        if target == 0:
            actions.append(SimulatedAction(actor, game_map, direction, MoveCommand))
        elif not isinstance(target, int) and target in opponents_set:
            actions.append(SimulatedAction(actor, game_map, direction, AttackCommand))
    return actions


def evaluate(player, enemies):
    """Оценочная функция для минимакса."""
    alive_enemies = [e for e in enemies if e.model.health > 0]
    enemy_health = sum(e.model.health for e in alive_enemies)
    player_health = max(player.model.health, 0)

    score = enemy_health * EVAL_ENEMY_HEALTH_WEIGHT - player_health * EVAL_PLAYER_HEALTH_WEIGHT

    if alive_enemies and player.model.health > 0:
        avg_dist = sum(
            abs(e.model.tile_x - player.model.tile_x) +
            abs(e.model.tile_y - player.model.tile_y)
            for e in alive_enemies
        ) / len(alive_enemies)
        score -= avg_dist * EVAL_DISTANCE_WEIGHT
    return score


def minimax(game_map, player, enemies, turn_order, turn_index, depth, alpha, beta):
    """Минимакс с альфа-бета отсечением."""
    all_entities = enemies + [player]

    if depth == 0 or player.model.health <= 0 or all(e.model.health <= 0 for e in enemies):
        return evaluate(player, enemies)

    if turn_index >= len(turn_order):
        return evaluate(player, enemies)

    actor = turn_order[turn_index]
    if actor.model.health <= 0:
        return minimax(game_map, player, enemies, turn_order, turn_index + 1, depth - 1, alpha, beta)

    is_enemy_turn = actor in enemies
    opponents = [player] if is_enemy_turn else enemies

    actions = generate_legal_actions(actor, game_map, opponents)
    if not actions:
        return minimax(game_map, player, enemies, turn_order, turn_index + 1, depth - 1, alpha, beta)

    if is_enemy_turn:
        value = float("-inf")
        for action in actions:
            action.execute(all_entities)
            value = max(value, minimax(game_map, player, enemies, turn_order, turn_index + 1, depth - 1, alpha, beta))
            action.undo()
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float("inf")
        for action in actions:
            action.execute(all_entities)
            value = min(value, minimax(game_map, player, enemies, turn_order, turn_index + 1, depth - 1, alpha, beta))
            action.undo()
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


def find_best_action(actor, game_map, player, enemies, turn_order, turn_index, depth=AI_DEPTH):
    """Находит лучшее действие для актора."""
    opponents = enemies if actor.model.is_player else [player]
    actions = generate_legal_actions(actor, game_map, opponents)
    if not actions:
        return None

    is_player_turn = actor.model.is_player
    best_value = float("inf") if is_player_turn else float("-inf")
    best_action = None
    alpha, beta = float("-inf"), float("inf")
    all_entities = enemies + [player]

    for action in actions:
        action.execute(all_entities)
        value = minimax(game_map, player, enemies, turn_order, turn_index + 1, depth - 1, alpha, beta)
        action.undo()

        if is_player_turn:
            # Игрок минимизирует
            if value < best_value:
                best_value = value
                best_action = action
            beta = min(beta, value)
        else:
            # Враг максимизирует
            if value > best_value:
                best_value = value
                best_action = action
            alpha = max(alpha, value)

        if alpha >= beta:
            break

    if best_action:
        return best_action.direction, best_action.command_cls
    return None
