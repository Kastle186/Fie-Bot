from craft import Craft
import math
class Character:
    def __init__(self, name: str, HP: int, EP:int, CP: int,
                 STR: int, DEF: int, SPD: int, ATS: int,
                 ADF: int, level: int, current_xp: int):
        self.name = name
        self.HP = HP
        self.STR = STR
        self.EP = EP
        self.CP = CP
        self.DEF = DEF
        self.SPD = SPD
        self.ATS = ATS
        self.ADF = ADF
        self.level = level
        self.current_xp = current_xp
        self.crafts = [Craft("Autumn Leaf Cutter", self.STR * 2, 20)]
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

    def getName(self):
        return self.name

    def getHP(self):
        return self.HP

    def setHP(self, HP: int):
        self.HP = HP

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

    def getLVL(self):
        return self.level

    def __str__(self):
        return str(self.crafts)

    def status(self):
        return (f"Name: {self.getName()}\n"
                f"Level: {self.getLVL()}\n"
                f"HP:  {self.getHP()}       EXP: {self.getXP()}\n"
                f"STR: {self.getSTR()}      ATS: {self.getATS()}\n"
                f"DEF: {self.getDEF()}      ADF: {self.getADF()}\n"
                f"SPD: {self.getSPD()}\n")

    def calculate_level(self):
        self.level = math.log2(self.current_xp)

    # IMPORTANT: This only works once. A new way has to be found for this
    def reset(self):
        # Restore attributes from the initial state
        self.__dict__ = self._initial_state.copy()



