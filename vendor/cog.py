import glob
import discord
from discord import app_commands
import vendor.env as env
import inspect

_groups = {}
_session = {}

DEBUG_SERVER = discord.Object(id=env.get("APP_DEBUG_SERVER"))

async def commandNotFound(interaction: discord.Interaction):
	if( str(interaction.user.id) == str(env.get("APP_OWNER")) ):
		await interaction.response.send_message('`Command not found 🔍🐑\nThis command may be outdated, 💻 use /update`', ephemeral=True)
	else:
		await interaction.response.send_message('`Command not found 🔍🐑\nThis command may be outdated :warning:, please try again in a few minutes 🕰️\nOr make a report to the bot owner 📝`', ephemeral=True)

def commandsFromFile(path):
	file = open(path,"r")
	code = file.read()
	file.close()

	_local_env = {}
	exec(code, globals(), _local_env)
	return _local_env

def functionFromClassFile(class_file, class_obj, func_name):
	_local_env = commandsFromFile(class_file)
	if( hasattr(_local_env[class_obj], func_name) ):
		return getattr( _local_env[class_obj], func_name)
	return commandNotFound

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
				func = getattr(commands[names[x]](), commandsList[y])
				if( callable( func ) ):
					attributes = str( inspect.signature(func))
					attributes_inside = f"({','.join(list(inspect.signature(func).parameters.keys()))})"

					exec( f"""
@_groups["{names[x]}"].command(name = "{commandsList[y]}", description = "none")
async def {commandsList[y]}{attributes}:
	if( interaction.user.id not in _session ):
		_session[interaction.user.id] = {{}}
	if( "wait" in _session[interaction.user.id] ):
		await interaction.response.send_message("`Wait untill the previous command stops 🕰️🐑`", ephemeral=True)
	else:
		_session[interaction.user.id]["wait"] = True
		try:
			await functionFromClassFile("{disCommand}", "{names[x]}", "{commandsList[y]}"){attributes_inside}
		except Exception as error:
			if( interaction.response.is_done() ):
				await interaction.edit_original_response(content=f"```Error occured in the '{disCommand}' module 💻🔍🐑\\n{{error}}```", embed=None)
			else:
				await interaction.response.send_message(f"```Error occured in the '{disCommand}' module 💻🔍🐑\\n{{error}}```", ephemeral=True)
		del _session[interaction.user.id]["wait"]
					""", globals(), locals() )
					#	Yes, i think it is not great to read the file with code everytime you run the command.
					#	But on the other hand, you can freely edit, install, remove your commands in real time
					#	With big changes like adding new commands, or changing command names, you can use /update to update the tree

	client.tree.copy_global_to(guild=DEBUG_SERVER)
	await client.tree.sync(guild=DEBUG_SERVER)