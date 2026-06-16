class MainMenu:
    def __init__(self, start_button, load_button, author_button, exit_button):
        self.start_button = start_button
        self.load_button = load_button
        self.author_button = author_button
        self.exit_button = exit_button

    def update(self, inputs, positions):
        data = inputs, positions

        self.start_button.update(*data)
        self.exit_button.update(*data)
        self.author_button.update(*data)
        self.load_button.update(*data)

    def draw(self, window):
        self.start_button.draw(window)
        self.exit_button.draw(window)
        self.author_button.draw(window)
        self.load_button.draw(window)

