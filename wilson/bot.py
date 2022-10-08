import discord
import os
import time
import yaml

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import errors
from .util.logger import *
from .util.bot_config import BotConfig
from .util.guild_settings import GuildSettings

cogs = [
    'wilson.cogs.admin',
    'wilson.cogs.generic',
    'wilson.cogs.fun',
    'wilson.cogs.guild',
    'wilson.cogs.moderator',
    'wilson.cogs.app_commands.role'
]


class Wilson(commands.Bot):
    def __init__(self, config: BotConfig):
        """Constructor function
        """
        self._config = config
        self._online_time = 0
        self._synced = False
        self.wilson_extensions = {}
        super().__init__(
            command_prefix=self._config.bot_settings.prefix, case_insensitive=True,
            owner_id=self._config.bot_settings.owner_id,
            intents=self._config.intents
        )
        self.remove_command('help')

        if not os.path.exists('.wilson'):
            log_warning('Created new hidden .wilson directory')
            os.mkdir('.wilson')

        # self.tree = app_commands.CommandTree(self)

    def run_bot(self) -> None:
        try:
            log_info('Starting bot')
            self.run(self.config.bot_settings.bot_token)
        except Exception as exc:
            log_error('An error occurred while running the bot', exc)

    def generate_embed(self, title: str, author: discord.Member, description: str = None, image_url: str = None,
                       thumbnail_url: str = None) -> discord.Embed:
        embed = discord.Embed(title=title, description=description, colour=0x1f0000)
        embed.set_author(name=f'Requested by {author.display_name}', icon_url=author.display_avatar.url)
        embed.set_footer(text=self.config.bot_settings.embed_footer, icon_url=self.user.avatar.url)

        if image_url is not None:
            embed.set_image(url=image_url)
        if thumbnail_url is not None:
            embed.set_thumbnail(url=thumbnail_url)

        return embed

    async def on_ready(self) -> None:
        await self.wait_until_ready()

        for cog in cogs:
            try:
                await self.load_extension(cog)
                log_info(f'Loaded cog {cog}')
            except Exception as exc:
                log_error(f'An error occurred loading cog {cog}', exc)

        default_presence = self.config.bot_settings.default_presence
        default_activity = discord.Activity(name=default_presence.activity_name, type=default_presence.activity_type)

        await self.change_presence(activity=default_activity, status=default_presence.status)
        self._online_time = time.time()

        if os.path.exists('extensions'):
            for extension_dir in os.listdir('extensions'):
                extension_path = f'extensions/{extension_dir}'
                items = os.listdir(extension_path)

                if 'extension.yml' in items:
                    config = yaml.safe_load(open(f'{extension_path}/extension.yml'))
                    extension_name = config['friendly_name']
                    key = extension_name.lower()

                    self.wilson_extensions[key] = {'name': f'{extension_name} (by {config["author"]})',
                                                   'help': f'{extension_path}/help/'}
                    await self.load_extension(config['cog'])

        log_info(f'Discord API Version: {discord.__version__}')
        log_message('Wilson appears...')

    async def on_member_join(self, member: discord.Member) -> None:
        guild = member.guild
        settings = GuildSettings.get_settings(guild.id)

        if settings.welcome_actions:
            if settings.welcome_channel_id != 0:
                channel = guild.get_channel(settings.welcome_channel_id)
                if channel is not None:
                    message_string = settings.welcome_message
                    message_string = message_string.replace('[@user]', f'<@{member.id}>')
                    message_string = message_string.replace('[!user]', member.display_name)
                    message_string = message_string.replace('[!server]', guild.name)

                    await channel.send(message_string)
            if settings.autorole_id != 0:
                role = guild.get_role(settings.autorole_id)
                if role is not None:
                    await member.add_roles(role)

    async def on_command(self, ctx: commands.Context) -> None:
        log_debug(f'{ctx.message.clean_content}')

    # async def on_error(self, event_method: str, /, *args, **kwargs):
    #     pass

    async def on_command_error(self, ctx: commands.Context, exc: errors.CommandError) -> None:
        if isinstance(exc, errors.CommandNotFound):
            if self.config.bot_settings.prefix == '|' and(
                '|' in self.config.bot_settings.prefix and not ctx.message.content.startswith(self.config.bot_settings.prefix + '|')):
                # If bot contains "|" in the prefix (when "|" is the prefix like in Wilson's case), distinguish between spoiler messages and command
                log_error('CommandNotFound', exc)
        elif isinstance(exc, errors.MissingRequiredArgument) or isinstance(exc, errors.BadArgument) or isinstance(
                exc, errors.UserInputError):
            log_error('MissingRequiredArgument or BadArgument', exc)
            await ctx.message.reply(
                'Oops, you\'ve either entered an invalid argument or you\'re missing one or more argument(s)')
        elif isinstance(exc, errors.MissingPermissions) or isinstance(exc, errors.NotOwner):
            log_error('MissingPermissions or NotOwner', exc)
            await ctx.message.reply('You do not have permission to do that.')
        elif isinstance(exc, errors.CommandOnCooldown):
            log_error('CommandOnCooldown', exc)
            await ctx.message.reply('This command is on cooldown...')
        elif isinstance(exc, errors.BotMissingPermissions) or isinstance(exc, errors.BotMissingAnyRole):
            log_error('BotMissingPermissions or BotMissingAnyRole', exc)
            await ctx.message.reply(
                'I don\'t have permission to do that... Check my roles/permissions in the server settings.')
        elif isinstance(exc, errors.NSFWChannelRequired):
            log_error('NSFWChannelRequired', exc)
            await ctx.message.reply('You need to be in a NSFW channel to do that')
        else:
            log_error('Unhandled Exception', exc)
            await ctx.message.reply('An unhandled error occurred while invoking the command')

    @property
    def config(self) -> BotConfig:
        return self._config

    @property
    def online_time(self) -> int:
        return self._online_time
