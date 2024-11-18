# File: fieutils.py

import random

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

# List of greetings Fie can use with the 'fie' command.

fiegreetings = [
    "Roger!",
    "Ja!",
    "Sylphid at your service!"]

# List of commands with a brief explanation on how they work.

fiehelp = ("'fie rps' -> Play rock/paper/scissors with yours truly\n"
           "'fie time' -> I indicate the time of some of the members' timezones\n"
           "'claussell' -> A random pic of me. Seriously, you guys are obsessed\n"
           "'fie' (with nothing added) -> Random greeting from yours truly\n"
           "'fie solve' -> I will solve some math problems... (+ - * / ! sqrt average)\n"
           "'fie how many days until' -> Days left until relevant dates (feel free to ask for more)\n"
           "'fie how many days until day-month-year' -> Days left until a date you want to calculate\n"
           "'fie hangman' -> Come guess random Trails words!")

def emote(emote_name: str) -> str:
    return fieemotes.get(emote_name, "???")

def sylphid_greeting() -> str:
    return random.choice(fiegreetings)

# Naming this one help_msg() instead of help() to avoid conflicting with Python's
# built-in help() function.
def help_msg():
    return f"What a pain... here are the commands you can use:\n{fiehelp}"
