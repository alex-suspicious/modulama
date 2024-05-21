
class test(commands.Cog):
    async def ping(self, interaction: discord.Interaction):
        curUser = user().where( "discord_id",interaction.user.id, create=True ).first()
        curUser.messages += 1
        curUser.save()

        await interaction.response.send_message(f'Messages: {curUser.messages}')