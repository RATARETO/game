class AttackCommand:
    def __init__(self, entity, game_map, controllers_entities):
        self.entity_controller = entity.controller
        self.entity_model = entity.model

        self.controllers_entities = controllers_entities

        self.game_map = game_map

        self.old_position = self.entity_model.tile_x, self.entity_model.tile_y

    def execute(self):
        direction_map = {
            "up": (0, -1),
            "right": (1, 0),
            "down": (0, 1),
            "left": (-1, 0)
        }
        dx, dy = direction_map[self.entity_model.direction_of_view]

        new_tile_x = self.entity_model.tile_x + dx
        new_tile_y = self.entity_model.tile_y + dy

        if self.game_map.in_map(new_tile_x, new_tile_y):
            if self.game_map.get_point(new_tile_x, new_tile_y) == 0:
                old_x, old_y = self.entity_model.tile_x, self.entity_model.tile_y

                self.game_map.set_point(old_x, old_y, 0)
                self.entity_controller.move(new_tile_x, new_tile_y)
                self.game_map.set_point(new_tile_x, new_tile_y, 1)

    def undo(self):
        direction_map = {
            "up": (0, 1),
            "right": (-1, 0),
            "down": (0, -1),
            "left": (1, 0)
        }
        dx, dy = direction_map[self.entity_model.direction_of_view]

        new_tile_x = self.entity_model.tile_x + dx
        new_tile_y = self.entity_model.tile_y + dy

        if self.game_map.in_map(new_tile_x, new_tile_y):
            if self.game_map.get_point(new_tile_x, new_tile_y) == 0:
                old_x, old_y = self.entity_model.tile_x, self.entity_model.tile_y

                self.game_map.set_point(old_x, old_y, 0)
                self.entity_controller.move(new_tile_x, new_tile_y)
                self.game_map.set_point(new_tile_x, new_tile_y, 1)
