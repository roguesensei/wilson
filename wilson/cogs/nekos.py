from discord.ext import commands
from wilson.bot import Wilson
from wilson.util.http import Http

http = Http('http://api.nekos.fun:8080/api')


def get(url: str):
    r = http.get(url)
    return r.json()


class Nekos(commands.Cog):
    def __init__(self, bot: Wilson):
        self._bot = bot

    @commands.command(name='4k')
    @commands.is_nsfw()
    async def nekos_4k(self, ctx: commands.Context):
        img = get('/4k')['image']

        embed = self._bot.generate_embed('4K Porn!', ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def ass(self, ctx: commands.Context):
        img = get('/anal')['image']

        embed = self._bot.generate_embed('Ass!', ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def bj(self, ctx: commands.Context):
        img = get('/blowjob')['image']

        embed = self._bot.generate_embed('Blowjob!', ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def boobs(self, ctx: commands.Context):
        img = get('/boobs')['image']

        embed = self._bot.generate_embed('Boobs!', ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def cum(self, ctx: commands.Context):
        img = get('/cum')['image']

        embed = self._bot.generate_embed('Cum!', ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command(aliases=['h'])
    @commands.is_nsfw()
    async def hentai(self, ctx: commands.Context, message: str = ''):
        is_gif = message.startswith('g')
        endpoint = '/gif' if is_gif else '/hentai'
        img = get(endpoint)['image']

        embed = self._bot.generate_embed('Hentai!', ctx.author, image_url=img)
        await ctx.send(embed=embed)

    @commands.command(aliases=['les', 'yuri'])
    @commands.is_nsfw()
    async def lesbian(self, ctx: commands.Context):
        img = get('/lesbian')['image']

        embed = self._bot.generate_embed('Yuri!', ctx.author, image_url=img)
        await ctx.send(embed=embed)


async def setup(bot: Wilson):
    await bot.add_cog(Nekos(bot))
