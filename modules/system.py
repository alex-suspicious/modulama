
#   Updating all the cog commands
class system:
    @staticmethod
    async def update(interaction: discord.Interaction):
        from vendor.cog import load
        from vendor.bot import client

        await interaction.response.send_message(f'`🥚 Updating...`')
        await load(client) 
        await interaction.edit_original_response(content="`🐑 Updated`")