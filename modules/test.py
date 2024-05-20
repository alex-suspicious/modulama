import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @cog_ext.cog_slash(name="hello", description="Say hello!")
    async def hello(self, ctx: SlashContext):
        await ctx.send('Hello, World!')

async def setup(bot):
    await bot.add_cog(test(bot))
