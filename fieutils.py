# File: fieutils.py

from discord import (
    Client,
    DMChannel,
    File,
    GroupChannel,
    Message,
    PartialMessageable,
    StageChannel,
    TextChannel,
    Thread,
    VoiceChannel
)

from collections import deque
from dataclasses import dataclass
from datetime import datetime, time, UTC, timedelta
from fieemotes import emote
from typing import TypeAlias, Union

import asyncio
import fiecommands
import fiegames
import random
import re

# Class to store the necessary info to send the daily messages accordingly.

@dataclass
class DailyMessage:
    has_been_sent_today: bool
    scheduled_time: time
    message: str

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
           "'fie how many days until' -> Days left until relevant dates"
           " (feel free to ask for more)\n"
           "'fie how many days until date (dd-mm-yyyy)' -> Days left until a date"
           " you want to calculate\n"
           "'fie hangman' -> Come guess random Trails words!")

# List of Fie images! We seriously are obsessed.

fie_image_files = [
    "images/fie.png",
    "images/Fie_Claussell_SD_29.png",
    "images/Rean x fie.png",
    "images/stylish fie.png",
    "images/cute fie.png",
    "images/fie bye bye.png",
    "images/fie (and laura).png",
    "images/ValentineKuro.png",
    "images/Fie CSI.png",
    "images/Fie CSII.png",
    "images/Fie CSIII.png",
    "images/Fie CSIV.png",
    "images/Fie Reverie.png",
    "images/Fie Daybreak.png",
]

# List of daily messages and their info to send them.

# NOTE: Right now, we depend on the bot getting restarted at least once a day to
#       get all messages to be sent. It would be cool to implement something to have
#       them reset on their own, if at some point we end up leaving the bot running
#       during the night too.

daily_messages = [
    DailyMessage(
        False,
        time(hour=22, tzinfo=UTC),
        ("<@98491257784909824> have you trained yet? "
         "Laura is expecting you <:Laura_S:1252956467779076106>")
    ),

    DailyMessage(
        False,
        time(hour=18, tzinfo=UTC),
        ("<@444271831118249996> it's a bit embarassing to hear how much you "
         f"appreciate me but thanks! I appreciate you too Yuuyuu {emote("GRINV")}")
    ),

    DailyMessage(
        False,
        time(hour=20, tzinfo=UTC),
        ("<@145607631149465600> <:Laura_S:1252956467779076106>: "
         "HELLO NANA, HOPE YOU HAD A GOOD DAY! I STILL DON'T KNOW HOW TO "
         "USE MY PHONE VERY WELL. HOPE YOU TAKE CARE OF YOURSELF - LAURA")
    ),

    DailyMessage(
        False,
        time(hour=0, tzinfo=UTC),
        ("<@164047938325184512> <:Fie_Claussell:1304860526936985620> "
         "You. Bed. Now. ")
    ),

    #DailyMessage(
     #   False,
      #  time(hour=21, tzinfo=UTC),
       # ("<@812099925600501882> <:Noel_SD:1303734969797054554> "
        # "Noel here! Have you been taking care of yourself? "
         #f"I will always support you no matter what! {emote("SALUTE")}")
    #),
]

# The running gag is about Fie chiming in whenever two people post the same message
# one after the other. So, keeping track of the last 2 messages is what we need here.
last_messages = deque(maxlen=2)

DiscordChannelType: TypeAlias = Union[
    DMChannel,
    GroupChannel,
    PartialMessageable,
    StageChannel,
    TextChannel,
    Thread,
    VoiceChannel
]

def sylphid_greeting() -> str:
    return random.choice(fiegreetings)

def help_msg():
    return f"What a pain... here are the commands you can use:\n{fiehelp}"


# ******************************************************************************* #
# MAIN MESSAGING FUNCTION:                                                        #
# This is the main function to process and handle all of the incoming messages we #
# read from the server. If in doubt about how the system works as a whole, start  #
# looking here.                                                                   #
# ******************************************************************************* #

