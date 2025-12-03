from enum import Enum

# Same as in art.py. Change "enum" for "Enum". Also, you forgot to annotate "status".

class Equipment:
    def __init__(self, equip_type: Enum, status):
        self.equip_type = equip_type
        self.status = status