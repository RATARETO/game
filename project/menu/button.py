import pygame


class Button:
    def __init__(self, x, y, width, height, text, font, passive_color, active_color, hover_color, action=None):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.text = text
        self.font = font

        self.active = False

        self.passive_color = passive_color  # цвет кнопки по умолчанию
        self.active_color = active_color  # цвет кнопки при нажатии
        self.hover_color = hover_color  # цвет кнопки при наведении

        self.color = self.passive_color

        self.action = action

    def update(self, inputs, positions):
        # TODO: вынести константы
        mouse_rect = pygame.Rect(positions[0], positions[1], 1, 1)  # прямоугольник мыши
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)  # прямоугольник кнопки

        self.active = False  # сбрасываем флаг нажатия

        self.color = self.passive_color
        if button_rect.colliderect(mouse_rect):
            self.color = self.hover_color
            if inputs.mouse_left_button:
                self.active = True
                self.color = self.active_color
                if self.action:
                    self.action()

    def draw(self, window):

        # рисуем блик сверху кнопки и тень снизу
        step = 4

        # TODO: вынести константы
        if self.active:
            pygame.draw.rect(window, (61, 76, 252), (self.x, self.y, self.width, self.height))
            pygame.draw.rect(window, self.color, (self.x, self.y, self.width - step, self.height - step))
        else:
            pygame.draw.rect(window, (172, 217, 248), (self.x, self.y, self.width, self.height))
            pygame.draw.rect(window, self.color, (self.x + step, self.y + step, self.width - step, self.height - step))

        # TODO: вынести константы
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))

        window.blit(text_surface, text_rect)
