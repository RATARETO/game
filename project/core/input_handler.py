import pygame
from project.command.history import History


class InputHandler:
    def __init__(self, history):
        self._mouse_left_button = False
        self._escape = False

        self._mouse_position = (0, 0)

        self.commands = {}

        self.commands_args = {}

        self.history = history

    def bind(self, key: int, command, **kwargs):
        self.commands[key] = command
        self.commands_args[command] = kwargs

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            # 1. Сначала обрабатываем специальные клавиши управления историей
            if event.key == pygame.K_z:
                self.history.undo()
                return  # ВАЖНО: выходим, чтобы не выполнять команду из словаря

            if event.key == pygame.K_y:
                self.history.redo()
                return  # ВАЖНО: выходим

            # 2. Затем обрабатываем обычные игровые команды
            if event.key in self.commands:
                command = self.commands[event.key]

                command_args = self.commands_args[command]

                if command is not None:
                    self.history.execute(command(**command_args))
                    print(command)

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

