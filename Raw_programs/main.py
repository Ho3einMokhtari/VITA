from telethon.sync import TelegramClient, events
from pymongo import MongoClient
import helper
import config
import sys
environment = 'Windows'

mongo_client = MongoClient('127.0.0.1:27017')
db = mongo_client.eitaa

api_id = int(config.read('telegram', 'api_id'))
api_hash = config.read('telegram', 'api_hash')
session_name = sys.argv[1]
if environment == 'Windows':
    base_file_path = config.read('telegram', 'base_file_path')
    client = TelegramClient(session_name, api_id, api_hash, proxy=('socks5', '127.0.0.1', 10808))

else:
    base_file_path = config.read('telegram', 'base_file_path')
    client = TelegramClient(session_name, api_id, api_hash)
client.start()

me = client.get_me()
me_id = me.id
file = open("filtering.txt", "r", encoding="UTF-8")
file_2 = file.read()
list_filtering = file_2.split("\n")
file.close()


@client.on(events.NewMessage())
async def print_new_msg(event):
    print(event.message)
    if helper.is_filtered(list_filtering, event.message.message):
        return
    prune_msg = helper.prune_msg(event.message.message)
    # if len(prune_msg) < 50:
    #     is_long = False
    # else:
    #     is_long = True
    has_media, peer_id, from_id = helper.deduct_from_event(event)

    if has_media:
        path = await client.download_media(event.message, base_file_path)
        path = helper.rename_file(path)
    else:
        path = None
    db.msg.insert_one({
        'text': prune_msg,
        'time': event.message.date,
        'in_eitaa': False,
        'has_media': has_media,
        'media_path': path,
        'peer_id': peer_id,
        'from_id': from_id,
        'user_id': me_id,
    })


if __name__ == '__main__':
    client.run_until_disconnected()
