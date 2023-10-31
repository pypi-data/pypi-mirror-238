from enum import Enum


class DiscordMethods(str, Enum):
    USER_GUILDS = 'users/@me/guilds'
    LOGIN = 'v9/auth/login'

    @staticmethod
    def guild_channels(guild_id: str):
        return f'guilds/{guild_id}/channels'
