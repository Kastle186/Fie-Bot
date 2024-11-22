from datetime import datetime, timedelta, time
from discord import Intents, Client, Message, File
from dotenv import load_dotenv
from typing import Final

from fieutils import emote, send_message
from fieresponses import get_response

import asyncio
import math
import os
import random
import statistics

# STEP -1: Define aliases, data structures, etc that will be used in the main code
#          here. Might be better to move them to their own file but we'll see about
#          later on.

# DiscordChannelType: TypeAlias = Union[
#     TextChannel,
#     StageChannel,
#     VoiceChannel,
#     Thread,
#     DMChannel,
#     GroupChannel,
#     PartialMessageable
# ]


# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')


# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)


# STEP 2: HANDLING THE STARTUP FOR OUR BOT
@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running!")


# async def send_message(
#         message_or_channel: Union[Message, DiscordChannelType],
#         user_message: str) -> None:
#     if not user_message:
#         print('(Message was empty because intents were not enabled probably)')
#         return

#     if is_private := user_message[0] == "?":
#         user_message = user_message[1:]

#     try:
#         # Defer to Fie to interpret the message and let her decide how she wants
#         # to respond :)
#         response = get_response(user_message)
#         destination = None

#         # Sometimes we might get a Message object, which contains a pointer to the
#         # channel object where it came from. Other times, we might get the channel
#         # object directly. So, we have to make that distinction here to call the
#         # send() method accordingly.

#         if type(message_or_channel) is Message:
#             destination = (message_or_channel.author if is_private
#                            else message_or_channel.channel)
#         elif isinstance(message_or_channel, DiscordChannelType):
#             destination = message_or_channel
#         else:
#             raise TypeError(f"Unrecognized channel type '{type(message_or_channel)}'")

#         await destination.send(response)

#     except Exception as e:
#         print(e)


sent = False
sent2 = False
sent3 = False
sent4 = False
last_messages = []

async def send_daily_message():
    global sent, sent2, sent3, sent4
    SPECIFIC_TIME = time(22, 0)
    SPECIFIC_TIME2 = time(18, 0)
    SPECIFIC_TIME3 = time(20,0)
    SPECIFIC_TIME4 = time(0, 0)

    await client.wait_until_ready()
    channel = client.get_channel(420709830622183434)
    channel2 = client.get_channel(1300997938335580171)

    while not client.is_closed():
        now = datetime.now().time()

        if not sent:
            if now.hour == SPECIFIC_TIME.hour and now.minute == SPECIFIC_TIME.minute:
                await channel.send("<@98491257784909824> have you trained yet? Laura is expecting you <:Laura_S:1252956467779076106>")
                sent = True

        if not sent2:
            if now.hour == SPECIFIC_TIME2.hour and now.minute == SPECIFIC_TIME2.minute:
                await channel2.send(f"<@444271831118249996> it's a bit embarassing to hear how much you appreciate me but thanks! i appreciate you too yuuyuu {emote("GRINV")}")
                sent2 = True

        if not sent3:
            if now.hour == SPECIFIC_TIME3.hour and now.minute == SPECIFIC_TIME3.minute:
                await channel.send("<@145607631149465600> <:Laura_S:1252956467779076106>: HELLO NANA, HOPE YOU HAD A GOOD DAY! I STILL DON'T KNOW HOW TO USE MY PHONE VERY WELL. HOPE YOU TAKE CARE OF YOURSELF - LAURA")
                sent3 = True

        if not sent4:

            if now.hour == SPECIFIC_TIME4.hour and now.minute == SPECIFIC_TIME4.minute:
                print("Sending message to channel 4")
                await channel.send("<@164047938325184512> <:Fie_Claussell:1304860526936985620> Are you still awake you son of a gun? Don't you have uni tomorrow? Or a life? Get your ass to bed immediately.")
                sent4 = True

        # Check every minute.
        await asyncio.sleep(60)

