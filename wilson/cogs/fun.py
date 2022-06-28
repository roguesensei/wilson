import asyncio
import discord
import random

from datetime import datetime
from discord.ext import commands
from wilson.bot import Wilson
from wilson.util.helpers import format_elapsed_time


class Fun(commands.Cog):
    def __init__(self, bot: Wilson):
        self._bot = bot

    @commands.command(aliases=['parrot', 'say'])
    async def puppet(self, ctx: commands.Context, *, message: str) -> None:
        if len(ctx.message.mentions) > 0 or len(ctx.message.role_mentions) > 0 or ctx.message.mention_everyone:
            await ctx.message.reply('I\'m not taking responsibility for a ping')
        # Fallback for users without @everyone perms
        elif '@everyone' in message or '@here' in message:
            await ctx.message.reply('I see what you\'re trying to do, you scrub')
        else:
            await ctx.message.delete()
            await asyncio.sleep(0.2, result=await ctx.send(message))

    @commands.command(aliases=['av'])
    async def avatar(self, ctx: commands.Context, user: discord.Member = None) -> None:
        if user is None:
            user = ctx.author

        embed = self._bot.generate_embed(f'Display Avatar to **{user.display_name}**', ctx.author,
                                         image_url=user.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name='guildav', aliases=['serverav'])
    async def guild_avatar(self, ctx: commands.Context) -> None:
        embed = self._bot.generate_embed(f'{ctx.guild.name} Avatar', ctx.author, image_url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['e'])
    async def emoji(self, ctx: commands.Context, emoji: discord.PartialEmoji) -> None:
        embed = self._bot.generate_embed(emoji.name, ctx.author, image_url=emoji.url)
        embed.add_field(name='Emoji ID', value=emoji.id, inline=True)
        embed.add_field(name='Animated', value=emoji.animated, inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    async def lenny(self, ctx: commands.Context) -> None:
        await ctx.message.delete()
        await ctx.send('( ͡° ͜ʖ ͡°)')

    @commands.command()
    async def f(self, ctx: commands.Context) -> None:
        user = ctx.message.author.id
        await ctx.send(f'<@{user}> paid their respects.')

    @commands.command()
    async def flip(self, ctx: commands.Context) -> None:
        coin = ['**Heads!**', '**Tails!**']
        await ctx.reply(random.choice(coin))

    @commands.command(aliases=['d'])
    async def dice(self, ctx: commands.Context, faces: int = 6) -> None:
        if faces > 0:
            await ctx.send(f'Rolling D{faces}')
            await ctx.typing()
            dice_roll = random.randint(1, faces)

            await asyncio.sleep(0.3, result=await ctx.send(f'**{dice_roll}!**'))
        else:
            await ctx.send('Invalid dice roll')

    @commands.command()
    async def whois(self, ctx: commands.Context, member: discord.Member):
        activity = member.activity
        user = self._bot.get_user(member.id)
        joined_discord = user.created_at.strftime('%x %X')
        joined_guild = member.joined_at.strftime('%x %X')

        embed = self._bot.generate_embed(str(member), ctx.author, thumbnail_url=member.display_avatar.url)
        embed.colour = member.colour
        embed.add_field(name='Display Name', value=member.display_name, inline=True)
        embed.add_field(name='Status', value=member.status, inline=True)
        embed.add_field(name='Joined Discord', value=f'`{joined_discord}`', inline=True)
        embed.add_field(name='Joined Guild', value=f'`{joined_guild}`', inline=True)

        if member.banner is not None:
            embed.set_image(url=member.banner.url)

        details = ''.format(len(member.roles))
        embed.add_field(name='Total Roles', value=str(len(member.roles)), inline=True)

        member_roles = member.roles
        member_roles.reverse()

        for role in member_roles:
            if role.name == '@everyone':
                details += str(role) + ' '
            else:
                details += f'<@&{role.id}> '
        embed.add_field(name='Roles', value=details, inline=True)

        if activity is not None:
            if activity.type == discord.ActivityType.playing:
                if member.bot:
                    embed.add_field(name='Activity', value=f'Playing **{activity.name}**')
                else:
                    current_time = datetime.utcnow()
                    time_elapsed = current_time - activity.start
                    formatted_time = format_elapsed_time(time_elapsed.seconds, include_days=False)
                    embed.add_field(name='Activity', value=f'Playing **{activity.name}** for `{formatted_time}`')
            elif activity.type == discord.ActivityType.listening:
                if member.bot:
                    embed.add_field(name='Activity', value=f'Listening to **{activity.name}**')
                else:
                    embed.add_field(name='Activity',
                                    value=f'Listening to **{activity.title}** on **{activity.album}** by **{activity.artist}**')
                    if activity.album_cover_url is not None:
                        embed.set_image(url=activity.album_cover_url)
            elif activity.type == discord.ActivityType.streaming:
                embed.add_field(name='Activity', value=f'Streaming **{activity.name}**')

        await ctx.send(embed=embed)

    @commands.command(aliases=['serverinfo'])
    async def guildinfo(self, ctx: commands.Context) -> None:
        embed = self._bot.generate_embed(ctx.guild.name, ctx.author, thumbnail_url=ctx.guild.icon.url)
        joined_discord = ctx.guild.created_at.strftime('%x %X')

        bot_count = 0
        for member in ctx.guild.members:
            if member.bot:
                bot_count += 1
        guild_members = ctx.guild.member_count - bot_count

        embed.add_field(name='Server Owner', value=ctx.guild.owner)
        embed.add_field(name='Members', value=guild_members)
        embed.add_field(name='Bots', value=bot_count)
        embed.add_field(name='Channel Categories', value=len(ctx.guild.categories))
        embed.add_field(name='Text Channels', value=len(ctx.guild.text_channels))
        embed.add_field(name='Voice Channels', value=len(ctx.guild.voice_channels))
        embed.add_field(name='Roles', value=len(ctx.guild.roles))
        embed.add_field(name='Emojis', value=len(ctx.guild.emojis))
        embed.add_field(name='Created At', value=f'`{joined_discord}`')

        await ctx.send(embed=embed)


async def setup(bot: Wilson):
    await bot.add_cog(Fun(bot))
