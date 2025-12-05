class Craft:
    def __init__(self, name: str, damage: int, cost: int):
        self.name = name
        self.damage = damage
        self.cost = cost

    def __str__(self):
        return f"{self.name} - {self.cost} CP"

