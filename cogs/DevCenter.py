import discord
from discord.ext import commands
from discord import app_commands


class DevCenter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        print("DevCenter.py is ready.")

    @app_commands.command(name="dev", description="Placeholder slash command for now")
    @commands.has_permissions(administrator=True)
    async def dev(self, interaction: discord.Interaction):
        commands_channel = discord.utils.get(interaction.guild.channels, name="dev-center")
        if interaction.channel.id == commands_channel.id:
            if interaction.user.id == 326050062473887755:
                await interaction.response.send_message("Command ran by dev", ephemeral=True)
            else:
                await interaction.response.send_message("You are not a dev", ephemeral=True)

    @app_commands.command(name="avatar", description="Sends user's avatar in a embed")
    @commands.has_permissions(administrator=True)
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        commands_channel = discord.utils.get(interaction.guild.channels, name="dev-center")
        if member is None:
            member = interaction.user
        elif member is not None:
            member = member
        if interaction.channel.id == commands_channel.id:
            avatar_embed = discord.Embed(title=f"{member.name}'s Avatar", color=discord.Color.random())
            avatar_embed.set_image(url=member.avatar)
            avatar_embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar)

            await interaction.response.send_message(embed=avatar_embed, ephemeral=True)

    # Slash command to send a message as the Bot
    @app_commands.command(name="send", description="Send a message to the community!")
    @commands.has_permissions(administrator=True)
    async def send(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(f"@everyone {message}")

    # Hybrid userinfo command
    @commands.hybrid_command(name="userinfo", description="Get info about any user")
    @commands.has_permissions(administrator=True)
    async def userinfo(self, ctx, user: discord.User = None):
        commands_channel = discord.utils.get(ctx.guild.channels, name="dev-center")
        if user is None:
            user = ctx.author
        elif user is not None:
            user = user
        if ctx.channel.id == commands_channel.id:
            info_embed = discord.Embed(title=f"{user.name}'s User Information", description="All information about this user.", color=user.color)
            info_embed.set_thumbnail(url=user.avatar)
            info_embed.add_field(name="Name:", value=user.name, inline=False)
            info_embed.add_field(name="Nickname:", value=user.display_name + "#" + user.discriminator, inline=True)
            # info_embed.add_field(name="Discriminator:", value=user.discriminator, inline=False)
            info_embed.add_field(name="ID:", value=user.id, inline=False)
            info_embed.add_field(name="Top Role:", value=user.top_role, inline=False)
            info_embed.add_field(name="Status:", value=user.status, inline=False)
            info_embed.add_field(name="Bot User?", value=user.bot, inline=False)
            info_embed.add_field(name="Creation Date:", value=user.created_at.__format__("%A, %d. %B %Y @ %H:%M:%S"), inline=False)

            await ctx.send(embed=info_embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(DevCenter(bot))