async def handle_message(client_obj: Client, message_obj: Message) -> None:
    user_message = message_obj.content

    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    if is_private := user_message[0] == "?":
        user_message = user_message[1:]

    message = user_message.casefold()
    fie_res = fie_response(message)

    # We got one of the responses from Fie! So we send it to the server as is.
    if not fie_res == "<empty>":
        await send_text(message_obj, fie_res, is_private)

    # Skip bot messages
    if message_obj.author.bot:
        return

    # AUTO XP GAIN
    user_id = str(message_obj.author.id)
    xp_result = fiecommands.add_xp(user_id, 10)  # Add 10 XP per message

    # Send level-up messages to a specific channel
    if "leveled up" in xp_result[0]:
        await send_text(message_obj.channel, xp_result[0], is_private=False)
        await send_file(message_obj, xp_result[1], is_private=False)

    # #################################### #
    # Commands triggered by one word only. #
    # #################################### #

    elif message == "claussell":
        img_to_send = random.choice(fie_image_files)
        await send_file(message_obj, img_to_send, is_private)

    elif message == "kastle":
        await send_file(message_obj, "images/Noel.png", is_private)

    elif message == "kayrennede007":
        await send_file(message_obj, "images/HOT-SHOT_-_Renne_Kuro.png", is_private)

    # ###################################################### #
    # Commands triggered by a phrase in a message: Utilities #
    # ###################################################### #

    elif "fie time" in message:
        timezones_str = fiecommands.fie_time(message_obj.channel.id)
        await send_text(message_obj, timezones_str, is_private)

    elif "fie solve" in message:
        math_result = fiecommands.fie_solve(message)
        await send_text(message_obj, math_result, is_private)

    elif "fie how many days until" in message:
        days_until = fiecommands.fie_days_until(message)
        await send_text(message_obj, days_until, is_private)

    # TODO: Add the option to also recognize 'fie what is' as the command.
    elif "fie what's" in message:
        fun_fact = fiecommands.fie_what_is(message)
        await send_text(message_obj, fun_fact, is_private)

    elif "fie scores" in message:
        scores = fiecommands.fie_scores(message)
        await send_text(message_obj, scores, is_private)

    elif "fie leaderboard" in message:
        osu_lb = fiecommands.fie_leaderboard()
        await send_text(message_obj, osu_lb, is_private)


    elif "fie level" in message:

        user_id = str(message_obj.author.id)

        user_name = message_obj.author.display_name

        level_info = fiecommands.fie_level(user_id, user_name)

        if isinstance(level_info, tuple):

            text, image_path = level_info

            await send_text(message_obj, text, is_private)

            await send_file(message_obj, image_path, is_private)

        else:

            await send_text(message_obj, level_info, is_private)

    elif message.startswith("fie switch character"):
        tokens = message.split()
        if len(tokens) >= 4:
            new_char = tokens[3].capitalize()
            switch_msg = fiecommands.fie_switch_character(user_id, new_char)
            await send_text(message_obj.channel, switch_msg, is_private)

    elif message == "fie characters":
        char_list = fiecommands.fie_characters(user_id, message_obj.author.display_name)
        await send_text(message_obj, char_list, is_private)


    # ################################################## #
    # Commands triggered by a phrase in a message: Games #
    # ################################################## #

    elif "fie rps" in message:
        await fiegames.fie_rps(client_obj, message_obj)

    elif "fie hangman" in message:
        await fiegames.fie_hangman(client_obj, message_obj)

    # ################################### #
    # Demi's own command for his schedule #
    # ################################### #

    elif message == "fie schedule":
        tasks = [
            "19 de Maio - SD (Teste)",
            "20 de Maio - BD (Teste)",
            "21 de Maio - CG (Teste) ",
            "23 de Maio - BD (Trabalho)",
            "26 de Maio - TW (Trabalho)",
            "27 de Maio - TW (Teste)",
            "28 de Maio - CG (Blender)",
            "28 de Maio - SD (Trabalho)"
        ]

        user = await client_obj.fetch_user(164047938325184512)
        await user.send('\n'.join(tasks))
        await send_text(message_obj, "sent!", is_private)

    # ############################### #
    # The rest of message processing! #
    # ############################### #

    # Configure the daily messages watcher.
    client_obj.loop.create_task(send_daily_message(client_obj, is_private))

    # Repeated messages gag :)
    last_messages.append((message_obj.content, message_obj.author))
    print(last_messages)

    if is_repeated_msg(last_messages):
        await send_text(message_obj, last_messages[1][0], is_private)




# ******************************************************************************** #
# SEND MESSAGES TO SERVER FUNCTIONS:                                               #
# The following send_* functions are the helpers in charge of sending the messages #
# to the server and/or users in Discord.                                           #
# ******************************************************************************** #

async def send_text(
        message_or_channel_obj: Union[Message, DiscordChannelType],
        contents: str,
        is_private: bool) -> None:
    await send_message(message_or_channel_obj, contents, is_private, False)


async def send_file(
        message_or_channel_obj: Union[Message, DiscordChannelType],
        contents: str,
        is_private: bool) -> None:
    await send_message(message_or_channel_obj, contents, is_private, True)


