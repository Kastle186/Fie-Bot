# File: fietrails.py

from fieemotes import emote

from actions import Art, Craft
from character import Character
from trailsutils import Stat

# WIP: Dictionary to store the functions containing each action functionality.
#      It will provide us cleaner code than an if-elif-else or even case statements.

options = {
    "1": "Fight",
    "2": "Equipment",
    "3": "Orbments",
    "4": "Status",
}

def test():
    crafts = [
        Craft("Crimson Slash", 20, 20),
        Craft("Crescent Flash", 40, 25)
    ]

    the_stats = {
        Stat.HP:  540,
        Stat.EP:  200,
        Stat.CP:  200,
        Stat.STR: 67.96,
        Stat.DEF: 31.86,
        Stat.ATS: 57.16,
        Stat.ADF: 27,
        Stat.SPD: 41.591,
        Stat.DEX: 38.168,
        Stat.AGL: 26.152
    }

    character = Character("Rean Schwarzer", 1, 0, 100, the_stats, None, crafts, [])
    print(str(character))

# ************************ #
# DESCRIPTION COMING SOON! #
# ************************ #

def fie_trails():
    menu_choice = input("Welcome back! What do you want to do\n"
                        "1 - Fight!\n"
                        "2 - Change Equipment\n"
                        "3 - Change Orbment\n"
                        "4 - Check Status\n")

    if not menu_choice in options:
        print("Are you serious? All you had to do was choose a number between"
              f"1 and 4... I'm going back to sleep! {emote("SLEEP")}")
        return

    options[menu_choice]()
