#############
## Imports ##
#############

import logging
import os

from disnake.ext import commands
from disnake.ext.commands.bot import when_mentioned_or
from dotenv import load_dotenv
from embeds.help import helpembed, rtfmhelp

#############
## Configs ##
#############

logging.basicConfig(level=logging.DEBUG)
bot = commands.Bot(command_prefix=when_mentioned_or("ch "))
bot.remove_command("help")
load_dotenv()
doc_links = {
    "pyc": "https://docs.pycord.dev/en/master",
    "nc": "https://nextcord.readthedocs.io/en/latest",
    "dpy": "https://discordpy.readthedocs.io/en/latest",
    "disnake": "https://docs.disnake.dev/en/latest",
    "gd": "https://docs.godotengine.org/en/stable/",
}

##########################
## Events And Listeners ##
##########################


@bot.event
async def on_ready():
    logging.info("Ready!")


########################
## Help Command Group ##
########################


@bot.group(name="help", invoke_without_command=True)
async def help(ctx: commands.Context):
    await ctx.reply(embed=helpembed)


@help.command()
async def rtfm(ctx: commands.Context):
    await ctx.reply(embed=rtfmhelp)

#######################
## Startup Functions ##
#######################

bot.load_extension(name=".cog", package="bot")
bot.load_extension(name=".ext.SlashCmds.cog", package="bot")

bot.run(os.getenv("token"))
