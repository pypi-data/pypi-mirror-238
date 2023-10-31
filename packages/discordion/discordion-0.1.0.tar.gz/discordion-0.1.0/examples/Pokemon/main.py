import discord
import os
from dotenv import load_dotenv

load_dotenv()

from tasks import *
from discordion.tasks import Tasks

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
print('outside', OPENAI_API_KEY)
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await Tasks.run(message)

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
