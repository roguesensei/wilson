import asyncio
import discord
import random

from datetime import datetime
from discord import app_commands
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

        embed = self._generate_avatar_embed(user, ctx.author)

        await ctx.send(embed=embed)

    @app_commands.command(name='avatar', description='Display a member\'s avatar')
    async def slash_avatar(self, interaction: discord.Interaction, user: discord.Member) -> None:
        embed = self._generate_avatar_embed(user, interaction.user)

        await interaction.response.send_message(embed=embed)

    @commands.command(name='guildav', aliases=['serverav'])
    async def guild_avatar(self, ctx: commands.Context) -> None:
        embed = self._generate_guild_avatar_embed(ctx.guild, ctx.author)

        await ctx.send(embed=embed)
    
    @app_commands.command(name='guild_avatar', description='Display the guild avatar')
    async def slash_guild_avatar(self, interaction: discord.Interaction) -> None:
        embed = self._generate_guild_avatar_embed(interaction.guild, interaction.user)

        await interaction.response.send_message(embed=embed)

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
        embed = await self._generate_whois_embed(member, ctx.author)
        
        await ctx.send(embed=embed)

    @app_commands.command(name='whois', description='Display member info')
    async def slash_whois(self, interaction: discord.Interaction, member: discord.Member) -> None:
        embed = await self._generate_whois_embed(member, interaction.user)

        await interaction.response.send_message(embed=embed)

    @commands.command(aliases=['serverinfo'])
    async def guildinfo(self, ctx: commands.Context) -> None:
        embed = self._generate_guild_info_embed(ctx.guild, ctx.author)

        await ctx.send(embed=embed)
    
    @app_commands.command(name='guild_info', description='Display guild info')
    async def slash_guildinfo(self, interaction: discord.Interaction) -> None:
        embed = self._generate_guild_info_embed(interaction.guild, interaction.user)

        await interaction.response.send_message(embed=embed)
    
    def _generate_avatar_embed(self, user: discord.Member, author: discord.Member) -> discord.Embed:
        embed = self._bot.generate_embed(f'Display Avatar to **{user.display_name}**', author, image_url=user.display_avatar.url)

        return embed

    def _generate_guild_avatar_embed(self, guild: discord.Guild, author: discord.Member) -> discord.Embed:
        embed = self._bot.generate_embed(f'{guild.name} Avatar', author, image_url=guild.icon.url)

        return embed
    
    async def _generate_whois_embed(self, member: discord.Member, author: discord.Member) -> discord.Embed:
        activity = member.activity
        user = await self._bot.fetch_user(member.id)

        joined_discord = user.created_at.strftime('%x %X')
        joined_guild = member.joined_at.strftime('%x %X')

        embed = self._bot.generate_embed(str(member), author, thumbnail_url=member.display_avatar.url)
        embed.colour = member.colour
        embed.add_field(name='Display Name', value=member.display_name, inline=True)
        embed.add_field(name='Status', value=member.status, inline=True)
        embed.add_field(name='Joined Discord', value=f'`{joined_discord}`', inline=True)
        embed.add_field(name='Joined Guild', value=f'`{joined_guild}`', inline=True)

        if user.banner is not None:
            embed.set_image(url=user.banner.url)

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
            elif activity.type == discord.ActivityType.watching:
                embed.add_field(name='Activity', value=f'Watching **{activity.name}**')
        
        return embed

    def _generate_guild_info_embed(self, guild: discord.Guild, author: discord.Member) -> discord.Embed:
        embed = self._bot.generate_embed(guild.name, author, thumbnail_url=guild.icon.url)
        created_at = guild.created_at.strftime('%x %X')

        bot_count = 0
        for member in guild.members:
            if member.bot:
                bot_count += 1
        guild_members = guild.member_count - bot_count

        embed.add_field(name='Server Owner', value=guild.owner)
        embed.add_field(name='Members', value=guild_members)
        embed.add_field(name='Bots', value=bot_count)
        embed.add_field(name='Channel Categories', value=len(guild.categories))
        embed.add_field(name='Text Channels', value=len(guild.text_channels))
        embed.add_field(name='Voice Channels', value=len(guild.voice_channels))
        embed.add_field(name='Roles', value=len(guild.roles))
        embed.add_field(name='Emojis', value=len(guild.emojis))
        embed.add_field(name='Created At', value=f'`{created_at}`')

        return embed


async def setup(bot: Wilson):
    await bot.add_cog(Fun(bot))
