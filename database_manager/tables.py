
def createTables(cur, connection):
    try:
        print("Creating database tables")
        cur.execute("CREATE TABLE IF NOT EXISTS config (id SERIAL PRIMARY KEY, modlog_channel_id varchar(25), commands_channel_id varchar(25), arts_channel_id varchar(25), recrutation_category_id varchar(25), recrutation_role_id varchar(25), recrutation_common_role_id varchar(25), recrutation_message text, mod_role_id varchar(25), deleted_messages_channel_id varchar(25), edited_messages_channel_id varchar(25), welcome_channel_id varchar(25), welcome_message text, farewell_message text, reminders_channel varchar(25), trigram_similarity decimal);")
        connection.commit()
        #reminders_channel
        cur.execute("SELECT * FROM config WHERE id = 1;")
        if bool(cur.fetchone()) is False:
            print("Creating config row")
            cur.execute('insert into config (modlog_channel_id, commands_channel_id, arts_channel_id, recrutation_category_id, recrutation_role_id, recrutation_common_role_id, recrutation_message, mod_role_id, deleted_messages_channel_id, edited_messages_channel_id, welcome_channel_id, welcome_message, farewell_message, reminders_channel, trigram_similarity) VALUES (NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 0.5) ON CONFLICT DO NOTHING;')
        cur.execute("CREATE TABLE IF NOT EXISTS vulgs (id SERIAL PRIMARY KEY, vulg text);")
        cur.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')
        cur.execute("CREATE TABLE IF NOT EXISTS notification_manager (id SERIAL PRIMARY KEY, user_id text, url text, date_from date, date_to date, new_episode_time text);")
        cur.execute("CREATE TABLE IF NOT EXISTS emotes (id SERIAL PRIMARY KEY, emote text, message_id varchar(25), role_id varchar(25), category_name varchar(30));")
        connection.commit()
    except Exception as e:print(e)

def clearDB():
    # cur.execute('TRUNCATE notification_manager;DELETE FROM notification_manager;')
    # cur.execute('DROP SCHEMA public CASCADE;')
    # cur.execute('CREATE SCHEMA public;')
    pass