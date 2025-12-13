# File: art.py

from dataclasses import dataclass

from fie_trails.element import Element
from fie_trails.skill import Skill

@dataclass
class Art(Skill):
    element: Element
    delay: int