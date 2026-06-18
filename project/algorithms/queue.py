class Queue:
    def __init__(self, entities):
        self.entities = entities

        self.index_entity = 0
        self.next_entity = self.entities[self.index_entity]  # добавить очередь с приоритетами

    def next_motion(self):
        self.index_entity = (self.index_entity + 1) % len(self.entities)
        self.next_entity = self.entities[self.index_entity]

