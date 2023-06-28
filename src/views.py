
from discord.ext import commands
import discord
from extensions.channelsManager import channelManager
from extensions.messagesManager import messagesManager
from extensions.rolesManager import rolesManager
from extensions.error_handler import Error
import datetime

async def timeout_user(client: commands.Bot, *, user_id: int, guild_id: int, until, reason_mute):
    headers = {"Authorization": f"Bot {client.http.token}", "X-Audit-Log-Reason": reason_mute}
    url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
    if until is not None:
        timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=until)).isoformat()
    else:
        timeout = None
    json = {'communication_disabled_until': timeout}
    async with client.session.patch(url, json=json, headers=headers) as session:
        if session.status in range(200, 299):
           return True
        return False

class SimpleView(discord.ui.View):
    def __init__(self, bot: commands.Bot,
                            channel_manager: channelManager,
                            messages_manager: messagesManager,
                            role_manager: rolesManager
                            ):
        self.bot = bot
        self.channel_manager = channel_manager
        self.messages_manager = messages_manager
        self.role_manager = role_manager
        super().__init__(timeout=None)
    foo : bool = None

    @discord.ui.button(label="Rekrutacja",
                       style=discord.ButtonStyle.success,
                       custom_id="persistent_view:recrutation")
    async def recrutation(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.foo = True
        await interaction.response.defer()
        try:
            guild = self.bot.get_guild(interaction.guild.id)
            member = guild.get_member(interaction.user.id)
            common_role = guild.get_role(self.role_manager.recrutationCommonRole())
            await member.add_roles(common_role)
            role_recrutation = discord.utils.get(guild.roles, id=self.role_manager.recrutationRole())
            channel_name = member.name + ' ' + '{}'.format(interaction.user.id)
            cat = discord.utils.get(guild.categories, id=self.channel_manager.recrutationCategory())
            if '{}'.format(interaction.user.id) not in '{}'.format(cat.channels):
                channel = await guild.create_text_channel(channel_name, category=cat)
                message = f"{self.messages_manager.recrutationMessage()}".replace(r"{user}", f"<@{interaction.user.id}>").replace("\\n", "\n")
                message += f" <@&{role_recrutation.id}>"
                await channel.send(message)
                await channel.edit(sync_permissions=True)
                await channel.set_permissions(member, read_messages=True, send_messages=True)
                await channel.set_permissions(role_recrutation, read_messages=True, send_messages=True, view_channel=True)
                return channel
        except Exception as e: Error(e)