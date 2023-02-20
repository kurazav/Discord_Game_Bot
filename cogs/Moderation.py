import discord
from discord.ext import commands


# Staff Commands and User Logging
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Console Message at initialization
    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation.py is online")

    # Logs users' messages in the #message log channel. The Bot's messages are ignored.
    @commands.Cog.listener()
    async def on_message(self, message):
        message_log_channel = discord.utils.get(message.guild.channels, name="message")
        if message.author == self.bot.user:
            return
        else:
            event_embed = discord.Embed(title="Message Logged", description="Message Content and Origin", color=discord.Color.green())
            event_embed.set_thumbnail(url=message.author.avatar)
            event_embed.add_field(name="Message Author:", value=message.author.mention, inline=False)
            event_embed.add_field(name="Channel Origin:", value=message.channel.mention, inline=False)
            event_embed.add_field(name="Message Content:", value=message.content, inline=False)

            await message_log_channel.send(embed=event_embed)

    # Logs Member Join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        join_log_channel = discord.utils.get(member.guild.channels, name="join-leave")

        event_embed = discord.Embed(title="Arrival Logged", description="This user landed in the server!", color=discord.Color.green())
        event_embed.set_image(url=member.avatar)
        event_embed.add_field(name="User Joined:", value=member.mention, inline=False)

        await join_log_channel.send(embed=event_embed)

    # Logs Members Leave
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        join_log_channel = discord.utils.get(member.guild.channels, name="join-leave")

        event_embed = discord.Embed(title="Departure Logged", description="This user left the server!", color=discord.Color.green())
        event_embed.set_image(url=member.avatar)
        event_embed.add_field(name="User Left:", value=member.mention, inline=False)

        await join_log_channel.send(embed=event_embed)

    # Staff Command to Delete a certain amount of message in the channel
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, messages: int):
        await ctx.channel.purge(limit=messages)
        await ctx.send(f"{messages} message(s) have been deleted!")

    # Staff Command To Kick User for a reason
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick_user(self, ctx, member: discord.Member, *, mod_reason):
        await ctx.guild.kick(member)

        conf_embed = discord.Embed(title="Success!", color=discord.Color.green())
        conf_embed.add_field(name="Kicked:", value=f"{member.mention} has been kicked from the server by {ctx.author.mention}.", inline=True)
        conf_embed.add_field(name="Reason:", value=mod_reason, inline=False)

        await ctx.send(embed=conf_embed)

    # Error handling for the Clear command -> No Permissions / Missing Amount of messages to delete
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("!!! Error: Missing Required Permissions!")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("!!! Error: Missing Required Arguments!")


async def setup(bot):
    await bot.add_cog(Moderation(bot))