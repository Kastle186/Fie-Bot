# File: fietrails.py

from discord import Client, Message
from fieemotes import emote
from combat import Combat
from character import Character
from enemy import Enemy

import asyncio
import csv
import os
import random

Rean = Character("Rean",500,50,50,25,30,30,1)
Dino = Enemy("Scary Dinosaur",400,30,30,20,20,20,1)
combat: Combat()


async def fie_trails(client_obj: Client, message_obj: Message):
    player_name = message_obj.author.name
    src_channel = message_obj.channel
    await src_channel.send("Welcome back! For the purpose of this test, let's fight!\n")
    combat.start_fight(Rean, Dino)

