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

class Stat(Enum):
    HP  = 1
    EP  = 2
    CP  = 3
    STR = 4
    DEF = 5
    ATS = 6
    ADF = 7
    SPD = 8
    DEX = 9
    AGL = 10

type StatTuple = tuple[Stat, float]
type CharStatsMap = dict[Stat, float]

def init_blank_stats() -> CharStatsMap:
    zero_stats = {
        Stat.HP:  0,
        Stat.EP:  0,
        Stat.CP:  0,
        Stat.STR: 0,
        Stat.DEF: 0,
        Stat.ATS: 0,
        Stat.ADF: 0,
        Stat.SPD: 0,
        Stat.DEX: 0,
        Stat.AGL: 0
    }
    return zero_stats

def char_stats_str(stats: CharStatsMap) -> str:
    return (f"HP:  {stats[Stat.HP]}\n"
            f"EP:  {stats[Stat.EP]}\n"
            f"CP:  {stats[Stat.CP]}\n"
            f"STR: {stats[Stat.STR]}\n"
            f"DEF: {stats[Stat.DEF]}\n"
            f"ATS: {stats[Stat.ATS]}\n"
            f"ADF: {stats[Stat.ADF]}\n"
            f"SPD: {stats[Stat.SPD]}\n"
            f"DEX: {stats[Stat.DEX]}\n"
            f"AGL: {stats[Stat.AGL]}")
