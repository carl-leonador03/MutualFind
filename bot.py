import discord
import os

from discord import app_commands

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
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
    userObj = await client.get_user(int(user_id))
    return {
        "name": userObj.name,
        "id": userObj.id,
        "global_name": userObj.global_name,
        "bot": userObj.bot,
        "mutual_guilds": [g.id for g in userObj.mutual_guilds],
        "avatar": userObj.avatar.url
    }

"""@tree.command(name="mutuals", description="Retrieves a summary of mutual servers found in current server.")
async def mutuals_command(
    interaction: discord.Interaction,
    hidden: bool = False
    ):

    wait_embed = discord.Embed(title="MutualFind", description="Working, please wait...")
    wait_embed.set_thumbnail(url="https://carlleonador03.pythonanywhere.com/embed/assets/mutuals_loading.gif")

    await ctx.send(embed=wait_embed)
    await interaction.response.defer()
    
    embed = discord.Embed(title="MutualFind", description="Summary of our findings in this server:")
    embed.set_thumbnail(url="https://carlleonador03.pythonanywhere.com/embed/assets/mutuals_thumbnail.png")
    #embed.add_field(name="Top 5 Servers you're mutual with:", value=" ", inline=True)
    embed.add_field(name="Mutual Members")

    channel = ctx.channel

    await ctx.edit_message()"""

async def start_bot():
    await client.start(os.environ["BOT_TOKEN"])