from time import sleep
import fieutils
from fie_trails.character import Character
from fie_trails.enemy import Enemy
from fie_trails.craft import Craft
import random
import asyncio
from fieemotes import emote
from discord import Client, Message

# I don't know what I was thinking here
# But we need to fix this properly lol
# JSON

Rean = Character("Rean Schwarzer", 0 )
Dino = Enemy("Scary Dinosaur", 400, 400,30, 30, 20, 20, 20, 1, 50, 1, 500, [Craft("Bite", 30 * 2, 20), Craft("Decimate", 30 * 3, 40)])
initialized = False

async def wait_for_digit_reply(client, author, channel, timeout=120.0):
    """Waits for a numeric message from a specific user in a specific channel."""
    def check(m):
        return (
            m.author == author and
            m.channel == channel and
            m.content.isdigit()
        )

    try:
        return await client.wait_for("message", check=check, timeout=timeout)
    except asyncio.TimeoutError:
        return None


async def fight(client_obj: Client, message_obj: Message) -> None:
    src_channel = message_obj.channel

    async def choose_craft(character: Character):
        craft_list = " "
        for i in range(0, len(character.crafts)):
            craft_list += (f"{i+1} - " + str(character.get_crafts()[i]) + "\n")
        await src_channel.send(craft_list)

        # USE REUSABLE FUNCTION
        craft_choice = await wait_for_digit_reply(
            client_obj, message_obj.author, message_obj.channel
        )

        if craft_choice is None:
            await src_channel.send(
                f"You took too long to decide! I'm going to sleep {emote('SLEEP')}"
            )
            return

        craft_chosen = int(craft_choice.content)
        character.setCP(character.getCP() - character.crafts[craft_chosen-1].cost)
        if character.crafts[craft_chosen-1].name == "S-Craft - Flame Slash":
            await src_channel.send("Aoki honoo yo...\n")
            sleep(1)
            await src_channel.send("Waga ken ni tsudoe!\n")
            sleep(1)
            await fieutils.send_file(message_obj, "images/Rean_Schwarzer_S-Craft_Summer.png", False)
            sleep(0.5)
            await src_channel.send("Haaaaaaaa... zan!\n")
            sleep(2)
        return character.crafts[craft_chosen-1].damage

    async def choose_art(character: Character):
        art_list = " "
        for i in range(0, len(character.get_equipped_arts())):
            art_list += (f"{i + 1} - " + str(character.get_equipped_arts()[i]) + "\n")

        await src_channel.send(art_list)

        art_choice = await wait_for_digit_reply(
            client_obj, message_obj.author, message_obj.channel
        )

        if art_choice is None:
            await src_channel.send(
                f"You took too long to decide! I'm going to sleep {emote('SLEEP')}"
            )
            return

        art_chosen = int(art_choice.content)
        character.setEP(character.getEP() - character.get_equipped_arts()[art_chosen - 1].cost)

        return character.get_equipped_arts()[art_chosen - 1].damage

    async def character_turn(character: Character):
        await src_channel.send("Choose an action\n"
                               "1-Normal Attack\n"
                               "2-Crafts\n"
                               "3-Arts\n"
                               "4-Items\n")

        # USE REUSABLE FUNCTION
        combat_choice = await wait_for_digit_reply(
            client_obj, message_obj.author, message_obj.channel
        )

        if combat_choice is None:
            await src_channel.send(
                f"You took too long to decide! I'm going to sleep {emote('SLEEP')}"
            )
            return

        option = int(combat_choice.content)
        match option:
            case 1:
                return character.STR
            case 2:
                return await choose_craft(character)
            case 3:
                return await choose_art(character)
            case 4:
                return 0
            case _:
                await src_channel.send("Are you serious? All you have to do is choose between 1 and 4...")

    async def enemy_turn(enemy: Enemy):
        choice = random.randint(0, 2)

        if choice != 0:
            await src_channel.send(f"{enemy.get_name()} used {enemy.get_specific_craft(choice-1)}\n")
        else:
            await src_channel.send(f"{enemy.get_name()} used a normal attack!\n")
        sleep(1)

        match choice:
            case 0:
                return enemy.STR
            case _:
                enemy.setCP(enemy.getCP() - enemy.crafts[choice-1].cost)
                return enemy.crafts[choice-1].damage

    def reset_everyone(enemy: Enemy, character: Character):
        character.reset()
        enemy.reset()

    async def check_victory(enemy: Enemy, character: Character):
        if enemy.get_current_HP() <= 0:
            print(enemy.get_current_HP())
            await src_channel.send("You won!\n")
            reset_everyone(enemy, character)
            character.setXP(character.getXP() + enemy.getXP())
            await src_channel.send(f"XP gained: {enemy.getXP()}")
            return True
        return False

    async def check_defeat(character: Character, enemy: Enemy):
        if character.get_current_HP() <= 0:
            print(character.get_current_HP())
            await src_channel.send("You lost!\n")
            reset_everyone(enemy, character)
            return True
        return False

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
        while character.current_HP > 0 and enemy.current_HP > 0:
            if character.SPD >= enemy.SPD:
                difference = dif(await character_turn(character) - enemy.getDEF())
                enemy.set_current_HP(enemy.get_current_HP() - difference)
                await src_channel.send("Enemy HP: " + str(enemy.get_current_HP()) + f" (-{difference})\n")
                sleep(1)

                if await check_victory(enemy, character):
                    return

                difference = dif(await enemy_turn(enemy) - character.getDEF())
                character.set_current_HP(character.get_current_HP() - difference)
                await src_channel.send("Character HP: " + str(character.get_current_HP()) + f" (-{difference})\n")
                sleep(1)

                if await check_defeat(character, enemy):
                    return

            else:
                difference = dif(await enemy_turn(enemy) - character.getDEF())
                character.set_current_HP(character.get_current_HP() - difference)
                await src_channel.send("Character HP: " + str(character.get_current_HP()) + f" (-{difference})\n")
                sleep(1)

                if await check_defeat(character, enemy):
                    return

                difference = dif(await character_turn(character) - enemy.getDEF())
                enemy.set_current_HP(enemy.get_current_HP() - difference)
                await src_channel.send("Enemy HP: " + str(enemy.get_current_HP()) + f" (-{difference})\n")
                sleep(1)

                if await check_victory(enemy, character):
                    return

        await check_victory(enemy, character)
        await check_defeat(character, enemy)

    await start_fight(Rean, Dino)

