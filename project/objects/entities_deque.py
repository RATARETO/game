import pygame

from project.settings import ConfigurationProject

config = ConfigurationProject()


class EntitiesDeque:
    def __init__(self, entities):
        self.entities = entities  # max 18

        self.size = 50

    def draw(self, screen):
        first_entity = self.entities[0]
        pygame.draw.rect(
            screen,
            first_entity.color,
            (25, 25, 100, 100)
        )

        start_weight, start_height = 3.0, 0.5

        for n, entity in enumerate(self.entities[1:]):
            # потом иконки буду брать
            pygame.draw.rect(
                screen,
                entity.color,
                (
                    (start_weight + n) * config.TILE_SIZE + n,
                    start_height * config.TILE_SIZE,
                    self.size,
                    self.size
                )
            )


class ParameterInterface:
    pass


class EntitiesInterface:
    pass
