# File: fietrails.py

from fieemotes import emote
from actions import Craft

# WIP: Dictionary to store the functions containing each action functionality.
#      It will provide us cleaner code than an if-elif-else or even case statements.

options = {
    "1": "Fight",
    "2": "Equipment",
    "3": "Orbments",
    "4": "Status",
}

def test():
    print(emote("BLUSHV"))
    craft = Craft(name="name", cost=20, damage=10)
    print(str(craft))


# ************************ #
# DESCRIPTION COMING SOON! #
# ************************ #

def fie_trails():
    menu_choice = input("Welcome back! What do you want to do\n"
                        "1 - Fight!\n"
                        "2 - Change Equipment\n"
                        "3 - Change Orbment\n"
                        "4 - Check Status\n")

    if not menu_choice in actions:
        print("Are you serious? All you had to do was choose a number between"
              f"1 and 4... I'm going back to sleep! {emote("SLEEP")}")
        return

    options[menu_choice]()
