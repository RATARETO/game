import pygame


class Game:
    def __init__(self, window, input_handler, menu, controller, grid, controlled_entities, ui, queue, enemies, map):

        self.window = window
        self.clock = pygame.time.Clock()

        self.input_handler = input_handler

        self.menu = menu

        self.controller = controller

        self.grid = grid

        self.controlled_entities = controlled_entities

        self.ui = ui
        self.queue = queue

        self.enemies = enemies

        self.map = map

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
                self.ui.update(self.input_handler, self.input_handler.mouse_position)

                if self.input_handler.escape:
                    self.controller.state = "menu"
                # отрисовка
                self.grid.draw()
                self.ui.draw(self.window)

                for controlled_entity in self.controlled_entities:
                    controlled_entity.renderer.render(controlled_entity.model)
                    # print(controlled_entity[0].start_index_direction_of_view)

                for enemy in self.enemies:
                    enemy.renderer.render(enemy.model)

            if self.controller.state == "game over":
                pass

            if self.controller.state == "exit":
                pygame.quit()
                exit()

            pygame.display.update()
            self.clock.tick(60)


