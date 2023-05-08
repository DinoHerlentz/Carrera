import nextcord
import humanfriendly
import datetime
from nextcord import Interaction
from nextcord.ext import commands
from async_timeout import timeout
from main import bot


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name = "timeout", description = "Timeout a member so they can't chat/speak/react to a message", aliases = ['to', 'mute'])
    @commands.has_permissions(moderate_members = True)
    async def timeout(self, ctx: commands.Context, member: nextcord.Member, time, *, reason = None):
        """
        Timeout a member so they can't chat/speak/react to a message

        Usage : 
        ```>>timeout [member] (reason)```
        """

        if member == ctx.author:
            em = nextcord.Embed(title = "Error", description = "❌ You can't mute yourself.", color = nextcord.Color.red())
            await ctx.reply(embed = em, mention_author = False)

        elif member.top_role >= ctx.author.top_role:
            em2 = nextcord.Embed(title = "Error", description = "❌ You can only moderate members below your role.", color = nextcord.Color.red())
            await ctx.reply(embed = em2, mention_author = False)
        
        else:
            time = humanfriendly.parse_timespan(time)
            await member.edit(timeout = nextcord.utils.utcnow() + datetime.timedelta(seconds = time))

            em3 = nextcord.Embed(title = "Timeout", description = f"{ctx.author.mention} has use timeout on {member.mention}\nReason : {reason}", color = nextcord.Color.red())
            await ctx.send(embed = em3)

            em4 = nextcord.Embed(title = "Timeout", description = f"You've been muted in {ctx.guild.name}\nReason : {reason}", color = nextcord.Color.red())
            await member.send(embed = em4)
    

    @commands.command(name = "removetimeout", description = "Remove timeout from a member", aliases = ['rt', 'unmute'])
    @commands.has_permissions(moderate_members = True)
    async def removetimeout(self, ctx: commands.Context, member: nextcord.Member, *, reason = None):
        """
        Remove timeout from a member

        Usage : 
        ```>>removetimeout [member] (reason)```
        """

        if member.top_role >= ctx.author.top_role:
            em = nextcord.Embed(title = "Error", description = "❌ You can only moderate members below your role.", color = nextcord.Color.red())
            await ctx.reply(embed = em, mention_author = False)

        else:
            await member.edit(timeout = None)
            em2 = nextcord.Embed(title = "Timeout Remove", description = f"{ctx.author.mention} has removed {member.mention} timeout\nReason : {reason}", color = 0x2ECC71)
            await ctx.send(embed = em2)

            em3 = nextcord.Embed(title = "Timeout Remove", description = f"You've been unmuted in {ctx.guild.name}\nReason : {reason}", color = 0x2ECC71)
            await member.send(embed = em3)
    

    @commands.command(name = "purge", description = "Clear a message", aliases = ['cls', 'clear'])
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx: commands.Context, amount, arg: str = None):
        """
        Clear a message

        Usage : 
        ```>>purge [amount]```
        """

        await ctx.message.delete()
        await ctx.channel.purge(limit = int(amount))
    

    @commands.command(name = "nick", desciption = "Change member's server nickname")
    @commands.has_permissions(manage_nicknames = True)
    async def nick(self, ctx: commands.Context, member: nextcord.Member, *, nickname):
        """
        Change member's server nickname

        Usage : 
        ```>>nick [new nickname]```
        """

        await member.edit(nick = nickname)
        await ctx.reply(f"Successfully changed {member.mention} nicknames to `{nickname}`", mention_author = False)
    

    @commands.command(name = "slowmode", description = "Set a slowmode to the current channel", aliases = ['sm'])
    @commands.has_permissions(manage_channels = True)
    async def slowmode(self, ctx: commands.Context, seconds: int = None):
        """
        Set a slowmode to the current channel

        Usage : 
        ```slowmode [seconds]```
        """

        await ctx.channel.edit(slowmode_delay = seconds)

        em = nextcord.Embed(title = f"Slowmode in this channel has been set to {seconds} seconds.", color = 0x2ECC71)
        await ctx.reply(embed = em, mention_author = False)
    

def setup(bot):
    bot.add_cog(Moderation(bot))