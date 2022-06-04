import time
import wilson.util.logger as log

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
        embed = self._bot.generate_embed(title='Pong!', author=ctx.author)

        message = await ctx.send(embed=embed)

        response_time = time.perf_counter() - before
        embed.description = f'Time taken: `{response_time}` seconds'
        await message.edit(embed=embed)

    @commands.command()
    async def help(self, ctx: commands.Context, help_category: str = 'all', help_command: str = 'default'):
        try:
            with open(f'./res/help/{help_category.lower()}/{help_command.lower()}.txt') as f:
                if help_category == 'all':
                    help_command = 'Help'  # Just for title
                elif help_command == 'default':
                    help_command = f'{help_category} commands'

                bot_avatar = self._bot.user.avatar.url
                body = f.read()

                embed = self._bot.generate_embed(title=f'{help_command.title()}!', author=ctx.author, description=body)
                embed.set_thumbnail(url=bot_avatar)

                await ctx.send(embed=embed)
        except Exception as exc:
            log.log_error('Error invoking help command', exc)
            await ctx.send(
                'An error has occurred. The help file either doesn\'t nor will exist or hasn\'t been implemented yet.')


async def setup(bot: Wilson):
    await bot.add_cog(Generic(bot))
