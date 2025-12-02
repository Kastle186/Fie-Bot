# File: fietrails.py

from discord import Client, Message

from fie_trails.customization import change_orbments
from fieemotes import emote
from fie_trails.combat import fight, Rean
from fie_trails.character import Character
import asyncio
import fieutils


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

async def fie_trails(client_obj: Client, message_obj: Message):
    player_name = message_obj.author.name
    src_channel = message_obj.channel
    while True:
        await src_channel.send("Welcome back! What do you want to do?\n"
                               "1 - Fight\n"
                               "2 - Change Equipment\n"
                               "3 - Change Orbments\n"
                               "4 - Check status\n"
                               "0 - Quit\n")

        menu_choice = await wait_for_digit_reply(
            client_obj,
            message_obj.author,
            message_obj.channel,
            timeout=120.0
        )

        if menu_choice is None:
            await src_channel.send(
                f"You took too long to decide! I'm going to sleep {emote('SLEEP')}"
            )
            return

        option = int(menu_choice.content)
        match option:
            # Choose someone to fight
            case 1:
                await fight(client_obj, message_obj)
            # Change Equipment
            case 2:
                await src_channel.send("Work in progress!")
                return 0
            # Change Orbments
            case 3:
                await change_orbments(client_obj, message_obj, Rean)
            # Show status
            case 4:
                await fieutils.send_file(message_obj, "images/Rean_Menu_CSI.png", False)
                await src_channel.send(Character.status(Rean))
            case 0:
                await src_channel.send(f"Until next time! {emote("WAVE")}\n")
                return
            case _:
                return await src_channel.send("Are you serious? All you have to do is choose between 1 and 4...\n")


