import pygame


class InputHandler:
    def __init__(self):
        self._mouse_left_button = False
        self._escape = False

        self._mouse_position = (0, 0)

        self.commands = {}

    def bind(self, key: int, command):
        self.commands[key] = command

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.commands:
                command = self.commands[event.key]
                command.execute()

    def update(self):
        self._mouse_left_button = False
        self._escape = False

        self._mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self._escape = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._mouse_left_button = True

            self.handle_event(event)

    @property
    def escape(self):
        return self._escape

    @property
    def mouse_left_button(self):
        return self._mouse_left_button

    @property
    def mouse_position(self):
        return self._mouse_position

