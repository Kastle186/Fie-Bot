import enum


class Art:
    def __init__(self, name: str, damage: int, cost: int, element: enum):
        self.name = name
        self.damage = damage
        self.cost = cost
        self.element = element


    def __str__(self):
        return self.name + " - " + str(self.cost) + " EP"