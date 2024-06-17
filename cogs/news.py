import discord
from discord.ext import commands, tasks
import requests
from config import NEWS_API_KEY, NEWS_CHANNEL_ID

class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.news_update.start()

    @tasks.loop(hours=3)
    async def news_update(self):
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'
        response = requests.get(url).json()
        articles = response['articles'][:5]
        channel = self.bot.get_channel(NEWS_CHANNEL_ID)
        if channel is not None:
            for article in articles:
                await channel.send(f"**{article['title']}**\n{article['description']}\n{article['url']}")
        else:
            print(f"Channel with ID {NEWS_CHANNEL_ID} not found.")

    @commands.command(name='news')
    async def news(self, ctx):
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'
        response = requests.get(url).json()
        articles = response['articles'][:5]
        for article in articles:
            await ctx.send(f"**{article['title']}**\n{article['description']}\n{article['url']}")

    @news_update.before_loop
    async def before_news_update(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(News(bot))
