# File: character.py

from actions import Art, Craft
from dataclasses import dataclass

# Things we might add later on!
# - Status Ailments
# - Criticals
# - Arts and Crafts Delays
# - Elemental Weaknesses
# - Other Characters

@dataclass
class Character:
    name: str
    level: int
    exp: int
    next_lv_exp: int

    hp: int
    ep: int
    cp: int

    stats: CharStats
    equipment: CharEquipment
    crafts: list[Craft]
    arts: list[Art]


@dataclass
class CharStats:
    strength: int
    defense: int
    arts_strength: int
    arts_defense: int
    speed: int
    dexterity: int
    agility: int

    def accurracy() -> float:
        pass

    def evasion() -> float:
        pass


@dataclass
class CharEquipment:
    pass
