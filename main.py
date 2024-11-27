from discord import Intents, Client, Message
from dotenv import load_dotenv
from fieutils import handle_message

import asyncio
import os

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

    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    print(f"{channel} {username}: {user_message}")
    await handle_message(client, message)


# STEP 4: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)

if __name__ == "__main__":
    main()
