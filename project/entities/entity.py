import pygame
from project.settings import TILE_SIZE, MAP_START_X, MAP_START_Y, MAP_WEIGHT, MAP_HEIGHT


class ModelEntity:
    """Модель сущности, управляемой игроком"""

    def __init__(self, tile_x, tile_y, size, color, health, damage, name):
        # tile_x, tile_y — координаты ВНУТРИ сетки (0..MAP_WEIGHT-1, 0..MAP_HEIGHT-1)
        self.tile_x = tile_x
        self.tile_y = tile_y

        self.directions_of_view = ["up", "right", "down", "left"]
        self.start_index_direction_of_view = 0
        self.direction_of_view = self.directions_of_view[self.start_index_direction_of_view]

        self.color = color
        self.size = size
        self.health = health
        self.damage = damage
        self.is_moving = False
        self.name = name


class RenderEntity:
    def __init__(self, window):
        self.window = window
        self._name_font = pygame.font.SysFont(None, 20)

    def _get_pixel_position(self, tile_x, tile_y):
        """Преобразует координаты сетки в пиксельные координаты"""
        px = (MAP_START_X + tile_x) * TILE_SIZE
        py = (MAP_START_Y + tile_y) * TILE_SIZE
        return px, py

    def _draw_name(self, player):
        px, py = self._get_pixel_position(player.tile_x, player.tile_y)
        text_surface = self._name_font.render(player.name, True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            center=(px + player.size // 2, py - 5)
        )
        self.window.blit(text_surface, text_rect)

    def _draw_direction_of_view(self, player):
        px, py = self._get_pixel_position(player.tile_x, player.tile_y)
        direction = player.direction_of_view
        polygon_color = (255, 255, 255)
        offset = player.size // 4

        if direction == "up":
            points = [
                (px + player.size // 2, py + offset),
                (px + player.size - offset, py + player.size - offset),
                (px + offset, py + player.size - offset)
            ]
        elif direction == "right":
            points = [
                (px + player.size - offset, py + player.size // 2),
                (px + offset, py + offset),
                (px + offset, py + player.size - offset)
            ]
        elif direction == "down":
            points = [
                (px + offset, py + offset),
                (px + player.size - offset, py + offset),
                (px + player.size // 2, py + player.size - offset)
            ]
        elif direction == "left":
            points = [
                (px + offset, py + player.size // 2),
                (px + player.size - offset, py + offset),
                (px + player.size - offset, py + player.size - offset)
            ]
        else:
            points = []

        if points:
            pygame.draw.polygon(self.window, polygon_color, points)

    def render(self, player):
        px, py = self._get_pixel_position(player.tile_x, player.tile_y)
        pygame.draw.rect(
            self.window,
            player.color,
            (px, py, player.size, player.size)
        )
        self._draw_direction_of_view(player)
        self._draw_name(player)


class ControllerEntity:
    def __init__(self, entity):
        self.player = entity

    def _set_direction_of_view(self):
        self.player.direction_of_view = self.player.directions_of_view[
            self.player.start_index_direction_of_view
        ]

    def right_turn(self):
        self.player.start_index_direction_of_view = (self.player.start_index_direction_of_view + 1) % 4
        self._set_direction_of_view()

    def left_turn(self):
        self.player.start_index_direction_of_view = (self.player.start_index_direction_of_view - 1) % 4
        self._set_direction_of_view()

    def move(self, end_tile_x, end_tile_y):
        self.player.tile_x = end_tile_x
        self.player.tile_y = end_tile_y

    def move_straight_ahead(self, game_map):
        pass

    def attack(self, entities):
        pass


class ControlledEntity:
    def __init__(self, model, renderer, controller):
        self.model = model
        self.renderer = renderer
        self.controller = controller
