#############
## Imports ##
#############

import disnake

helpembed = disnake.Embed(
    title="The Help Menu",
    description="The Place to get help!",
    color=disnake.Color.dark_theme(),
)
helpembed.add_field(
    name="Categorys", value="to get help just do `ch help <command>` to get help!"
)
rtfmhelp = disnake.Embed(title="rtfm", color=disnake.Color.dark_theme())
rtfmhelp.add_field(
    name="What does this do?", value="Brings you a rtfm result from a readthedocs link."
)
