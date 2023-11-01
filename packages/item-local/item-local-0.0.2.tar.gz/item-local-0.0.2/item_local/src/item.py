from abc import ABC, abstractmethod


# TOOD Shall we add @abstractmethod method id() -> int?
class Item(ABC):
    # TODO What is the diffrent between display and __STR__?
    @abstractmethod
    def display(self):
        pass
