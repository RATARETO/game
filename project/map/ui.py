class UI:
    def __init__(self):

        self.buttons = []

    def update(self, inputs, positions):
        for button in self.buttons:
            data = inputs, positions

            button.update(*data)

    def draw(self, window):
        for button in self.buttons:
            button.draw(window)

    def add_button(self, button):
        self.buttons.append(button)
