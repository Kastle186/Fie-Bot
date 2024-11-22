# File.py

# from fieutils import emote, help_msg, sylphid_greeting
from datetime import datetime, timedelta, UTC
from typing import TypeAlias, Union, get_args

# print(f"Emote: {emote("BLUSHV")}")
# print(emote("NOT HERE"))
# print(sylphid_greeting())
# print(f"\n{help_msg()}")

# lowered = "Oh yes hi Fie!".lower()

# if any(msg in lowered for msg in
#        ["hi fie",
#         "hey fie"]):
#     print(f"\nHey what's up {emote("WAVE")}\n")

TestAliasType = Union[
    int,
    str,
    list
]

print(TestAliasType)
x = 1
l = "test"
p = [2.3, 3.5]

xtype = type(x)
ltype = type(l)
ptype = type(p)

print(xtype is int)
print(ltype)
print(ptype)

names = list(map(lambda x: x.__name__, list(TestAliasType.__args__)))
print(names)
print(TestAliasType)
print(isinstance(p, TestAliasType))

class FiePoint:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

a: TypeAlias = Union[int, str, FiePoint]
b = FiePoint(1, 2, 3)

print(f"\n{isinstance(b, a)}")
print(isinstance(p, a))
print(str(FiePoint))

# raise TypeError("Testing Exceptions!")

touseforifassigntest = "I will be assigned at condition!"

if ifassigntest := touseforifassigntest[0] == "I":
    print(f"\nTest was {ifassigntest}!")

if ifassigntest2 := touseforifassigntest[0] == "T":
    print(f"Test was {ifassigntest}")

print(touseforifassigntest)
print(ifassigntest)
print(ifassigntest2)

def f1(arg1: int, arg2: str) -> None:
    print(f"I got the args '{arg1}' & '{arg2}'!")

fdict = { "fkey": f1 }

testthere = fdict.get("fkey", None)
testnotthere = fdict.get("gkey", None)

if testthere is not None:
    print("FKey had a function!")
    testthere(1, "string")
else:
    print("FKey did not have a function!")

if testnotthere is not None:
    print("GKey had a function!")
    testnotthere(2, "string2")
else:
    print("GKey did not have a function!")

print(datetime.now())
print(datetime.now(UTC))
print((datetime.now() + timedelta(hours=3)).strftime("%H:%M:%S"))
