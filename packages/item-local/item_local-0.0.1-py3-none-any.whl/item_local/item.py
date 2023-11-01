from abc import ABC, abstractmethod


class Item(ABC):
    @abstractmethod
    def display(self):
        pass
