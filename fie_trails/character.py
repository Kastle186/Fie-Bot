# File: character.py

from dataclasses import dataclass, field

from fie_trails.art import Art
from fie_trails.craft import Craft


@dataclass
class Stat:
    name: str
    base_value: int
    growth_per_level: int
    current_value: int = field(init=False)

    def __post_init__(self):
        # Initializing this to its Level 1 value by default.
        self.current_value = self.base_value + self.growth_per_level

    def set_to_level(self, level: int):
        self.current_value = self.base_value + (self.growth_per_level * level)


@dataclass
class CharacterStats:
    HP: Stat
    EP: int
    CP: int
    LV: int

    STR: Stat = field(init=False)
    DEF: Stat = field(init=False)
    ATS: Stat = field(init=False)
    ADF: Stat = field(init=False)
    DEX: Stat = field(init=False)
    AGL: Stat = field(init=False)
    SPD: Stat = field(init=False)


    def __post_init__(self):
        # Read the stats values from the file here, and calculate their `current_value`
        # according to the `LV` value by calling `self._update_stats()`, if LV is
        # different from 1.
        pass


    def __setattr__(self, key, value):
        super().__setattr__(key, value)

        # Automatically update the stats so the game code doesn't have to do it
        # when the level changes.
        if key == 'LV' and getattr(self, key, None) != value:
            self._update_stats()


    def _update_stats(self) -> None:
        self.STR.set_to_level(self.LV)
        self.DEF.set_to_level(self.LV)
        self.ATS.set_to_level(self.LV)
        self.ADF.set_to_level(self.LV)
        self.DEX.set_to_level(self.LV)
        self.AGL.set_to_level(self.LV)
        self.SPD.set_to_level(self.LV)


class Character:
    name: str
    crafts: list[Craft]
    arts: list[Art]
    stats: CharacterStats

    def __init__(self):
        # Read data from files here.
        pass