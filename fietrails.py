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
    await src_channel.send("Welcome back! For the purpose of this test, let's fight!\n")
    await fight(client_obj, message_obj)

