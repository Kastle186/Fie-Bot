from datetime import datetime, timedelta, time
from discord import Intents, Client, Message, File
from dotenv import load_dotenv
from fieutils import handle_message
from typing import Final

import asyncio
import math
import os
import random
import statistics


# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')


# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)


# STEP 2: HANDLING THE STARTUP FOR OUR BOT
@client.event
async def on_ready() -> None:
    print(f"{client.user} is now running!")


# STEP 3: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f"{channel} {username}: {user_message}")
    await handle_message(client, message)

    """
    REPEAT MESSAGE
    """
    last_messages.append((message.content, message.author))
    print(last_messages)
    if len(last_messages) > 2:
        last_messages.pop(0)

    if len(last_messages) == 2 and last_messages[0][0] == last_messages[1][0] and last_messages[0][1] != last_messages[1][1]:
        await message.channel.send(last_messages[1][0])


# STEP 4: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()
