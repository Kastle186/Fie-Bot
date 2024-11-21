# File: fieutils.py

from discord import (
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

from responses import get_response
from typing import TypeAlias, Union

import asyncio
import random

# NOTE: Don't forget to restore the greeting and help commands.

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

DiscordChannelType: TypeAlias = Union[
    DMChannel,
    GroupChannel,
    PartialMessageable,
    StageChannel,
    TextChannel,
    Thread,
    VoiceChannel
]


def emote(emote_name: str) -> str:
    return fieemotes.get(emote_name, "???")


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

async def handle_message(message_obj: Message) -> None:
    user_message = message_obj.content

    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    if is_private := user_message[0] == "?":
        user_message = user_message[1:]

    message = user_message.casefold()
    fie_response = get_response(message)

    # We got one of the responses from Fie! So we send it to the server as is.
    if not fie_response == "<empty>":
        await send_text(message_obj, fie_response, is_private)
        return


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
