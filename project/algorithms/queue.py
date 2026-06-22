class Queue:
    def __init__(self, entities=None):
        self._queue = list(entities) if entities else []
        self._history = []

    def push(self, entity):
        self._queue.append(entity)

    def pop(self):
        if self._queue:
            entity = self._queue.pop(0)
            self._history.append(entity)
            return entity
        return None

    def first_motion(self):
        return self._queue[0] if self._queue else None

    def is_empty(self):
        return len(self._queue) == 0

    def next_motion(self):
        if not self.is_empty():
            self.pop()

    def get_all_entities(self):
        return self._history.copy()

    def clear_history(self):
        self._history.clear()

    def restore_entity(self, entity):
        if entity in self._history:
            for i in range(len(self._history) - 1, -1, -1):
                if self._history[i] == entity:
                    self._queue.insert(i, entity)
                    self._history.pop(i)
                    return True
        self._queue.insert(0, entity)
        return True

    def remove_entity_from_history(self, entity):
        if entity in self._history:
            self._history.remove(entity)

    def restore_to_front(self, entity):
        if entity in self._queue:
            self._queue.remove(entity)
        self._queue.insert(0, entity)