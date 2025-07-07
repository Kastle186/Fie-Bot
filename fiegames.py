# File: fiegames.py

from discord import Client, Message
from fieemotes import emote

import asyncio
import csv
import os
import random

rps_choices = ['rock', 'paper', 'scissors']

trails_words = [
    "agate", "albarea", "alisa", "altina", "arcus", "arkride", "arseid", "arts",
    "ash", "bannings", "bareahard", "bose", "bright", "calvard", "capua", "cassius",
    "celdic", "claussell", "claire", "crafts", "crossbell", "crow", "elie", "elise",
    "elliot", "emma", "erebonia", "estelle", "eugent", "fie", "fran", "gaius",
    "grancel", "guild", "guy", "heimdallr", "heiyue", "joshua", "josette", "juna",
    "jusis", "kea", "kloe", "kurt", "laura", "lechter", "leeves", "legram", "liberl",
    "lloyd", "machias", "macdowell", "millium", "mishelam", "mueller", "musse",
    "noel", "olivert", "orbment", "ordis", "orlando", "osborne", "ouroboros", "parm",
    "plato", "randy", "raquel", "rean", "reinford", "remiferia", "renne", "rixia",
    "roer", "roland", "ruan", "rufus", "sara", "schwarzer", "seeker", "tio", "tita",
    "toval", "towa", "trista", "valimar", "van", "vander", "wazy", "ymir", "zeiss", "zin"
]

leaderboard_file = 'fie_games_leaderboard.csv'
leaderboard_talk_file = "fie_talk_leaderboard.csv"
leaderboard = dict()
lb_talk = dict()

# ****************************************************************************** #
# FIE MINI-GAMES:                                                                #
#                                                                                #
# These are the functions that run the mini-games Fie can play with you in the   #
# server. Right now, she knows how to play Rock/Paper/Scissors, and Hangman with #
# words from the Trails world.                                                   #
# ****************************************************************************** #

async def fie_rps(client_obj: Client, message_obj: Message) -> None:

    # Initialize leaderboard dictionary lazily for the sake of efficiency.

    if len(leaderboard) == 0:
        init_leaderboard()

    player_name = message_obj.author.name
    src_channel = message_obj.channel
    await src_channel.send("Best of how many? (Type an odd number pls)")

    # For best results with the Discord API, it is best to define the check function
    # as a nested function here.

    def check_for_bestof_answer(m):
        return m.author == message_obj.author    \
            and m.channel == message_obj.channel \
            and m.content.isdigit()

    try:
        # Since in a Discord server, there are multiple users, it is not uncommon
        # for someone else to type and send something while another is waiting to
        # play. This call to wait_for() combined with check_for_bestof_answer()
        # looks for the message intended to be the input for the bot.
        best_of_msg = await client_obj.wait_for(
            'message',
            check=check_for_bestof_answer,
            timeout=30.0)

        # We can't play Best-Of games with an even number.
        best_of = int(best_of_msg.content)
        if best_of % 2 == 0:
            await src_channel.send("Hey dummy, do you know what an odd number is?")
            return

    except asyncio.TimeoutError:
        await src_channel.send(
            f"You took too long to decide! I'm going to sleep {emote("SLEEP")}")
        return

    # If this is the first time of the current player playing a Fie-Game, then add
    # their respective entry to the leaderboard.

    if not player_name in leaderboard:
        leaderboard[player_name] = [0, 0]

    await src_channel.send("Let's play then!")

    player_score = 0
    fie_score = 0

    # The mini-game's main loop!

    while not is_rps_complete(best_of, player_score, fie_score):
        result_msg = ""
        await src_channel.send("Choose rock, paper, or scissors")

        def check_for_rps_answer(m):
            return m.author == message_obj.author    \
                and m.channel == message_obj.channel \
                and m.content.casefold() in rps_choices

        try:
            player_choice_msg = await client_obj.wait_for(
                'message',
                check=check_for_rps_answer,
                timeout=30.0)

        except asyncio.TimeoutError:
            await src_channel.send(
                f"You took too long to decide! I'm going to sleep {emote("SLEEP")}")
            return

        player_choice = player_choice_msg.content.casefold()
        fie_choice = random.choice(rps_choices)

        match check_rps_round_result(player_choice, fie_choice):
            case 0:
                # Tie!
                result_msg = "It's a tie! Rematch! Go go!!!"

            case 1:
                # Player Wins Round
                result_msg = f"Ngh! I won't let you win the next one... {emote("TRIUMPH")}"
                player_score += 1

            case 2:
                # Fie Wins Round
                result_msg = f"I won this round! {emote("GRINV")}"
                fie_score += 1

        # Fie will tell the round's result, as well as the total scores so far
        # after each round.

        await src_channel.send(
            f"You chose {player_choice}, I chose {fie_choice}. {result_msg}")
        await src_channel.send(
            f"Current Score - You: {player_score}, Fie: {fie_score}")

    if player_score > fie_score:
        # Placeholder while we define how to score this game.
        update_leaderboard(player_name, best_of, 0)
        await src_channel.send(f"Damn... I lost the series {emote("PENSIVE")}")
    else:
        await src_channel.send(f"I won the series! {emote("GRINV")}")


