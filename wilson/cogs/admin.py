import asyncio
import sys

import discord
import os
import wilson.util.logger as log

from discord.ext import commands
from wilson.bot import Wilson


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
                activity=discord.Activity(name=presence.activity_name, type=presence.activity_type),
                status=presence.status)

    @commands.command()
    @commands.is_owner()
    async def upgrade(self, ctx: commands.Context) -> None:
        await ctx.send('Fetching from the repository...')
        output = os.popen('git fetch && git pull').read()

        await ctx.reply(f'```\n{output}\n```')

    @commands.command()
    async def sync(self, ctx: commands.Context, guild = 0) -> None:
        fmt = []
        if guild != 0:
            fmt = await ctx.bot.tree.sync(guild=discord.Object(id=guild))
        else:
            fmt = await ctx.bot.tree.sync()
        await ctx.reply(f'Synced {len(fmt)} slash commands')



async def setup(bot: Wilson):
    await bot.add_cog(Admin(bot))
    log.log_info('Admin cog loaded')
