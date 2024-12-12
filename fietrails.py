# File: fietrails.py

from discord import Client, Message
from fieemotes import emote
from combat import fight
from character import Character
from enemy import Enemy

import asyncio
import csv
import os
import random


async def fie_trails(client_obj: Client, message_obj: Message):
    player_name = message_obj.author.name
    src_channel = message_obj.channel
    await src_channel.send("Welcome back! What do you want to do?\n"
                           "1 - Fight\n"
                           "2 - Change Equipment\n"
                           "3 - Change Orbments\n"
                           "4 - Check status\n")
    def check_menu_choice(m):
        return m.author == message_obj.author \
            and m.channel == message_obj.channel \
            and m.content.isdigit()
    try:
        menu_choice = await client_obj.wait_for(
            'message',
            check=check_menu_choice,
            timeout=120.0)
    except asyncio.TimeoutError:
        await src_channel.send(
            f"You took too long to decide! I'm going to sleep {emote("SLEEP")}")
        return

    option = int(menu_choice.content)
    match option:
        # Choose someone to fight
        case 1:
            await fight(client_obj, message_obj)
        # Change Equipment
        case 2:
            return 0
        # Change Orbments
        case 3:
            return 0
        # Show status
        case 4:
            return 0

        case _:
            return "Are you serious? All you have to do is choose between 1 and 4...\n"


