import asyncio
import sys

import discord
import os

from discord.ext import commands
from wilson.bot import Wilson


class Admin(commands.Cog):
    def __init__(self, bot: Wilson):
        self._bot = bot

    @commands.command(aliases=['restart'])
    @commands.is_owner()
    async def pstart(self, ctx: commands.Context, type: str = 'hard'):
        if type.lower() == 'hard':
            await ctx.send('Initiating Hard pstart...')
            if ctx.voice_client is not None:
                await ctx.voice_client.disconnect(force=True)
            os.system('./run.sh')
            sys.exit()
        elif type.lower() == 'soft':
            await ctx.reply('Initiating Soft pstart...')
            presence = self._bot.config.bot_settings.default_presence

            await self._bot.change_presence(
                activity=discord.Activity(name=presence.activity_name, type=presence.activity_type),
                status=presence.status)

    @commands.command()
    @commands.is_owner()
    async def upgrade(self, ctx):
        await ctx.send('Fetching from the repository...')
        output = os.popen('git fetch && git pull').read()

        await ctx.reply(f'```\n{output}\n```')


async def setup(bot: Wilson):
    await bot.add_cog(Admin(bot))
