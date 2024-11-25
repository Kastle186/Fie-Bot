# File: fiegames-local.py

from fieemotes import emote
import random

rps_choices = ['rock', 'paper', 'scissors']

# ******************************************************************************* #
# FIE MINI-GAMES:                                                                 #
#                                                                                 #
# These are the exact same mini-games but built to run locally and printing to    #
# console, rather than asynchronously sending the messages to the Discord server. #
# So we can test more easily :)                                                   #
# ******************************************************************************* #

def fie_rps():
    best_of = int(input("Best of how many? (Type an odd number pls): "))

    if best_of % 2 == 0:
        print("Hey dummy, do you know what an odd number is?")
        return

    print("Let's play then!")

    player_score = 0
    fie_score = 0

    while not is_rps_complete(best_of, player_score, fie_score):
        result_msg = ""
        player_input = input("\nChoose rock, paper, or scissors: ").casefold()

        if not player_input in rps_choices:
            print("Hey dummy, you have to pick rock, paper, or scissors. Try again!")
            continue

        fie_input = random.choice(rps_choices)

        match check_round_result(player_input, fie_input):
            case 0:
                result_msg = "It's a tie! Rematch! Go go!!!"

            case 1:
                result_msg = f"Ngh! I won't let you win the next one... {emote("TRIUMPH")}"
                player_score += 1

            case 2:
                result_msg = f"I won this round! {emote("GRINV")}"
                fie_score += 1

        print(f"You chose {player_input}, I chose {fie_input}. {result_msg}")
        print(f"Score: You - {player_score} ; Fie - {fie_score}")

    if player_score > fie_score:
        print(f"Damn... I lost the series {emote("PENSIVE")}")
    else:
        print(f"I won the series! {emote("GRINV")}")


def is_rps_complete(best_of: int, score1: int, score2: int) -> bool:
    rounds_needed = (best_of // 2) + 1
    return score1 >= rounds_needed or score2 >= rounds_needed


def check_round_result(choice1: str, choice2: str) -> int:
    if choice1 == choice2:
        return 0

    if (choice1 == "rock" and choice2 == "scissors") \
       or (choice1 == "paper" and choice2 == "rock") \
       or (choice1 == "scissors" and choice2 == "paper"):
        return 1

    return 2
