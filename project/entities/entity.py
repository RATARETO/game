import pygame
from project.settings import TILE_SIZE, MAP_START_X, MAP_START_Y
from project.utils.constants import DIRECTIONS


class ModelEntity:
    """Модель – только данные, без визуальных атрибутов."""
    def __init__(self, tile_x, tile_y, health, damage, name, initiative=0, is_player=False):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.health = health
        self.damage = damage
        self.name = name
        self.is_player = is_player

        self.directions_of_view = DIRECTIONS[:]
        self.start_index_direction_of_view = 0
        self.direction_of_view = self.directions_of_view[0]

        self.maximum_initiative = initiative
        self.initiative = initiative
        self.max_count_move = 1
        self.count_move = 1
        self.is_moving = False


class RenderEntity:
    """Отвечает только за отрисовку, содержит визуальные параметры."""
    def __init__(self, window, color, size=TILE_SIZE):
        self.window = window
        self.color = color
        self.size = size
        self._name_font = pygame.font.SysFont(None, 20)

    def _get_pixel_position(self, tile_x, tile_y):
        px = (MAP_START_X + tile_x) * TILE_SIZE
        py = (MAP_START_Y + tile_y) * TILE_SIZE
        return px, py

    def _draw_name(self, model):
        px, py = self._get_pixel_position(model.tile_x, model.tile_y)
        text_surface = self._name_font.render(model.name, True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            center=(px + self.size // 2, py - 5)
        )
        self.window.blit(text_surface, text_rect)

    def _draw_direction(self, model):
        px, py = self._get_pixel_position(model.tile_x, model.tile_y)
        direction = model.direction_of_view
        polygon_color = (255, 255, 255)
        offset = self.size // 4
        points = []
        if direction == "up":
            points = [
                (px + self.size // 2, py + offset),
                (px + self.size - offset, py + self.size - offset),
                (px + offset, py + self.size - offset)
            ]
        elif direction == "right":
            points = [
                (px + self.size - offset, py + self.size // 2),
                (px + offset, py + offset),
                (px + offset, py + self.size - offset)
            ]
        elif direction == "down":
            points = [
                (px + offset, py + offset),
                (px + self.size - offset, py + offset),
                (px + self.size // 2, py + self.size - offset)
            ]
        elif direction == "left":
            points = [
                (px + offset, py + self.size // 2),
                (px + self.size - offset, py + offset),
                (px + self.size - offset, py + self.size - offset)
            ]
        if points:
            pygame.draw.polygon(self.window, polygon_color, points)

    def render(self, model):
        px, py = self._get_pixel_position(model.tile_x, model.tile_y)
        pygame.draw.rect(self.window, self.color, (px, py, self.size, self.size))
        self._draw_direction(model)
        self._draw_name(model)


class ControllerEntity:
    """Управляет состоянием модели (поворот, движение, урон)."""
    def __init__(self, model):
        self.model = model

    def _set_direction_of_view(self):
        self.model.direction_of_view = self.model.directions_of_view[
            self.model.start_index_direction_of_view
        ]

    def right_turn(self):
        self.model.start_index_direction_of_view = (self.model.start_index_direction_of_view + 1) % 4
        self._set_direction_of_view()

    def left_turn(self):
        self.model.start_index_direction_of_view = (self.model.start_index_direction_of_view - 1) % 4
        self._set_direction_of_view()

    def move(self, end_tile_x, end_tile_y):
        self.model.tile_x = end_tile_x
        self.model.tile_y = end_tile_y

    def get_damage(self, damage):
        self.model.health -= damage

    def set_is_moving(self, value, max_move):
        self.model.count_move = max_move
        self.model.is_moving = value

    # Управление ходами
    def has_moves(self):
        return self.model.count_move > 0

    def use_move(self):
        if self.model.count_move > 0:
            self.model.count_move -= 1

    def restore_move(self):
        self.model.count_move += 1

    def reset_moves(self):
        self.model.count_move = self.model.max_count_move

    def is_dead(self):
        return self.model.health <= 0


class Entity:
    """Составная сущность: модель + рендерер + контроллер."""
    def __init__(self, model, renderer, controller):
        self.model = model
        self.renderer = renderer
        self.controller = controller

    def __repr__(self):
        return self.model.name
