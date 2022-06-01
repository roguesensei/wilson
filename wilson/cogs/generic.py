import time

from discord.ext import commands
from random import randint
from wilson.bot import Wilson


class Generic(commands.Cog):
    def __init__(self, bot: Wilson):
        self._bot = bot

    @commands.command()
    async def hello(self, ctx: commands.Context, message: str):
        if message.lower() == 'there':  # General Kenobi
            if randint(1, 4) == 4:
                await ctx.send('https://media1.tenor.com/images/b365e7d26fe05de381a4fdfd9d8f9517/tenor.gif')
            elif randint(1, 4) == 4:
                await ctx.send('https://media3.giphy.com/media/8JTFsZmnTR1Rs1JFVP/giphy.gif')
            else:
                await ctx.send('https://i.giphy.com/media/xTiIzJSKB4l7xTouE8/giphy.webp')
        else:
            await ctx.send('Greetings mortal...')

    @commands.command()
    async def ping(self, ctx: commands.Context):
        before = time.perf_counter()
        embed = self._bot.generate_embed(title='Pong!')

        message = await ctx.send(embed=embed)

        response_time = time.perf_counter() - before
        embed.description = f'Time taken: `{response_time}` seconds'
        await message.edit(embed=embed)


async def setup(bot: Wilson):
    await bot.add_cog(Generic(bot))
