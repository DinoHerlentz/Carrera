import nextcord
import psutil
import json
import requests
import aiohttp
import asyncio
from nextcord import Interaction
from nextcord.ext import commands
from googlesearch import search
from main import bot


class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name = "ping", description = "Shows the bot latency")
    async def ping(self, ctx: commands.Context):
        """Shows the bot latency"""
        await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")
    

    @commands.command(name = "cleardm", description = "Clear a message from bot in DMs", aliases = ['cd', 'cm', 'cc'])
    async def cleardm(self, ctx: commands.Context, amount, arg: int = None):
        """
        Clear a message from bot in DMs

        Usage : 
        ```-cleardm [amount]```
        """

        dmchannel = await ctx.author.create_dm()

        async for message in dmchannel.history(limit = int(amount)):
            await message.delete()
    

    @commands.command(name = "quote", description = "Get some random inspirating quotes")
    async def quote(self, ctx: commands.Context):
        """Get some random inspirating quotes"""
        r = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(r.text)
        quote = json_data[0]['q'] + "\n\n~" + json_data[0]['a']
        await ctx.send(quote)
    

    @commands.command(name = "wsay", description = "Send a message with webhook", aliases = ['webhooksay'])
    async def wsay(self, ctx: commands.Context, *, message = None):
        """
        Send a message with webhook

        Usage : 
        ```-wsay [message]```
        """
        
        if message == None:
            await ctx.reply("Please provide a message.", mention_author = False)
            return
        
        webhook = await ctx.channel.create_webhook(name = ctx.author.name)

        await webhook.send(str(message), username = ctx.author.name, avatar_url = ctx.author.avatar.url)
        await ctx.message.delete()

        webhooks = await ctx.channel.webhooks()

        for webhook in webhooks:
            await webhook.delete()
    

    @commands.command(name = "id", description = "Get user ID")
    async def id(self, ctx: commands.Context, member: nextcord.Member = None):
        """Get user ID"""
        if member == None:
            await ctx.reply(ctx.author.id, mention_author = False)
        
        else:
            await ctx.reply(member.id, mention_author = False)
    

    @commands.command(name = "membercount", description = "Get the member count of the current server", aliases = ['mc'])
    async def membercount(self, ctx: commands.Context):
        """Get the member count of the current server"""
        await ctx.reply(f"This member has {ctx.guild.member_count} members.", mention_author = False)
    

    @commands.command(name = "stats", description = "Get the bot statistics",  aliases = ['stat', 'statistic', 'statistics'])
    async def stats(self, ctx: commands.Context):
        """Get the bot statistics"""
        em = nextcord.Embed(title = "Carrera Bot Statistics", color = 0xF1C40E)
        em.add_field(name = "CPU", value = f"{psutil.cpu_percent()}%", inline = False)
        em.add_field(name = "RAM", value = f"{psutil.virtual_memory()[2]}%", inline = False)

        await ctx.send(embed = em)
    

    @commands.command(name = "weather", description = "Shows weather information of a city")
    async def weather(self, ctx: commands.Context, *, city: str):
        """
        Shows weather information of a city

        Usage : 
        ```-weather [city name]```
        """

        api_key = "c6e381d5c0b39faad3bfdcfd1aa5b074"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + api_key + "&q=" + city
        res = requests.get(complete_url)
        x = res.json()

        if x['cod'] != "404":
            y = x['main']

            current_temperature = y['temp']
            current_temperature_celcius = str(round(current_temperature - 273.15))
            current_pressure = y['pressure']
            current_humidity = y['humidity']
            z = x['weather']
            weather_description = z[0]['description']

            em = nextcord.Embed(title = f"{city.title()} Weather Information", color = 0xF1C40E)
            em.add_field(name = "Weather Description", value = f"**{weather_description.title()}**", inline = False)
            em.add_field(name = "Temperature (C)", value = f"**{current_temperature_celcius}°C**", inline = False)
            em.add_field(name = "Temperature (K)", value = f"**{current_temperature} K**", inline = False)
            em.add_field(name = "Atmospheric Pressure (hPa)", value = f"**{current_pressure}**", inline = False)
            em.add_field(name = "Humidity (%)", value = f"{current_humidity}", inline = False)
            em.set_thumbnail(url = "https://i.ibb.co/CMrsxdX/weather.png")
            em.timestamp = ctx.message.created_at

            await ctx.send(embed = em)
        
        else:
            await ctx.reply(f"No City Found - {city}")
    

    @commands.command(name = "announce", description = "Announe a message to the specified channel")
    @commands.has_permissions(manage_messages = True)
    async def announce(self, ctx: commands.Context, channel: nextcord.TextChannel, *, message = None):
        """
        Announce a message to the specified channel

        Usage : 
        ```-announce [channel] [message]```
        """

        await ctx.reply("Announcement has been sent.", mention_author = False)

        em = nextcord.Embed(title = "New Announcement", description = f"{message}", color = 0xF1C40E)
        em.set_footer(text = f"Announcement from {ctx.author}", icon_url = ctx.author.avatar.url)
        em.timestamp = ctx.message.created_at

        await channel.send(embed = em)
    
    
    @commands.command(name = "google", description = "Search anything on google", aliases = ['find', 'f', 'g'])
    async def google(self, ctx, *, query):
        """
        Search anythng on google
        
        Usage : 
        ```-google [query]```
        """
        
        await ctx.reply(f"Searching {query}...")
        
        async with ctx.typing():
            for j in search(query, tld = "co.in", num = 1, stop = 1, pause = 1):
                await ctx.send(f"{j}")
    
    
    @commands.command(name = "emojiinfo", description = "Get the emoji info", aliases= ['ei'])
    async def emojiinfo(self, ctx: commands.Context, emoji: nextcord.Emoji):
        """
        Get the emoji info
        
        Usage : 
        ```-ei [emoji]```
        """
        
        try:
            emoji = await emoji.guild.fetch_emoji(emoji.id)
        
        except nextcord.NotFound:
            await ctx.reply("Couldn't find that emoji.", mention_author = False)
        
        is_managed = True if emoji.managed else False
        is_animated = True if emoji.animated else False
        require_colons = True if emoji.require_colons else False
        created_time = emoji.created_at.strftime("%I:%M %p %B %d, %Y")
        can_use_emoji = "Everyone" if not emoji.roles else " ".join(role.name for role in emoji.roles)

        em = nextcord.Embed(title = f"`{emoji.name}` Emoji Informations")
        em.add_field(name = "Name", value = emoji.name, inline = False)
        em.add_field(name = "ID", value = emoji.id, inline = False)
        em.add_field(name = "Emoji Guild Name", value = emoji.guild.name, inline = False)
        em.add_field(name = "Emoji Guild ID", value = emoji.guild.id, inline = False)
        em.add_field(name = "URL", value = f"[Click Here]({str(emoji.url)})", inline = False)
        em.add_field(name = "Author", value = emoji.user.mention, inline = False)
        em.add_field(name = "Created At", value = created_time, inline = False)
        em.add_field(name = "Usable Status", value = can_use_emoji, inline = False)
        em.add_field(name = "Animated", value = is_animated, inline = False)
        em.add_field(name = "Managed", value = is_managed, inline = False)
        em.add_field(name = "Requires Colons", value = require_colons, inline = False)

        await ctx.send(embed = em)
    
    
    @commands.command(name = "avatar", description = "Shows user avatar", aliases = ['av'])
    async def avatar(self, ctx: commands.Context, member: nextcord.User = None):
        """
        Shows user avatar
        
        Usage : 
        ```-avatar (user)```
        """
        if member == None:
            member = ctx.author
        
        icon_url = member.avatar.url
        
        em = nextcord.Embed()
        em.set_image(url = f"{icon_url}")
        em.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)
        em.timestamp = ctx.message.created_at
        
        await ctx.send(embed = em)
    
    
    @commands.command(name = "timer", description = "Set a timer")
    async def timer(self, ctx: commands.Context, seconds = None):
        """
        Set a timer
        
        Usage : 
        ```-timer [seconds]```
        """
        
        try:
            secondint = int(seconds)
            
            if secondint <= 0:
                await ctx.reply("I don't think I can do negatives.", mention_author = False)
                raise BaseException
            
            message = await ctx.send(f"Timer : {seconds}")
            
            while True:
                secondint -= 1
                
                if secondint == 0:
                    await message.edit(content = "Ended!")
                    break
                
                await message.edit(content = f"Timer : {secondint}")
                await asyncio.sleep(1)
            
            await ctx.send(f"{ctx.author.mention}, your countdown has ended!")
        
        except ValueError:
            await ctx.reply("Please enter a number.", mention_author = False)
    
    
    @commands.command(name = "weather", description = "Shows weather informations of a city")
    async def weather(self, ctx: commands.Context, *, city):
        """
        Shows weather informations of a city
        
        Usage : 
        ```-weather [city]```
        """
        url = "https://api.weatherapi.com/v1/current.json"
        
        
        params = {
			"key": "73602374fbea4e7fbeb135655231903",
			"q": city
		}
        
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url, params = params) as res:
                data = await res.json()
                
                location = data['location']['name']
                temp_c = data['current']['temp_c']
                temp_f = data['current']['temp_f']
                humidity = data['current']['humidity']
                wind_kph = data['current']['wind_kph']
                wind_mph = data['current']['wind_mph']
                condition = data['current']['condition']['text']
                image_url = "http" + data['current']['condition']['icon']
                
                em = nextcord.Embed(title = f"{location} Weather Information", description = f"Current condition in `{location}` is `{condition}`")
                # em.set_thumbnail(url = image_url)
                em.add_field(name = "Temperature", value = f"C : {temp_c}°C | F : {temp_f}°F", inline = False)
                em.add_field(name = "Humidity", value = f"{humidity}", inline = False)
                em.add_field(name = "Wind Speed", value = f"KPH : {wind_kph} | MPH : {wind_mph}", inline = False)
                
                await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(Miscellaneous(bot))