import asyncio
import discord
import wilson.util.helpers as h
import wilson.util.img as i
import wilson.util.logger as log

from datetime import datetime, timedelta
from discord.ext import commands
from wilson.bot import Wilson


class Moderator(commands.Cog):
    def __init__(self, bot: Wilson):
        self._bot = bot

    @commands.command(aliases=['nick'])
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx: commands.Context, user: discord.Member, *, nickname: str):
        if h.compare_roles(ctx.me, user):
            if len(nickname) > 32:
                await ctx.reply('Nickname to long')
            else:
                await user.edit(nick=nickname)
                await ctx.reply(f'Nickname changed to **{nickname}**')
        else:
            await ctx.reply('Cannot edit a user with a higher role than me')

    @commands.command(aliases=['copy'])
    @commands.guild_only()
    @commands.has_permissions(manage_emojis=True)
    async def clone(self, ctx: commands.Context, emoji: discord.PartialEmoji):
        guild_emojis = [guild_emoji.id for guild_emoji in ctx.guild.emojis]
        if emoji.id in guild_emojis:
            await ctx.reply('This emoji already exists')
        else:
            emoji_bytes = i.get_image_url_bytes(str(emoji.url))
            new_emoji = await ctx.guild.create_custom_emoji(name=emoji.name, image=emoji_bytes)

            await ctx.message.add_reaction(new_emoji)

    @commands.command(aliases=['prune'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def sweep(self, ctx: commands.Context, limit: int = 20):
        if limit > 100:
            await ctx.reply('Too many! You\'re not even paying me.')
        elif limit == 1:
            await ctx.reply('Seriously? One message? Do it yourself you lazy human.')
        elif limit < 1:
            await ctx.reply('My disappointment is immeasurable and my day is ruined')
        else:
            try:
                await ctx.message.delete()
                await ctx.channel.purge(limit=limit)
                message = await ctx.send(f'All done, {limit} messages cleared. <:wilson_triumphant:764899295300157441>')
                await asyncio.sleep(3)
                await message.delete()
            except Exception as exc:
                log.log_error('Error while sweeping messages', exc)
                await ctx.send('Something went wrong, likely because I cannot bulk delete messages older than 14 days')

    @commands.command(aliases=['giverole'])
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx: commands.Context, user: discord.Member, role: discord.Role):
        if h.compare_roles(ctx.message.author, user):
            await user.add_roles(role)
            await ctx.reply(f'**{user.display_name}** has been granted role **{role.name}**')
        else:
            await ctx.reply('Cannot assign a role higher than your own')

    @commands.command(aliases=['removerole'])
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def takerole(self, ctx: commands.Context, user: discord.Member, role: discord.Role):
        if h.compare_roles(ctx.message.author, user):
            await user.remove_roles(role)
            await ctx.reply(f'**{role.name}** role removed from **{user.display_name}**')
        else:
            await ctx.reply('Cannot remove a role higher than your own')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def cleanroles(self, ctx: commands.Context):
        bot_role = ctx.me.top_role
        roles = ctx.guild.roles
        count = 0
        for role in roles:
            if role.position < bot_role.position and len(role.members) == 0:
                await role.delete()
                count += 1
        await ctx.send(f'Deleted `{count}` roles')

    @commands.command(aliases=['mute', 'silence', 'timeout'])
    @commands.guild_only()
    @commands.has_permissions(moderate_members=True)
    async def shun(self, ctx: commands.Context, user: discord.Member, hours: int = 1):
        if hours < 1:
            await ctx.reply('Are we time travellers now?')
        elif hours > 168:
            await ctx.reply('Too long! Maximum 168 hours (1 week)')
        elif not user.is_timed_out():
            await user.timeout(timedelta(hours=hours))
            await ctx.reply(f'**{user.display_name}** has been shunned for {hours} hours')
        else:
            await ctx.reply(f'**{user.display_name}** is already shunned')

    @commands.command(aliases=['unmute', 'untimeout'])
    @commands.guild_only()
    @commands.has_permissions(moderate_members=True)
    async def unshun(self, ctx: commands.Context, user: discord.Member):
        if user.is_timed_out():
            await user.timeout(timedelta(0))
            await ctx.reply(f'**{user.display_name}** has been unshunned')
        else:
            await ctx.reply(f'**{user.display_name}** is already unshunned')


async def setup(bot: Wilson):
    await bot.add_cog(Moderator(bot))
