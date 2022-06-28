import datetime
import discord


def format_elapsed_time(duration: float, include_days: bool = True) -> str:
    """Format elapsed time to number of days/hours etc"""
    sec = datetime.timedelta(seconds=duration)
    d = datetime.datetime(1, 1, 1) + sec
    return ('%dd %dh %dm %ds' % (d.day - 1, d.hour, d.minute, d.second)) if include_days else (
            '%dh %dm %ds' % (d.hour, d.minute, d.second))


def compare_roles(u1: discord.Member, u2: discord.Member) -> bool:
    """Compares if user u1 has a higher role than user u2"""
    return u1.top_role.position > u2.top_role.position
