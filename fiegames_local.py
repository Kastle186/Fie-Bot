# File: fiegames-local.py

from fieemotes import emote
import random

rps_choices = ['rock', 'paper', 'scissors']

trails_words = [
    "agate", "albarea", "alisa", "altina", "arcus", "arkride", "arseid", "arts",
    "ash", "bannings", "bright", "calvard", "capua", "cassius", "claussell", "claire",
    "crafts", "crossbell", "crow", "elie", "elise", "elliot", "emma", "erebonia",
    "estelle", "eugent", "fie", "fran", "gaius", "guild", "guy", "heiyue", "joshua",
    "josette", "juna", "jusis", "kea", "kloe", "kurt", "laura", "lechter", "liberl",
    "lloyd", "machias", "macdowell", "millium", "mueller", "musse", "noel", "olivert",
    "orbment", "orlando", "osborne", "ouroboros", "plato", "randy", "rean", "reinford",
    "remiferia", "renne", "rixia", "rufus", "sara", "schwarzer", "seeker", "tio",
    "tita", "toval", "towa", "valimar", "van", "vander", "zin"
]

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

        match check_rps_round_result(player_input, fie_input):
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


def fie_hangman():
    print("\nTry to guess the trails related word! It can be people, terms, or countries!")
    word = random.choice(trails_words)
    lives = 1 * len(word)
    has_guessed = False

    # List where we keep track of the player's correct guesses so far.
    player_guesses = [''] * len(word)

    while not has_guessed:
        if lives == 0:
            print(f"\nYou lost! The correct word was '{word}'.")
            break

        print(f"\n{player_guesses}")
        print("Guess a letter/the word!")
        print(f"Lives: {lives}\n")
        next_guess = input("Your guess: ").casefold()

        # We received a letter as a guess. So, check whether it matches one of more
        # of the missing letters of the word.
        if len(next_guess) == 1:
            letter_matches = [i for i, char in enumerate(word) if char == next_guess]

            if len(letter_matches) == 0:
                print("Nuh uh, wrong letter. Try again!")
                lives -= 1
                continue

            # Fill up the guesses list with the letter where it goes.
            for i in letter_matches:
                player_guesses[i] = word[i]

            # If there are no more empty slots in the guesses list, then that means
            # the player has successfully guessed the word :)
            if not "" in player_guesses:
                has_guessed = True

        # We received a correct guess of the full word.
        elif next_guess == word:
            print(f"That's right! The correct answer is {word}!")
            has_guessed = True

        # We received a wrong guess of the full word.
        else:
            print("Wrong! Try again!")
            lives -= 1

    if has_guessed:
        print("Congratulations! You won this one!")
    else:
        print("Better luck next time!")


# *************************************************************************** #
# MINI-GAMES HELPERS:                                                         #
# Any additional function to help with the logic of the mini-games goes here! #
# *************************************************************************** #

def is_rps_complete(best_of: int, score1: int, score2: int) -> bool:
    rounds_needed = (best_of // 2) + 1
    return score1 >= rounds_needed or score2 >= rounds_needed


def check_rps_round_result(choice1: str, choice2: str) -> int:
    if choice1 == choice2:
        return 0

    if (choice1 == "rock" and choice2 == "scissors") \
       or (choice1 == "paper" and choice2 == "rock") \
       or (choice1 == "scissors" and choice2 == "paper"):
        return 1

    return 2
