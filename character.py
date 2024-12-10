from craft import Craft
class Character:
    def __init__(self, name: str, HP: int, STR: int,
                 DEF: int, SPD: int, ATS: int, ADF: int,
                 level: int):
        self.name = name
        self.HP = HP
        self.STR = HP
        self.STR = STR
        self.DEF = DEF
        self.SPD = SPD
        self.ATS = ATS
        self.ADF = ADF
        self.level = level
        self.crafts = [Craft("Autumn Leaf Cutter", self.STR * 2, 20)]

    def initialize_rean(self):
        if self.level >= 5:
            self.crafts.append(Craft("Motivate", 0, 10))
        if self.level >= 15:
            self.crafts.append(Craft("Arc Slash", self.STR * 2, 30))
        if self.level >= 35:
            self.crafts.append(Craft("Gale", self.STR * 3, 35))
        if self.level >= 55:
            self.crafts.append(Craft("Flame Impact", self.STR * 4, 35))
