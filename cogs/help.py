import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='infohub')
    async def infohub_help(self, ctx):
        help_text = """
        **InfoHub Bot Commands:**
        - `!news`: Get the latest news headlines.
        - `!weather [location]`: Get the current weather for the specified location (default is London).
        - `!crypto [symbol]`: Get the current price of the specified cryptocurrency (default is top 10).
        - `!stock [symbol]`: Get the current price of the specified stock (default is AAPL).
        """
        await ctx.send(help_text)

async def setup(bot):
    await bot.add_cog(Help(bot))
