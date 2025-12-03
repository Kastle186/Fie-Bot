import enum
from fie_trails.art import Art

# Same enum thingy lol.

class Orbment:
    def __init__(self, name: str, status_change: int, element: enum, art_produced: Art = None):
        self.name = name
        self.status_change = status_change
        self.element = element
        self.art_produced = art_produced


    def __str__(self):
        return self.name + " (" + str(self.art_produced) + " )"