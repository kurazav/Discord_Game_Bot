import discord
from discord.ext import commands
import random


class GameCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # On Ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("GameCommand.py is online.")

    # /register - TO DO
    @commands.command()
    async def register(self, ctx):
        # await ctx.author.send("hah not working yet")
        commands_channel = discord.utils.get(ctx.guild.channels, name="🧠┃commands")

        if ctx.channel.id == commands_channel.id:
            # to do
            await ctx.send("Command ran successfully")


async def setup(bot):
    await bot.add_cog(GameCommand(bot))

