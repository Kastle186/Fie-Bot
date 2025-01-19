# File: character.py

from actions import Art, Craft
from dataclasses import dataclass
from trailsutils import CharStatsMap, char_stats_str, init_blank_stats
from typing import Self

# Things we might add later on!
# - Status Ailments
# - Criticals
# - Arts and Crafts Delays
# - Elemental Weaknesses
# - Other Characters

@dataclass
class Equipment:
    pass

@dataclass
class Character:
    name: str
    level: int
    exp: int
    next_lv_exp: int
    stats: CharStatsMap
    equipment: Equipment
    crafts: list[Craft]
    arts: list[Art]

    def __init__(self: Self,
                 name_val: str = "unnamed_char",
                 level_val: int = -1,
                 exp_val: int = -1,
                 next_lv_val: int = -1,
                 stats_map: CharStatsMap = None,
                 equip_list: Equipment = None,
                 crafts_lst: list[Craft] = [],
                 arts_lst: list[Art] = []):

        self.name = name_val
        self.level = level_val
        self.exp = exp_val
        self.next_lv_exp = next_lv_val

        if stats_map is not None:
            self.stats = stats_map
        else:
            self.stats = init_blank_stats()

        # When we implement Equipment, we'll initialize it here.

        self.crafts = crafts_lst
        self.arts = arts_lst

    def __str__(self):
        res = f"CHARACTER:\n\nNAME: {self.name}\nLV: {self.level}\nEXP: {self.exp}\n"
        res += f"NEXT LV: {self.next_lv_exp}\n"
        res += f"\n{char_stats_str(self.stats)}\n"

        res += f"\nCRAFTS:"

        for craft in self.crafts:
            res += f"\n{craft}"

        res += f"\n\nARTS:"

        for art in self.arts:
            res += f"\n{art}"

        return res
