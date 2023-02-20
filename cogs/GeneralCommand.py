import discord
from discord.ext import commands
import random


class GeneralCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("GeneralCommand.py is online!")

    # /welcome | /gm /morning | Command
    @commands.command(aliases=['gm', 'morning'])
    async def autoresponse(self, ctx):
        with open("data/responses.txt", "r") as f:
            random_responses = f.readlines()
            response = random.choice(random_responses)

            await ctx.send(response)

    # /embed Command
    @commands.command()
    async def test(self, ctx):
        commands_channel = discord.utils.get(ctx.guild.channels, name="🧠┃commands")
        if ctx.channel.id == commands_channel.id:
            embed_message = discord.Embed(title="Title", description="Description", color=discord.Color.green())

            embed_message.set_author(name=f"Requested by {ctx.author.mention}", icon_url=ctx.author.avatar)
            embed_message.set_thumbnail(url=ctx.guild.icon)
            embed_message.set_image(url=ctx.guild.icon)
            embed_message.add_field(name="Field Name", value="Field Value", inline=False)
            embed_message.set_footer(text="This is the footer", icon_url=ctx.author.avatar)

            await ctx.send(embed=embed_message)

    @commands.command()
    async def simon(self, ctx, *, message: str):
        commands_channel = discord.utils.get(ctx.guild.channels, name="🧠┃commands")
        if ctx.channel.id == commands_channel.id:
            await ctx.send(f"Simon Says: {message}")

    @simon.error
    async def simon_error(self, ctx, error):
        commands_channel = discord.utils.get(ctx.guild.channels, name="🧠┃commands")
        if ctx.channel.id == commands_channel.id:
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send("!!! Error: Missing Required Arguments!")


async def setup(bot):
    await bot.add_cog(GeneralCommand(bot))