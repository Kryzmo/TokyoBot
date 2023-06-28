from discord.ext import commands
import re
from preconditions.requireAdminOrMod import preconditionsRequireAdminOrMod
from preconditions.requireChannelOrCategory import preconditionsRequireChannelOrCategory
from extensions.channelsManager import channelManager
from extensions.messagesManager import messagesManager
from extensions.rolesManager import rolesManager
import discord
from extensions.error_handler import Error
from src.views import SimpleView
import datetime
import requests



class Polecenia_administracji(commands.Cog, name="Polecenia Administracji"):
    def __init__(self, bot: commands.Bot, 
                            permissionAdminMod: preconditionsRequireAdminOrMod,
                            permissionChannelCategory: preconditionsRequireChannelOrCategory,
                            channel_manager: channelManager,
                            messages_manager: messagesManager,
                            role_manager: rolesManager,
                            connection,
                            cur
                            ):
        
        self.bot = bot
        global _permissionAdminMod
        _permissionAdminMod = permissionAdminMod
        self.permissionChannelCategory = permissionChannelCategory
        self.channel_manager = channel_manager
        self.messages_manager = messages_manager
        self.role_manager = role_manager
        self.connection = connection
        self.cur = cur
    
    def extract_anime_names(self, url_list):
        anime_names = []
        for url in url_list:
            match = re.search(r'/anime/\d+/(.*)', url)
            if match:
                anime_name = match.group(1).replace('_', ' ')
                anime_names.append(anime_name)
        return anime_names

    def has_mod_role():
        async def predicate(ctx: commands.Context):
            if _permissionAdminMod.requireAdminOrMod(ctx.author):
                return True
            else:
                embed = discord.Embed(
                    title="Tokyo",
                    description="You have no power here!",
                    color=discord.Color.red()
                )
                embed.set_image(url="https://i.imgur.com/GmsawV4.gif")
                embed.set_footer(text=f"{ctx.bot.user.name}", icon_url=str(ctx.bot.user.avatar.url))
                await ctx.reply(embed=embed)
                return False
        return commands.check(predicate)
    
    @has_mod_role()
    @commands.command(aliases=['rekrutacja'], help='Wysyla wiadomość rekrutacyjną.')
    async def recrutation(self, ctx: commands.Context, *description):
        description = ' '.join(description).replace("\\n", "\n");print(description)
        try:
            if not ctx.author.bot:
                view = SimpleView(self.bot, self.channel_manager, self.messages_manager, self.role_manager)
                embed = discord.Embed()
                embed.description = "{}".format(description)
                await ctx.send(embed=embed, view=view)
        except Exception as e:
            Error(e)

    @has_mod_role()
    @commands.command(aliases=['dodaj_wulgaryzm'], help='Dodaje wulgaryzm do listy zabronionych.')
    async def vulg_add(self, ctx: commands.Context, vulg: str):
        self.messages_manager.vulgMessageAdd(vulg)
        await ctx.reply("Wulgaryzm został pomyślnie dodany.")

    @has_mod_role()
    @commands.command(aliases=['usun_wulgaryzm'], help='Usuwa wulgaryzm z listy zabronionych.')
    async def vulg_remove(self, ctx: commands.Context, vulg: str):
        self.messages_manager.vulgMessageRemove(vulg)
        await ctx.reply("Wulgaryzm został pomyślnie usunięty.")

    @has_mod_role()
    @commands.command(aliases=['pokaz_wulgaryzmy'], help='Wyświetla liste zabronionych wulgaryzmów')
    async def vulg_list(self, ctx: commands.Context):
        x = self.messages_manager.vulgMessageList()
        embed = discord.Embed(title="Lista Wulgaryzmów.", description=f"{x}")
        embed.set_footer(text = f"{self.bot.user.name}", icon_url = f"{self.bot.user.avatar.url}")
        await ctx.reply(embed=embed)

    # MUTE COMMAND #
    @has_mod_role()
    @commands.command(aliases=['wycisz', 'shutup', 'stfu'], help='Wycisza użytkownika.')
    async def mute(self, ctx: commands.Context, member = None, until = None, *, reason = None):
            try:
                if int(until) <= 40320:
                    if reason is not None:
                        member_id = re.findall("[0-9]", member)
                        if "{}".format(member_id) == "{}".format(433691890416877580):
                            member_id = ctx.author.id
                        else:
                            member_id = member_id
                        # print(int(''.join(member_id)))
                        
                        guild = await self.bot.fetch_guild(ctx.guild.id)
                        user = await guild.fetch_member(int(''.join(member_id)))
                        user_mod = await guild.fetch_member(ctx.author.id)
                        handshake = await self.timeout_user(user_id=int(''.join(member_id)), guild_id=ctx.guild.id, until=int(until), reason_mute=reason)
                        if handshake:
                            modlog = self.bot.get_channel(self.channel_manager.modLog())
                            embed = discord.Embed(title=f'**{user}**', color=16249435, description=f"**Powód**\n{reason}")
                            embed.add_field(name='User ID:', value=int(''.join(member_id)), inline=True)
                            embed.add_field(name='Mod ID:', value=ctx.author.id, inline=True)
                            embed.add_field(name='Czas trwania:', value=f"{until} min.", inline=True)
                            embed.add_field(name='Kiedy:', value=datetime.datetime.now())
                            embed.add_field(name='Typ:', value='Mute', inline=True)
                            embed.set_footer(text = f'Przez: {user_mod}', icon_url = f"{self.bot.user.avatar.url}")
                            await modlog.send(embed=embed)
                            return await ctx.send(f"Wyciszono {member} na {until} minut. Z powodu \"{reason}\"")
                        await ctx.send("Coś poszło nie tak.")
                    else:
                        await ctx.reply("Musisz podać powód!")
                else:
                    await ctx.send("Za duża wartość!")

            except Exception as e:
                Error(e)
                print(member)
                await ctx.send("Podano złego użytkownika bądz czas.")

    @has_mod_role()
    @commands.command(aliases=['odcisz'], help='Odcisza użytkownika.')
    async def unmute(self, ctx: commands.Context, member = None, *, reason = None):
            try:
                if reason is not None:
                    member_id = re.findall("[0-9]", member)
                    # print(int(''.join(member_id)))
                    guild = await self.bot.fetch_guild(ctx.guild.id)
                    user = await guild.fetch_member(int(''.join(member_id)))
                    user_mod = await guild.fetch_member(ctx.author.id)
                    handshake = await self.timeout_user(user_id=int(''.join(member_id)), guild_id=ctx.guild.id, until=None, reason_mute=reason)
                    if handshake:
                        modlog = self.bot.get_channel(self.channel_manager.modLog())
                        embed = discord.Embed(title=f'**{user}**', color=3145631, description=f"**Powód**\n{reason}")
                        embed.add_field(name='User ID:', value=int(''.join(member_id)), inline=True)
                        embed.add_field(name='Mod ID:', value=ctx.author.id, inline=True)
                        embed.add_field(name='Kiedy:', value=datetime.datetime.now())
                        embed.add_field(name='Typ:', value='Unmute', inline=True)
                        embed.set_footer(text = f'Przez: {user_mod}', icon_url = f"{self.bot.user.avatar.url}")
                        await modlog.send(embed=embed)
                        return await ctx.send(f"Odciszono {member}. Z powodu \"{reason}\"")
                    await ctx.send("Coś poszło nie tak.")
                else:
                    await ctx.reply("Musisz podać powód!")
            except Exception as e:
                Error(e)
                # print(member)
                await ctx.send("Podano złego użytkownika.")

    # BAN COMMAND #
    @has_mod_role()
    @commands.command(aliases=['zbanuj', 'usun'], help='Banuje użytkownika.')
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason = None):
        try:
            if reason is not None:
                guild = await self.bot.fetch_guild(ctx.guild.id)
                user = await guild.fetch_member(member.id)
                user_mod = await guild.fetch_member(ctx.author.id)
                modlog = self.bot.get_channel(self.channel_manager.modLog())
                embed = discord.Embed(title=f'**{user}**', color=16711680, description=f"**Powód**\n{reason}")
                embed.add_field(name='User ID:', value=member.id, inline=True)
                embed.add_field(name='Mod ID:', value=ctx.author.id, inline=True)
                embed.add_field(name='Kiedy:', value=datetime.datetime.now())
                embed.add_field(name='Typ:', value='Ban', inline=True)
                embed.set_footer(text = f'Przez: {user_mod}', icon_url = f"{self.bot.user.avatar.url}")
                await modlog.send(embed=embed)
                await member.ban(reason = reason)
                return await ctx.send(f'Użytkownik {member} został zbanowany!')
            else:
                await ctx.send('Nie podano powodu!')
        except:
            await ctx.send('Nie znaleziono użytkownika.')

    @has_mod_role()
    @commands.command(aliases=['odbanuj', 'przywroc'], help='Odbanowywuje użytkownika.')
    async def unban(self, ctx: commands.Context, id: int, *, reason = None):
        if reason is not None:
            print(id)
            user = await self.bot.fetch_user(id)
            guild = await self.bot.fetch_guild(ctx.guild.id)
            user_mod = await guild.fetch_member(ctx.author.id)
            modlog = self.bot.get_channel(self.channel_manager.modLog())
            embed = discord.Embed(title=f'**{user}**', color=255, description=f"**Powód**\n{reason}")
            embed.add_field(name='User ID:', value=id, inline=True)
            embed.add_field(name='Mod ID:', value=ctx.author.id, inline=True)
            embed.add_field(name='Kiedy:', value=datetime.datetime.now())
            embed.add_field(name='Typ:', value='Unban', inline=True)
            embed.set_footer(text = f'Przez: {user_mod}', icon_url = f"{self.bot.user.avatar.url}")
            await modlog.send(embed=embed)
            await ctx.reply('Użytkownik został odbanowany!')
            await ctx.guild.unban(user)
        else:
            await ctx.send('Nie podano powodu!')

    # KICK COMMAND ##
    @has_mod_role()
    @commands.command(aliases=['wyrzuc'], help='Wyrzuca użytkownika.')
    async def kick(self, ctx: commands.Context, member :discord.Member, *, reason=None):
        if reason is not None:
            guild = await self.bot.fetch_guild(ctx.guild.id)
            user = await guild.fetch_member(member.id)
            user_mod = await guild.fetch_member(ctx.author.id)
            modlog = self.bot.get_channel(self.channel_manager.modLog())
            embed = discord.Embed(title=f'**{user}**', color=14001047, description=f"**Powód**\n{reason}")
            embed.add_field(name='User ID:', value=member.id, inline=True)
            embed.add_field(name='Mod ID:', value=ctx.author.id, inline=True)
            embed.add_field(name='Kiedy:', value=datetime.datetime.now())
            embed.add_field(name='Typ:', value='Kick', inline=True)
            embed.set_footer(text = f'Przez: {user_mod}', icon_url = f"{self.bot.user.avatar.url}")
            await modlog.send(embed=embed)
            await ctx.send(f"{member} został wyrzucony z powodu: \"{reason}\"")
            await member.kick(reason=reason)
        else:
            await ctx.send("Nie podano powodu!")

    @has_mod_role()
    @commands.command(aliases=['purge'], help='Usuwa dana ilosc wiadomosci.')
    async def clear(self, ctx: commands.Context, amount):
        amount = int(amount)
        if amount != "":
            if amount > 50:
                await ctx.reply('Nie można usunąć więcej niż 50!')
            else:
                await ctx.channel.purge(limit=amount + 1)
        else:
            await ctx.reply('Nie podano ilości!')

    @has_mod_role()
    @commands.command(aliases=['series'], help='Dodaje informacje do funkcji przypomnienia o odcinkach.')
    async def add_series(self, ctx: commands.Context, user_id, link):
        if "https://myanimelist.net/" in f"{link}" and user_id != "":
            get_id = re.findall('\d+', link)
            anime_id = get_id[0]
            api_url = 'https://api.jikan.moe/v4/anime/{}'.format(anime_id)
            headers = { 
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.117', 
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
            'Accept-Language' : 'en-US,en;q=0.5', 
            'Accept-Encoding' : 'gzip', 
            'DNT' : '1',
            'Connection' : 'close' }
            r = requests.get(api_url, headers=headers)
            r_json = r.json()
            date_from = r_json['data']['aired']['from']
            date_to = r_json['data']['aired']['to']
            time_broadcast = r_json['data']['broadcast']['time']
            try:
                if date_to:
                    self.cur.execute('insert into notification_manager (user_id, url, date_from, date_to, new_episode_time) values (%s, %s, %s, %s, %s)', (user_id, link, date_from, date_to, time_broadcast))
                else:
                    self.cur.execute('insert into notification_manager (user_id, url, date_from, new_episode_time) values (%s, %s, %s, %s)', (user_id, link, date_from, time_broadcast))
                self.connection.commit()
                await ctx.reply("Pomyślnie dodano!")
            except Exception as e:
                await ctx.reply("Wystąpił błąd pytaj jukajki")
                Error(e)
        else:
            await ctx.reply("Podane dane są nieprawidłowe")

    @has_mod_role()
    @commands.command(aliases=['pokaz_serie'], help='Pokazuje baze danych serii.')
    async def get_series(self, ctx: commands.Context):
            try:
                self.cur.execute('select id, user_id, url, date_from, date_to, new_episode_time from notification_manager')
                rows = self.cur.fetchall()
                import pandas as pd
                ids = []
                usr = []
                url = []
                date_fr = []
                date_t = []
                ep_time = []
                for r in rows:
                    print(rows)
                    ids.append(r[0])
                    usr.append(r[1])
                    url.append(r[2])
                    date_fr.append(r[3])
                    date_t.append(r[4])
                    ep_time.append(r[5])
                    # print(f'user_id: {r[0]} url: {r[1]} date_from: {r[2]} date_to: {r[3]} new_episode_time: {r[4]}')
                df = pd.DataFrame({'id': ids,'user_id': usr,'url': self.extract_anime_names(url), 'date_from': date_fr, 'date_to': date_t, 'japan_time': ep_time})
                df.sort_values(by=['id'], inplace=True)
                df.set_index('id', inplace=True, drop=True)
                df = df.rename_axis(None)
                print(df)
                await ctx.send("""```{}```""".format(df))
            except Exception as e:
                Error(e)
    @has_mod_role()
    @commands.command(aliases=['usun_serie'], help='Usuwa serie z bazy danych.')
    async def delete_series(self, ctx: commands.Context, series_id):
        print(series_id)
        try:
            print(type(series_id))
            series_id = "{}".format(series_id)
            self.cur.execute('delete from notification_manager where id=%s;', (series_id,))
            self.connection.commit()
            await ctx.reply("Pomyslnie usunieto element.")
        except Exception as e:Error(e)
    # doesnt have permission

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            # await ctx.reply("Nie masz wymaganych uprawnień do wykonania tej komendy.")
            # Create embed for "You have no power here" meme
            embed = discord.Embed(
                title="Tokyo",
                description="You have no power here!",
                color=discord.Color.red()
            )
            embed.set_image(url="https://i.imgur.com/GmsawV4.gif")
            await ctx.send(embed=embed)