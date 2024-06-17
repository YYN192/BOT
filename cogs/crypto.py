import discord
from discord.ext import commands, tasks
import requests
from config import CRYPTO_API_KEY, CRYPTO_CHANNEL_ID

class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.crypto_update.start()

    @tasks.loop(minutes=30)
    async def crypto_update(self):
        url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        headers = {'X-CMC_PRO_API_KEY': CRYPTO_API_KEY}
        response = requests.get(url, headers=headers).json()
        channel = self.bot.get_channel(CRYPTO_CHANNEL_ID)
        if 'data' in response:
            top_cryptos = response['data'][:10]  # Get the top 10 cryptocurrencies
            message = "Top 10 Cryptocurrencies:\n"
            for crypto in top_cryptos:
                name = crypto['name']
                symbol = crypto['symbol']
                price = crypto['quote']['USD']['price']
                message += f"{name} ({symbol}): ${price:.2f}\n"
            await channel.send(message)
        else:
            await channel.send("Error fetching cryptocurrency data.")

    @commands.command(name='crypto')
    async def crypto(self, ctx, symbol=None):
        url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        headers = {'X-CMC_PRO_API_KEY': CRYPTO_API_KEY}
        response = requests.get(url, headers=headers).json()
        if 'data' in response:
            if symbol:
                crypto = next((c for c in response['data'] if c['symbol'].upper() == symbol.upper()), None)
                if crypto:
                    name = crypto['name']
                    price = crypto['quote']['USD']['price']
                    await ctx.send(f"{name} ({symbol.upper()}): ${price:.2f}")
                else:
                    await ctx.send(f"Cryptocurrency with symbol '{symbol}' not found.")
            else:
                top_cryptos = response['data'][:10]
                message = "Top 10 Cryptocurrencies:\n"
                for crypto in top_cryptos:
                    name = crypto['name']
                    symbol = crypto['symbol']
                    price = crypto['quote']['USD']['price']
                    message += f"{name} ({symbol}): ${price:.2f}\n"
                await ctx.send(message)
        else:
            await ctx.send("Error fetching cryptocurrency data.")

    @crypto_update.before_loop
    async def before_crypto_update(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Crypto(bot))
