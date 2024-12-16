import requests
import asyncio
import os

API_ENDPOINT = "https://discord.com/api/v10/"
BOT_TOKEN = os.environ["BOT_TOKEN"]

def get_user_info(user_token, user_id):
    headers = {
        "Authentication": user_token,
        "Accept-Type": "application/json"
    }

    user_info = requests.get(
        API_ENDPOINT + "users/" + user_id + "/profile",
        headers = headers
    )

    return user_info.json()

def get_guild_info(guild_id):
    headers = {
        "Authentication": f"Bot {BOT_TOKEN}",
        "Accept-Type": "application/json"
    }

    guild_info = requests.get(
        API_ENDPOINT + "guilds/" + guild_id,
        headers = headers
    )

    return guild_info.json()