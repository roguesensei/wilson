import discord
import wilson.util.logger as log

from discord import Intents
from discord.ext import commands
from discord.ext.commands import errors
from wilson.util.bot_config import BotConfig

cogs = ['wilson.cogs.generic']


class Wilson(commands.Bot):
    def __init__(self, owner_id: int, token: str, config_path: str = 'config.yml'):
        self._config = BotConfig(config_path)
        self._token = token

        intents_conf = self.config.intents
        bot_intents = Intents(
            bans=intents_conf.bans,
            emojis=intents_conf.emojis,
            guilds=intents_conf.guilds,
            members=intents_conf.members,
            message_content=intents_conf.message_content,
            messages=intents_conf.messages,
            reactions=intents_conf.reactions,
            voice_states=intents_conf.voice_states
        )
        super().__init__(
            command_prefix=self.config.bot_settings.prefix, case_insensitive=True,
            owner_id=owner_id,
            intents=bot_intents
        )
        self.remove_command('help')

    def run_bot(self):
        try:
            log.log_info('Starting bot', self.config.bot_settings.debug_mode)
            self.run(self._token)
        except Exception as exc:
            log.log_error('An error occurred while running the bot', exc)

    def generate_embed(self, title, author: discord.Member, description='') -> discord.Embed:
        embed = discord.Embed(title=title, description=description, colour=0x1f0000)
        embed.set_author(name=f'Requested by {author.display_name}', icon_url=author.display_avatar.url)
        embed.set_footer(text=self.config.bot_settings.embed_footer, icon_url=self.user.avatar.url)

        return embed

    async def on_ready(self) -> None:
        for cog in cogs:
            await self.load_extension(cog)

        default_presence = self.config.bot_settings.default_presence
        default_activity = discord.Activity(name=default_presence.activity_name, type=default_presence.activity_type)

        await self.change_presence(activity=default_activity, status=default_presence.status)
        log.log_message('Wilson appears...')

    async def on_command_error(self, ctx: commands.Context, exc: errors.CommandError) -> None:
        if isinstance(exc, errors.CommandNotFound):
            if '|' in self.config.bot_settings.prefix and not ctx.message.content.startswith(
                    self.config.bot_settings.prefix + '|'):
                # If bot contains "|" in the prefix, distinguish between spoiler messages and command
                log.log_error('CommandNotFound', exc)
        elif isinstance(exc, errors.MissingRequiredArgument) or isinstance(exc, errors.BadArgument) or isinstance(
                exc, errors.UserInputError):
            log.log_error('MissingRequiredArgument or BadArgument', exc)
            await ctx.send(
                'Oops, you\'ve either entered an invalid argument or you\'re missing one or more argument(s)')
        elif isinstance(exc, errors.MissingPermissions) or isinstance(exc, errors.NotOwner):
            log.log_error('MissingPermissions or NotOwner', exc)
            await ctx.send('You do not have permission to do that.')
        elif isinstance(exc, errors.CommandOnCooldown):
            log.log_error('CommandOnCooldown', exc)
            await ctx.send('This command is on cooldown...')
        elif isinstance(exc, errors.BotMissingPermissions) or isinstance(exc, errors.BotMissingAnyRole):
            log.log_error('BotMissingPermissions or BotMissingAnyRole', exc)
            await ctx.send('I don\'t have permission to do that... Check my roles/permissions in the server settings.')
        elif isinstance(exc, errors.NSFWChannelRequired):
            log.log_error('NSFWChannelRequired', exc)
            await ctx.send('You need to be in a NSFW channel to do that')
        else:
            log.log_error('Unhandled Exception', exc)
            await ctx.send('An unhandled error occurred while invoking the command')

    @property
    def config(self) -> BotConfig:
        return self._config
