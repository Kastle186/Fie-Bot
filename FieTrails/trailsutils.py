# File: trailsutils.py

from dataclasses import dataclass
from enum import Enum

class Element(Enum):
    EARTH = 1
    WATER = 2
    FIRE = 3
    WIND = 4
    TIME = 5
    SPACE = 6
    MIRAGE = 7

@dataclass
class VitalityStats:
    health_points: int
    energy_points: int
    craft_points: int

    def __str__(self) -> str:
        return (f"HP: {self.health_points}\n"
                f"EP: {self.energy_points}\n"
                f"CP: {self.craft_points}")
