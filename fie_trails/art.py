# "enum" is not what you want to annotate. "enum" is the module. What you want
# is the type "Enum".
# Change this import to "from enum import Enum"
import enum


class Art:
    # And then change "element: enum" to "element: Enum".
    def __init__(self, name: str, damage: int, cost: int, element: enum):
        self.name = name
        self.damage = damage
        self.cost = cost
        self.element = element


    def __str__(self):
        return self.name + " - " + str(self.cost) + " EP"