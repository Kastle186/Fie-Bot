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

from dataclasses import dataclass
from datetime import datetime, time, UTC
from fieemotes import emote
from typing import TypeAlias, Union

import asyncio
import fiecommands
import fiegames
import random

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
    "fie.png",
    "Fie_Claussell_SD_29.png",
    "Rean x fie.png",
    "stylish fie.png",
    "cute fie.png",
    "fie bye bye.png",
    "fie (and laura).png",
    "ValentineKuro.png"
]

# List of daily messages and their info to send them.

# NOTE: Right now, we depend on the bot getting restarted at least once a day to
#       get all messages to be sent. It would be cool to implement something to have
#       them reset on their own, if at some point we end up leaving the bot running
#       during the night too.

daily_messages = [
    DailyMessage(
        False,
        time(hour=23, tzinfo=UTC),
        ("<@98491257784909824> have you trained yet? "
         "Laura is expecting you <:Laura_S:1252956467779076106>")
    ),

    DailyMessage(
        False,
        time(hour=19, tzinfo=UTC),
        ("<@444271831118249996> it's a bit embarassing to hear how much you "
         f"appreciate me but thanks! I appreciate you too Yuuyuu {emote("GRINV")}")
    ),

    DailyMessage(
        False,
        time(hour=21, tzinfo=UTC),
        ("<@145607631149465600> <:Laura_S:1252956467779076106>: "
         "HELLO NANA, HOPE YOU HAD A GOOD DAY! I STILL DON'T KNOW HOW TO "
         "USE MY PHONE VERY WELL. HOPE YOU TAKE CARE OF YOURSELF - LAURA")
    ),

    DailyMessage(
        False,
        time(hour=1, tzinfo=UTC),
        ("<@164047938325184512> <:Fie_Claussell:1304860526936985620> "
         "Are you still awake you son of a gun? Don't you have uni tomorrow? "
         "Or a life? Get your ass to bed immediately.")
    ),
]

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
    fie_res = fiecommands.fie_response(message)

    # We got one of the responses from Fie! So we send it to the server as is.
    if not fie_res == "<empty>":
        await send_text(message_obj, fie_res, is_private)

    # #################################### #
    # Commands triggered by one word only. #
    # #################################### #

    if message == "claussell":
        img_to_send = random.choice(fie_image_files)
        await send_file(message_obj, img_to_send, is_private)

    if message == "kastle":
        await send_file(message_obj, "Noel.png", is_private)

    if message == "kayrennede007":
        await send_file(message_obj, "HOT-SHOT_-_Renne_Kuro.png", is_private)

    # ###################################################### #
    # Commands triggered by a phrase in a message: Utilities #
    # ###################################################### #

    if message in "fie time":
        timezones_str = fiecommands.fie_time(message_obj.channel.id)
        await send_text(message_obj, timezones_str, is_private)

    if message in "fie solve":
        math_result = fiecommands.fie_solve(message)
        await send_text(message_obj, math_result, is_private)

    if message in "fie how many days until":
        days_until = fiecommands.fie_days_until(message)
        await send_text(message_obj, days_until, is_private)

    # TODO: Add the option to also recognize 'fie what is' as the command.
    if message in "fie what's":
        fun_fact = fiecommands.fie_what_is(message)
        await send_text(message_obj, fun_fact, is_private)

    # ################################################## #
    # Commands triggered by a phrase in a message: Games #
    # ################################################## #

    if message in "fie rps":
        await fiegames.fie_rps(client_obj, message_obj)

    if message in "fie hangman":
        await fiegames.fie_hangman(client_obj, message_obj)

    # ################################### #
    # Demi's own command for his schedule #
    # ################################### #

    if message == "fie schedule":
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

        user = await client_obj.fetch_user(164047938325184512)
        await user.send('\n'.join(tasks))
        await send_text(message_obj, "sent!", is_private)

    # ############################### #
    # The rest of message processing! #
    # ############################### #

    # Configure the daily messages watcher.
    client_obj.loop.create_task(send_daily_message(client_obj, is_private))


# ******************************************************************************** #
# SEND MESSAGES TO SERVER FUNCTIONS:                                               #
# The following send_* functions are the helpers in charge of sending the messages #
# to the server and/or users in Discord.                                           #
# ******************************************************************************** #

async def send_text(
        message_or_channel_obj: Union[Message, DiscordChannelType],
        contents: str,
        is_private: bool) -> None:
    await send_message(message_or_channel, user_message, is_private, False)


async def send_file(
        message_or_channel_obj: Union[Message, DiscordChannelType],
        contents: str,
        is_private: bool) -> None:
    await send_message(message_or_channel, user_message, is_private, True)


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

        if type(message_or_channel) is Message:
            destination = (message_or_channel.author if is_private
                           else message_or_channel.channel)
        elif isinstance(message_or_channel, DiscordChannelType):
            destination = message_or_channel
        else:
            raise TypeError(f"Unrecognized channel type '{type(message_or_channel)}'")

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

async def send_daily_message(client: Client, is_private: bool):
    await client.wait_until_ready()

    channel1 = client.get_channel(420709830622183434)
    channel2 = client.get_channel(1300997938335580171)

    while not client.is_closed():
        now = datetime.now(UTC).time()

        # One message goes to channel2, and the rest go to channel1. So, we need
        # the index to know when to send to which channel.
        for i in range(0, len(daily_messages)):
            daily_msgobj = daily_messages[i]
            dest_channel = channel2 if i == 1 else channel1

            if not is_ready_to_send(daily_msgobj, now):
                continue

            await send_text(dest_channel, daily_msgobj.message, is_private)
            daily_msgobj.has_been_sent_today = True

        # Check every minute.
        await asyncio.sleep(60)


def is_ready_to_send(msg_obj: DailyMessage, curr_time: time) -> bool:
    return (not msg_obj.has_been_sent_today) \
        and (msg_obj.scheduled_time.hour == curr_time.hour \
             and msg_obj.scheduled_time.minute == curr_time.minute)
