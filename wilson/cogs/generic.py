from discord.ext import commands
from wilson.bot import Wilson


class Generic(commands.Cog):
    def __init__(self, bot: Wilson):
        self._bot = bot

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send('Greetings mortal...')


async def setup(bot: Wilson):
    await bot.add_cog(Generic(bot))
