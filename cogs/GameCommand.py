import discord
from discord.ext import commands
from db_checks import create_user, get_user
import re
from discord import app_commands


def check(email):
    pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pat, email):
        return True
    return False

# s = "popular_website15@comPany.com"
# print(solve(s))


class GameCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # On Ready
    @commands.Cog.listener()
    async def on_ready(self):
        print("GameCommand.py is online.")

    # Slash command to register your account
    @app_commands.command(name="register", description="Use your email to register to Ivory Village!!")
    async def register(self, interaction: discord.Interaction, email: str):
        register_channel = discord.utils.get(interaction.guild.channels, name="💬┃chat")
        if interaction.channel.id == register_channel.id:
            if check(email):
                user = get_user(interaction.user.id)
                if user is None:
                    create_user(interaction.user.id, interaction.user.name, email)
                    new_user = get_user(interaction.user.id)
                    await interaction.response.send_message(f"User Created: {new_user}", ephemeral=True)

                    member = interaction.user
                    register_role = discord.utils.get(member.guild.roles, name="Villager")
                    await interaction.user.add_roles(register_role)
                else:
                    await interaction.response.send_message(f"You already have an account: {user}", ephemeral=True)
            else:
                await interaction.response.send_message("Invalid Email!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(GameCommand(bot))

