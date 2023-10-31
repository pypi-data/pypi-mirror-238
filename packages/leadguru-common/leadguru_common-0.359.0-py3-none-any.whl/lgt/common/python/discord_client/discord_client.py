import requests
from .methods import DiscordMethods


class DiscordClient:
    base_url = 'https://discord.com/api/'
    token: str
    headers: dict

    def __init__(self, token: str = None):
        self.token = token
        self.headers = {"Authorization": self.token}

    def login(self, login: str, password: str, captcha_key: str = None) -> dict:
        payload = {
            'login': login,
            'password': password,
            'captcha_key': captcha_key,
            "undelete": False,
            "login_source": "",
            "gift_code_sku_id": None,
        }
        response = requests.post(f"{self.base_url}{DiscordMethods.LOGIN.value}", json=payload)
        if response.status_code == 400 or response.status_code == 200:
            return response.json()

        return {}

    def get_servers(self) -> list:
        response = requests.get(f"{self.base_url}{DiscordMethods.USER_GUILDS.value}", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return []

    def get_channels(self, guild_id: str) -> list:
        response = requests.get(f"{self.base_url}{DiscordMethods.guild_channels(guild_id)}", headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return []
