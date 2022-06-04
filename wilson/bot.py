import discord
import wilson.util.logger as log

from discord import Intents
from discord.ext import commands
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

    async def on_ready(self):
        for cog in cogs:
            await self.load_extension(cog)
        log.log_message('Wilson appears...')

    @property
    def config(self) -> BotConfig:
        return self._config
