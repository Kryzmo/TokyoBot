from yt_dlp import YoutubeDL
from discord.ext import commands
import discord
from extensions.error_handler import Error

class Polecenia_Muzyczne(commands.Cog, name="Polecenia Muzyczne"):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'False'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.vc = ""

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item,
                                        download=False)['entries'][0]
            except Exception:
                return False
        info = ydl.sanitize_info(info)
        url = info['url']
        title = info['title']
        return {
            'title': title,
            'source': url
        }

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(aliases=['graj', 'pusc', 'p'], name="play", help="Puszcza wybraną piosenke z youtuba.")
    async def p(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Połącz się z kanałem głosowym aby aktywować bota.")
        else:
            try:
                song = self.search_yt(query)
            except Exception as e: Error(e)
            if type(song) == type(True):
                await ctx.send("Nie można pobrać piosenki spróbuj inną fraze bądź link.")
            else:
                await ctx.send("Piosenka dodana do kolejki.")
                self.music_queue.append([song, voice_channel])
                print(self.is_playing)
                if self.is_playing == False:
                    await self.play_music()

    @commands.command(aliases=['kolejka'], name="queue", help="Wyświetla aktualne piosenki w playliscie.")
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"
        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("Brak piosenek w kolejce")

    @commands.command(aliases=['pomin'], name="skip", help="Pomija aktualna piosenke w kolejce.")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()

            await self.play_music()
            
    @commands.command(aliases=['dc', 'rozlacz', 'stop', 'leave'], name="disconnect", help="Rozłącza bota z voicechatu.")
    async def dc(self, ctx):
        await self.vc.disconnect()

