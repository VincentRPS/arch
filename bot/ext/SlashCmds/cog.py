#############
## Imports ##
#############

import disnake
from disnake.ext import commands

from ...embeds.help import helpembed, rtfmhelp

#########
## Cog ##
#########


class CoreSlashCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def help(self, inter: disnake.AppCmdInter):
        """Get help on a certain command!"""
        await inter.send(embed=helpembed)

    @help.sub_command()
    async def rtfm(self, inter: disnake.AppCmdInter):
        """Help on the RTFM Command."""
        await inter.send(embed=rtfmhelp)

    @commands.slash_command()
    async def rtfm(self, inter: disnake.AppCmdInter):
        """Brings you a rtfm result from a readthedocs link."""
        await inter.send("This feature is currenly in-progress.")


###########
## SetUp ##
###########


def setup(bot):
    bot.add_cog(CoreSlashCog(bot))
