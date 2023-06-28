from discord.ext import tasks
import datetime
import requests
import pytz
import re
from extensions.channelsManager import channelManager
from extensions.error_handler import Error

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=pytz.timezone('Asia/Tokyo')).astimezone(tz=None)
@tasks.loop(minutes=59)
async def check_series(client, cur, connection, db):
    channel_manager = channelManager(db)
    channel = client.get_channel(channel_manager.remindersChannel())
    try:
        cur.execute('select id, date_to, date_from, new_episode_time, user_id, url from notification_manager')
        rows = cur.fetchall()
        for r in rows:
            if r[1] is not None:
                day_end = datetime.datetime.strptime("{}".format(utc_to_local(datetime.datetime.strptime(f"{r[1]} {r[3]}", '%Y-%m-%d %H:%M')))[:-9], '%Y-%m-%d %H:%M')
            day_start = datetime.datetime.strptime("{}".format(utc_to_local(datetime.datetime.strptime(f"{r[2]} {r[3]}", '%Y-%m-%d %H:%M')))[:-9], '%Y-%m-%d %H:%M')
            if r[1] is None or day_end > datetime.datetime.now():
                if len(r[4]) == 18:
                    user_id_or_nick = "<@!{}>".format(r[4])
                else:
                    user_id_or_nick = "{}".format(r[4])
                if r[1] is None:
                    if day_start.strftime("%A") == datetime.datetime.now().strftime("%A"):
                        if day_start.time().hour == datetime.datetime.now().time().hour:

                            await channel.send(f'{user_id_or_nick} twoja seria <{r[5]}> w przeciągu najbliższej godziny pojawi się na `nyaa.si` przygotuje się do tłumaczenia!')
                            get_id = re.findall('\d+', r[5])
                            anime_id = get_id[0]
                            api_url = 'https://api.jikan.moe/v4/anime/{}'.format(anime_id)
                            headers = { 
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.117', 
                            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
                            'Accept-Language' : 'en-US,en;q=0.5', 
                            'Accept-Encoding' : 'gzip', 
                            'DNT' : '1',
                            'Connection' : 'close' }
                            r = requests.get(api_url, headers=headers)
                            r_json = r.json()
                            date_to = r_json['data']['aired']['to']
                            if date_to is not None:
                                cur.execute("UPDATE notification_manager set date_to=%s where id=%s;", (r[0], date_to))
                                connection.commit()
                else:
                    if day_start.strftime("%A") == datetime.datetime.now().strftime("%A"):
                        if day_start.time().hour == datetime.datetime.now().time().hour:
                            await channel.send(f'{user_id_or_nick} twoja seria <{r[5]}> w przeciągu najbliższej godziny pojawi się na `nyaa.si` przygotuje się do tłumaczenia!')

        
    except Exception as e:
        Error(e)
