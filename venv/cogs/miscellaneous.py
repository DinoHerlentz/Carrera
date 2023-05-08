import nextcord
import psutil
import json
import requests
import aiohttp
import asyncio
import datetime
import openai
import time
import wikipedia
from nextcord import Interaction
from nextcord.ext import commands
from googlesearch import search
from bs4 import BeautifulSoup
from main import bot

openai.api_key = os.environ['OPENAI']
API_KEY = os.environ['OPENAI']


class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name = "ping", description = "Shows the bot latency")
    async def ping(self, ctx: commands.Context):
        """Shows the bot latency"""
        await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")
    

    @commands.command(name = "math", description = "Evaluate any math expressions")
    async def math(self, ctx: commands.Context, *, expression: str):
        """
        Evaluate the math expression

        Usage : 
        ```>>math [expression]```
        """

        expression = expression.replace(" ", "")

        try:
            result = float(eval(expression))
            await ctx.reply(f"Result : {result}")
        
        except ZeroDivisionError:
            await ctx.reply(f"Error : Division by zero.")
        
        except:
            await ctx.reply("Invalid mathematical expression")
    

    @commands.command(name = "dogfacts", description = "Get some random fact about dogs")
    async def dogfacts(self, ctx: commands.Context):
        res = requests.get("https://some-random-api.ml/facts/dog")
        fact = res.json()['fact']
        await ctx.send(fact)
    

    @commands.command(name = "poll", description = "Create a poll")
    async def poll(self, ctx: commands.Context, question, *options):
        """
        Create a poll

        Usage : 
        ```>>poll [question] [options]
        """

        if len(options) > 10:
            await ctx.send("You can only have up to 10 options.")
            return
        if len(options) < 2:
            await ctx.send("You need at least 2 options")
            return
        
        reactions = ["\U0001F1E6", "\U0001F1E7", "\U0001F1E8", "\U0001F1E9", "\U0001F1EA", "\U0001F1EB", "\U0001F1EC", "\U0001F1ED", "\U0001F1EE", "\U0001F1EF"]
        option_text = ""

        for i, option in enumerate(options):
            option_text += f"\n{reactions[i]} {option}"
        
        em = nextcord.Embed(title = question, description = option_text)
        em.timestamp = datetime.datetime.utcnow()
        poll_message = await ctx.send(embed = em)

        for i in range(len(options)):
            await poll_message.add_reaction(reactions[i])
    

    @commands.command(name = "fact", description = "Get some random facts")
    async def fact(self, ctx: commands.Context, category = None):
        """Get some random facts"""

        url = "https://api.chucknorris.io/jokes/random"

        if category:
            url += f"?category={category}"
        
        res = requests.get(url).json()
        fact = res['value']

        await ctx.send(fact)
    

    """
    @commands.command(name = "lyrics", description = "Get the lyrics of a song")
    async def lyrics(self, ctx: commands.Context, *, song):
        api_key = os.environ['GENIUS']
        url = f"https://api.genius.com/search?q={song}"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(url, headers = headers).json()

        
        if "error" in response or not response['response']['hits']:
            await ctx.send(f"Couldn't find the lyrics for {song}")
        
        else:
            song_id = response['response']['hits'][0]['result']['id']
            url = f"https://api.genius.com/songs/{song_id}/lyrics"
            response = requests.get(url, headers = headers).json()
            lyrics = response['response']['lyrics']['full']

            em = nextcord.Embed(title = f"{song.capitalize()}", description = f"{lyrics}")
            em.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed = em)
    """
    

    @commands.command(name = "image", description = "Search for images using the Google Custom Search API")
    async def image(self, ctx: commands.Context, *, query):
        """
        Search for images using the Google Custom Search API

        Usage : 
        ```>>image [query]```
        """

        image_api = os.environ['IMAGE']
        cx = os.environ['CX']
        url = f"https://www.googleapis.com/customsearch/v1?key={image_api}&cx={cx}&q={query}&searchType=image&num=1"
        res = requests.get(url).json()

        if "items" not in res:
            await ctx.send(f"Couldn't find an image for {query}")
        
        else:
            image_url = res['items'][0]['link']
            await ctx.send(image_url)


    @commands.command(name = "joke", description = "Get some random jokes")
    async def joke(self, ctx: commands.Context):
        """
        Get some random jokes
        """

        res = requests.get("https://official-joke-api.appspot.com/random_joke")
        joke = res.json()

        em = nextcord.Embed(title = "Joke")
        em.add_field(name = "Setup", value = f"{joke['setup']}", inline = False)
        em.add_field(name = "Punchline", value = f"{joke['punchline']}", inline = False)

        await ctx.send(embed = em)

    

    @commands.command(name = "ud", description = "Get the definition of a word from Urban Dictionary")
    async def ud(self, ctx: commands.Context, *, word):
        """
        Get the definition of a word from Urban Dictionary

        Usage : 
        ```>>ud [word]```
        """

        url = f"https://www.urbandictionary.com/define.php?term={word}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3)"}
        res = requests.get(url, headers = headers)
        soup = BeautifulSoup(res.text, "html.parser")
        definition = soup.select(".meaning")[0].getText().strip()
        
        em = nextcord.Embed(title = f"{word.title()}", description = f"{definition}")
        em.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = em)
    

    @commands.command(name = "wikipedia", description = "Get a summary of a Wikipedia article")
    async def wikipedia(self, ctx: commands.Context, *, query):
        """
        Get a summary of a Wikipedia article

        Usage : 
        ```>>wikipedia [query]```
        """
        try:
            summary = wikipedia.summary(query, sentences = 2)
            await ctx.send(summary)
        
        except wikipedia.exceptions.DisambiguationError as e:
            await ctx.send(f"{e.options}")
        
        except wikipedia.exceptions.PageError:
            await ctx.send(f"No wikipedia page found for {query}")
    

    @commands.command(name = "chatgpt", description = "Ask anything to ChatGPT")
    async def chatgpt(self, ctx: commands.Context, *, prompt: str):
        """
        Ask anything to ChatGPT

        Usage : 
        ```>>chatgpt [prompt]```
        """

        async with aiohttp.ClientSession() as ses:
            payload = {
                "model": "text-davinci-003",
                "prompt": prompt,
                "temperature": 0.5,
                "max_tokens": 512,
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "best_of": 1
            }

            headers = {"Authorization": f"Bearer {API_KEY}"}

            async with ses.post("https://api.openai.com/v1/completions", json = payload, headers = headers) as res:
                response = await res.json()

                em = nextcord.Embed(title = "ChatGPT", description = response['choices'][0]['text'])
                em.timestamp = datetime.datetime.now()

                await ctx.send(embed = em)
    

    @commands.command(name = "stats", description = "Shows bot statistics")
    async def stats(self, ctx: commands.Context):
        """Shows bot statistics"""

        cpu_usage = psutil.cpu_percent()
        mem_stats = psutil.virtual_memory()
        used_mem = mem_stats.used / 1024 ** 2
        total_mem = mem_stats.total / 1024 ** 2
        free_mem = total_mem - used_mem
        uptime = time.monotonic() - self.start_time
        events_sec = len(self.bot._connection.dispatch_hooks) / uptime

        em = nextcord.Embed(title = "Bot Statistics")
        em.add_field(name = "Guilds", value = len(self.bot.guilds), inline = False)
        em.add_field(name = "Users", value = len(self.bot.users), inline = False)
        em.add_field(name = "Free Memory", value = f"{free_mem:.2f} MB", inline = False)
        em.add_field(name = "Uptime", value = f"{uptime:.2f}s", inline = False)
        em.add_field(name = "CPU Usage", value = f"{cpu_usage}%", inline = False)
        em.add_field(name = "Load Average", value = f"{psutil.getloadavg()[0]:.2f}", inline = False)
        em.add_field(name = "Events/sec", value = f"{events_sec:.2f}", inline = False)

        await ctx.send(embed = em)
        
        print(cpu_usage)
        print(mem_stats)
        print(used_mem)
        print(total_mem)
        print(free_mem)
        print(uptime)
        print(events_sec)


    @commands.command(name = "cleardm", description = "Clear a message from bot in DMs", aliases = ['cd', 'cm', 'cc'])
    async def cleardm(self, ctx: commands.Context, amount, arg: int = None):
        """
        Clear a message from bot in DMs

        Usage : 
        ```>>cleardm [amount]```
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
        ```>>wsay [message]```
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
        ```>>weather [city name]```
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
            await ctx.reply(f"No City Found >> {city}")
    

    @commands.command(name = "announce", description = "Announe a message to the specified channel")
    @commands.has_permissions(manage_messages = True)
    async def announce(self, ctx: commands.Context, channel: nextcord.TextChannel, *, message = None):
        """
        Announce a message to the specified channel

        Usage : 
        ```>>announce [channel] [message]```
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
        ```>>google [query]```
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
        ```>>ei [emoji]```
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
        ```>>avatar (user)```
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
        ```>>timer [seconds]```
        """
        
        try:
            secondint = int(seconds)
            
            if secondint <= 0:
                await ctx.reply("I don't think I can do negatives.", mention_author = False)
                raise BaseException
            
            message = await ctx.send(f"Timer : {seconds}")
            
            while True:
                secondint >>= 1
                
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
        ```>>weather [city]```
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
