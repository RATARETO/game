import pygame
from project.menu.button import Button

from project.core.input_handler import InputHandler


class Game:
    def __init__(self, window, input_handler, menu, controller, grid, controlled_entities):

        self.window = window
        self.clock = pygame.time.Clock()

        self.input_handler = input_handler

        self.menu = menu

        self.controller = controller

        self.grid = grid

        self.controlled_entities = controlled_entities

    def run(self):
        while True:
            self.window.fill((0, 0, 0))
            # обработка ввода
            self.input_handler.update()

            if self.controller.state == "menu":
                # обработка логики
                self.menu.update(self.input_handler, self.input_handler.mouse_position)

                if self.input_handler.escape:
                    self.controller.state = "exit"

                # отрисовка
                self.menu.draw(self.window)

            if self.controller.state == "game":
                # обработка логики
                if self.input_handler.escape:
                    self.controller.state = "menu"
                # отрисовка
                self.grid.draw()

                for controlled_entity in self.controlled_entities:
                    controlled_entity.renderer.render(controlled_entity.model)
                    # print(controlled_entity[0].start_index_direction_of_view)

            if self.controller.state == "game over":
                pass

            if self.controller.state == "exit":
                pygame.quit()
                exit()

            pygame.display.update()
            self.clock.tick(60)


