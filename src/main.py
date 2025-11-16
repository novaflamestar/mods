import discord
from discord.ext import commands
from discord import Client
from discord import app_commands
import os
import logging

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = os.environ["DISCORD_GUILD_ID"]

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

guild_id = discord.Object(id=GUILD_ID)

class AppClient(Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=guild_id)
        await self.tree.sync(guild=guild_id)

intents = discord.Intents.all()
client = AppClient(intents=intents)

@client.tree.command(description="Bans a member from the server. (not really but you know it feels good)")
async def mods_ban(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"banning {member.mention}...")

@mods_ban.error
async def ping_error(interaction: discord.Interaction, error):
    await interaction.response.send_message("An error occurred, please annoy david to fix it.")

client.run(TOKEN)
