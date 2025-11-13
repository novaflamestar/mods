import discord
from discord.ext import commands
import os

TOKEN = os.getenv('DISCORD_BOT_TOKEN')



intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-mods ", intents=intents)

@bot.event
async def on_ready():
    print("online")


@bot.command(name="ban")
async def ping(ctx, member: discord.Member):
    await ctx.send(f"banning {member.mention}...")

bot.run(TOKEN)
