#############
## Imports ##
#############

import logging
import os

from discord.ext import commands
from discord.ext.commands.bot import when_mentioned_or
from dotenv import load_dotenv
from embeds.help import helpembed, rtfmhelp

#############
## Configs ##
#############

logging.basicConfig(level=logging.INFO)
bot = commands.Bot(command_prefix=when_mentioned_or(os.getenv("prefix")))
load_dotenv()
doc_links = {
    "pyc": "https://docs.pycord.dev/en/master",
    "nc": "https://nextcord.readthedocs.io/en/latest",
    "dpy": "https://discordpy.readthedocs.io/en/latest",
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


@bot.group(name="help")
async def help(ctx: commands.Context):
    await ctx.reply(embed=helpembed)


@help.command()
async def rtfm(ctx: commands.Context):
    await ctx.reply(embed=rtfmhelp)


#######################
## Startup Functions ##
#######################

bot.load_extension(name=".cog", package="bot")

bot.connect()
bot.start(os.getenv("token"))
