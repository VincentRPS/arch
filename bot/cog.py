#############
## Imports ##
#############

from discord.ext import commands

#########
## Cog ##
#########


class CoreCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["doc", "docs", "rtfd"])
    async def rtfm(self, ctx: commands.Context):
        await ctx.reply("This feature is currenly in-progress.")


###########
## SetUp ##
###########


def setup(bot):
    bot.add_cog(CoreCog(bot))
