import nextcord
import os
import traceback
import json
import asyncio
# import wavelink
import datetime
import aiosqlite
import requests
from traceback import format_exception
from googlesearch import search
# from wavelink.ext import spotify
from nextcord.ext import commands, activities
from nextcord.ext.application_checks import ApplicationNotOwner, ApplicationMissingPermissions, ApplicationMissingRole, ApplicationMissingAnyRole, ApplicationBotMissingPermissions, ApplicationBotMissingRole, ApplicationBotMissingAnyRole, ApplicationNSFWChannelRequired, ApplicationNoPrivateMessage, ApplicationPrivateMessageOnly
from nextcord.abc import GuildChannel
from nextcord import Interaction
from nextcord.abc import GuildChannel
from nextcord.ext.commands import CommandNotFound, BadArgument, MissingPermissions, MissingRequiredArgument, BotMissingPermissions, CommandOnCooldown, DisabledCommand, MemberNotFound


intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix = "-", intents = intents, case_insensitive = True)
bot.remove_command("help")
lyrics_url = "https://some-random-api.ml/lyrics?title="

# Event Decorator
@bot.event
async def on_ready():
    await bot.change_presence(status = nextcord.Status.idle, activity = nextcord.Game("-help"))
    print("We have logged in as {0.user}".format(bot))
    
    """
    # Music
    bot.loop.create_task(node_connect())
    """

"""
@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node {node.identifier} is ready")


async def node_connect():
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot = bot, host = "lavalinkinc.ml", port = 443, password = "incognito", https = True, spotify_client = spotify.SpotifyClient(client_id = "975981c3179a436883021b5ac45f352f", client_secret = "8aa73f51cebf4c1e924303e3558ea6fa"))


@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.YouTubeTrack, reason):
    try:
        ctx: commands.Context = player.ctx
        vc: player = ctx.voice_client
    
    except nextcord.HTTPException:
        interaction = player.interaction
        vc: player = interaction.guild.voice_client

    if vc.loop:
        return await vc.play(track)

    elif vc.queue.is_empty:
        return await vc.disconnect()

    try:
        next_song = vc.queue.get()
        await vc.play(next_song)
    
    except wavelink.errors.QueueEmpty:
        pass

    try:
        em = nextcord.Embed(title = "Music Play", description = f"Now playing -> `{next_song.title}`", color = 0xF1C40E)
        em.timestamp = ctx.message.created_at
        await ctx.send(embed = em)
    
    except nextcord.HTTPException:
        em2 = nextcord.Embed(title = "Music Play", description = f"Now playing -> `{next_song.title}`", color = 0xF1C40E)
        em2.timestamp = datetime.datetime.utcnow()
        await interaction.send(embed = em2)
"""


@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, CommandNotFound):
        em = nextcord.Embed(title = "Invalid Command", description = "Type `-help` to see available commands", color = 0xF1C40E)
        await ctx.send(embed = em)

    elif isinstance(error, MissingRequiredArgument):
        pass

    elif isinstance(error, MissingPermissions):
        pass

    elif isinstance(error, BadArgument):
        pass

    elif isinstance(error, MemberNotFound):
        em2 = nextcord.Embed(title = "Error", description = "Couldn't find that member", color = nextcord.Color.red())
        await ctx.reply(embed = em2, mention_author = False)

    elif isinstance(error, BotMissingPermissions):
        em3 = nextcord.Embed(title = "Error", description = "Bot missing required permissions", color = nextcord.Color.red())
        await ctx.reply(embed = em3, mention_author = False)

    elif isinstance(error, CommandOnCooldown):
        em4 = nextcord.Embed(title = "Cooldown", description = "This command is still on cooldown. Try again in {:.2f} seconds".format(error.retry_after), color = nextcord.Color.red())
        await ctx.reply(embed = em4, mention_author = False)

    elif isinstance(error, DisabledCommand):
        em5 = nextcord.Embed(title = "Error", description = "This command is disabled", color = nextcord.Color.red())
        await ctx.reply(embed = em5, mention_author = False)


@bot.event
async def on_reaction_add(reaction, user):
    if str(reaction.emoji) == "🗑️":
        await nextcord.Message.delete(reaction.message)


"""
@bot.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    guild = str(message.guild.name)
    guild_id = str(message.guild.id)
    
    print(f"{username} : {user_message} ({channel}) ({guild}) ({guild_id})")
"""


# Cogs Setup
for fn in os.listdir("./venv/cogs"):
    if fn.endswith(".py"):
        bot.load_extension(f"cogs.{fn[:-3]}")


@bot.command(name = "load", description = "Load an extension")
@commands.is_owner()
async def load(ctx: commands.Context, extension):
    """
    Load an extension

    Usage : 
    ```-load [extension]```
    """
    
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Successfully load {extension} extension.")


@bot.command(name = "unload", description = "Unload an extension.")
@commands.is_owner()
async def unload(ctx: commands.Context, extension):
    """
    Unload an extension
    
    Usage :
    ```-unload [extension]```
    """
    
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Successfully unload {extension} extension.")


@bot.command(name = "reload", description = "Reload an extension.")
@commands.is_owner()
async def reload(ctx: commands.Context, extension):
    """
    Reload an extension

    Usage : 
    ```-reload [extension]```
    """
    
    bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Successfully reload {extension} extension.")


bot.run("OTkzNzAzMzkxNjE0MjA1OTYy.Ga2uWP.RnIhRf3e7flxXCsBflTAwjZcYnR9xmxEEfA55E")