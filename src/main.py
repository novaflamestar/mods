import discord
from discord.ext import commands
import os

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

def print_censored_token(token):
    print(f"Bot token: {token[:4]}...{token[-4:]}")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-mods ", intents=intents)

@bot.event
async def on_ready():
    print("online")


@bot.command(name="ban")
async def ping(ctx, member: discord.Member):
    await ctx.send(f"banning {member.mention}...")

print_censored_token(TOKEN)

bot.run(TOKEN)
