from discord.ext import commands
import requests
import discord
from extensions.channelsManager import channelManager
from preconditions.requireAdminOrMod import preconditionsRequireAdminOrMod
from preconditions.requireChannelOrCategory import preconditionsRequireChannelOrCategory
from typing import Optional
from extensions.error_handler import Error

discordapibaseurl = 'https://discord.com/api'


class Polecenia_uzytkownika(commands.Cog, name="Polecenia użytkownika"):
    def __init__(self, bot: commands.Bot, permissionAdminMod: preconditionsRequireAdminOrMod, permissionChannelCategory: preconditionsRequireChannelOrCategory, channel_manager: channelManager, token):
        self.bot = bot
        global _permissionAdminMod
        _permissionAdminMod = permissionAdminMod
        self.permissionAdminMod = permissionAdminMod
        global _permissionChannelCategory
        _permissionChannelCategory = permissionChannelCategory
        self.permissionChannelCategory = permissionChannelCategory
        global _channel_manager
        _channel_manager = channel_manager
        self.channel_manager = channel_manager
        self.token = token

    def get_content_type(self, url):
        return requests.head(url).headers['Content-Type']
    
    def shorten_list(self, lst: list):
        try:
            total_length = sum(len(x) for x in lst)
            if total_length <= 1024 - len(lst):
                return lst
            else:
                for i in range(len(lst)-1, -1, -1):
                    total_length -= len(lst[i])
                    del lst[i]
                    if total_length <= 1024 - len(lst):
                        break
                return lst
        except Exception as e: Error(e)

    def is_channel_or_mod():
        async def predicate(ctx: commands.Context):
            if _permissionAdminMod.requireAdminOrMod(ctx.author) is True or _permissionChannelCategory.requireCommandsChannel(ctx.channel.id) is True:
                return True
            else:
                embed = discord.Embed(
                    title="Tokyo",
                    description=f"Poleceń używamy na kanale <#{_channel_manager.commandsChannel()}>!",
                    color=discord.Color.red()
                )
                # await ctx.send(embed=embed)
                embed.set_footer(text=f"{ctx.bot.user.name}", icon_url=str(ctx.bot.user.avatar.url))
                await ctx.reply(embed=embed)
                return False
        return commands.check(predicate)

    @is_channel_or_mod()
    @commands.command(help='Wyświetla opóźnienie.')
    async def ping(self, ctx: commands.Context):
        await ctx.reply(f"Ping {round(self.bot.latency * 1000)}ms")

    @is_channel_or_mod()
    @commands.command(aliases=['profilowe'], help="Pokazuje avatar wybranego użytkownika.")
    async def avatar(self, ctx: commands.Context, member = None):
        try:
            if member is not None:
                member_id = ""
                for char in member:
                    if char.isdigit():
                        member_id += char    
            else:
                member_id = ctx.author.id
            user = requests.get('{}/users/{}'.format(discordapibaseurl, member_id), headers={'Authorization': f'Bot {self.token}'}).json()
            if ("avatar" in user):
                avatar = 'https://cdn.discordapp.com/avatars/{}/{}'.format(member_id, user["avatar"])
                if "gif" in f"{self.get_content_type(avatar)}":
                    avatar += ".gif?size=1024"
                else:
                    avatar += "?size=1024"
                embed = discord.Embed(title=user['username'])
                embed.set_author(name="Avatar")
                embed.set_image(url=avatar)
                embed.set_footer(text = f"{self.bot.user.name}", icon_url = f"{self.bot.user.avatar.url}")
                await ctx.reply(embed=embed)
            else:
                await ctx.reply("Wystąpił błąd.")
        except Exception as e: Error(e)

    @is_channel_or_mod()
    @commands.command(aliases=['informacje'], help='Pokazuje informacje o serverze oraz bocie.')
    async def serverinfo(self, ctx: commands.Context):
        try:
            embed = discord.Embed(title=f"{ctx.guild.name}", description="Informacje o serwerze", timestamp=ctx.message.created_at, color=discord.Color.blue())
            embed.set_thumbnail(url=f"{ctx.guild.icon.url}")
            embed.add_field(name="Właściciel serwera:", value=f"{ctx.guild.owner}", inline=True)
            embed.add_field(name="Liczba członków:", value=f"{ctx.guild.member_count}", inline=True)
            embed.add_field(name="Liczba botów:", value=f"{len([m for m in ctx.guild.members if m.bot])}", inline=True)
            embed.add_field(name="Role twórców bota:", value="yuukis#2050", inline=True)
            embed.add_field(name="Wersja:", value="1.0.9", inline=True)
            embed.add_field(name="Role", value=" ".join(self.shorten_list(list(reversed([r.mention for r in ctx.guild.roles])))), inline=False)
            embed.set_footer(text="TokyoSubs", icon_url=self.bot.user.avatar.url)
            await ctx.send(embed=embed)
        except Exception as e: Error(e)

    @commands.command(aliases=['obrazek'], help='Daje ładne obrazki. Użyj po prostu `!art` bądź któreś z tagiem przykład `!art waifu`. Dostępne tagi:\n- uniform\n- maid\n- waifu\n- marin-kitagawa\n- mori-calliope\n- raiden-shogun\n- selfies')
    async def art(self, ctx: commands.Context, tag: Optional[str]):
        try:
            if self.permissionAdminMod.requireAdminOrMod(ctx.author) is True or self.permissionChannelCategory.requireArtChannel(ctx.channel.id) is True:
                existing_list = ['uniform', 'maid', 'waifu', 'marin-kitagawa', 'mori-calliope', 'raiden-shogun', 'oppai', 'selfies', 'ass', 'hentai', 'milf', 'oral', 'paizuri', 'ecchi', 'ero', 'deamovsky', None]
                if tag in existing_list or None:
                    if tag == None:
                        url = 'https://api.waifu.im/search/?included_tags=waifu'
                    else:
                        url = 'https://api.waifu.im/search/?included_tags={}'.format(tag)
                    r = requests.get(url)
                    r_js = r.json()
                    forbbiden_list = ['ass', 'hentai', 'milf', 'oral', 'paizuri', 'ecchi', 'ero', 'deamovsky']
                    # forbbiden_list = ['deamovsky']
                    if tag in forbbiden_list:
                        embed = discord.Embed(title='Hentai!')
                        embed.set_image(url='https://c.tenor.com/t2pLAIENp_EAAAAC/anime-kanna.gif')
                        embed.set_footer(text = f"{self.bot.user.name}", icon_url = f"{self.bot.user.avatar.url}")
                        await ctx.reply(embed=embed)
                    else:
                        for i in r_js['images']:
                            embed_color = '{}'.format(i['dominant_color']).replace('#', '')
                            embed_color_decimal = int(embed_color, 16)
                            embed = discord.Embed(title='Obrazek', color=embed_color_decimal)
                            embed.set_image(url='{}'.format(i['url']))
                            embed.set_footer(text = f"{self.bot.user.name}", icon_url = f"{self.bot.user.avatar.url}")
                            await ctx.reply(embed=embed)
                else:
                    await ctx.reply('Nie posiadam takiego tagu!')
            else:
                await ctx.reply('Polecenie można wykonać tylko na kanale arty!')
        except Exception as e: Error(e)