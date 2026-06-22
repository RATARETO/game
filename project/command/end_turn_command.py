from project.command.base_command import BaseCommand


class EndTurnCommand(BaseCommand):
    def __init__(self, turn_manager, game_engine, entity):
        self.turn_manager = turn_manager
        self.game_engine = game_engine
        self.entity = entity
        self.applied = False

    def execute(self):
        if self.applied:
            return
        # Передаём ход следующему
        self.turn_manager.advance()
        current = self.turn_manager.get_current()
        self.game_engine.ui.set_text(f"Ходит: {current.model.name}" if current else "Очередь пуста")
        self.applied = True

    def undo(self):
        if not self.applied:
            return
        # Восстанавливаем текущего (упрощённо)
        self.turn_manager.set_current(self.entity)
        self.game_engine.ui.set_text(f"Ходит: {self.entity.model.name}")
        self.applied = False

    def redo(self):
        self.execute()
