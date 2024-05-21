import vendor.env as env
from typing import Optional
import discord
from discord import app_commands
from vendor.data import createDBFolder
from app.Models.user import user

MY_GUILD = discord.Object(id=env.get("APP_DEBUG_SERVER"))  # replace with your guild id


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        createDBFolder()
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        #await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.tree.command()
async def count(interaction: discord.Interaction):
    curUser = user().where( "discord_id",interaction.user.id, create=True ).first()
    curUser.messages += 1
    curUser.save()

    await interaction.response.send_message(f'Messages: {curUser.messages}')

client.run(env.get("APP_TOKEN"))

