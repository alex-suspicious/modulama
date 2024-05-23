import asyncio, discord
import glob
import os
import json
import requests
from vendor.cog import load
from vendor.bot import client

class lmm:
    @staticmethod
    @app_commands.checks.has_permissions(administrator=True)
    async def update(interaction: discord.Interaction):
        await interaction.response.send_message(f"`Searching repositories on github... 🌐🔍🐑`", ephemeral=True)

        url = 'https://api.github.com/search/repositories'
        params = {
            'q': 'modulama-module',
            'order': 'desc',
            'sort': 'stars',
            'per_page': 10000,
            'page': 1
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            await interaction.edit_original_response(content=f"```Saving repositories... 💾🐑```")

            repos = open("github.modules","w")
            repos.write(response.text)
            repos.close()
        else:
            await interaction.edit_original_response(content=f"```Something went wrong 🐑❓```")
            return None

        await interaction.edit_original_response(content=f"```Repositories were updated 🐑🎉```")

    @staticmethod
    @app_commands.checks.has_permissions(administrator=True)
    async def search(interaction: discord.Interaction, name: str):
        if not os.path.exists("github.modules"):
            await interaction.response.send_message(f"```You need to update the repositories list 🐑🤌\nUse /lmm update```")
            return None

        await interaction.response.send_message(f"`Searching {name}... 🔍🐑`", ephemeral=True)
        repos_file = open("github.modules","r")
        repos = json.loads(repos_file.read())
        repos_file.close()

        filtered = []
        for x in range(len(repos["items"])):
            if( name in repos["items"][x]["name"] ):
                filtered.append( repos["items"][x]["name"].replace("modulama-module-","") )

        await interaction.edit_original_response(content=f"```Modules found 📜🐑\n\n· " + ("\n· ".join(filtered)) + "```")

    @staticmethod
    @app_commands.checks.has_permissions(administrator=True)
    async def install(interaction: discord.Interaction, name: str):
        if not os.path.exists("github.modules"):
            await interaction.response.send_message(f"```You need to update the repositories list 🐑🤌\nUse /lmm update```")
            return None

        await interaction.response.send_message(f"`Searching {name}... 🔍🐑`", ephemeral=True)
        repos_file = open("github.modules","r")
        repos = json.loads(repos_file.read())
        repos_file.close()

        condidate = -1
        for x in range(len(repos["items"])):
            if( name == repos["items"][x]["name"].replace("modulama-module-","") ):
                condidate = x

        if( condidate == -1 ):
            await interaction.edit_original_response(content="`Module not found 🐑🤌`")
            return None

        await interaction.edit_original_response(content="`Installing module... 🧩🪛🐑`")
        response = requests.get("https://github.com/"+repos["items"][condidate]["full_name"]+"/blob/main/main.py?raw=true")

        module = open( "modules/" + repos["items"][condidate]["name"].replace("modulama-module-","") + ".py","w")
        module.write(response.text)
        module.close()

        await interaction.edit_original_response(content=f"`Updating the command tree... 🥚`")
        await load(client) 
        await interaction.edit_original_response(content="`Module was installed 🐑🎉`")

    @staticmethod
    @app_commands.checks.has_permissions(administrator=True)
    async def installed(interaction: discord.Interaction):
        pyfiles = glob.glob("modules/*.py")
        await interaction.response.send_message(f"```Installed modules 📜🐑\n\n· " + ('\n· '.join(pyfiles)).replace(".py","").replace("modules/","") + "```", ephemeral=True)

    @staticmethod
    @app_commands.checks.has_permissions(administrator=True)
    async def uninstall(interaction: discord.Interaction, name: str):
        pyfiles = glob.glob("modules/*.py")
        condidate = ""
        for x in range(len(pyfiles)):
            if( name in pyfiles[x] ):
                condidate = pyfiles[x]
                break

        if( not condidate ):
            await interaction.response.send_message("`Module not found 🐑🤌`", ephemeral=True)
            return

        class yesOrNo(discord.ui.View):
            @discord.ui.button(label="Yes", style=discord.ButtonStyle.primary, emoji="🗑️")
            async def yes_callback(self, interactionT, button):
                await interaction.edit_original_response(content=f"`Uninstalling module '{condidate}' 🕰️🐑`",view=None)
                os.remove(condidate)
                await interaction.edit_original_response(content=f"`Updating the command tree... 🥚`",view=None)
                await load(client) 
                await interaction.edit_original_response(content="`Module was uninstalled 🐑🎉`",view=None)

            @discord.ui.button(label="No", style=discord.ButtonStyle.primary, emoji="⛔")
            async def no_callback(self, interactionT, button):
                await interaction.edit_original_response(content="`Nothing happend 🐑🎉`",view=None)

        await interaction.response.send_message(f"```Are you sure 🐑❓\n\n· {condidate}```", ephemeral=True, view=yesOrNo())