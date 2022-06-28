import discord
import wilson.util.helpers as h
import wilson.util.img as i

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
                await ctx.send('Nickname to long')
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


async def setup(bot: Wilson):
    await bot.add_cog(Moderator(bot))
