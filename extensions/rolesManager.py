from extensions.error_handler import Error
from database_manager.manage_data import DatabaseManager

class rolesManager():
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def recrutationRole(self) -> int:
        try:
            x = self.db.getConfigRows()
            return int(x[5])
        except Exception as e: Error(e)

    def recrutationCommonRole(self) -> int:
        try:
            x = self.db.getConfigRows()
            return int(x[6])
        except Exception as e: Error(e)