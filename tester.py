# File: tester.py

from fieutils import emote, help_msg, sylphid_greeting
from typing import TypeAlias, Union, get_args

print(f"Emote: {emote("BLUSHV")}")
print(emote("NOT HERE"))
print(sylphid_greeting())
print(f"\n{help_msg()}")

lowered = "Oh yes hi Fie!".lower()

if any(msg in lowered for msg in
       ["hi fie",
        "hey fie"]):
    print(f"\nHey what's up {emote("WAVE")}\n")

# TestAliasType: TypeAlias = Union[
#     int,
#     str,
#     list[float]
# ]

TestAliasType = Union[
    int,
    list
]

print(TestAliasType)
x = 1
l = "test"
p = [2.3, 3.5]

print(type(x) is int)
print(type(l))
print(type(p))

names = list(map(lambda x: x.__name__, list(TestAliasType.__args__)))
print(names)
