from extensions.error_handler import Error
from database_manager.manage_data import DatabaseManager


class preconditionsRequireChannelOrCategory():
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def requireArtChannel(self, channel_id) -> bool:
        try:
            x = self.db.getConfigRows()
            if channel_id == int(x[3]):
                return True
        except Exception as e: Error(e)

    def requireCommandsChannel(self, channel_id) -> bool:
        try:
            x = self.db.getConfigRows()
            if channel_id == int(x[2]):
                return True
        except Exception as e: Error(e)