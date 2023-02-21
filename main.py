# This example requires the 'message_content' intent.
import discord
import os
import asyncio
from discord.ext import commands, tasks
from itertools import cycle
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Command prefix and Bot Status
bot = commands.Bot(command_prefix='!', intents=intents)
bot_status = cycle(["Type in '/bot --help for help!", "Thank you! Have fun!"])

# Load the .env file
load_dotenv()

# Things to happen on ready
@bot.event
async def on_ready():
    await bot.tree.sync()
    change_status.start()


# Slash command /ping to get the bot's latency
@bot.tree.command(name="ping", description="Shows the latency of the bot")
async def ping(interaction: discord.Interaction):
    b_latency = round(bot.latency * 1000)  # latency
    commands_channel = discord.utils.get(interaction.guild.channels, name="🧠┃commands")

    if interaction.channel.id == commands_channel.id:
        await interaction.response.send_message(f"Pong! {b_latency} ms.", ephemeral=True)


# Change the bot's status in the members list
@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(bot_status)))


async def load():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"{filename[:-3]} is loaded")


async def main():
    async with bot:
        await load()
        await bot.start(os.getenv('DISCORD_BOT_TOKEN'))


asyncio.run(main())
