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
    async def info(interaction: discord.Interaction):
        await interaction.response.send_message(f'```I am a Modulama 🐑\nVersion {version}```')
