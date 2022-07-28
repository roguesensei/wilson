import discord

import wilson.util.helpers as h

from discord.ext import commands
from wilson.bot import Wilson
from wilson.util.http import Http

http_sfw = Http('https://nekos.life/api/v2')
http_nsfw = Http('http://api.nekos.fun:8080/api')


def get_sfw(url: str):
    r = http_sfw.get(url)
    return r.json()


def get_nsfw(url: str):
    r = http_nsfw.get(url)
    return r.json()


class Nekos(commands.Cog):
    def __init__(self, bot: Wilson):
        self._bot = bot

    @commands.command(aliases=['8ball', 'fortune'])
    async def ball(self, ctx: commands.Context, *, message: str = ''):
        if message == '':
            message = 'The 8 ball'

        img = get_sfw('/8ball')['url']
        embed = self._bot.generate_embed(h.add_escape_characters(message), ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command()
    async def cuddle(self, ctx: commands.Context, user: discord.Member = None):
        subject = 'themselves'
        if user is not None:
            subject = h.add_escape_characters(user.display_name)
        action = f'**{h.add_escape_characters(ctx.author.display_name)}** cuddles **{subject}**'

        img = get_sfw('/img/cuddle')['url']
        embed = self._bot.generate_embed(action, ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command()
    async def hug(self, ctx: commands.Context, user: discord.Member = None):
        subject = 'themselves'
        if user is not None:
            subject = h.add_escape_characters(user.display_name)
        action = f'**{h.add_escape_characters(ctx.author.display_name)}** hugs **{subject}**'

        img = get_sfw('/img/hug')['url']
        embed = self._bot.generate_embed(action, ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command(aliases=['mwah', 'smooch'])
    async def kiss(self, ctx: commands.Context, user: discord.Member = None):
        subject = 'themselves'
        if user is not None:
            subject = h.add_escape_characters(user.display_name)
        action = f'**{h.add_escape_characters(ctx.author.display_name)}** kisses **{subject}** (mwah!)'

        img = get_sfw('/img/kiss')['url']
        embed = self._bot.generate_embed(action, ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command(aliases=['pap', 'pet'])
    async def pat(self, ctx: commands.Context, user: discord.Member = None):
        subject = 'themselves'
        if user is not None:
            subject = h.add_escape_characters(user.display_name)
        action = f'**{h.add_escape_characters(ctx.author.display_name)}** pats **{subject}**'

        img = get_sfw('/img/pat')['url']
        embed = self._bot.generate_embed(action, ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command(aliases=['smack', 'bitch'])
    async def slap(self, ctx: commands.Context, user: discord.Member = None):
        subject = 'themselves'
        if user is not None:
            subject = h.add_escape_characters(user.display_name)
        action = f'**{h.add_escape_characters(ctx.author.display_name)}** slaps **{subject}**'

        img = get_sfw('/img/slap')['url']
        embed = self._bot.generate_embed(action, ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command()
    async def smug(self, ctx: commands.Context, user: discord.Member = None):
        subject = 'the discord mods'
        if user is not None:
            subject = h.add_escape_characters(user.display_name)
        action = f'**{h.add_escape_characters(ctx.author.display_name)}** is smug toward **{subject}**'

        img = get_sfw('/img/smug')['url']
        embed = self._bot.generate_embed(action, ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command()
    async def tickle(self, ctx: commands.Context, user: discord.Member = None):
        subject = 'themselves'
        if user is not None:
            subject = h.add_escape_characters(user.display_name)
        action = f'**{h.add_escape_characters(ctx.author.display_name)}** tickles **{subject}**'

        img = get_sfw('/img/tickle')['url']
        embed = self._bot.generate_embed(action, ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command(name='4k')
    @commands.is_nsfw()
    async def nekos_4k(self, ctx: commands.Context):
        img = get_nsfw('/4k')['image']

        embed = self._bot.generate_embed('4K Porn!', ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def ass(self, ctx: commands.Context):
        img = get_nsfw('/anal')['image']

        embed = self._bot.generate_embed('Ass!', ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def bj(self, ctx: commands.Context):
        img = get_nsfw('/blowjob')['image']

        embed = self._bot.generate_embed('Blowjob!', ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def boobs(self, ctx: commands.Context):
        img = get_nsfw('/boobs')['image']

        embed = self._bot.generate_embed('Boobs!', ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def cum(self, ctx: commands.Context):
        img = get_nsfw('/cum')['image']

        embed = self._bot.generate_embed('Cum!', ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command(aliases=['h'])
    @commands.is_nsfw()
    async def hentai(self, ctx: commands.Context, message: str = ''):
        is_gif = message.startswith('g')
        endpoint = '/gif' if is_gif else '/hentai'
        img = get_nsfw(endpoint)['image']

        embed = self._bot.generate_embed('Hentai!', ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command(aliases=['les', 'yuri'])
    @commands.is_nsfw()
    async def lesbian(self, ctx: commands.Context):
        img = get_nsfw('/lesbian')['image']

        embed = self._bot.generate_embed('Yuri!', ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command(aliases=['vagina'])
    @commands.is_nsfw()
    async def pussy(self, ctx: commands.Context):
        img = get_nsfw('/pussy')['image']

        embed = self._bot.generate_embed('Pussy!', ctx.author, image_url=img)
        await ctx.send(embed=embed)


async def setup(bot: Wilson):
    await bot.add_cog(Nekos(bot))
