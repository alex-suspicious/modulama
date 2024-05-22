
#   Example of Database interaction
class counter:
    @staticmethod
    async def add(interaction: discord.Interaction):
        from app.Models.user import user

        curUser = user().where( "discord_id",interaction.user.id, create=True ).first()
        curUser.messages += 1
        curUser.save()

        await interaction.response.send_message(f'Counted: {curUser.messages}')

    @staticmethod
    async def result(interaction: discord.Interaction):
        from app.Models.user import user
        curUser = user().where( "discord_id",interaction.user.id, create=True ).first()

        await interaction.response.send_message(f'Counted: {curUser.messages}')


#   Adding command to system group that already exists in the system.py file
#   If you want to add new commands in your module to already existing group, you will have no problem.             
class system:
    @staticmethod
    async def info(interaction: discord.Interaction):
        from vendor.bot import version
        await interaction.response.send_message(f'```I am a Modulama 🐑\nVersion{version}```')
