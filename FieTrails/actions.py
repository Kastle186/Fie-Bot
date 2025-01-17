# File: actions.py

from abc import ABC, abstractmethod
from trailsutils import Element, VitalityStats

# NOTE: We might probably have to change how Damage/Heal/Buff/Nerf work here.
#       - Damage and Heal can also target EP/CP, even if it's uncommon.
#       - Buff and Nerf might need to become tuples, so that we can keep the data
#         on which stat is modified, as well as the numerical value, rather than
#         just the latter.

class Action(ABC):
    name: str
    cost: int
    damage: VitalityStats
    heal: VitalityStats
    buff_stat: int
    nerf_stat: int
    delay: int

    @abstractmethod
    def __init__(self,
                 name_val: str = "<empty>"
                 cost_val: int = 0,
                 dmg_val:  VitalityStats = None,
                 heal_val: VitalityStats = None,
                 buff_val: int = 0,
                 nerf_val: int = 0,
                 delay_val: int = 0):

        self.name = name_val
        self.cost = cost_val
        self.delay = delay_val

        if dmg_val is None:
            self.damage = VitalityStats(0, 0, 0)
        else:
            self.damage = dmg_val

        if heal_val is None:
            self.heal = VitalityStats(0, 0, 0)
        else:
            self.heal = heal_val

        self.buff_stat = buff_val
        self.nerf_stat = nerf_val

    @abstractmethod
    def __str__(self) -> str:
        return (f"Name: {self.name}\n"
                f"Cost: {self.cost}\n"
                f"\nDamage: {str(self.damage)}\n"
                f"\nHeal: {str(self.heal)}\n"
                f"\nBuff: {self.buff_stat}\n"
                f"Nerf: {self.nerf_stat}\n"
                f"Delay: {self.delay}")


class Art(Action):
    element: Element

    def __init__(self,
                 elem_val: str,
                 name_val: str,
                 cost_val: int = 0,
                 dmg_val:  int = 0,
                 heal_val: int = 0,
                 buff_val: int = 0,
                 nerf_val: int = 0
                 delay_val: int = 0):

        self.element = Element[elem_val.upper()]
        super().__init__(name_val, cost_val, dmg_val, heal_val, buff_val, nerf_val)

    def __str__(self) -> str:
        return (f"ART DATA:\n"
                f"\n{super().__str__()}\n"
                f"Element: {self.element.name}")


class Craft(Action):
    def __init__(self,
                 name_val: str,
                 cost_val: int = 0,
                 dmg_val:  int = 0,
                 heal_val: int = 0,
                 buff_val: int = 0,
                 nerf_val: int = 0):
        super().__init__(name_val, cost_val, dmg_val, heal_val, buff_val, nerf_val)

    def __str__(self) -> str:
        return ("CRAFT DATA:\n"
                f"\n{super().__str__()}")
