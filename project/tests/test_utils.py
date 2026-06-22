from project.entities.entity import ModelEntity, ControllerEntity, Entity

# Заглушка для рендерера — не использует pygame


class DummyRenderer:
    def render(self, model):
        pass


def create_test_entity(name, x, y, health=3, damage=1, is_player=False, color=(255,0,0)):
    model = ModelEntity(x, y, health, damage, name, initiative=0, is_player=is_player)
    renderer = DummyRenderer()   # вместо RenderEntity(None, ...)
    controller = ControllerEntity(model)
    return Entity(model, renderer, controller)


def create_test_map():
    from project.map.map import Map
    return Map()


def create_test_player(x=5, y=5):
    return create_test_entity("player", x, y, health=5, damage=2, is_player=True, color=(0,255,0))


def create_test_enemy(x=6, y=5, health=3, damage=1):
    return create_test_entity("enemy", x, y, health, damage, is_player=False, color=(255,0,0))