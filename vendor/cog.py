import glob
import discord
from discord import app_commands
import vendor.env as env

_groups = {}
_group_env = {}

DEBUG_SERVER = discord.Object(id=env.get("APP_DEBUG_SERVER"))

def commandsFromFile(path):
	file = open(path,"r")
	code = file.read()
	file.close()

	if( path not in _group_env ):
		_group_env[path] = {}


	_local_env = globals()
	_local_env.update( _group_env[path] )

	exec(code, globals(), _group_env[path])
	return _group_env[path]

async def load(client):
	global _groups
	if( "tree" in dir(client) ):
		client.tree.clear_commands(guild=None)
		client.tree.clear_commands(guild=DEBUG_SERVER)
		_groups = {}
	else:
		client.tree = app_commands.CommandTree(client)
	
	pyfiles = glob.glob("modules/*.py")

	for disCommand in pyfiles:
		commands = commandsFromFile(disCommand)
		names = list(commands.keys())

		for x in range(len(names)):
			if( not isinstance(commands[names[x]], type) ):
				continue

			commandsList = [ x for x in dir( commands[names[x]]() ) if "__" not in x ]

			if( names[x] not in _groups ):
				_groups[ names[x] ] = app_commands.Group(name=names[x], description="none")
				client.tree.add_command(_groups[ names[x] ])


			for y in range( len(commandsList) ):

				if( callable( getattr(commands[names[x]](), commandsList[y]) ) ):
					exec( f"""
@_groups["{names[x]}"].command(name = "{commandsList[y]}", description = "none")
async def {commandsList[y]}(interaction: discord.Interaction):
	await getattr( commandsFromFile("{disCommand}")["{names[x]}"], "{commandsList[y]}")( interaction )
					""", globals(), locals() )
					#	Yes, i think it is not great to read the file with code everytime you run the command.
					#	But on the other hand, you can freely edit, install, remove your commands in real time
					#	With big changes like adding new commands, or changing command names, you can use /update to update the tree
					#	TODO: Check if command exist, and return error to end user if not.

	client.tree.copy_global_to(guild=DEBUG_SERVER)
	#await client.tree.sync(guild=DEBUG_SERVER)