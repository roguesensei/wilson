import discord
import wilson.util.helpers as h
import wilson.util.logger as log

from discord.ext import commands
from wilson.bot import Wilson
from wilson.util.guild_settings import GuildSettings


class Guild(commands.Cog):
    def __init__(self, bot: Wilson):
        self._bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def optin(self, ctx: commands.Context):
        guild_id = ctx.guild.id
        prefix = self._bot.config.bot_settings.prefix
        settings = GuildSettings(guild_id)

        if settings.opted_in:
            await ctx.reply(
                f'You are already opted in. If you would prefer to opt out, you can type `{prefix}optout`')
        else:
            settings.save_settings()
            await ctx.reply(f'Done! You can now view your settings by typing `{prefix}settings`')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def optout(self, ctx: commands.Context):
        guild_id = ctx.guild.id
        prefix = self._bot.config.bot_settings.prefix

        if not GuildSettings(guild_id).opted_in:
            await ctx.reply(
                f'You are already opted out. If you would prefer to opt in, you can type `{prefix}optin`')
        else:
            GuildSettings.delete_settings(guild_id)
            await ctx.reply(f'Done! You can always opt back in anytime by typing `{prefix}optin`')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def settings(self, ctx: commands.Context):
        guild_id = ctx.guild.id
        prefix = self._bot.config.bot_settings.prefix
        settings = GuildSettings.get_settings(guild_id)

        if not settings.opted_in:
            await ctx.reply(
                f'You are not opted in to use guild settings, type `{prefix}optin` to use guild settings. For more information, type `{prefix}help settings data`')
        else:
            settings_body = f'''
**Toggles**
```yml
welcome_actions: {settings.welcome_actions}
```
'''
            embed = self._bot.generate_embed('Guild Settings', ctx.author, description=settings_body)

            if settings.welcome_actions:
                embed.description = embed.description + f'**Welcome Message** ```yml\nwelcome_message: {settings.welcome_message}\n```'
                if settings.welcome_channel_id != 0:
                    embed.add_field(name='**Welcome Channel**', value=f'<#{settings.welcome_channel_id}>')
                if settings.autorole_id != 0:
                    embed.add_field(name='**Default/Auto Role**', value=f'<@&{settings.autorole_id}>')

            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def toggle(self, ctx: commands.Context, key: str):
        guild_id = ctx.guild.id
        prefix = self._bot.config.bot_settings.prefix
        settings = GuildSettings.get_settings(guild_id)
        options = ['welcome_actions']

        if not settings.opted_in:
            await ctx.reply(
                f'You are not opted in to use guild settings, type `{prefix}optin` to use guild settings. For more information, type `{prefix}help settings data`')
        elif key not in options:
            await ctx.reply(f'Invalid option: {key}')
        else:
            set_to = False

            if key == options[0]:
                settings.welcome_actions = not settings.welcome_actions
                set_to = settings.welcome_actions

            settings.save_settings()
            await ctx.reply(f'`{key}` set to `{set_to}`')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def autorole(self, ctx: commands.Context, autorole: discord.Role):
        guild_id = ctx.guild.id
        prefix = self._bot.config.bot_settings.prefix
        settings = GuildSettings.get_settings(guild_id)

        if not settings.opted_in:
            await ctx.reply(
                f'You are not opted in to use guild settings, type `{prefix}optin` to use guild settings. For more information, type `{prefix}help settings data`')
        elif not settings.welcome_actions:
            await ctx.reply(f'Please enable `welcome_actions` first by typing `{prefix}toggle welcome_actions`')
        else:
            settings.autorole_id = autorole.id
            settings.save_settings()
            await ctx.reply(f'Default role set to <@&{autorole.id}>')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def welcome_channel(self, ctx: commands.Context, welcome_channel: discord.TextChannel):
        guild_id = ctx.guild.id
        prefix = self._bot.config.bot_settings.prefix
        settings = GuildSettings.get_settings(guild_id)

        if not settings.opted_in:
            await ctx.reply(
                f'You are not opted in to use guild settings, type `{prefix}optin` to use guild settings. For more information, type `{prefix}help settings data`')
        elif not settings.welcome_actions:
            await ctx.reply(f'Please enable `welcome_actions` first by typing `{prefix}toggle welcome_actions`')
        else:
            settings.welcome_channel_id = welcome_channel.id
            settings.save_settings()
            await ctx.reply(f'Welcome channel set to <#{welcome_channel.id}>')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def welcome_message(self, ctx: commands.Context, *, welcome_message: str):
        guild_id = ctx.guild.id
        prefix = self._bot.config.bot_settings.prefix
        settings = GuildSettings.get_settings(guild_id)

        if not settings.opted_in:
            await ctx.reply(
                f'You are not opted in to use guild settings, type `{prefix}optin` to use guild settings. For more information, type `{prefix}help settings data`')
        elif not settings.welcome_actions:
            await ctx.reply(f'Please enable `welcome_actions` first by typing `{prefix}toggle welcome_actions`')
        else:
            settings.welcome_message = welcome_message
            settings.save_settings()
            await ctx.reply(f'Welcome message set to `{welcome_message}`')


async def setup(bot: Wilson):
    await bot.add_cog(Guild(bot))
    log.log_info('Guild cog loaded')
