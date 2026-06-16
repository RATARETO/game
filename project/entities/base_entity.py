class BaseEntityController:
    def __init__(self, entity):
        self.entity = entity

    def update(self):
        pass


class BaseEntityRenderer:
    def __init__(self, entity):
        self.entity = entity

    def render(self, screen):
        pass


class BaseEntity:
    def __init__(self, tile_x, tile_y, size, health, damage):
        self.tile_x = tile_x
        self.tile_y = tile_y

        self.size = size

        self.health = health  # компоненты здоровья
        self.damage = damage  # компоненты нанесения урона


