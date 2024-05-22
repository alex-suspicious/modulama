import vendor.env as env
from typing import Optional
import discord
from discord.ext import commands
from vendor.data import createDBFolder
from vendor.cog import load as cogLoad
version = "0.0.1"

class MyClient(commands.Bot):
    def __init__(self, *, command_prefix, intents: discord.Intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        createDBFolder()

intents = discord.Intents.all()
client = MyClient(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')

@client.event
async def setup_hook():
    await cogLoad(client)

client.run(env.get("APP_TOKEN"))