from fie_trails.craft import Craft

class SCraft(Craft):
    def __init__(self, **kwargs):
        Craft.__init__(self, **kwargs)
        self.cost = 200