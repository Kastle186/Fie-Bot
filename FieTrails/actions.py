# File: actions.py

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Action(ABC):
    name: str
    cost: int

    @abstractmethod
    def __str__(self):
        pass


@dataclass
class Craft(Action):
    damage: int

    def __str__(self):
        return f"{self.name} - {self.cost}CP - {self.damage}DMG"
