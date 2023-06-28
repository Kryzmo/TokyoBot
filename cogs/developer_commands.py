from discord.ext import commands
from discord import Embed
from src.developer_functions import *
from json import load
from database_manager.manage_data import DatabaseManager
from preconditions.requireAdminOrMod import preconditionsRequireAdminOrMod, MissingAdminPermission
from extensions.error_handler import Error
from discord.utils import get
from typing import Optional
from discord import PartialEmoji
from re import sub, compile
ConfigRead = open('config.json')
ConfigLoad = load(ConfigRead)

class Developer_options(commands.Cog, name="Developer_options"):
    def __init__(self, bot, cur, connection):
        self.bot = bot
        self.prefix = f"{ConfigLoad['prefix']}dev "
        self.cur = cur
        self.connection = connection
        self.embed = Embed()
        self.db = DatabaseManager(cur, connection)
        self.admin_precondition = preconditionsRequireAdminOrMod(self.db)
        
    def replace_emojis(self, lst):
        emoji_pattern = compile(r'<:([a-zA-Z0-9_]+):\d+>')
        new_list = []
        for item in lst:
            if isinstance(item, str):
                new_list.append(sub(emoji_pattern, r'\1', item))
            else:
                new_list.append(item)
        return new_list
    
    async def cog_check(self, ctx):
        try:
            return ctx.prefix == self.prefix
        except Exception as e: Error(e)
    
    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['show config'], help='Pokazuje aktualną konfiguracje bota.')
    async def show_config(self, ctx: commands.Context):
            r = self.db.getConfigRows()
            user = r"{user}"
            try:
                self.embed.title = "Lista Poleceń - Administracja"
                self.embed.description = f"""
**prefix**
{ConfigLoad['prefix']}

**Trigram similarity**
{f"{r[15]}" if r[15] != None else ''}

**Channels**
modlog - {f"<#{r[1]}>" if r[1] != None else ''}
arts - {f"<#{r[3]}>" if r[3] != None else ''}
deletedMessages - {f"<#{r[9]}>" if r[9] != None else ''}
userlogs - {f"<#{r[10]}>" if r[10] != None else ''}
recrutation - {f"<#{r[4]}>" if r[4] != None else ''}
commands - {f"<#{r[2]}>" if r[2] != None else ''} 
joinLeaveChannel - {f"<#{r[11]}>" if r[11] != None else ''} 
reminders - {f"<#{r[14]}>" if r[14] != None else ''} 

**Roles**
mod - {f"<@&{r[8]}>" if r[8] != None else ''} 
recrutation - {f"<@&{r[5]}>" if r[5] != None else ''}
recrutationCommonRole - {f"<@&{r[6]}>" if r[6] != None else ''} 

**Messages**
welcome - {f"`{r[12]}`" if r[12] != None else ''}
farewell - {f"`{r[13]}`" if r[13] != None else ''}
recrutation - {f"`{r[7]}`" if r[7] != None else ''}
                """
                await ctx.reply(embed=self.embed)
            except Exception as e: Error(e)

    @commands.has_permissions(administrator=True)
    @commands.command(help="Ustawia trigram similarity od 1.0 do 0.1. Im mniej tym większa dokładność.")
    async def set_similarity(self, ctx: commands.Context, similarity: float):
        try:
            self.db.setVar("trigram_similarity", float(similarity))
            await ctx.reply(f"Pomyślnie ustawiono similarity na {similarity}")
        except Exception as e: Error(e)

    @commands.has_permissions(administrator=True)
    @commands.command(help="Updatuje / Restartuje bota.")
    async def update(self, ctx: commands.Context):
        try:
            embed = Embed()
            embed.title = "Tokyo"
            embed.description = "Następuje update albo naprawa..."
            embed.set_footer(text="Ciekawe czy jukis cos popsul...")
            x = open("updateNow", "x")
            await ctx.reply(embed=embed)
        except Exception as e: Error(e)
    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['set channel'], help='Polecenie do konfiguracji kanałów.', description="Opcje argumentu <channel_type>:\nmodlog, arts, deleted_messages, user_data, recrutation, commands, joinleavechannel, reminder")
    async def set_channel(self, ctx: commands.Context, channel_type: str, id):
            options = ['modlog', 'arts', 'deleted_messages', 'user_data', 'recrutation', 'commands', 'joinleavechannel', 'reminder']
            options_dict = {
                 "modlog": "modlog_channel_id",
                 "arts": "arts_channel_id",
                 "deleted_messages": "deleted_messages_channel_id",
                 "user_data": "edited_messages_channel_id",
                 "recrutation": "recrutation_category_id",
                 "commands": "commands_channel_id",
                 "joinleavechannel": "welcome_channel_id ",
                 "reminder": "reminders_channel"
            }
            channel_type = channel_type.lower()
            if channel_type in options:
                self.db.setVar(f"{options_dict[f'{channel_type}']}", int(id))
                await ctx.reply(f"Kanał {channel_type} został ustawiony na <#{id}>")

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['set role'], help='Polecenie do konfiguracji roli.', description="Opcje argumentu <role_type>:\nmod, recrutation, recrutation_common_role")
    async def set_role(self, ctx: commands.Context, role_type: str, id):
            options = ['mod', 'recrutation', 'recrutation_common_role']
            options_dict = {
                 "mod": "mod_role_id",
                 "recrutation": "recrutation_role_id",
                 "recrutation_common_role": "recrutation_common_role_id"
            }
            role_type = role_type.lower()
            if role_type in options:
                self.db.setVar(f"{options_dict[f'{role_type}']}", int(id))
                await ctx.reply(f"Rola {role_type} została ustawiona na <@&{id}>")

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['set message'], help='Polecenie do konfiguracji wiadomości. Wstaw \{user\} w miejscu gdzie ma być uznany użytkownik.', description="Opcje argumentu <message_type>:\nwelcome, farewell, recrutation")
    async def set_message(self, ctx: commands.Context, message_type: str, *message):
            print(message)
            user = r"{user}"
            options = ['welcome', 'farewell', 'recrutation']
            options_dict = {
                 "welcome": "welcome_message",
                 "farewell": "farewell_message ",
                 "recrutation": "recrutation_message"
            }
            message_type = message_type.lower()
            msg = ' '.join(message)
            if message_type in options:
                self.db.setVar(f"{options_dict[f'{message_type}']}", msg)
                await ctx.reply(f"Wiadomość `{message_type}` została ustawiona na \"{msg}\"")

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['add emote'], help='Dodaje nową serię do funkcji rang na emotkach', description="")
    async def add_emote(self, ctx: commands.Context, message_id, emoji, role_id, category_name):
        emoji = PartialEmoji(name=emoji)
        if message_id == None or emoji == None or role_id == None:
            await ctx.reply(f"Poprawne uzycie: add_emote <id_wiadomosci_z_emotkami> <nazwa_emotki> <id_rangi> <nazwa_kategorii>!")
            return
        try:
            self.db.addEmoji(message_id, emoji, role_id, category_name)
            await ctx.reply(f"Seria dodana pomyślnie!")
        except Exception as e:
            Error(e)
    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['remove emote'], help='Usuwa serię z funkcji rang na emotkach', description="")
    async def remove_emote(self, ctx: commands.Context, emoji):
        if emoji == None:
            await ctx.reply(f"Poprawne uzycie: remove_emoji <nazwa_emotki>")
            return
        try:
            self.db.removeEmoji(emoji)
            await ctx.reply(f"Seria usunięta pomyślnie!")
        except Exception as e:
            Error(e)

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['show emotes'], help='Wyświetla wszystkie autorole w bazie danych', description="")
    async def show_emotes(self, ctx: commands.Context):
            rows = self.db.getEmotesData()
            
            if rows == None:
                await ctx.reply(f"Brak autoról w bazie danych!")
                return
            try:
                self.embed.title = f"Lista autoról"
                self.embed.description = f"""
**Emoji** - **Rola** - **Kategoria**
                """
                for r in rows:
                    #print("Emote: {} is {}".format(r[1], f"{r[1]}".isascii()))
                    if f"{r[1]}".isascii() is True:
                        emoji = get(ctx.message.guild.emojis, name=f"{r[1]}")
                    elif f"{r[1]}".isascii() is False:
                        emoji = f"{r[1]}"
                    self.embed.description += f"""
{f"{emoji}"} - {f"<@&{r[3]}>" if r[2] != None else ''} - {f"{r[4]}" if r[4] != None else ''}
                    """
                await ctx.reply(embed=self.embed)
            except Exception as e:
                Error(e)
    
    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['add multiple emoji'], help='Dodaje wiadomość z reakcjami.', description="", usage="<header> <description> <--emotki emoji1 emoji2 emoji3 --role role1 role2 role3 --kategoria kategoria>")
    async def add_multiple_emoji(self, ctx: commands.Context, header: str, description: str, *emoji_and_roles):
        try:
            x = list(emoji_and_roles)
            x.index('--role')
            x.index('--emotki')
            x.index('--kategoria')
            emojis = x[x.index('--emotki')+1:x.index('--role')]
            roles = x[x.index('--role')+1:x.index('--kategoria')]
            category = x[x.index('--kategoria')+1:]
            desc = f"{description}".replace("_", " ").replace("\\n", "\n")
            self.embed.title = ""
            self.embed.description = f"""
{desc}
            """
            
            _emoji = self.replace_emojis(emojis)
            for i in range(len(_emoji)):
                __emoji = PartialEmoji(name=_emoji[i])
                if f"{__emoji}".isascii() is True:
                    _emojis = get(ctx.message.guild.emojis, name=f"{__emoji}")
                elif f"{__emoji}".isascii() is False:
                    _emojis = __emoji
                self.embed.description += f"""
{f"{_emojis}"} - {f"<@&{roles[i]}>" if roles[i] != None else ''} 
                """
            self.embed.title = f"{header}".replace("_", " ")
            self.embed.set_footer(text="Autorole", icon_url = f"{self.bot.user.avatar.url}")
            msg = await ctx.send(embed=self.embed)
            self.embed = Embed()
            for em in _emoji:
                try:
                    __emoji = PartialEmoji(name=em)
                    if f"{__emoji}".isascii() is True:
                        emoji = get(ctx.message.guild.emojis, name=f"{em}")
                    elif f"{__emoji}".isascii() is False:
                        emoji = __emoji
                    await msg.add_reaction(emoji)
                except Exception as e:
                    print('')
                    Error(e)
            for i in range(len(_emoji)):
                __emoji = PartialEmoji(name=_emoji[i])
                self.db.addEmoji(msg.id, __emoji, roles[i], category[0])
        except Exception as e: 
            Error(e)
            await ctx.reply("Error!")
    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['delete multiple emoji'], help='Usuwa autorole z kategorią.', description="", usage="<nazwa_kategorii>")
    async def delete_multiple_emoji(self, ctx: commands.Context, category_name):
        try:
            self.db.deleteEmojisByCategory(category_name)
            await ctx.reply(f"Usunięto wszystkie autorole z kategorii {category_name}!")
        except Exception as e:
            Error(e)
            await ctx.reply("Error!")
    @commands.has_permissions(administrator=True)
    @commands.command(aliases=['pomoc'], help='Pomoc konfiguracji.')
    async def h(self, ctx: commands.Context, command: Optional[str] = None):
        try:
            if not command:
                help_embed = Embed(title="Lista poleceń:", description="", color=0x00FFFF)
                help_embed.set_footer(text=f"Aby wyświetlić sposób użycia {ConfigLoad['prefix']}dev <polecenie>.")
                for command in self.get_commands():
                    if not command.hidden:
                        help_embed.description += f"`{self.prefix}{command.name}`: {command.help}\n"
                await ctx.send(embed=help_embed)
            else:
                if hasattr(self, command):
                    method = getattr(self, command)
                    self.embed.title = f"Pomoc - {command}"
                    message = f"{method.help}"
                    if method.description:
                        message += f"\n\n{method.description}"
                    self.embed.description = message
                    self.embed.add_field(name="Sposób użycia:", value=f"`{self.prefix}{command} {method.signature}`", inline=False)
                    if isinstance(method, commands.Group):
                        subcommands = [subcommand for subcommand in method.commands]
                        subcommands_description = "\n".join([f"{subcommand.name}: {subcommand.help}" for subcommand in subcommands])
                        self.embed.add_field(name="Dostępne podkomendy:", value=subcommands_description, inline=False)
                    await ctx.reply(embed=self.embed)
                    self.embed = Embed()
                else:
                    await ctx.reply("Podana komenda nie istnieje.")
        except Exception as e: Error(e)