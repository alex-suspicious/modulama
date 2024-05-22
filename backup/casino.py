from app.Models.user import user
import asyncio, random, discord

spin_numbers = [
    "https://i.imgur.com/EzcABfM.png",
    "https://i.imgur.com/l2es8uw.png",
    "https://i.imgur.com/9us1oKa.png",
    "https://i.imgur.com/VyEMPfL.png",
    "https://i.imgur.com/NLEX9eC.png",
    "https://i.imgur.com/WQoTiLC.png",
    "https://i.imgur.com/bWpm9sC.png",
    "https://i.imgur.com/BTgrMJ7.png",
    "https://i.imgur.com/IkoQ5uI.png"
]

class casino:
    @staticmethod
    async def spin(interaction: discord.Interaction, amount: int):
        userData = user().where( "discord_id",interaction.user.id, create=True ).first()
        if( userData.money - amount < 0 ):
            embed = discord.Embed(title="Transaction failed", description="", color = discord.Color.from_rgb(255, 219, 148) )
            embed.set_thumbnail( url = interaction.user.avatar )
            embed.add_field(name="Information",value=
                ":dollar: You have no enough money"
            ,inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)
            return


        userData.money -= amount
        userData.save()

        embed = discord.Embed(title=interaction.user.name + " spins a wheel", description="", color = discord.Color.from_rgb(255, 219, 148) )
        embed.set_image( url = "https://i.imgur.com/lWwjZOv.gif" )
        await interaction.response.send_message(embed=embed)
        await asyncio.sleep(4)
        

        random_number = random.randint(0,8)

        userData.money += int(amount*random_number)
        userData.save()

        embed = discord.Embed(title=interaction.user.name + " spins a wheel", description="", color = discord.Color.from_rgb(255, 219, 148) )
        embed.set_image(url=spin_numbers[random_number])
        embed.set_footer( text=f"{amount*random_number}$ was sent to you" )
        await interaction.edit_original_response(embed=embed)