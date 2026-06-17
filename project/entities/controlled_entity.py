import pygame

from project.entities.base_entity import BaseEntity, BaseEntityRenderer, BaseEntityController
from project.settings import TILE_SIZE


class ControllerControlledEntity(BaseEntityController):
    def __init__(self, entity):
        super().__init__(entity)
        self.player = entity

    def _set_direction_of_view(self):
        self.player.direction_of_view = self.player.directions_of_view[self.player.start_index_direction_of_view]

    def right_turn(self):
        self.player.start_index_direction_of_view = (self.player.start_index_direction_of_view + 1) % 4
        self._set_direction_of_view()

    def left_turn(self):
        self.player.start_index_direction_of_view = (self.player.start_index_direction_of_view - 1) % 4
        self._set_direction_of_view()

    def update(self):
        print("update")


class RenderControlledEntity:
    def __init__(self, window):
        self.window = window

    def _draw_direction_of_view(self, player):
        direction = player.direction_of_view

        polygon_color = (255, 255, 255)
        offset = player.size // 4

        if direction == "up":
            pygame.draw.polygon(self.window, polygon_color, (
                (player.tile_x * TILE_SIZE + player.size // 2, player.tile_y * TILE_SIZE + offset),
                (player.tile_x * TILE_SIZE + player.size - offset, player.tile_y * TILE_SIZE + player.size - offset),
                (player.tile_x * TILE_SIZE + offset, player.tile_y * TILE_SIZE + player.size - offset)
            ))
        if direction == "right":
            pygame.draw.polygon(self.window, polygon_color, (
                (player.tile_x * TILE_SIZE + player.size - offset, player.tile_y * TILE_SIZE + player.size // 2),
                (player.tile_x * TILE_SIZE + offset, player.tile_y * TILE_SIZE + offset),
                (player.tile_x * TILE_SIZE + offset, player.tile_y * TILE_SIZE + player.size - offset)
            ))
        if direction == "down":
            pygame.draw.polygon(self.window, polygon_color, (
                (player.tile_x * TILE_SIZE + offset, player.tile_y * TILE_SIZE + offset),
                (player.tile_x * TILE_SIZE + player.size - offset, player.tile_y * TILE_SIZE + offset),
                (player.tile_x * TILE_SIZE + player.size // 2, player.tile_y * TILE_SIZE + player.size - offset)
            ))
        if direction == "left":
            pygame.draw.polygon(self.window, polygon_color, (
                (player.tile_x * TILE_SIZE + offset, player.tile_y * TILE_SIZE + player.size // 2),
                (player.tile_x * TILE_SIZE + player.size - offset, player.tile_y * TILE_SIZE + offset),
                (player.tile_x * TILE_SIZE + player.size - offset, player.tile_y * TILE_SIZE + player.size - offset)
            ))

    def render(self, player):
        pygame.draw.rect(
            self.window,
            player.color,
            (
                player.tile_x * TILE_SIZE,
                player.tile_y * TILE_SIZE,
                player.size, player.size))

        self._draw_direction_of_view(player)


class ModelControlledEntity(BaseEntity):
    """Модель сущности, управляемой игроком"""
    def __init__(
            self,
            tile_x, tile_y, size, color,
            health, damage):

        super().__init__(tile_x, tile_y, size, health, damage)

        self.directions_of_view = ["up", "right", "down", "left"]
        self.start_index_direction_of_view = 0
        self.direction_of_view = self.directions_of_view[self.start_index_direction_of_view]

        self.tile_x = tile_x
        self.tile_y = tile_y

        self.color = color

        self.size = size

        self.health = health
        self.damage = damage


class ControlledEntity:
    def __init__(self, model, renderer, controller):
        self.model = model

        self.renderer = renderer
        self.controller = controller



