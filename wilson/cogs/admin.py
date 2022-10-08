import asyncio
import discord
import git
import os
import sys
import yaml

from discord.ext import commands
from git import Repo
from ..bot import Wilson
from ..util.logger import *


class Admin(commands.Cog):
    def __init__(self, bot: Wilson):
        self._bot = bot

    @commands.command(aliases=['restart'])
    @commands.is_owner()
    async def pstart(self, ctx: commands.Context, type: str = 'hard') -> None:
        if type.lower() == 'hard':
            await ctx.send('Initiating Hard pstart...')
            if ctx.voice_client is not None:
                await ctx.voice_client.disconnect(force=True)
            os.system(self._bot.config.bot_settings.pstart_command)
            sys.exit()
        elif type.lower() == 'soft':
            await ctx.reply('Initiating Soft pstart...')
            presence = self._bot.config.bot_settings.default_presence

            await self._bot.change_presence(
                activity=discord.Activity(
                    name=presence.activity_name, type=presence.activity_type),
                status=presence.status)

    @commands.command()
    @commands.is_owner()
    async def upgrade(self, ctx: commands.Context) -> None:
        await ctx.send('Fetching from the repository...')
        output = os.popen('git fetch && git pull').read()

        await ctx.reply(f'```\n{output}\n```')

    @commands.command()
    async def sync(self, ctx: commands.Context, guild=0) -> None:
        fmt = []
        if guild != 0:
            fmt = await ctx.bot.tree.sync(guild=discord.Object(id=guild))
        else:
            fmt = await ctx.bot.tree.sync()
        await ctx.reply(f'Synced {len(fmt)} slash commands')

    @commands.command(aliases=['pkg'])
    @commands.is_owner()
    async def package(self, ctx: commands.Context, action: str, pkg: str) -> None:
        packages = yaml.safe_load(open('res/packages.yml'))

        if action.startswith('i'):  # Install
            try:
                url = packages[pkg]
                await ctx.send('Cloning repository...')
                try:
                    git.Git('extensions/').clone(url)
                    await ctx.reply('Done!')
                except Exception as exc:
                    log_error('Could not clone repository', exc)
                    await ctx.reply(f'Could not install the package, likely because it is already installed. Try updating it with `{self._bot.config.bot_settings.prefix}package update {pkg}`')
            except KeyError:
                await ctx.reply('Package not found')
        elif action.startswith('u'):
            repo_dir = f'extensions/{pkg}/'
            if os.path.exists(repo_dir):
                repo = Repo(f'extensions/{pkg}')
                try:
                    repo.remote().fetch()
                    repo.remote().pull()
                    await ctx.reply('Package up to date')
                except Exception as exc:
                    log_error('Could not update repository', exc)
                    await ctx.reply('Could not update package')
            else:
                await ctx.reply('Package not installed')
        elif action.startswith('q'): # Query
            pkgs = '```yml\n'
            count = 0
            for key in packages:
                if pkg in key:
                    pkgs += f'- {key}\n'
                    count += 1
            if count == 0:
                pkgs += 'No packages found\n'
            pkgs += '```'

            embed = self._bot.generate_embed(
                'Package Query', ctx.author, description=pkgs)
            await ctx.reply(embed=embed)
        else:
            await ctx.reply('Unrecognised action')


async def setup(bot: Wilson):
    await bot.add_cog(Admin(bot))
