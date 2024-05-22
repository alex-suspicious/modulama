from vendor.cog import load
from vendor.bot import client

#   Updating all the cog commands
class system:
    @staticmethod
    async def update(interaction: discord.Interaction):
        await interaction.response.send_message(f'`🥚 Updating...`')
        await load(client) 
        await interaction.edit_original_response(content="`🐑 Updated`")