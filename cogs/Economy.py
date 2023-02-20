import discord
from discord.ext import commands
import json
import random


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Economy is online")

    @commands.command(aliases=["bal", "inventory", "i"])
    async def balance(self, ctx, member: discord.Member = None):
        with open("cogs/json/economy.json", "r") as f:
            user_economy = json.load(f)
        if member is None:
            member = ctx.author
        elif member is not None:
            member = member

        if str(member.id) not in user_economy:
            user_economy[str(member.id)] = {}
            user_economy[str(member.id)]["Balance"] = 100

            with open("cogs/json/economy.json", "w") as f:
                json.dump(user_economy, f, indent=4)

        economy_embed = discord.Embed(title=f"{member.name}'s Current Balance",
                                      description="The current balance of this user.",
                                      color=discord.Color.green())
        economy_embed.add_field(name="Current Balance:",
                                value=f"C{user_economy[str(member.id)]['Balance']}")
        economy_embed.set_footer(text="Want to increase balance? Try running some economy based commands!",
                                 icon_url=None)

        await ctx.send(embed=economy_embed)

    @commands.cooldown(1, per=3600)
    @commands.command()
    async def beg(self, ctx):
        commands_channel = discord.utils.get(ctx.guild.channels, name="🧠┃commands")
        if ctx.channel.id == commands_channel.id:
            with open("cogs/json/economy.json", "r") as f:
                user_economy = json.load(f)

            if str(ctx.author.id) not in user_economy:
                user_economy[str(ctx.author.id)] = {}
                user_economy[str(ctx.author.id)]["Balance"] = 100

                with open("cogs/json/economy.json", "w") as f:
                    json.dump(user_economy, f, indent=4)

            current_balance = user_economy[str(ctx.author.id)]["Balance"]
            amount = random.randint(-10, 5)
            new_balance = current_balance + amount

            if current_balance > new_balance:
                economy_embed = discord.Embed(title="No bueno! - You've been robbed!",
                                              description="A group of creatures took advantage of you and stole some of your coins!",
                                              color=discord.Color.red())
                economy_embed.add_field(name="New Balance:", value=f"C{new_balance}", inline=False)
                economy_embed.set_footer(text="You should probably move to a new place in the Outerlands...", icon_url=None)
                await ctx.send(embed=economy_embed, ephemeral=True)

                user_economy[str(str(ctx.author.id))]["Balance"] += amount

                with open("cogs/json/economy.json", "w") as f:
                    json.dump(user_economy, f, indent=4)

            elif current_balance < new_balance:
                economy_embed = discord.Embed(title="Feels great!",
                                              description="There are still some good creatures out there!",
                                              color=discord.Color.green())
                economy_embed.add_field(name="New Balance:",
                                        value=f"C{new_balance}",
                                        inline=False)
                economy_embed.set_footer(text="While this feels great, you must not be greedy and wait for at least 1 hour until you shall beg again",
                                         icon_url=None)
                await ctx.send(embed=economy_embed, ephemeral=True)

                user_economy[str(str(ctx.author.id))]["Balance"] += amount

                with open("cogs/json/economy.json", "w") as f:
                    json.dump(user_economy, f, indent=4)

            elif current_balance == new_balance:
                economy_embed = discord.Embed(title="No luck this time!",
                                              description="No good karma for you yet, it seems like.",
                                              color=discord.Color.green())
                economy_embed.add_field(name="Balance:", value=f"C{current_balance}", inline=False)
                economy_embed.set_footer(
                    text="While this feels bad, you must control your emotions and wait for at least 1 hour until you shall beg again",
                    icon_url=None)
                await ctx.send(embed=economy_embed, ephemeral=True)

    @commands.cooldown(1, per=3600)
    @commands.command()
    async def work(self, ctx):
        commands_channel = discord.utils.get(ctx.guild.channels, name="🧠┃commands")
        if ctx.channel.id == commands_channel.id:
            with open("cogs/json/economy.json", "r") as f:
                user_economy = json.load(f)

            if str(ctx.author.id) not in user_economy:
                user_economy[str(ctx.author.id)] = {}
                user_economy[str(ctx.author.id)]["Balance"] = 100

                with open("cogs/json/economy.json", "w") as f:
                    json.dump(user_economy, f, indent=4)

            amount = random.randint(30, 75)
            user_economy[str(ctx.author.id)]["Balance"] += amount

            economy_embed = discord.Embed(title="Work Well Done!",
                                          description="You've been working for some shady creatures in the Outerlands, and here's what you earned...",
                                          color=discord.Color.green())
            economy_embed.add_field(name="Earnings:",
                                    value=f"C{amount}",
                                    inline=False)
            economy_embed.add_field(name="New Balance:",
                                    value=f"C{user_economy[str(ctx.author.id)]['Balance']}",
                                    inline=False)
            economy_embed.set_footer(text="While this feels great, you must not be greedy and wait for at least 1 hour until you shall work again.",
                                     icon_url=None)
            await ctx.send(embed=economy_embed, ephemeral=True)

            with open("cogs/json/economy.json", "w") as f:
                json.dump(user_economy, f, indent=4)

    @beg.error
    async def beg_error(self, ctx, error):
        commands_channel = discord.utils.get(ctx.guild.channels, name="🧠┃commands")
        if ctx.channel.id == commands_channel.id:
            if isinstance(error, commands.CommandOnCooldown):
                await ctx.send("!!! Your command is on cooldown!", ephemeral=True)

    @work.error
    async def work_error(self, ctx, error):
        commands_channel = discord.utils.get(ctx.guild.channels, name="🧠┃commands")
        if ctx.channel.id == commands_channel.id:
            if isinstance(error, commands.CommandOnCooldown):
                await ctx.send("!!! Your command is on cooldown!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Economy(bot))