async def send_message(
        message_or_channel_obj: Union[Message, DiscordChannelType],
        contents: str,
        is_private: bool,
        is_file: bool) -> None:
    try:
        destination = None

        # Sometimes we might get a Message object, which contains a pointer to the
        # channel object where it came from. Other times, we might get the channel
        # object directly. So, we have to make that distinction here to call the
        # send() method accordingly.

        if type(message_or_channel_obj) is Message:
            destination = (message_or_channel_obj.author if is_private
                           else message_or_channel_obj.channel)
        elif isinstance(message_or_channel_obj, DiscordChannelType):
            destination = message_or_channel_obj
        else:
            raise TypeError(f"Unrecognized channel type '{type(message_or_channel_obj)}'")

        if is_file:
            await destination.send(file=File(contents))
        else:
            await destination.send(contents)

    except Exception as e:
        print(e)


# ******************************************************************************* #
# OTHER UTILITIES:                                                                #
# Any other utility functions that are not specific to a command or game go here. #
# ******************************************************************************* #

# NOTE: This should go elsewhere, but I'm done dealing with that stupid circular
#       import error :skull:
def fie_response(user_input: str) -> str:
    if user_input == "best girl":
        return "Yeah that's me!"

    elif user_input == "fie":
        return sylphid_greeting()

    elif user_input == "fie help":
        return help_msg()

    elif any(msg in user_input for msg in ["hi fie", "hey fie"]):
        return f"Hey what's up {emote("WAVE")}"

    elif any(msg in user_input for msg in ["thank you fie", "thanks fie"]):
        return f"At your service {emote("SALUTE")}"

    elif any(msg in user_input for msg in
           ["good job fie",
            "good work fie",
            "nice job fie",
            "nice work fie"]):
        return f"Thanks~ {emote("BLUSHV")}"

    elif emote("GRINV") in user_input:
        return emote("GRINV")

    elif "good night fie" in user_input:
        return f"Night night {emote("SLEEP")}"

    elif "professorpd" in user_input:
        return f"ProfessorPd owns me {emote("PENSIVE")}"

    elif "yuuyuu" in user_input:
        return f"He's a good boy {emote("RELAXED")}"

    elif "good morning fie" in user_input:
        return f"Morning {emote("WAVE")}"

    # IDEA: Would be cool to somehow use some sports news outlet's API to get
    #       actual results of games here.

    if "fie gsw" in user_input:
        return "The Warriors are 0-0!"

    if "warriors" in user_input:
        return "WARRIORS!"

    if "fie bulls" in user_input:
        return "The Bulls are 29-39, but they will show off at the play-in ;)"

    if "nekotina" in user_input:
        return "Can you SHUT THE FUCK UP @nekotina"

    # Fie ain't taking blame on being mean ever >:)
    if "fie you're a meanie" in user_input:
        return "No u!"

    if "I love you fie" in user_input:
        return "Thanks! I love myself as well!"

    if "onana" in user_input:
        return "Get this trash GK out of United ASAP"

    if any(msg in user_input for msg in
             ["aaron",
              "kastle",
              "kay",
              "professor",
              "scooter",
              "nana",
              "sovy"]):
        return "Cool guy!"

    if "demi" in user_input:
        return "Never heard of him!"

    if "fox" in user_input:
        return "Cool guy! But needs to play trails!"
    return "<empty>"


async def send_daily_message(client: Client, is_private: bool):
    await client.wait_until_ready()

    channel1 = client.get_channel(420709830622183434)
    channel2 = client.get_channel(1300997938335580171)
    channel3 = client.get_channel(1299453968363032760)


    while not client.is_closed():
        now = datetime.now(UTC).time()

        # One message goes to channel2, and the rest go to channel1. So, we need
        # the index to know when to send to which channel.
        for i in range(0, len(daily_messages)):
            daily_msgobj = daily_messages[i]
            if i == 4:
                dest_channel = channel3
            elif i == 1:
                dest_channel = channel2
            else:
                dest_channel = channel1

            if not is_ready_to_send(daily_msgobj, now):
                continue

            print(f"Sending daily message {i+1} to channel {dest_channel}.")
            await send_text(dest_channel, daily_msgobj.message, is_private)
            daily_msgobj.has_been_sent_today = True

        # Check every minute.
        await asyncio.sleep(60)


def is_ready_to_send(msg_obj: DailyMessage, curr_time: time) -> bool:
    return (not msg_obj.has_been_sent_today) \
        and (msg_obj.scheduled_time.hour == curr_time.hour \
             and msg_obj.scheduled_time.minute == curr_time.minute)


def is_repeated_msg(msg_history: deque) -> bool:
    if len(msg_history) < 2:
        return False

    msg1 = msg_history[0]
    msg2 = msg_history[1]

    # Each element of the message history is a tuple containing the message content
    # first, and the author second. So, to define whether a message is repeated,
    # we have to check for same content but different author.
    return msg1[0] == msg2[0] and msg1[1] != msg2[1]


