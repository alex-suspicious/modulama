import vendor.env as env
from typing import Optional
import discord
from vendor.data import createDBFolder
from vendor.cog import load as cogLoad
version = "0.0.1"

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        createDBFolder()
        

    async def setup_hook(self):
        await cogLoad(self)

intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')

client.run(env.get("APP_TOKEN"))