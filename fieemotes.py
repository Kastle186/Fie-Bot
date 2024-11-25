# File: fieemotes.py

# Had to add this file because everyone needs the emotes and Python wouldn't stop
# complaining about circular imports if we had it in fieutils.py :|

# Emotes dictionary! The purpose of this is to make the code that implements
# emotes easier to maintain, extend, and overall easier to type. Use the
# getter function `emote()` to use them in your code.
#
# Have any new combination of emotes you want to use? Just add a new entry here!

fieemotes = {
    "BLUSHV": ":blush::v:",
    "FROWN": ":slight_frown:",
    "GRINV": ":grin::v:",
    "PENSIVE": ":pensive:",
    "RELAXED": ":relaxed:",
    "SALUTE": ":saluting_face:",
    "SLEEP": ":sleeping_face:",
    "TRIUMPH": ":triumph:",
    "WAVE": ":wave:"
}

def emote(emote_name: str) -> str:
    return fieemotes.get(emote_name, "???")

