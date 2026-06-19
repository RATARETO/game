from project.command.base_command import BaseCommand


class AttackCommand(BaseCommand):
    def __init__(self, entity, game_map):
        self.applied = True

        self.entity = entity
        self.entity_model = self.entity.model
        self.entity_controller = self.entity.controller

        self.old_x = self.entity_model.tile_x
        self.old_y = self.entity_model.tile_y

        self.new_x = self.entity_model.tile_x
        self.new_y = self.entity_model.tile_y

        self.game_map = game_map

        # Переменные для отслеживания состояния
        self.attacker_moved = False

        self.target_entity = None
        self.target_x = 0
        self.target_y = 0

        self.target_damaged = False
        self.target_old_hp = 0
        self.target_new_hp = 0

        self.target_knocked_back = False
        self.knockback_new_x = 0
        self.knockback_new_y = 0

        # Отслеживание смерти и удаления цели
        self.target_died = False
        self.target_was_removed = False
        self.target_final_x = 0
        self.target_final_y = 0

    def execute(self):
        direction_map = {
            "up": (0, -1), "right": (1, 0),
            "down": (0, 1), "left": (-1, 0)
        }

        dx, dy = direction_map[self.entity_model.direction_of_view]

        self.target_x = self.entity_model.tile_x + dx
        self.target_y = self.entity_model.tile_y + dy

        target = self.game_map.get_point(self.target_x, self.target_y)

        # 1. Перемещение атакующего
        if (self.game_map.in_map(self.target_x, self.target_y) and target == 0):
            self.game_map.set_point(self.old_x, self.old_y, 0)
            self.entity_controller.move(self.target_x, self.target_y)
            self.game_map.set_point(self.target_x, self.target_y, self.entity)

            self.new_x, self.new_y = self.target_x, self.target_y
            self.attacker_moved = True
            self.applied = True

        # 2. Атака цели
        if not isinstance(target, int):
            self.target_entity = target
            self.target_old_hp = target.model.health

            target.controller.get_damage(self.entity_model.damage)

            self.target_new_hp = target.model.health
            self.target_damaged = True

            # Проверяем, умерла ли цель
            if self.target_new_hp <= 0:
                self.target_died = True

            # 3. Откидывание
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
                self.target_final_x = new_target_x
                self.target_final_y = new_target_y

                print(self.entity_model.name, "attacked")
            else:
                # Цель не была откинута, остаётся на месте
                self.target_final_x = self.target_x
                self.target_final_y = self.target_y

            # Проверяем, была ли цель удалена с карты после смерти
            # (это зависит от вашей реализации - может быть в get_damage или где-то ещё)
            current_on_map = self.game_map.get_point(self.target_final_x, self.target_final_y)
            if current_on_map != self.target_entity:
                self.target_was_removed = True

    def undo(self):
        # Откат в обратном порядке

        # Откат откидывания
        if self.target_knocked_back and self.target_entity:
            self.game_map.set_point(self.knockback_new_x, self.knockback_new_y, 0)
            self.target_entity.controller.move(self.target_x, self.target_y)
            self.game_map.set_point(self.target_x, self.target_y, self.target_entity)

        # Откат урона
        if self.target_damaged and self.target_entity:
            self.target_entity.model.health = self.target_old_hp

        # Если цель была удалена с карты, возвращаем её обратно
        if self.target_was_removed and self.target_entity:
            self.game_map.set_point(self.target_final_x, self.target_final_y, self.target_entity)

        # Откат перемещения атакующего
        if self.attacker_moved:
            self.game_map.set_point(self.new_x, self.new_y, 0)
            self.entity_controller.move(self.old_x, self.old_y)
            self.game_map.set_point(self.old_x, self.old_y, self.entity)

    def redo(self):
        # Применяем сохранённые изменения напрямую

        # 1. Перемещение атакующего
        if self.attacker_moved:
            self.game_map.set_point(self.old_x, self.old_y, 0)
            self.entity_controller.move(self.new_x, self.new_y)
            self.game_map.set_point(self.new_x, self.new_y, self.entity)

        # 2. Урон цели
        if self.target_damaged and self.target_entity:
            self.target_entity.model.health = self.target_new_hp

        # 3. Откидывание цели
        if self.target_knocked_back and self.target_entity:
            self.game_map.set_point(self.target_x, self.target_y, 0)
            self.target_entity.controller.move(self.knockback_new_x, self.knockback_new_y)
            self.game_map.set_point(self.knockback_new_x, self.knockback_new_y, self.target_entity)

        # Если цель была удалена, удаляем её снова
        if self.target_was_removed:
            self.game_map.set_point(self.target_final_x, self.target_final_y, 0)
            