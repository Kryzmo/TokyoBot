import discord
from discord.ext import commands
import datetime
from database_manager.manage_data import DatabaseManager
from preconditions.requireAdminOrMod import preconditionsRequireAdminOrMod
from extensions.channelsManager import channelManager
from extensions.messagesManager import messagesManager
from src.views import timeout_user
from extensions.error_handler import Error


class ListenerCog(commands.Cog):
    def __init__(self, bot: commands.Bot,
                        db: DatabaseManager,
                        permissionAdminMod: preconditionsRequireAdminOrMod,
                        channel_manager: channelManager,
                        messages_manager: messagesManager,
                        prefix,
                        cmds
                        ):
        self.bot = bot
        self.db = db
        self.permissionAdminMod = permissionAdminMod
        self.channel_manager = channel_manager
        self.messages_manager = messages_manager
        self.prefix = prefix
        self.cmds = cmds
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            if eval(' and '.join(self.cmds)):
                if not message.author.bot:
                    msg_author_content = '{}'.format(message.content).lower()
                    if self.messages_manager.vulgMessageCheck(msg_author_content) and not self.permissionAdminMod.requireAdminOrMod(message.author):
                        await timeout_user(self.bot, user_id=int(message.author.id), guild_id=message.guild.id, until=5, reason_mute='Wulgaryzm')
                        await message.reply('Wulgaryzmy są nie do pomyślenia trzymaj w nagrode mute.')
                await self.bot.process_commands(message)
        except Exception as e: Error(e)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            rows = self.db.getEmotesData()
            for row in rows:
                if f"{payload.message_id}" == f"{row[2]}" and f"{payload.emoji.name}" == f"{row[1]}":
                    guild = self.bot.get_guild(payload.guild_id)
                    member = guild.get_member(payload.user_id)
                    role = discord.utils.get(guild.roles, id=int(row[3]))
                    await member.add_roles(role)
        except Exception as e:
            Error(e)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        try:
            rows = self.db.getEmotesData()
            for row in rows:
                if f"{payload.message_id}" == f"{row[2]}" and f"{payload.emoji.name}" == f"{row[1]}":
                    guild = self.bot.get_guild(payload.guild_id)
                    member = guild.get_member(payload.user_id)
                    role = discord.utils.get(guild.roles, id=int(row[3]))
                    await member.remove_roles(role)
        except Exception as e:
            Error(e)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(self.channel_manager.welcomeChannel())
        channel_logs = self.bot.get_channel(self.channel_manager.newUserDataChannel())
        dt = datetime.datetime.now()
        timenow = dt.strftime("%Y-%m-%d %H:%M:%S")
        ct = member.created_at
        createdtime = ct.strftime("%Y-%m-%d %H:%M:%S")
        message = "{}".format(self.messages_manager.welcomeMessage()).replace(r"{user}", f"<@!{member.id}>").replace("\\n", "\n")
        await channel.send(message)
        embed = discord.Embed(title=f"{member} dołączył do servera",
                            description=f"<@!{member.id}>", color=2105893)
        embed.add_field(name="Konto utworzono:", value=createdtime,
                        inline=False)
        embed.add_field(name="ID użytkownika:", value=f"{member.id}",
                        inline=False)
        embed.set_footer(text = timenow, icon_url = f"{self.bot.user.avatar.url}")
        embed.set_author(name=f"{self.bot.user.name}", icon_url=str(member.avatar.url))
        await channel_logs.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        try:
            channel = self.bot.get_channel(self.channel_manager.welcomeChannel())
            message = "".format(self.messages_manager.farewellMessage()).replace(r"{user}", f"<@!{member.id}>").replace("\\n", "\n")
            await channel.send(message)
        except Exception as e: Error(e)


    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        try:
            async for entry in message.guild.audit_logs(limit=1,action=discord.AuditLogAction.message_delete):
                deleter = entry.user

            embed = discord.Embed(title="{} usunął wiadomość należącą do {}".format(deleter, message.author.name),
                                description="", color=2105893)
            embed.add_field(name="Usunięta wiadomość", value="```" + message.content + "```",
                            inline=False)
            embed.add_field(name="Na kanale", value=f"<#{message.channel.id}>",
                            inline=False)
            embed.add_field(name="User ID", value=f"{message.author.id}",
                            inline=True)
            embed.set_footer(text = datetime.datetime.now(), icon_url = f"{self.bot.user.avatar.url}")
            embed.set_author(name="Skasowana wiadomość", icon_url=str(message.author.avatar.url))
            channel = self.bot.get_channel(self.channel_manager.deletedMessages())
            await channel.send(embed=embed)
        except Exception as e: Error(e)


    @commands.Cog.listener()
    async def on_message_edit(self, message_before: discord.Message, message_after: discord.Message):
        if not message_after.author.bot:
            embed = discord.Embed(title="{} edytował wiadomość.".format(message_before.author.name),
                                description=f"[Link do wiadomości](https://discord.com/channels/{message_after.guild.id}/{message_after.channel.id}/{message_after.id})", color=2105893)
            embed.add_field(name="Oryginalna wiadomość", value="```" + message_before.content + "```",
                            inline=False)
            embed.add_field(name="Wiadomość po edycji", value="```" + message_after.content + "```",
                            inline=False)
            embed.add_field(name="Na kanale", value=f"<#{message_after.channel.id}>",
                            inline=False)
            embed.add_field(name="User ID", value=f"{message_after.author.id}",
                            inline=True)
            embed.set_footer(text = datetime.datetime.now(), icon_url = f"{self.bot.user.avatar.url}")
            embed.set_author(name="Edytowana wiadomość", icon_url=str(message_after.author.avatar.url))
            channel = self.bot.get_channel(self.channel_manager.deletedMessages())
            await channel.send(embed=embed)

