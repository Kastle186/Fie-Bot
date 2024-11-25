# File: fiegames.py

from discord import Message
from fieemotes import emote

import asyncio
import random

rps_choices = ['rock', 'paper', 'scissors']

# ****************************************************************************** #
# FIE MINI-GAMES:                                                                #
#                                                                                #
# These are the functions that run the mini-games Fie can play with you in the   #
# server. Right now, she knows how to play Rock/Paper/Scissors, and Hangman with #
# words from the Trails world.                                                   #
# ****************************************************************************** #

async def fie_rps(client_obj: Client, message_obj: Message) -> None:
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

    except asyncio.TimeoutError:
        await src_channel.send(
            f"You took too long to decide! I'm going to sleep {emote("SLEEP")}")
        return

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
            f"You chose {player_input}, I chose {fie_input}. {result_msg}")
        await src_channel.send(
            f"Current Score - You: {player_score}, Fie: {fie_score}")

        if player_score > fie_score:
            await src_channel.send(f"Damn... I lost the series {emote("PENSIVE")}")
        else:
            await src_channel.send(f"I won the series! {emote("GRINV")}")


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
