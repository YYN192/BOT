import discord
from discord.ext import commands, tasks
import requests
from config import STOCK_API_KEY, STOCK_CHANNEL_ID

class Stock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stock_update.start()

    @tasks.loop(hours=3)
    async def stock_update(self):
        symbol = 'AAPL'
        url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={STOCK_API_KEY}'
        response = requests.get(url).json()
        channel = self.bot.get_channel(STOCK_CHANNEL_ID)
        if channel is not None:
            if 'c' in response:
                current_price = response['c']
                message = f"**{symbol} Stock Price Update**\nCurrent Price: ${current_price:.2f}"
                await channel.send(message)
            else:
                await channel.send("Error fetching stock data.")
        else:
            print(f"Channel with ID {STOCK_CHANNEL_ID} not found.")

    @commands.command(name='stock')
    async def stock(self, ctx, symbol='AAPL'):
        url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={STOCK_API_KEY}'
        response = requests.get(url).json()
        if 'c' in response:
            current_price = response['c']
            await ctx.send(f"{symbol} Stock Price: ${current_price:.2f}")
        else:
            await ctx.send("Error fetching stock data.")

    @stock_update.before_loop
    async def before_stock_update(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Stock(bot))
