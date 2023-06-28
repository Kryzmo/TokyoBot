#Added for future modifications
from discord import Member, Permissions
from discord.ext import commands
from extensions.error_handler import Error
from database_manager.manage_data import DatabaseManager
class MissingAdminPermission(commands.CheckFailure):
    pass

class preconditionsRequireAdminOrMod():
    def __init__(self, db: DatabaseManager):
        self.db = db

    def isServerOwner(self, member: Member) -> bool:
        return member == member.guild.owner
    
    def requireAdmin(self, member: Member) -> bool:
        try:
            if self.isServerOwner(member):
                return True
            permissions: Permissions = member.guild_permissions
            return permissions.administrator
        except Exception as e: Error(e)

    def requireAdminOrMod(self, member: Member) -> bool:
        try:
            if self.isServerOwner(member):
                return True
            permissions: Permissions = member.guild_permissions
            has_role = any(role.id == int(self.db.getPreconditions()) for role in member.roles)
            return permissions.administrator or has_role
        except Exception as e:
            Error(e)
