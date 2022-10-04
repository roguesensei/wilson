import datetime
import os.path

import discord


def add_escape_characters(string: str):
    """Adds escape characters to format properly in discord message"""
    protected_chars = ['*', '\\']
    new_string = ''
    if len(string) == 0:
        return string
    for char in string:
        if char in protected_chars:
            char = '\\{}'.format(char)
        new_string += char
    return new_string


def compare_roles(u1: discord.Member, u2: discord.Member) -> bool:
    """Compares if user u1 has a higher role than user u2"""
    return u1.top_role.position > u2.top_role.position


def format_elapsed_time(duration: float, include_days: bool = True) -> str:
    """Format elapsed time to number of days/hours etc"""
    sec = datetime.timedelta(seconds=duration)
    d = datetime.datetime(1, 1, 1) + sec
    return ('%dd %dh %dm %ds' % (d.day - 1, d.hour, d.minute, d.second)) if include_days else (
        '%dh %dm %ds' % (d.hour, d.minute, d.second))


def contains_role(member: discord.Member, role: discord.Role) -> bool:
    """Checks if given member has the given role"""
    for r in member.roles:
        if r.id == role.id:
            return True
    return False
