import discord
from discord.ext import commands
import asyncio
import os
from config import TOKEN

# Define the intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the intent to read message content

# Initialize the bot with a command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Load cogs
async def load_cogs():
    cogs = ['cogs.news', 'cogs.weather', 'cogs.crypto', 'cogs.stock']
    for cog in cogs:
        await bot.load_extension(cog)

# Start the bot
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='infohub')
async def infohub_help(ctx):
    help_text = """
    **InfoHub Bot Commands**
    `!news` - Get the latest news headlines.
    `!weather [location]` - Get the current weather for the specified location. Defaults to London.
    `!crypto [symbol]` - Get the current price for the specified cryptocurrency symbol. Defaults to top 10.
    `!stock [symbol]` - Get the current stock price for the specified stock symbol. Defaults to AAPL.
    """
    await ctx.send(help_text)

async def main():
    await load_cogs()
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
