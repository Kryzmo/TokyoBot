from extensions.error_handler import Error
from database_manager.manage_data import DatabaseManager

class messagesManager():
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def vulgMessageAdd(self, message: str):
        try:
            x = self.db.addVulg(message)
            return x
        except Exception as e: Error(e)

    def vulgMessageRemove(self, message: str):
        try:
            x = self.db.removeVulg(message)
            return x
        except Exception as e: Error(e)

    def vulgMessageCheck(self, message: str):
        try:
            for i in message.split():
                x = self.db.checkVulg(i)
                if x:
                    return x
        except Exception as e: Error(e)

    def vulgMessageList(self):
        try:
            x = self.db.listVulg()
            return ', '.join(x)
        except Exception as e: Error(e)

    def recrutationMessage(self) -> str:
        try:
            x = self.db.getConfigRows()
            return str(x[7])
        except Exception as e: Error(e)

    def welcomeMessage(self) -> str:
        try:
            x = self.db.getConfigRows()
            return str(x[12])
        except Exception as e: Error(e)

    def farewellMessage(self) -> str:
        try:
            x = self.db.getConfigRows()
            return str(x[13])
        except Exception as e: Error(e)
