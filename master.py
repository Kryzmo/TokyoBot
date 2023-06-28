# coding=utf8
import discord
import json
import asyncio
import aiohttp
from discord.ext import commands
import warnings
import psycopg2
from src.listeners import ListenerCog
from src.views import SimpleView
from src.loop_tasks import check_series
from cogs.developer_commands import Developer_options
from cogs.music_commands import Polecenia_Muzyczne
from cogs.user_commands import Polecenia_uzytkownika
from cogs.administration_commands import Polecenia_administracji 
from database_manager.tables import createTables
from database_manager.manage_data import DatabaseManager
from preconditions.requireAdminOrMod import preconditionsRequireAdminOrMod
from preconditions.requireChannelOrCategory import preconditionsRequireChannelOrCategory
from extensions.channelsManager import channelManager
from extensions.messagesManager import messagesManager
from extensions.rolesManager import rolesManager
from cogs.help import MyHelpCommand
from config import postgres_data

warnings.filterwarnings("ignore", category=DeprecationWarning)
connection = psycopg2.connect(**postgres_data)
cur = connection.cursor()
print(connection)

db = DatabaseManager(cur, connection)
permissionAdminMod = preconditionsRequireAdminOrMod(db)
permissionChannelCategory = preconditionsRequireChannelOrCategory(db)
channel_manager = channelManager(db)
messages_manager = messagesManager(db)
role_manager = rolesManager(db)

ConfigRead = open('config.json')
ConfigLoad = json.load(ConfigRead)


def get_prefixes(bot, message):
    cog_prefixes = (cog.prefix for cog in bot.cogs.values() if hasattr(cog, 'prefix'))
    default_prefixes = (f"{ConfigLoad['prefix']}")
    return (*cog_prefixes, *default_prefixes)

help_command = MyHelpCommand()

intents = discord.Intents().all()
intents.members = True
intents.message_content = True
activity = discord.Activity(type=discord.ActivityType.playing, name=f"Wpisz {ConfigLoad['prefix']}help aby uzyskać listę poleceń.")
client = commands.Bot(command_prefix=get_prefixes, help_command = help_command, intents=intents, activity=activity)

cmds = []
@client.event
async def on_ready():
    createTables(cur, connection)
    check_series.start(client, cur, connection, db)
    print('We have logged in as {0.user}'.format(client))
    cmds.append(f"not message.content.startswith('{ConfigLoad['prefix']}help')")
    cmds.append(f"not message.content.startswith('{ConfigLoad['prefix']}dev')")
    cogs = client.cogs.values()
    for cog in cogs:
        for command in cog.get_commands():
            cmds.append(f"not message.content.startswith('{ConfigLoad['prefix']}{command.name}')")

@client.event
async def on_command_error(self, ctx: commands.Context, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Nie masz wymaganych uprawnień do wykonania tej komendy.")

async def main():
    await client.add_cog(Developer_options(client, cur, connection))
    await client.add_cog(ListenerCog(client, db, permissionAdminMod, channel_manager, messages_manager, ConfigLoad['prefix'], cmds))
    await client.add_cog(Polecenia_Muzyczne(client))
    await client.add_cog(Polecenia_uzytkownika(client, permissionAdminMod, permissionChannelCategory, channel_manager, ConfigLoad['token']))
    await client.add_cog(Polecenia_administracji(client, permissionAdminMod, permissionChannelCategory, channel_manager, messages_manager, role_manager, connection, cur))
    client.session = aiohttp.ClientSession()
    client.add_view(SimpleView(client, channel_manager, messages_manager, role_manager))
    await client.start(ConfigLoad['token'])

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())