import discord
import time
import wilson.util.logger as log

from discord import app_commands
from discord.ext import commands
from random import randint
from wilson.bot import Wilson
from wilson.util.helpers import format_elapsed_time


class Generic(commands.Cog):
    def __init__(self, bot: Wilson):
        self._bot = bot

    @commands.command()
    async def hello(self, ctx: commands.Context, message: str = None) -> None:
        if message is not None and message.lower() == 'there':  # General Kenobi
            if randint(1, 4) == 4:
                await ctx.message.reply('https://media1.tenor.com/images/b365e7d26fe05de381a4fdfd9d8f9517/tenor.gif')
            elif randint(1, 4) == 4:
                await ctx.message.reply('https://media3.giphy.com/media/8JTFsZmnTR1Rs1JFVP/giphy.gif')
            else:
                await ctx.message.reply('https://i.giphy.com/media/xTiIzJSKB4l7xTouE8/giphy.webp')
        else:
            await ctx.message.reply('Greetings mortal...')

    @app_commands.command(name='hello', description='My slash commands debut, I wonder what it does...')
    async def slash_hello(self,ctx: discord.Interaction):
        await ctx.response.send_message('Greetings mortal...')

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        before = time.perf_counter()
        embed = self._bot.generate_embed(title='Pong!', author=ctx.author)

        message = await ctx.send(embed=embed)

        response_time = time.perf_counter() - before
        embed.description = f'Time taken: `{response_time}` seconds'
        await message.edit(embed=embed)

    @commands.command()
    async def embed(self, ctx: commands.Context, *, message: str) -> None:
        embed_message = message
        embed = self._bot.generate_embed(f'Notice from {ctx.author}', author=ctx.author)

        if '--#' in embed_message:
            str_hex = embed_message.split('--#')[1][:6].strip()
            if len(str_hex) < 6:
                await ctx.send('Invalid colour hex')
                return
            try:
                converted_hex = int(str_hex, 16)
                embed_message = embed_message.replace(f'--#{str_hex}', '')
                embed.colour = converted_hex
            except Exception as exc:
                log.log_error(f'Could not parse colour hex "{str_hex}"', exc)
                await ctx.send('Could not parse the colour hex')
                return
        embed.description = embed_message

        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command(aliases=['img'])
    async def image(self, ctx: commands.Context, message: str) -> None:
        await ctx.message.delete()
        embed = self._bot.generate_embed(None, author=ctx.author, image_url=message)
        await ctx.send(embed=embed)

    @commands.command(aliases=['info'])
    async def release(self, ctx: commands.Context) -> None:
        current_time = time.time()
        app_info = await self._bot.application_info()

        embed = self._bot.generate_embed(f'{self._bot.user.name} Release Info', ctx.author,
                                         thumbnail_url=self._bot.user.avatar.url)
        embed.add_field(name='Bot Owner', value=app_info.owner, inline=True)
        embed.add_field(name='Current Update', value=self._bot.config.bot_settings.release.update_name, inline=True)
        embed.add_field(name='Current Version', value=self._bot.config.bot_settings.release.version.__str__(), inline=True)
        embed.add_field(name='Uptime', value=format_elapsed_time(current_time - self._bot.online_time), inline=True)
        embed.add_field(name='Total Guilds', value=len(self._bot.guilds).__str__(), inline=True)
        embed.add_field(name='Total Users', value=len(self._bot.users).__str__(), inline=True)
        await ctx.message.reply(embed=embed)

    @commands.command()
    async def help(self, ctx: commands.Context, help_category: str = 'all', help_command: str = 'default') -> None:
        try:
            base_dir = self._bot.wilson_extensions[help_category]['help'] if help_category in self._bot.wilson_extensions else './res/help'

            with open(f'{base_dir}/{help_category.lower()}/{help_command.lower()}.txt') as f:
                if help_category == 'all':
                    help_command = 'Help'  # Just for title
                elif help_command == 'default':
                    help_command = f'{help_category} commands'

                extensions_body = ''
                if len(self._bot.wilson_extensions) > 0:
                    extensions_body += '\n**Extensions**\n```yml\n'
                    for key in self._bot.wilson_extensions:
                        extension = self._bot.wilson_extensions[key]["name"]
                        extensions_body += f'- {extension}\n'
                    extensions_body += '\n```'

                bot_avatar = self._bot.user.avatar.url

                slash_commands = []
                app_commands = self._bot.tree.get_commands()
            
                for command in app_commands:
                    slash_commands.append(f'`/{command.name}`')

                body = f.read().format(extensions_body, ' '.join(slash_commands))


                embed = self._bot.generate_embed(title=f'{help_command.title()}!', author=ctx.author, description=body,
                                                 thumbnail_url=bot_avatar)

                await ctx.message.reply(embed=embed)
        except Exception as exc:
            log.log_error('Error invoking help command', exc)
            await ctx.message.reply(
                'An error has occurred. The help file either doesn\'t nor will exist or hasn\'t been implemented yet.')


async def setup(bot: Wilson):
    await bot.add_cog(Generic(bot))
    log.log_info('Generic cog loaded')
