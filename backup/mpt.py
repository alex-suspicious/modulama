import asyncio, discord
import glob
import os

class mpt:
    @staticmethod
    async def search(interaction: discord.Interaction, name: str):
        await interaction.response.send_message(f"`Searching {name}... 🔍🐑`", ephemeral=True)
        await asyncio.sleep(2)
        await interaction.edit_original_response(content=f"```Modules found 📜🐑```")

    @staticmethod
    async def installed(interaction: discord.Interaction):
        pyfiles = glob.glob("modules/*.py")

        await interaction.response.send_message(f"```Installed modules 📜🐑\n\n· " + ('\n· '.join(pyfiles)).replace(".py","").replace("modules/","") + "```", ephemeral=True)

    @staticmethod
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
                os.remove(condidate)
                await interaction.edit_original_response(content="`Module was uninstalled 🎈🐑`",view=None)

            @discord.ui.button(label="No", style=discord.ButtonStyle.primary, emoji="⛔")
            async def no_callback(self, interactionT, button):
                await interaction.edit_original_response(content="`Nothing happend 🐑🎉`",view=None)


        await interaction.response.send_message(f"```Are you sure 🐑❓\n\n· {condidate}```", ephemeral=True, view=yesOrNo())