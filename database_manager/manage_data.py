from extensions.error_handler import Error
from config import postgres_data
import psycopg2
class DatabaseManager():
    def __init__(self, cur, connection):
        self.cur = cur
        self.connection = connection
    def getConfigRows(self):
        try:
            self.cur.execute('select id, modlog_channel_id, commands_channel_id, arts_channel_id, recrutation_category_id, recrutation_role_id, recrutation_common_role_id, recrutation_message, mod_role_id, deleted_messages_channel_id, edited_messages_channel_id, welcome_channel_id , welcome_message, farewell_message, reminders_channel, trigram_similarity from config where id = 1;')
            data = self.cur.fetchone()
            return data
        except Exception as e: Error(e)
  

    def setVar(self, var, id):
        try:
            self.cur.execute('UPDATE config SET {} = \'{}\' where id = 1;'.format(var, id))
            self.connection.commit()
        except Exception as e: Error(e)

    def getEmotesData(self):
        try:
            self.cur.execute("SELECT * FROM emotes")
            data = self.cur.fetchall()
            return data
        except psycopg2.ProgrammingError as e:
            Error(e)
            self.connection.rollback()
        except psycopg2.InterfaceError as e:
            Error(e)
            self.connection = psycopg2.connect(**postgres_data)
            self.cur = self.connection.cursor()
        except Exception as e: Error(e)
        
    
    def getPreconditions(self):
        try:
            self.cur.execute("SELECT mod_role_id FROM config where id = 1")
            data = self.cur.fetchone()
            return int(''.join(data))
        except psycopg2.ProgrammingError as e:
            Error(e)
            self.connection.rollback()
        except psycopg2.InterfaceError as e:
            Error(e)
            self.connection = psycopg2.connect(**postgres_data)
            self.cur = self.connection.cursor()
        except Exception as e: Error(e)

    def addEmoji(self, message_id, emoji_name, rank_id, category_name):
        try:
            self.cur.execute("INSERT INTO emotes (emote, message_id, role_id, category_name) VALUES ('{}', '{}', '{}', '{}')".format(emoji_name, message_id, rank_id, category_name))
            self.connection.commit()
        except psycopg2.ProgrammingError as e:
            Error(e)
            self.connection.rollback()
        except psycopg2.InterfaceError as e:
            Error(e)
            self.connection = psycopg2.connect(**postgres_data)
            self.cur = self.connection.cursor()
        except Exception as e: Error(e)

    def removeEmoji(self, emoji_name):
        try:
            self.cur.execute("DELETE FROM emotes WHERE emote = '{}'".format(emoji_name))
            self.connection.commit()
        except psycopg2.ProgrammingError as e:
            Error(e)
            self.connection.rollback()
        except psycopg2.InterfaceError as e:
            Error(e)
            self.connection = psycopg2.connect(**postgres_data)
            self.cur = self.connection.cursor()
        except Exception as e: Error(e)

    def deleteEmojisByCategory(self, category_name):
        try:
            self.cur.execute("DELETE FROM emotes WHERE category_name = '{}'".format(category_name))
            self.connection.commit()
        except psycopg2.ProgrammingError as e:
            Error(e)
            self.connection.rollback()
        except psycopg2.InterfaceError as e:
            Error(e)
            self.connection = psycopg2.connect(**postgres_data)
            self.cur = self.connection.cursor()
        except Exception as e: Error(e)

    def addVulg(self, vulg):
        try:
            self.cur.execute("INSERT INTO vulgs (vulg) VALUES ('{}');".format(vulg))
            self.connection.commit()
            return True
        except psycopg2.ProgrammingError as e:
            Error(e)
            self.connection.rollback()
            return False
        except psycopg2.InterfaceError as e:
            Error(e)
            self.connection = psycopg2.connect(**postgres_data)
            self.cur = self.connection.cursor()
            return False
        except Exception as e:
            Error(e)
            return False
        
    def removeVulg(self, vulg):
        try:
            self.cur.execute("DELETE FROM vulgs WHERE vulg = '{}'".format(vulg))
            self.connection.commit()
            return True
        except psycopg2.ProgrammingError as e:
            Error(e)
            self.connection.rollback()
            return False
        except psycopg2.InterfaceError as e:
            Error(e)
            self.connection = psycopg2.connect(**postgres_data)
            self.cur = self.connection.cursor()
            return False
        except Exception as e:
            Error(e)
            return False
        
    def getSimilarityValue(self):
        try:
            self.cur.execute("SELECT trigram_similarity FROM config WHERE id = 1;")
            value = self.cur.fetchone()
            if value:
                return float(value[0])
            else:
                #raise ValueError("Config value {} not found".format(config_name))
                return 0.5
        except psycopg2.ProgrammingError as e:
            Error(e)
            self.connection.rollback()
            return False
        except psycopg2.InterfaceError as e:
            Error(e)
            self.connection = psycopg2.connect(**postgres_data)
            self.cur = self.connection.cursor()
            return False
        except Exception as e:
            Error(e)
            return False
        
    def checkVulg(self, vulg):
        try:
            similarity = self.getSimilarityValue()
            # self.cur.execute("set pg_trgm.similarity_threshold = {};".format(similarity))
            # self.connection.commit()
            self.cur.execute("SELECT vulg FROM vulgs WHERE similarity(vulg, '{}') > {};".format(vulg, similarity))
            rows = self.cur.fetchall()
            vulg = [r[0] for r in rows]
            return bool(vulg)
        except psycopg2.ProgrammingError as e:
            Error(e)
            self.connection.rollback()
        except psycopg2.InterfaceError as e:
            Error(e)
            self.connection = psycopg2.connect(**postgres_data)
            self.cur = self.connection.cursor()
        except Exception as e: Error(e)

    def listVulg(self):
        try:
            self.cur.execute("SELECT vulg FROM vulgs;")
            rows = self.cur.fetchall()
            vulg = sorted([r[0] for r in rows])
            return vulg
        except psycopg2.ProgrammingError as e:
            Error(e)
            self.connection.rollback()
        except psycopg2.InterfaceError as e:
            Error(e)
            self.connection = psycopg2.connect(**postgres_data)
            self.cur = self.connection.cursor()
        except Exception as e: Error(e)