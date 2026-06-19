from abc import ABC, abstractmethod


class BaseCommand(ABC):
    @abstractmethod
    def __init__(self):
        self.applied = False

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

    @abstractmethod
    def redo(self):
        pass


