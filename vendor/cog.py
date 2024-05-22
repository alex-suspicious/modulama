import glob
import discord
from discord import app_commands
from discord.ext import commands
import vendor.env as env
import inspect
import os
import time

_groups = {}
_session = {}

_cached_env = {}
_cached_code = {}
_cached_edit = {}

DEBUG_SERVER = discord.Object(id=env.get("APP_DEBUG_SERVER"))

async def commandNotFound(interaction: discord.Interaction, *args):
	if( str(interaction.user.id) == str(env.get("APP_OWNER")) ):
		await interaction.response.send_message('`Command not found 🔍🐑\nThis command may be outdated, 💻 use /update`', ephemeral=True)
	else:
		await interaction.response.send_message('`Command not found 🔍🐑\nThis command may be outdated :warning:, please try again in a few minutes 🕰️\nOr make a report to the bot owner 📝`', ephemeral=True)

def commandsFromFile(path):
	ti_m = os.path.getmtime(path)
	m_ti = time.ctime(ti_m)

	if( path in _cached_edit ):
		if( m_ti == _cached_edit[path] ):
			return _cached_env[path]

	file = open(path,"r")
	code = file.read()
	file.close()

	_local_env = {}
	exec(code, globals(), _local_env)

	_globals_env = {}
	_globals_env.update( globals() )
	_globals_env.update( _local_env )
	_local_env = {}

	exec(code, _globals_env, _local_env)

	_cached_edit[path] = m_ti
	_cached_env[path] = _local_env
	_cached_code[path] = code
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
		commandsFile = commandsFromFile(disCommand)
		names = list(commandsFile.keys())
		sources = _cached_code[disCommand].split("\n")

		for x in range(len(names)):
			if( not isinstance(commandsFile[names[x]], type) ):
				continue
			if( "slot " not in str(commandsFile[names[x]].__init__) ):
				continue

			commandsList = [ x for x in dir( commandsFile[names[x]]() ) if "__" not in x ]

			if( names[x] not in _groups ):
				_groups[ names[x] ] = app_commands.Group(name=names[x], description="none")
				client.tree.add_command(_groups[ names[x] ])


			for y in range( len(commandsList) ):
				func = getattr(commandsFile[names[x]](), commandsList[y])
				if( callable( func ) ):
					attributes = str( inspect.signature(func))
					attributes_inside = f"({','.join(list(inspect.signature(func).parameters.keys()))})"

					condidate = 0
					for g in range( len(sources) ):
						if( f"async def {commandsList[y]}" in sources[g] ):
							condidate = g
							break

					decorations = []
					if( condidate ):
						for g in range(condidate-1,0, -1):
							if( "@staticmethod" in sources[g] ):
								break
							elif( sources[g] ):
								decorations.append( sources[g].replace("    ","") )
							
						decorations.reverse()

					code = f"""
@_groups["{names[x]}"].command(name = "{commandsList[y]}", description = "none")
"""+("\n".join(decorations))+f"""
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
					"""
					exec( code, globals(), locals() )

	client.tree.copy_global_to(guild=DEBUG_SERVER)
	await client.tree.sync(guild=DEBUG_SERVER)