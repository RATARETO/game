import pygame


class Game:
    def __init__(self, window, input_handler, menu, controller, grid, ui, queue, map):

        self.window = window
        self.clock = pygame.time.Clock()

        self.input_handler = input_handler

        self.menu = menu

        self.controller = controller

        self.grid = grid

        self.ui = ui
        self.queue = queue

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

                for enemy in self.map.enemies:

                    if enemy.model.health <= 0:
                        self.map.set_point(enemy.model.tile_x, enemy.model.tile_y, 0)

                if self.input_handler.escape:
                    self.controller.state = "menu"

                # отрисовка
                self.grid.draw()
                self.ui.draw(self.window)

                for enemy in self.map.enemies:
                    enemy.renderer.render(enemy.model)

            if self.controller.state == "game over":
                pass

            if self.controller.state == "exit":
                pygame.quit()
                exit()

            pygame.display.update()
            self.clock.tick(60)


