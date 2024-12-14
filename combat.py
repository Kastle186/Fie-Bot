from time import sleep
import fieutils
from character import Character
from enemy import Enemy
from craft import Craft
import random
import asyncio
from fieemotes import emote
from discord import Client, Message

Rean = Character("Rean Schwarzer", 500, 50, 50, 25, 30, 30, 30, 20, 60, 0)
Dino = Enemy("Scary Dinosaur", 400, 30, 30, 20, 20, 20, 1, 50, 1, 50, [Craft("Bite", 30 * 2, 20), Craft("Decimate", 30 * 3, 40)])
initialized = False

async def fight(client_obj: Client, message_obj: Message) -> None:
    src_channel = message_obj.channel

    async def choose_craft(character: Character):
        for i in range(0, len(character.crafts)):
            await src_channel.send(f"{i+1} - " + str(character.get_crafts()[i]) + "\n")

        def check_craft_choice(m):
            return m.author == message_obj.author \
                and m.channel == message_obj.channel \
                and m.content.isdigit()

        try:
            craft_choice = await client_obj.wait_for(
                'message',
                check=check_craft_choice,
                timeout=120.0)
        except asyncio.TimeoutError:
            await src_channel.send(
                f"You took too long to decide! I'm going to sleep {emote("SLEEP")}")
            return

        craft_chosen = int(craft_choice.content)
        character.setCP(character.getCP() - character.crafts[craft_chosen-1].cost)
        if character.crafts[craft_chosen-1].name == "S-Craft - Flame Slash":
            await src_channel.send("Aoki honoo yo...\n")
            sleep(1)
            await src_channel.send("Waga ken ni tsudoe!\n")
            sleep(1)
            await fieutils.send_file(message_obj, "images/Rean_Schwarzer_S-Craft_Summer.png", True)
            sleep(0.5)
            await src_channel.send("Haaaaaaaa... zan!\n")
            sleep(2)
        return character.crafts[craft_chosen-1].damage

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
                timeout=120.0)
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

    async def enemy_turn(enemy: Enemy):
        choice = random.randint(0, 2)

        # Let's let the user know what the enemy used!
        if choice != 0:
            await src_channel.send(f"{enemy.get_name()} used {enemy.get_specific_craft(choice-1)}\n")
        else:
            await src_channel.send(f"{enemy.get_name()} used a normal attack!\n")
        sleep(1)
        match choice:
            # Normal Attack
            case 0:
                return enemy.STR
            # Random craft
            case _:
                enemy.setCP(enemy.getCP() - enemy.crafts[choice-1].cost)
                return enemy.crafts[choice-1].damage

    # When the fight is over, reset everyone's stats
    def reset_everyone(enemy: Enemy, character: Character):
        character.reset()
        enemy.reset()
    async def check_victory(enemy: Enemy, character: Character):
        if enemy.getHP() <= 0:
            print(enemy.getHP())
            await src_channel.send("You won!\n")

            # Note: We should reset the stats before the characters gets XP
            reset_everyone(enemy, character)
            character.setXP(character.getXP() + enemy.getXP())
            await src_channel.send(f"XP gained: {enemy.getXP()}")
            return True
        return False

    async def check_defeat(character: Character, enemy: Enemy):
        if character.getHP() <= 0:
            await src_channel.send("You lost!\n")
            reset_everyone(enemy, character)
            return True
        return False

    # We don't want people regenerating
    def dif(difference: int):
        if difference < 0:
            return 0
        else:
            return difference

    async def start_fight(character: Character, enemy: Enemy):
        global initialized
        if not initialized:
            character.initialize_rean()
            initialized = True
        while character.HP > 0 and enemy.HP > 0:
            if character.SPD >= enemy.SPD:

                # Player Attack
                difference = dif(await character_turn(character) - enemy.getDEF())
                enemy.setHP(enemy.getHP() - difference)
                await src_channel.send("Enemy HP: " + str(enemy.getHP()) + f" (-{difference})\n")
                sleep(1)

                # Check if the enemy is dead
                if await check_victory(enemy, character):
                    return

                # Enemy attack
                difference = dif(await enemy_turn(enemy) - character.getDEF())
                character.setHP(character.getHP() - difference)
                await src_channel.send("Character HP: " + str(character.getHP()) + f" (-{difference})\n")
                sleep(1)
                # Check if the player is dead
                if await check_defeat(character, enemy):
                    return

            else:
                # Enemy attack
                difference = dif(await enemy_turn(enemy) - character.getDEF())
                character.setHP(character.getHP() - difference)
                await src_channel.send("Character HP: " + str(character.getHP()) + f" (-{difference})\n")
                sleep(1)

                # Check if the player is dead
                if await check_defeat(character, enemy):
                    return

                # Player attack
                difference = dif(await character_turn(character) - enemy.getDEF())
                enemy.setHP(enemy.getHP() - difference)
                await src_channel.send("Enemy HP: " + str(enemy.getHP()) + f" (-{difference})\n")
                sleep(1)

                # Check if the enemy is dead
                if await check_victory(enemy, character):
                    return

        await check_victory(enemy, character)
        await check_defeat(character, enemy)

    await start_fight(Rean, Dino)

