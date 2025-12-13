# File: skill.py

from abc import ABC
from dataclasses import dataclass

from enum import (
    IntFlag,
    auto
)


# Most Crafts only cost CP, and most Arts only cost EP. However, there are a few that
# take from different "currencies", potentially all three. So, we're representing the
# cost universally as a small dataclass.

@dataclass
class SkillCost:
    hp: int
    ep: int
    cp: int


class TargetType(IntFlag):
    CASTER = auto()
    ONE_ALLY = auto()
    MULTIPLE_ALLIES = auto()
    ALL_ALLIES = auto()
    ONE_ENEMY = auto()
    MULTIPLE_ENEMIES = auto()
    ALL_ENEMIES = auto()


class EffectType(IntFlag):
    DAMAGE = auto()
    HEAL = auto()


@dataclass
class SkillResult:
    targets: TargetType
    effect: EffectType
    strength: int


@dataclass
class Skill(ABC):
    name: str
    cost: SkillCost
    results: list[SkillResult]