from abc import ABC, abstractmethod


class Item(ABC):
    @abstractmethod
    def get_id(self):
        pass

    def __str__(self):
        return f"Item id= {self.get_id()}"
