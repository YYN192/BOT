import discord
from discord.ext import commands, tasks
import requests
from config import WEATHER_API_KEY, WEATHER_CHANNEL_ID

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.weather_update.start()

    @tasks.loop(hours=3)
    async def weather_update(self):
        location = 'London'
        url = f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}'
        response = requests.get(url).json()
        channel = self.bot.get_channel(WEATHER_CHANNEL_ID)
        if 'error' in response:
            await channel.send(f"Error fetching weather data: {response['error']['message']}")
        else:
            weather = response['current']['condition']['text']
            temp = response['current']['temp_c']
            await channel.send(f"Weather in {location}: {weather}, {temp}°C")

    @commands.command(name='weather')
    async def weather(self, ctx, *, location='London'):
        url = f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}'
        response = requests.get(url).json()
        if 'error' in response:
            await ctx.send(f"Error fetching weather data: {response['error']['message']}")
        else:
            weather = response['current']['condition']['text']
            temp = response['current']['temp_c']
            await ctx.send(f"Weather in {location}: {weather}, {temp}°C")

    @weather_update.before_loop
    async def before_weather_update(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Weather(bot))
