class Enemy:
    def __init__(self, name: str, max_HP: int, current_HP: int, EP: int, CP: int,
                 STR: int, DEF: int, SPD: int, ATS: int,
                 ADF: int, level: int, xp: int, crafts=None):

        if crafts is None:
            crafts = []
        self.name = name
        self.max_HP = max_HP
        self.current_HP = current_HP
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
        self._initial_state = self.__dict__.copy()

    def get_name(self):
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

    def get_specific_craft(self, index: int):
        return self.crafts[index]

    def get_crafts(self):
        return self.crafts

    def __str__(self):
        return str(self.crafts)

    # IMPORTANT: This only works once. A new way has to be found for this
    def reset(self):
        self.set_current_HP(self.max_HP)
