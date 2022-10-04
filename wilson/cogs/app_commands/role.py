import discord
import wilson.util.helpers as h

from discord import app_commands
from discord.ext import commands
from wilson.bot import Wilson


class SlashRole(commands.GroupCog, name='role'):
    def __init__(self, bot: Wilson):
        self._bot = bot

    @app_commands.command(name='add', description='Give role to user')
    @app_commands.describe(member='Member to give role to', role='Role for member')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_roles=True)
    async def add_role(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        if role.id == interaction.user.top_role.id:
            await interaction.response.send_message('Cannot add a role the same as your own')
        elif h.compare_roles(interaction.user, member):
            if h.contains_role(member, role):
                await interaction.response.send_message(f'**{member.display_name}** already has the role')
                return
            await member.add_roles(role)
            await interaction.response.send_message(f'**{member.display_name}** has been granted role **{role.name}**')
        else:
            await interaction.response.send_message('Cannot add a role higher than your own')
    
    @app_commands.command(name='take', description='Take role from user')
    @app_commands.describe(member='Member to take role from', role='Member\'s role')
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_roles=True)
    async def take_role(self, interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        if role.id == interaction.user.top_role.id:
            await interaction.response.send_message('Cannot take a role the same as your own')
        elif h.compare_roles(interaction.user, member):
            if not h.contains_role(member, role):
                await interaction.response.send_message(f'**{member.display_name}** already lacks the role')
                return
            await member.remove_roles(role)
            await interaction.response.send_message(f'**{member.display_name}** has been revoked role **{role.name}**')
        else:
            await interaction.response.send_message('Cannot take a role higher than or equal your own')


async def setup(bot: Wilson):
    await bot.add_cog(SlashRole(bot))
