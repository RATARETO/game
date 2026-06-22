from project.map.map import Map
from project.entities.entity import Entity


def remove_dead_entities_from_map(game_map: Map, all_entities: list):
    """
    Удаляет с карты и из списка врагов всех мёртвых сущностей.
    Возвращает список удалённых (entity, x, y) для восстановления.
    """
    removed = []
    for entity in all_entities:
        if entity.model.health <= 0:
            x, y = entity.model.tile_x, entity.model.tile_y
            if game_map.in_map(x, y) and game_map.get_point(x, y) is entity:
                game_map.remove_entity(entity)
                removed.append((entity, x, y))
    return removed


def restore_dead_entities(game_map: Map, removed_list: list):
    """
    Восстанавливает ранее удалённые мёртвые сущности на карту.
    """
    for entity, x, y in removed_list:
        if game_map.in_map(x, y):
            game_map.set_point(x, y, entity)
