import asyncio
from discord import Client, Message
from fie_trails.character import Character
from fie_trails.art import Art
from fieemotes import emote


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

async def change_orbments(client_obj: Client, message_obj: Message, character: Character) -> None:
    src_channel = message_obj.channel
    orbment_list = ""

    # CHARACTER'S EQUIPPED ORBMENTS
    for i in range(0, len(character.get_equipped_orbments())):
        orbment_list += (f"{i + 1} - " + str(character.get_equipped_orbments()[i]) + "\n")

    if orbment_list == "":
        await src_channel.send("No current equipped orbments found.\n")
    else:
        await src_channel.send("Equipped orbments:\n" + orbment_list)

    await src_channel.send("0 - Exit")

    orbment_choice = await wait_for_digit_reply(
        client_obj, message_obj.author, message_obj.channel
    )

    if orbment_choice is None:
        await src_channel.send(
            f"You took too long to decide! I'm going to sleep {emote('SLEEP')}"
        )
        return

    orbment_chosen = int(orbment_choice.content)
    if orbment_chosen == 0:
        return
    elif orbment_chosen > 6:
        await src_channel.send("That's not an available slot!")
        return
    else:
        available_orbment_list = " "

        # CHARACTER'S AVAILABLE ORBMENTS
        for i in range(0, len(character.get_available_orbments())):
            available_orbment_list += (f"{i + 1} - " + str(character.get_available_orbments()[i]) + "\n")

        if available_orbment_list == " ":
            await src_channel.send("No current available orbments found.\n")
        else:
            await src_channel.send("Available orbments:\n" + available_orbment_list)
        await src_channel.send("0 - Exit")

        replacement_choice = await wait_for_digit_reply(client_obj, message_obj.author, message_obj.channel)
        if orbment_choice is None:
            await src_channel.send(
                f"You took too long to decide! I'm going to sleep {emote('SLEEP')}"
            )
            return

        available_chosen = int(replacement_choice.content)
        if available_chosen == 0:
            return

        else:
            # We will set a new orbment here
            await src_channel.send(f"Replaced orbment: {character.get_equipped_orbments()[orbment_chosen - 1]} for "
                                   f"{character.get_available_orbments()[available_chosen - 1]}" )

            trader = character.get_available_orbments()[available_chosen - 1]
            character.set_available_orbments(available_chosen - 1, character.get_equipped_orbments()[orbment_chosen - 1])
            character.set_equipped_orbments(orbment_chosen - 1, trader)

        
async def change_equipment(client_obj: Client, message_obj: Message, character: Character) -> None:
    src_channel = message_obj.channel
    # WIP