async def fie_hangman(client_obj: Client, message_obj: Message):

    # Initialize leaderboard dictionary lazily for the sake of efficiency.

    if len(leaderboard) == 0:
        init_leaderboard()

    player_name = message_obj.author.name
    src_channel = message_obj.channel
    await src_channel.send(
        "Try to guess the trails related word! It can be people, terms, towns/cities, or countries!\n"
        "First, choose a difficulty, trails style hehe...\n"
        "1 - Easy\n"
        "2 - Normal\n"
        "3 - Hard\n"
        "4 - Nightmare\n")

    # IDEA: Might be cool to keep track of the frequency of the words outside of
    #       this code. So that we can have a better chance of getting them all
    #       in the game :)

    def check_for_difficulty_answer(m):
        return m.author == message_obj.author \
            and m.channel == message_obj.channel \
            and m.content.isdigit()
    try:
        difficulty_chosen_msg = await client_obj.wait_for(
            'message',
            check=check_for_difficulty_answer,
            timeout=30.0)

    except asyncio.TimeoutError:
        await src_channel.send(
            f"You took too long to decide! I'm going to sleep {emote("SLEEP")}")
        return

    # If this is the first time of the current player playing a Fie-Game, then add
    # their respective entry to the leaderboard.

    if not player_name in leaderboard:
        leaderboard[player_name] = [0, 0]

    word = random.choice(trails_words)
    difficulty_index = int(difficulty_chosen_msg.content)
    lives = 0

    match difficulty_index:
        # Easy
        case 1:
            lives = 4 * len(word)
        # Normal
        case 2:
            lives = 3 * len(word)
        # Hard
        case 3:
            lives = 2 * len(word)
        # Nightmare
        case 4:
            lives = len(word)
        case _:
            await src_channel.send(f"Hey dummy, there is no '{difficulty_index}' option!")
            return

    # List where we keep track of the player's correct guesses so far.
    player_guesses = [""] * len(word)
    has_guessed = False

    def check_for_guess(m):
        return m.author == message_obj.author and m.channel == message_obj.channel

    while not has_guessed:
        if lives == 0:
            await src_channel.send(f"You lost! The correct word was '{word}'.")
            break

        await src_channel.send(get_hangman_progress(player_guesses))
        await src_channel.send(f"Guess a letter/the word!\nLives: {lives}")

        try:
            next_guess_msg = await client_obj.wait_for(
                'message',
                check=check_for_guess,
                timeout=120.0)

        except asyncio.TimeoutError:
            await src_channel.send(
                f"You took too long to respond! I'm going to sleep {emote("SLEEP")}")
            return

        next_guess = next_guess_msg.content.casefold()
        print(next_guess)

        # We received a letter as a guess. So, check whether it matches one of more
        # of the missing letters of the word.
        if len(next_guess) == 1:
            letter_matches = [i for i, char in enumerate(word) if char == next_guess]

            if len(letter_matches) == 0:
                await src_channel.send("Nuh uh, wrong letter. Try again!")
                lives -= 1
                continue

            # Fill up the guesses list with the letter where it goes.
            for i in letter_matches:
                player_guesses[i] = word[i]

            # If there are no more empty slots in the guesses list, then that means
            # the player has successfully guessed the word :)
            if not '' in player_guesses:
                has_guessed = True

        # We received a correct guess of the full word.
        elif next_guess == word:
            await src_channel.send(f"That's right! The correct answer is {word}!")
            has_guessed = True

        # We received a wrong guess of the full word.
        else:
            if next_guess not in trails_words:
                await src_channel.send("That word isn't in the database!")
            else:
                await src_channel.send("Wrong! Try again <:Fie_SD:1297250356019073065>")
                lives -= 1

    if has_guessed:
        # Add the score of this victory to this player's leaderboard entry.
        # Fie Hangman is the second stored score.
        update_leaderboard(player_name, difficulty_index, 1)
        await src_channel.send(f"Congratulations! You won this one {emote("GRINV")}")
    else:
        await src_channel.send("Better luck next time!")


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


def get_hangman_progress(guesses: list[str]) -> str:
    return ' '.join(map(lambda c: "\\_" if c == "" else c, guesses))


def init_leaderboard() -> None:
    # If there are no leaderboard records, then we'll just keep the empty one.
    if not os.path.exists(leaderboard_file):
        return

    # Otherwise, read its contents from its CSV file. Each entry comprises 3 values:
    # - Player's name (retrieved from message_obj.author)
    # - Player's total score in Fie RPS
    # - Player's total score in Fie Hangman

    with open(leaderboard_file, mode='r', newline='\n') as the_file:
        csv_contents = csv.reader(the_file)
        next(csv_contents, None) # Skip the header.

        for entries in csv_contents:
            leaderboard[entries[0]] = [int(entries[1]), int(entries[2])]


# TODO: It would be preferable to use an enum instead of a number to denote which
#       game's score we are updating. But I'm sleepy, so some other time :)

def update_leaderboard(player: str, score: int, game: int) -> None:
    global leaderboard

    # Update live dictionary object.
    leaderboard[player][game] += score

    fields = ['Player', 'RPS Score', 'Hangman Score']
    entries = [[key, value[0], value[1]] for key, value in leaderboard.items()]

    # Update leaderboard file.
    with open(leaderboard_file, mode='w', newline='\n') as the_file:
        csv_writer = csv.writer(the_file)
        csv_writer.writerow(fields)
        csv_writer.writerows(entries)


def update_talk_xp(player: str, xp: int) -> None:
    global lb_talk

    # Update live dictionary object.
    lb_talk[player] += xp

    fields = ['Player', 'XP']
    entries = [[key, value[0]] for key, value in lb_talk.items()]

    # Update leaderboard file.
    with open(leaderboard_file, mode='w', newline='\n') as the_file:
        csv_writer = csv.writer(the_file)
        csv_writer.writerow(fields)
        csv_writer.writerows(entries)
