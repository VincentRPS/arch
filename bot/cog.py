#############
## Imports ##
#############

import re

import disnake
import lavalink
import typing
from disnake.ext import commands

####################
## Lavalink Stuff ##
####################

url_composer = re.compile(r"https?://(?:www\.)?.+")


class LavalinkVoiceClient(disnake.VoiceClient):
    def __init__(self, client: disnake.Client, channel: disnake.abc.Connectable):
        self.client = client
        self.channel = channel
        if hasattr(self.client, "lavalink"):
            self.lavalink = self.client.lavalink
        else:
            self.client.lavalink = lavalink.Client(client.user.id)
            self.client.lavalink.add_node(  # you could want to change this.
                "lava.link", 80, "youshallnotpass", "singapore", "default-node"
            )
            self.lavalink = self.client.lavalink

    async def on_voice_server_update(self, data):
        lavalink_data = {"t": "VOICE_SERVER_UPDATE", "d": data}
        await self.lavalink.voice_update_handler(lavalink_data)

    async def on_voice_state_update(self, data):
        lavalink_data = {"t": "VOICE_STATE_UPDATE", "d": data}
        await self.lavalink.voice_update_handler(lavalink_data)

    async def connect(self, *, timeout: float, reconnect: bool) -> None:
        self.lavalink.player_manager.create(guild_id=self.channel.guild.id)
        await self.channel.guild.change_voice_state(channel=self.channel)

    async def disconnect(self, *, force: bool) -> None:
        player = self.lavalink.player_manager.get(self.channel.guild.id)

        if not force and not player.is_connected:
            return

        await self.channel.guild.change_voice_state(channel=None)

        player.channel_id = None
        self.cleanup()


#########
## Cog ##
#########


class CoreCog(commands.Cog):
    def __init__(self, bot): # Weird lavalink thingy?
        self.bot = bot
        self.client: disnake.Client()

        if not hasattr(
            bot, "lavalink"
        ):  # This ensures the client isn't overwritten during cog reloads.
            self.client.lavalink = lavalink.Client(self.client.user.id)
            self.client.lavalink.add_node(
                "lava.link", 80, "youshallnotpass", "singapore", "default-node"
            )  # Host, Port, Password, Region, Name

        lavalink.add_event_hook(self.track_hook)

    @commands.command(aliases=["doc", "docs", "rtfd"])
    async def rtfm(self, ctx: commands.Context):
        await ctx.reply("This feature is currenly in-progress.")

    ####################
    ## Music Commands ##
    ####################

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            guild = self.bot.get_guild(guild_id)
            await guild.voice_client.disconnect(force=True)

    @commands.command()
    async def play(self, ctx: commands.Context, *, search: str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = search.strip("<>")

        if not url_composer.match(query):
            query = f"ytsearch:{query}"

        results = await player.node.get_tracks(query)

        if not results or not results["tracks"]:
            return await ctx.reply("Couldn't find that track!")

        embed = disnake.Embed(color=disnake.Color.dark_theme())

        # Mostly inspired by the lavalink example.
        if results["loadType"] == "PLAYLIST_LOADED":
            tracks = results["tracks"]

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = "Playlist Enqueued!"
            embed.description = (
                f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
            )
        else:
            track = results["tracks"][0]
            embed.title = "Track Enqueued"
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'

            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        await ctx.reply(embed=embed)

        if not player.is_playing:
            await player.play()

    @commands.command()
    async def pause(self, ctx: commands.Context):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        await player.set_pause(True)

    @commands.command()
    async def unpause(self, ctx: commands.Context):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        await player.set_pause(False)

    @commands.command()
    async def stop(self, ctx: commands.Context):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            await ctx.reply("Not currently connected to a channel!")

        if not ctx.author.voice or (
            player.is_connected
            and ctx.author.voice.channel.id != int(player.channel_id)
        ):
            return await ctx.send("You're not in my voicechannel!")

        player.queue.clear()  # Clears the queue
        await player.stop()
        await ctx.voice_client.disconnect(force=True)  # Force disconnect
        await ctx.reply("Disconnected to the Voice Channel!")


###########
## SetUp ##
###########


def setup(bot):
    bot.add_cog(CoreCog(bot))
