from vendor.cog import load
from vendor.bot import client
from vendor.bot import version

class system:

    @staticmethod
    async def update(interaction: discord.Interaction):
        await interaction.response.send_message(f'`🥚 Updating...`')
        await load(client) 
        await interaction.edit_original_response(content="`🐑 Updated`")

    @staticmethod
    @app_commands.checks.has_permissions(administrator=True)
    async def info(interaction: discord.Interaction):
        await interaction.response.send_message(f'```I am a Modulama 🐑\nVersion {version}```')

    @staticmethod
    @app_commands.choices(choices=[
        app_commands.Choice(name="Rock", value="rock"),
        app_commands.Choice(name="Paper", value="paper"),
        app_commands.Choice(name="Scissors", value="scissors"),
    ])
    async def options(interaction: discord.Interaction, choices: app_commands.Choice[str]):
        await interaction.response.send_message(f'```{choices.value}```')
