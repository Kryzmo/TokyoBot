from extensions.error_handler import Error
from database_manager.manage_data import DatabaseManager

class channelManager():
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def modLog(self):
        try:
            x = self.db.getConfigRows()
            return int(x[1])
        except Exception as e: Error(e)

    def commandsChannel(self):
        try:
            x = self.db.getConfigRows()
            return int(x[2])
        except Exception as e: Error(e)

    def deletedMessages(self):
        try:
            x = self.db.getConfigRows()
            return int(x[9])
        except Exception as e: Error(e)

    def welcomeChannel(self):
        try:
            x = self.db.getConfigRows()
            return int(x[11])
        except Exception as e: Error(e)
        
    def recrutationCategory(self):
        try:
            x = self.db.getConfigRows()
            return int(x[4])
        except Exception as e: Error(e)

    def newUserDataChannel(self):
        try:
            x = self.db.getConfigRows()
            return int(x[10])
        except Exception as e: Error(e)

    def remindersChannel(self):
        try:
            x = self.db.getConfigRows()
            return int(x[14])
        except Exception as e: Error(e)

