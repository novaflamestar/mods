import discord
from discord import Client
from discord import app_commands
from steam import SteamCommands
import logging
from config import get_config
from db import init_db, Database

config = get_config()

handler = logging.getLogger('discord')
handler.setLevel(logging.INFO)

guild_id = discord.Object(id=config.DISCORD_GUILD_ID)


class AppClient(Client):
    def __init__(self, *, intents: discord.Intents, activity: discord.Activity = None):
        super().__init__(intents=intents, activity=activity)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        conn = await init_db()
        self.conn = Database(conn)
        self.tree.copy_global_to(guild=guild_id)
        self.tree.add_command(SteamCommands(self.conn), guild=guild_id)
        await self.tree.sync(guild=guild_id)


intents = discord.Intents.all()
client = AppClient(
    intents=intents,
    activity=discord.Activity(
        type=discord.ActivityType.watching, name="ur mum kek"),
)


@client.tree.command(description="Get user stats.")
async def mods_stats(interaction: discord.Interaction, member: discord.Member):
    target_member = await client.conn.upsert_user(str(member))
    await client.conn.init_stats(int(target_member['id']))
    stats = await client.conn.get_user_stats(str(member))
    if stats:
        await interaction.response.send_message(
            f"User {member.mention} has been banned {stats['target_bans']} times. You have banned others {stats['source_bans']} times.")
    else:
        await interaction.response.send_message(
            f"User {member.mention} has no ban records.")


@client.tree.command(description="Bans a member from the server. (not really but you know it feels good)")
async def mods_ban(interaction: discord.Interaction, member: discord.Member):
    handler.info(f"Testing user input: {str(member)}")
    target_member = await client.conn.upsert_user(str(member))
    handler.info(target_member)
    await client.conn.increment_target_bans(int(target_member['id']))
    source_member = await client.conn.upsert_user(str(interaction.user))
    handler.info(source_member)
    await client.conn.increment_source_bans(int(source_member['id']))
    await interaction.response.send_message(f"The rat {interaction.user.mention} has spoken. Banning {member.mention}...")


@mods_ban.error
@mods_stats.error
async def ping_error(interaction: discord.Interaction, error):
    await interaction.response.send_message("An error occurred, please annoy david to fix it.")


client.run(
    config.DISCORD_BOT_TOKEN,
)
