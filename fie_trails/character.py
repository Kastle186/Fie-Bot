from fie_trails.craft import Craft
from fie_trails.art import Art
from fie_trails.orbment import Orbment


class Character:
    def __init__(self, name: str, current_xp: int):
        self.name = name
        self.current_xp = current_xp
        self.level = self.calculate_level()

        # Base stats
        self.base_max_HP = 500
        self.base_EP = 100
        self.base_CP = 0
        self.base_STR = 20
        self.base_DEF = 15
        self.base_SPD = 10
        self.base_ATS = 12
        self.base_ADF = 10

        # Growth per level
        self.growth_HP = 40
        self.growth_EP = 5
        self.growth_SP_STATS = 2  # STR, DEF, ATS and ADF
        self.growth_SPD = 1

        # Scaled stats
        self.max_HP = self.base_max_HP + self.growth_HP * self.level
        self.current_HP = self.max_HP
        self.EP = self.base_EP + self.growth_EP * self.level
        self.CP = self.base_CP
        self.STR = self.base_STR + self.growth_SP_STATS * self.level
        self.DEF = self.base_DEF + self.growth_SP_STATS * self.level
        self.SPD = self.base_SPD + self.growth_SPD * self.level
        self.ATS = self.base_ATS + self.growth_SP_STATS * self.level
        self.ADF = self.base_ADF + self.growth_SP_STATS * self.level

        self.crafts = [Craft("Autumn Leaf Cutter", self.STR * 2, 20)]
        self.available_orbments: list[Orbment] = [Orbment("Attack 1", 0, "fire", Art("Fire Bolt", self.STR * 2, 20, "fire"))]
        self.equipped_orbments: list[Orbment] = [Orbment("Attack 2", 0, "fire", Art("Fire Bolt", self.STR * 2, 20, "fire"))]

        # Equipped arts should automatically come from equipped_orbments
        self.equipped_arts: list[Art] = []
        self._initial_state = self.__dict__.copy()

    def initialize_rean(self):
        if self.level >= 5:
            self.crafts.append(Craft("Motivate", 0, 10))
        if self.level >= 15:
            self.crafts.append(Craft("Arc Slash", self.STR * 2, 30))
        if self.level >= 35:
            self.crafts.append(Craft("Gale", self.STR * 3, 35))
        if self.level >= 55:
            self.crafts.append(Craft("Flame Impact", self.STR * 4, 35))
        if self.level >= 10:
            self.crafts.append(Craft("S-Craft - Flame Slash", self.STR * 10, 200))

        for orbment in self.equipped_orbments:
            if orbment.art_produced is not None:
                self.equipped_arts.append(orbment.art_produced)



    def getName(self):
        return self.name

    def get_max_HP(self):
        return self.max_HP

    def get_current_HP(self):
        return self.current_HP

    def set_max_HP(self, max_HP: int):
        self.max_HP = max_HP

    def set_current_HP(self, current_HP: int):
        self.current_HP = current_HP

    def getEP(self):
        return self.EP

    def setEP(self, EP: int):
        self.EP = EP

    def getCP(self):
        return self.CP

    def setCP(self, CP: int):
        self.CP = CP

    def get_crafts(self):
        return self.crafts

    def getSTR(self):
        return self.STR

    def setSTR(self, STR: int):
        self.STR = STR

    def getDEF(self):
        return self.DEF

    def setDEF(self, DEF: int):
        self.DEF = DEF

    def getSPD(self):
        return self.SPD

    def getATS(self):
        return self.ATS

    def getADF(self):
        return self.ADF

    def getXP(self):
        return self.current_xp

    def setXP(self, XP: int):
        self.current_xp = XP
        old_level = self.level
        self.level = self.calculate_level()

        # If level changed, update stats
        if self.level != old_level:
            self.refresh_stats()

    def getLVL(self):
        return self.level

    def get_available_orbments(self):
        return self.available_orbments

    def get_equipped_orbments(self):
        return self.equipped_orbments

    def get_equipped_arts(self):
        return self.equipped_arts

    def set_available_orbments(self, position: int, orbment: Orbment):
        self.available_orbments[position] = orbment

    def set_equipped_orbments(self, position: int, orbment: Orbment):
        self.equipped_orbments[position] = orbment

    def __str__(self):
        return str(self.crafts)

    def status(self):
        return (f"Name: {self.getName()}\n"
                f"Level: {self.getLVL()}\n"
                f"HP:  {self.get_max_HP()}       EXP: {self.getXP()}\n"
                f"STR: {self.getSTR()}      ATS: {self.getATS()}\n"
                f"DEF: {self.getDEF()}      ADF: {self.getADF()}\n"
                f"SPD: {self.getSPD()}\n")

    def calculate_level(self):
        return int((self.current_xp ** 0.5) / 10) + 1

    def refresh_stats(self):
        self.max_HP = self.base_max_HP + self.growth_HP * self.level
        self.EP = self.base_EP + self.growth_EP * self.level
        self.STR = self.base_STR + self.growth_SP_STATS * self.level
        self.DEF = self.base_DEF + self.growth_SP_STATS * self.level
        self.SPD = self.base_SPD + self.growth_SPD * self.level
        self.ATS = self.base_ATS + self.growth_SP_STATS * self.level
        self.ADF = self.base_ADF + self.growth_SP_STATS * self.level
        self.current_HP = min(self.current_HP, self.max_HP)

    def reset(self):
        # Restore attributes from the initial state
        self.set_current_HP(self.max_HP)



