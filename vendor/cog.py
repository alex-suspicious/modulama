import glob
import discord
from discord import app_commands
import vendor.env as env

_list = []

DEBUG_SERVER = discord.Object(id=env.get("APP_DEBUG_SERVER"))


def load(client):
	pyfiles = glob.glob("modules/*.py")
	print(pyfiles)

	client.tree = app_commands.CommandTree(client)
	client.tree.copy_global_to(guild=DEBUG_SERVER)