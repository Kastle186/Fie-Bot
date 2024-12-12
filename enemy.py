class Enemy:
    def __init__(self, name: str, HP: int, EP: int, CP: int,
                 STR: int, DEF: int, SPD: int, ATS: int,
                 ADF: int, level: int, xp: int, crafts=None):

        if crafts is None:
            crafts = []
        self.name = name
        self.HP = HP
        self.EP = EP
        self.CP = CP
        self.STR = STR
        self.DEF = DEF
        self.SPD = SPD
        self.ATS = ATS
        self.ADF = ADF
        self.level = level
        self.xp = xp
        self.crafts = crafts

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

    def getSTR(self):
        return self.STR

    def setSTR(self, STR: int):
        self.STR = STR

    def getDEF(self):
        return self.DEF

    def setDEF(self, DEF: int):
        self.DEF = DEF
    def getXP(self):
        return self.xp

    def get_crafts(self):
        return self.crafts

    def __str__(self):
        return str(self.crafts)
