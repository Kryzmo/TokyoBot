import discord
from discord.ext import commands
from extensions.channelsManager import channelManager
from preconditions.requireAdminOrMod import preconditionsRequireAdminOrMod
from preconditions.requireChannelOrCategory import preconditionsRequireChannelOrCategory

class ownDecorators():
    def __init__(self, permissionAdminMod: preconditionsRequireAdminOrMod, permissionChannelCategory: preconditionsRequireChannelOrCategory, channel_manager: channelManager):
        global _permissionAdminMod
        _permissionAdminMod = permissionAdminMod
        global _permissionChannelCategory
        _permissionChannelCategory = permissionChannelCategory
        global _channel_manager
        _channel_manager = channel_manager

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
                await ctx.send(embed=embed)
                return False
        return commands.check(predicate)

    def is_channel_or_mod():
        async def predicate(ctx: commands.Context):
            if _permissionAdminMod.requireAdminOrMod(ctx.author) is True or _permissionChannelCategory.requireCommandsChannel(ctx.channel.id) is True:
                return True
            else:
                await ctx.reply(f"Poleceń używamy na kanale <#{_channel_manager.commandsChannel()}>")
                return False
        return commands.check(predicate)