# STEP 3: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f"{channel} {username}: {user_message}")
    await handle_message(message)
    # await send_message(message, user_message)

    if any(word in message.content.lower() for word in ['fie rps']):
        """
        Rock Paper Scissors with any round number
        """
        await message.channel.send("How many rounds? (Type an odd number)")

        def check_rounds(m):
            return m.author == message.author and m.channel == message.channel and m.content.isdigit()

        try:
            rounds_msg = await client.wait_for('message', check=check_rounds, timeout=30.0)
            rounds_input = int(rounds_msg.content)

            if rounds_input % 2 == 1:
                rounds_needed = (int(rounds_msg.content) // 2) + 1
            else:
                await message.channel.send("Hey dummy, do you know what an odd number is?")

        except asyncio.TimeoutError:
            await message.channel.send("You took too long to decide! I'm going to sleep :sleeping:")
            return

        # Track scores
        user_score = 0
        bot_score = 0

        while user_score < rounds_needed and bot_score < rounds_needed:
            await message.channel.send("Let's play! Choose rock, paper, or scissors")

            def check(m):
                return m.author == message.author and m.channel == message.channel and m.content.lower() in ['rock',
                                                                                                             'paper',
                                                                                                             'scissors']

            try:
                user_choice = await client.wait_for('message', check=check, timeout=30.0)
            except asyncio.TimeoutError:
                await message.channel.send("You took too long to respond! I'm going to sleep :sleeping:")
                return

            user_choice = user_choice.content.lower()
            bot_choice = random.choice(['rock', 'paper', 'scissors'])

            # Determine the winner
            if user_choice == bot_choice:
                result = "It's a tie! Rematch! Go go!!!"
            elif (user_choice == 'rock' and bot_choice == 'scissors') or \
                    (user_choice == 'paper' and bot_choice == 'rock') or \
                    (user_choice == 'scissors' and bot_choice == 'paper'):
                result = "Ngh! I won't let you win the next one... :triumph:"
                user_score += 1
            else:
                result = "I won this round! :grin::v:"
                bot_score += 1

            # Send round result and current score for best of 7 mode
            await message.channel.send(f"You chose {user_choice}, I chose {bot_choice}. {result}")
            await message.channel.send(f"Current Score - You: {user_score}, Fie: {bot_score}")

        # Final game result
        if user_score > bot_score:
            await message.channel.send("Damn... I lost the series :pensive:")
        else:
            await message.channel.send("I won the series! :grin::v:")

    client.loop.create_task(send_daily_message())

    """
    REPEAT MESSAGE
    """
    last_messages.append((message.content, message.author))
    print(last_messages)
    if len(last_messages) > 2:
        last_messages.pop(0)

    if len(last_messages) == 2 and last_messages[0][0] == last_messages[1][0] and last_messages[0][1] != last_messages[1][1]:
        await message.channel.send(last_messages[1][0])

    if any(word in message.content.lower() for word in ['fie how many days until']):
        """
        Count your days!
        """
        today = datetime.today()
        new_list = [word for sentence in [message.content.lower()] for word in sentence.split()]
        if len(new_list) > 5:
            target = datetime.strptime(new_list[5], "%d-%m-%Y")
            delta = target - today
            if delta.days >= 0:
                await message.channel.send(f"There are {delta.days + 1} days until {target}")
            else:
                await message.channel.send(f"{delta.days * (-1) + 1} days have passed since {target}")
        else:
            target = datetime.strptime("25-12-2024", "%d-%m-%Y")
            target2 = datetime.strptime("14-02-2025", "%d-%m-%Y")
            delta = target - today
            delta2 = target2 - today
            await message.channel.send(f"Days until Christmas: {delta.days + 1}\n"
                                       f"Days until Daybreak II: {delta2.days + 1}\n"
                                       f"Days until Rean stops being dense: ∞\n")

    if any(word in message.content.lower() for word in ['fie schedule']) :
        tasks = [
            "20th of November - PCO (RP)",
            "25th of November - SO (Intermediate)",
            "27th of November - SI (TA3)",
            "27th of November - PCO (2nd Delivery)"
            "2nd of December - IPM (Test)",
            "4th of December - SO (Test)",
            "9th of December - SO (project due date)",
            "9th of December - PCO (forum)",
            "12th of December - SI (Test)",
            "13th of December - SI (TP)",
            "18th of December - PCO (Test)",
            "16th/19th of December - SI (presentation)"
        ]
        user = await client.fetch_user(164047938325184512)
        await user.send('\n'.join(tasks))
        await message.channel.send("sent!")

    if any(word in message.content.lower() for word in ['fie hangman']):
        words = ["arcus", "claussell", "laura", "renne", "ouroboros", "crafts", "arts", "toval", "arseid",
                 "arseid", "vander", "juna", "kurt", "altina", "orbments", "rean", "schwarzer", "alisa", "emma",
                 "reinford", "fie", "gaius", "bright", "estelle", "joshua", "lloyd", "bannings", "cassius",
                 "jusis", "machias", "millium", "crow", "osborne", "sara", "claire", "tio", "randy", "tita",
                 "kea", "elie", "agate", "towa", "noel", "rixia", "heiyue", "guy", "guild", "erebonia", "crossbell",
                 "liberl", "calvard", "remiferia", "olivert", "zin", "mueller", "kloe", "valimar", "lechter",
                 "rufus", "albarea", "elliot", "ash", "musse", "josette", "capua", "elise", "eugent"]

        await message.channel.send("Try to guess the trails related word! It can be people, terms, or countries!")
        word = random.randint(0, 66)
        chosen = words[word]
        list_chosen = []
        user_guessed = ["  "] * len(chosen)
        for i in chosen:
            list_chosen.append(i)

        lives = 3 * len(list_chosen)

        def check_choice(m):
            return m.author == message.author and m.channel == message.channel

        while True:
            correctly_guessed = False
            if lives == 0:
                await message.channel.send(f"You lost! The correct word was {chosen}")
                break
            await message.channel.send(f"{user_guessed}")
            await message.channel.send(f"Guess a letter/the word!\nLives: {lives}")
            try:
                user_choice = await client.wait_for('message', check=check_choice, timeout=120.0)
            except asyncio.TimeoutError:
                await message.channel.send("You took too long to respond! I'm going to sleep :sleeping:")
                return

            user_list = []
            for i in user_choice.content.lower():
                user_list.append(i)
                print(user_list)
            if user_choice.content.lower() == chosen or user_guessed == list_chosen:
                await message.channel.send(f"That's right! The correct answer is {chosen}!")
                break
            elif len(user_list) == 1:
                for position, letter in enumerate(list_chosen):
                    if letter == user_list[0]:
                        user_guessed[position] = user_list[0]
                        correctly_guessed = True

                if not correctly_guessed:
                    lives -= 1

            else:
                await message.channel.send("Wrong! Try again <:Fie_SD:1297250356019073065>")
                lives -= 1


    if any(word in message.content.lower() for word in ["fie what's"]):
        new_list = [word for sentence in [message.content.lower()] for word in sentence.split()]
        if new_list[2] == "zemurian" and new_list[3] == "ore":
            await message.channel.send("Zemurian Ore is an extremely rare material found in Zemuria. It's usually used in the series to craft very strong weapons!\n")
        elif new_list[2] == "zemuria":
            await message.channel.send("Zemuria is the continent made up of 37 regions on which the series takes place. It's the only known continent so far")
        elif new_list[2] == "zemuria":
            await message.channel.send(
                "Zemuria is the continent made up of 37 regions on which the series takes place. It's the only known continent so far")


# STEP 4: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()
