import nextcord
import asyncio
import aiohttp
import datetime
import random
from nextcord import Interaction
from nextcord.ext import commands
from main import bot


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name = "dice", description = "Roll a dice")
    async def dice(self, ctx: commands.Context):
        """Roll a dice"""
        
        message = await ctx.reply(f"{ctx.author.mention} rolled a dice and gets...", mention_author = False)
        await asyncio.sleep(3)
        await message.edit(content = f"{ctx.author.mention} rolled a dice and gets **{random.randint(1, 6)}** :game_die:")
    

    @commands.command(name = "say", description = "Ask the bot to say something")
    async def say(self, ctx: commands.Context, *, message = None):
        """
        Ask the bot to say something

        Usage : 
        ```>>say [message]```
        """

        funny_text = ["I'm stupid", "I'm Stupid", "i'm stupid", "Im stupid", "Im Stupid", "im stupid"]

        if message == None:
            await ctx.reply("Please provide a message.", mention_author = False)
        
        elif message in funny_text:
            await ctx.reply("Yeah you are.")


def setup(bot):
    bot.add_cog(Fun(bot))