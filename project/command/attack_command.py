from project.command.base_command import BaseCommand
from project.utils.constants import DIRECTION_VECTORS
from project.utils.helpers import remove_dead_entities_from_map, restore_dead_entities


class AttackCommand(BaseCommand):
    def __init__(self, entity, game_map):
        self.entity = entity
        self.game_map = game_map
        self.model = entity.model
        self.controller = entity.controller
        self.applied = False

        self.old_x = self.model.tile_x
        self.old_y = self.model.tile_y
        self.new_x = self.model.tile_x
        self.new_y = self.model.tile_y

        self.target_entity = None
        self.target_x = 0
        self.target_y = 0
        self.target_old_hp = 0
        self.target_new_hp = 0
        self.target_knocked_back = False
        self.knockback_new_x = 0
        self.knockback_new_y = 0
        self.target_died = False
        self.attacker_moved = False
        self.removed_corpses = []

    def execute(self):
        if not self.controller.has_moves() or self.model.is_moving:
            return

        self.controller.set_is_moving(True, self.model.max_count_move)

        dx, dy = DIRECTION_VECTORS[self.model.direction_of_view]
        self.target_x = self.model.tile_x + dx
        self.target_y = self.model.tile_y + dy
        target = self.game_map.get_point(self.target_x, self.target_y)

        # Попытка движения вперёд (если пусто)
        if self.game_map.in_map(self.target_x, self.target_y) and target == 0:
            self.game_map.set_point(self.old_x, self.old_y, 0)
            self.controller.move(self.target_x, self.target_y)
            self.game_map.set_point(self.target_x, self.target_y, self.entity)
            self.new_x, self.new_y = self.target_x, self.target_y
            self.attacker_moved = True

        # Атака, если есть цель
        if not isinstance(target, int):
            self.target_entity = target
            self.target_old_hp = target.model.health
            target.controller.get_damage(self.model.damage)
            self.target_new_hp = target.model.health
            if self.target_new_hp <= 0:
                self.target_died = True
            # Отбрасывание, если цель жива
            if self.target_new_hp > 0:
                new_target_x = self.target_x + dx
                new_target_y = self.target_y + dy
                if (self.game_map.in_map(new_target_x, new_target_y) and
                        self.game_map.get_point(new_target_x, new_target_y) == 0):
                    self.game_map.set_point(self.target_x, self.target_y, 0)
                    target.controller.move(new_target_x, new_target_y)
                    self.game_map.set_point(new_target_x, new_target_y, target)
                    self.target_knocked_back = True
                    self.knockback_new_x = new_target_x
                    self.knockback_new_y = new_target_y

        self.controller.use_move()
        # Удаляем мёртвых (включая возможных жертв)
        all_entities = [self.entity] + [self.target_entity] if self.target_entity else [self.entity]
        self.removed_corpses = remove_dead_entities_from_map(self.game_map, all_entities)
        self.applied = True

    def undo(self):
        # Восстанавливаем мёртвых (включая возможную жертву)
        restore_dead_entities(self.game_map, self.removed_corpses)
        self.removed_corpses = []

        self.controller.set_is_moving(False, self.model.max_count_move)

        if self.attacker_moved:
            self.game_map.set_point(self.new_x, self.new_y, 0)
            self.controller.move(self.old_x, self.old_y)
            self.game_map.set_point(self.old_x, self.old_y, self.entity)

        if self.target_entity:
            # Восстанавливаем здоровье цели всегда
            self.target_entity.model.health = self.target_old_hp

            # Если цель не умерла, но была отброшена – возвращаем на место
            if not self.target_died and self.target_knocked_back:
                self.game_map.set_point(self.knockback_new_x, self.knockback_new_y, 0)
                self.target_entity.controller.move(self.target_x, self.target_y)
                self.game_map.set_point(self.target_x, self.target_y, self.target_entity)
            elif self.target_died:
                # Если цель умерла, она была удалена с карты и восстановлена через restore_dead_entities,
                # но её здоровье уже восстановлено выше.
                pass

        self.applied = False

    def redo(self):
        self.execute()