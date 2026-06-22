from project.algorithms.queue import Queue


class TurnManager:
    def __init__(self, all_entities):
        self.all_entities = all_entities
        self.queue = Queue()
        self.current_entity = None
        self._rebuild_queue()

    def _rebuild_queue(self):
        """Собирает очередь из живых сущностей, сбрасывает ходы."""
        self.queue = Queue()
        for entity in self.all_entities:
            if entity.model.health > 0:
                entity.controller.reset_moves()
                entity.model.is_moving = False
                self.queue.push(entity)
        self.current_entity = self.queue.first_motion()

    def advance(self):
        """Переход к следующему ходу."""
        if self.queue.is_empty():
            self._rebuild_queue()
        else:
            self.queue.pop()
            if self.queue.is_empty():
                self._rebuild_queue()
            else:
                self.current_entity = self.queue.first_motion()

    def get_current(self):
        return self.current_entity

    def set_current(self, entity):
        """Принудительно установить текущего (используется при загрузке)."""
        self.current_entity = entity