import discord
import os

from discord import app_commands
from processor import Processor

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print("[i] Bot is online. Happy mutuals finding!")

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

async def get_members(guild_id):
    """Coroutine to fetch member ids from a guild."""
    current_guild = await client.fetch_guild(int(guild_id))

    members = []
    async for member in current_guild.fetch_members(limit=None):
        members.append(str(member.id))
    
    return members

async def get_user(user_id):
    """Coroutine to fetch user details via user id."""
    userObj = await client.fetch_user(int(user_id))
    return {
        "name": userObj.name,
        "id": user_id,
        "global_name": userObj.global_name,
        "bot": userObj.bot,
        "mutual_guilds": [g.id for g in userObj.mutual_guilds],
        "avatar": (userObj.avatar.key if userObj.avatar != None else None)
    }

async def get_mutuals(member_list: list, guild_id):
    proc = Processor(member_list, guild_id)
    return proc.get_mutuals()

async def sort_mutuals_users(mutual_servers_dict: dict):
    sorted_users = Processor.group_mutual_users(None, mutual_servers_dict)
    return sorted_users

async def get_guild_info(guild_id):
    guild_info =  await client.fetch_guild(guild_id)
    jsonified_info = {}

    jsonified_info['id'] = guild_id
    jsonified_info['name'] = guild_info.name
    
    if guild_info.icon == None:
        jsonified_info['icon'] = {
            'is_animated': False,
            'key': None,
            'url': None,
        }
    else:
        jsonified_info['icon'] = {
            'is_animated': guild_info.icon.is_animated(),
            'key': guild_info.icon.key,
            'url': guild_info.icon.url
        }

    return jsonified_info

@tree.command(name="mutuals", description="Retrieves a summary of mutual servers found in current server.")
async def mutuals_command(
    interaction: discord.Interaction,
    hidden: bool = False
    ):
    embed = discord.Embed(title="MutualFind", description="Summary of our findings in this server:")
    #embed.set_thumbnail(url="https://mutualfind.koyeb.app/static/assets/mutuals_thumbnail.png")
    #embed.add_field(name="Top 5 Servers you're mutual with:", value=" ", inline=True)
    embed.add_field(name="Mutual Members")

    await interaction.response.send_message(embed=embed, ephemeral=hidden)

async def start_bot():
    await client.start(os.environ["BOT_TOKEN"])