from app.Models.user import user
import discord

class economy:
    @staticmethod
    async def wallet(interaction: discord.Interaction):
        curUser = user().where( "discord_id",interaction.user.id, create=True ).first()

        embed = discord.Embed(title="Wallet " + interaction.user.name, description="", color = discord.Color.from_rgb(255, 219, 148) )
        embed.set_thumbnail( url = interaction.user.avatar )
        embed.add_field(name="Information",value=
            f":dollar: Ballance: {curUser.money}$\n" +
            f"💰 Salary: 0$ per day"
        ,inline=False)

        await interaction.response.send_message(embed=embed)

    @staticmethod
    async def transfer(interaction: discord.Interaction, member: discord.Member, amount: int):
        userData = user().where( "discord_id",interaction.user.id, create=True ).first()
        memberData = user().where( "discord_id",member.id, create=True ).first()

        if( userData.money - amount < 0 ):
            embed = discord.Embed(title="Transaction failed", description="", color = discord.Color.from_rgb(255, 219, 148) )
            embed.set_thumbnail( url = interaction.user.avatar )
            embed.add_field(name="Information",value=
                ":dollar: You have no enough money"
            ,inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed = discord.Embed(title="Transaction to " + member.name, description="", color = discord.Color.from_rgb(255, 219, 148) )
        embed.set_thumbnail( url = member.avatar )
        embed.add_field(name="Information",value=
            f":dollar: Transfered: {amount}$"
        ,inline=False)
       
        userData.money -= amount
        memberData.money += amount

        userData.save()
        memberData.save()

        await interaction.response.send_message(embed=embed)
