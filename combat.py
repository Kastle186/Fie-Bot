from character import Character
from enemy import Enemy
from craft import Craft
import random
import asyncio
from fieemotes import emote
from discord import Client, Message

Rean = Character("Rean",500,50,50,25,30,30,1, 0,1,0)
Dino = Enemy("Scary Dinosaur",400,30,30,20,20,20,1,50,1,50, [Craft("Bite", 30 * 2, 20), Craft("Decimate", 30 * 3, 40)])


async def fight(client_obj: Client, message_obj: Message) -> None:
    src_channel = message_obj.channel

    async def choose_craft(character: Character):
        for i in range(0, len(character.crafts)):
            await src_channel.send(f"{i}- " + str(character.crafts[i]) + "\n")

        def check_craft_choice(m):
            return m.author == message_obj.author \
                and m.channel == message_obj.channel \
                and m.content.isdigit()

        try:
            craft_choice = await client_obj.wait_for(
                'message',
                check=check_craft_choice,
                timeout=30.0)
        except asyncio.TimeoutError:
            await src_channel.send(
                f"You took too long to decide! I'm going to sleep {emote("SLEEP")}")
            return

        craft_chosen = int(craft_choice.content)
        character.setCP(character.getCP() - character.crafts[craft_chosen].cost)
        return character.crafts[craft_chosen].damage

    async def character_turn(character: Character):
        await src_channel.send("Choose an action\n"
                               "1-Normal Attack\n"
                               "2-Crafts\n"
                               "3-Arts\n"
                               "4-Items\n")

        def check_combat_choice(m):
            return m.author == message_obj.author \
                and m.channel == message_obj.channel \
                and m.content.isdigit()

        try:
            combat_choice = await client_obj.wait_for(
                'message',
                check=check_combat_choice,
                timeout=30.0)
        except asyncio.TimeoutError:
            await src_channel.send(
                f"You took too long to decide! I'm going to sleep {emote("SLEEP")}")
            return

        option = int(combat_choice.content)
        match option:
            # Normal Attack
            case 1:
                return character.STR
            # Crafts
            case 2:
                return await choose_craft(character)
            # Arts
            case 3:
                return 0
            # Items
            case 4:
                return 0

    def enemy_turn(enemy: Enemy):
        choice = random.randint(0, 2)
        match choice:
            # Normal Attack
            case 0:
                return enemy.STR
            # Random craft
            case _:
                enemy.setCP(enemy.getCP() - enemy.crafts[choice].cost)
                return enemy.crafts[choice]
    async def check_victory(enemy: Enemy, character: Character):
        if enemy.getHP() <= 0:
            await src_channel.send("You won!\n")
            character.setXP(character.getXP() + enemy.getXP())
            await src_channel.send("XP gained:")
            return True
        return False

    async def check_defeat(character: Character):
        if character.getHP() <= 0:
            await src_channel.send("You lost!\n")
            return True
        return False

    async def start_fight(character: Character, enemy: Enemy):
        while character.HP > 0 and enemy.HP > 0:
            if character.SPD >= enemy.SPD:
                enemy.setHP(enemy.getDEF() - await character_turn(character))
                # Check if the enemy is dead
                if await check_victory(enemy, character):
                    return

                character.setHP(character.getDEF() - enemy_turn(enemy))
                await src_channel.send(character.getHP())

                # Check if the player is dead
                if await check_defeat(character):
                    return

            else:
                character.setHP(character.getDEF() - enemy_turn(enemy))
                await src_channel.send(character.getHP())

                # Check if the player is dead
                if await check_defeat(character):
                    return

                enemy.setHP(enemy.getDEF() - await character_turn(character))
                await src_channel.send(enemy.getHP())

                # Check if the enemy is dead
                if await check_victory(enemy, character):
                    return

        await check_victory(enemy, character)
        await check_defeat(character)

    await start_fight(Rean,Dino)

