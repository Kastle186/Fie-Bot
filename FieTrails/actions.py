# File: actions.py

from abc import ABC, abstractmethod
from trailsutils import Element, StatTuple
from typing import Self

class Action(ABC):
    name: str
    cost: int
    delay: int
    effects: list[StatTuple]

    @abstractmethod
    def __init__(self: Self,
                 name_val: str,
                 cost_val: int,
                 delay_val: int,
                 effects_lst: list[StatTuple]):

        self.name = name_val
        self.cost = cost_val
        self.delay = delay_val
        self.effects = effects_lst

    @abstractmethod
    def __str__(self) -> str:
        res = f"NAME: {self.name}\nCOST: {self.cost}\nDELAY: {self.delay}"

        for eff in self.effects:
            res += f"\n{eff[0]}: {eff[1]}"

        return res


class Art(Action):
    element: Element

    def __init__(self: Self,
                 elem: Element,
                 name_val: str = "unnamed_art",
                 cost_val: int = -1,
                 delay_val: int = -1,
                 effects_lst: list[StatTuple] = []):
        self.element = elem
        super().__init__(name_val, cost_val, delay_val, effects_lst)

    def __str__(self) -> str:
        return (f"ART:\n"
                f"ELEMENT: {self.element}\n"
                f"{super().__str__()}")


class Craft(Action):
    def __init__(self: Self,
                 name_val: str = "unnamed_craft",
                 cost_val: int = -1,
                 delay_val: int = -1,
                 effects_lst: list[StatTuple] = []):
        super().__init__(name_val, cost_val, delay_val, effects_lst)

    def __str__(self) -> str:
        return (f"CRAFT:\n"
                f"{super().__str__()}")
