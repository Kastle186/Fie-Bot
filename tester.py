# File: tester.py

from fieutils import emote
from fieutils import help
from fieutils import sylphid_greeting

print(f"Emote: {emote("BLUSHV")}")
print(emote("NOT HERE"))
print(sylphid_greeting())
print(f"\n{help()}")

lowered = "Oh yes hi Fie!".lower()

if any(msg in lowered for msg in
       ["hi fie",
        "hey fie"]):
    print(f"Hey what's up {emote("WAVE")}")
