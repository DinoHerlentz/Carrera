import nextcord
import io
import traceback
import contextlib
from nextcord import Interaction
from nextcord.ext import commands, application_checks
from traceback import format_exception
from main import bot


def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    
    else:
        return content


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name = "eval", description = "Run python code (owner only)", aliases = ['e'])
    @commands.is_owner()
    async def eval(self, ctx: commands.Context, *, code):
        """
        Run python code (owner only)

        Usage : 
        ```-eval [code]```
        """
        
        code = clean_code(code)
        str_obj = io.StringIO()

        """
        try:
            with contextlib.redirect_stdout(str_obj):
                exec(code)
        
        except Exception as e:
            return await ctx.send(f"```py\n{e.__class__.__name__}: {e}```")
        """
        
        try:
            with contextlib.redirect_stdout(str_obj):
                exec(code)
        
        except Exception as e:
            em = nextcord.Embed(title = "Error", description = "```py\n" + "".join(format_exception(e.__class__, e, e.__traceback__)) + "```")
            return await ctx.send(embed = em)
        
        await ctx.send(f"```py\n{str_obj.getvalue()}```")


    @commands.command(name = "dm", description = "DM a user through the bot")
    @commands.is_owner()
    async def dm(self, ctx: commands.Context, member: nextcord.User, *, content):
        """
        DM a user through the bot

        Usage : 
        ```-dm [message]```
        """

        user = await member.create_dm()

        try:
            await user.send(content)
            await ctx.reply("Successfully sent the message.")
        
        except nextcord.Forbidden:
            await ctx.send("Couldn't DM that user.")
    

    @commands.command(name = "msg", description = "Send a message to a specified channel")
    @commands.is_owner()
    async def msg(self, ctx: commands.Context, channel: nextcord.TextChannel, *, message):
        """
        Send a message to a specified channel

        Usage : 
        ```-msg [channel] [message]```
        """

        # await ctx.reply("Successfully sent the message.")

        try:
            await channel.send(f"{message}")
        
        except nextcord.Forbidden:
            await ctx.reply("I don't have permissions to send a message in that channel.", mention_author = False)
    

    @commands.command(name = "act", description = "Pretend to be someone")
    @commands.is_owner()
    async def act(self, ctx: commands.Context, member: nextcord.Member = None, *, message = None):
        """
        Pretend to be someone

        Usage : 
        ```act [member] [message]```
        """

        if member == None:
            await ctx.reply("Please mention a user.", mention_author = False)
        
        elif message == None:
            await ctx.reply("Please provide a message.", mention_author = False)
        
        webhook = await ctx.channel.create_webhook(name = member.name)
        await webhook.send(str(message), username = member.name, avatar_url = member.avatar.url)
        await ctx.message.delete()

        webhooks = await ctx.channel.webhooks()

        for webhook in webhooks:
            await webhook.delete()
    

    @commands.command(name = "activity", description = "Change the bot activity status")
    @commands.is_owner()
    async def activity(self, ctx: commands.Context, *, activity):
        """
        Change the bot activity status

        Usage : 
        ```-activity [activity]```
        """

        await bot.change_presence(activity = nextcord.Game(activity))
        await ctx.reply(f"My activity has been set to {activity}")
    
    
    @commands.command(name = "join", description = "Join a voice channel")
    @commands.is_owner()
    async def join(self, ctx: commands.Context):
        """Join a voice channel"""
        
        if (ctx.author.voice):
            channel = ctx.message.author.voice.channel
            await channel.connect()
            await ctx.reply("Successfully joined the voice chat.", mention_author = False)
        
        else:
            await ctx.reply("You aren't connected to the voice channel.", mention_author = False)
    
    
    @commands.command(name = "toggle", description = "Enable/disable a command")
    @commands.is_owner()
    async def toggle(self, ctx: commands.Context, *, command):
        """
        Enable/disable a command
        
        Usage : 
        ```-toggle [command]```
        """
        
        if command == None:
            await ctx.reply("Couldn't find that command.", mention_author = False)
        
        elif ctx.command == command:
            em = nextcord.Embed(title = "Error", description = "You can't disable this command.", color = nextcord.Color.red())
            await ctx.reply(embed = em, mention_author = False)
        
        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            
            em2 = nextcord.Embed(title = "Command Toggle", description = f"Successfully {ternary} command {command.qualified_name}", color = 0x2ECC71)
            await ctx.reply(embed = em2, mention_author = False)


def setup(bot):
    bot.add_cog(Owner(bot))