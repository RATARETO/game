class History:
    def __init__(self):
        self._stack_undo = []
        self._stack_redo = []

    def execute(self, command):
        command.execute()
        if command.applied:
            self._stack_undo.append(command)
            self._stack_redo.clear()

    def undo(self):
        if not self._stack_undo:
            return
        command = self._stack_undo.pop()
        command.undo()
        self._stack_redo.append(command)

    def redo(self):
        if not self._stack_redo:
            return
        command = self._stack_redo.pop()
        command.redo()
        self._stack_undo.append(command)
