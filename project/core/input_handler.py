import pygame


class InputHandler:
    def __init__(self, history):
        self._mouse_left_button = False
        self._escape = False
        self._mouse_position = (0, 0)
        self.commands = {}
        self.commands_args = {}
        self.action_bindings = {}
        self.history = history
        self._undo_performed = False
        self.pressed_keys = set()

    def bind(self, key: int, command, **kwargs):
        self.commands[key] = command
        self.commands_args[command] = kwargs

    def bind_action(self, key: int, func):
        self.action_bindings[key] = func

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                self.history.undo()
                self._undo_performed = True
                return
            if event.key == pygame.K_y:
                self.history.redo()
                return
            if event.key in self.commands:
                command = self.commands[event.key]
                command_args = self.commands_args[command]
                self.history.execute(command(**command_args))
            if event.key in self.action_bindings:
                self.action_bindings[event.key]()

    def update(self):
        self._undo_performed = False
        self._mouse_left_button = False
        self._escape = False
        self._mouse_position = pygame.mouse.get_pos()
        self.pressed_keys.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self._escape = True
            if event.type == pygame.KEYDOWN:
                self.pressed_keys.add(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._mouse_left_button = True
            self.handle_event(event)

    @property
    def escape(self): return self._escape
    @property
    def mouse_left_button(self): return self._mouse_left_button
    @property
    def mouse_position(self): return self._mouse_position
    @property
    def undo_performed(self): return self._undo_performed
