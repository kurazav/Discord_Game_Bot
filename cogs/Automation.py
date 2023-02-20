import discord
from discord.ext import commands


class Automation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Automation.py ius ready.")

    # Auto-assign the 100 role to new members
    @commands.Cog.listener()
    async def on_member_join(self, member):
        join_role = discord.utils.get(member.guild.roles, name="100")

        await member.add_roles(join_role)


async def setup(bot):
    await bot.add_cog(Automation(bot))