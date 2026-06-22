class UI:
    def __init__(self, font, text):

        self.buttons = []

        # характеристики текста, который сообщает чей ход
        self.font = font
        self.text = text

        self.text_x, self.text_y = 25, 750
        self.text_width, self.text_height = 100, 50

    def set_text(self, text):
        self.text = text

    def _draw_text(self, window):
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(
            center=(self.text_x + self.text_width // 2, self.text_y + self.text_height // 2)
        )
        window.blit(text_surface, text_rect)

    def update(self, inputs, positions):
        for button in self.buttons:
            data = inputs, positions

            button.update(*data)

    def draw(self, window):
        for button in self.buttons:
            button.draw(window)

        self._draw_text(window)

    def add_button(self, button):
        self.buttons.append(button)
