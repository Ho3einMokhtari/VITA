import sys
import json

from telethon.sync import events

from .classes import Client
from rabbitmq.publisher import RabbitPublisher
from . import actions
from . import config


base_file_path = config.read('telegram', 'base_file_path')
api_id = int(config.read('telegram', 'api_id'))
api_hash = config.read('telegram', 'api_hash')
platform = config.read('telegram', 'platform')
amqp_url = config.read('rabbitmq', 'CLOUDAMQP_URL')
session_name = sys.argv[1]

with open("filtering.txt", "r", encoding="UTF-8") as f:
    list_filtering = f.read_lines()


client_config = Client(session_name, api_id, api_hash, platform, proxy)
client_config.start()
client = client_config.client

rabbitmq = RabbitPublisher(url=amqp_url, queue_name="eitaa")
rabbitmq.config_connection()


@client.on(events.NewMessage())
@actions.is_filtered(list_filtering)
async def procces_msg(event):

    prune_msg = actions.prune_msg(event.message.message)

    has_media, peer_id, from_id = actions.deduct_from_event(event)

    if has_media:
        path = await client.download_media(event.message, base_file_path)
        path = actions.rename_file(path)
    else:
        path = None

    data = {
        'text': prune_msg,
        'time': event.message.date,
        'in_eitaa': False,
        'has_media': has_media,
        'media_path': path,
        'peer_id': peer_id,
        'from_id': from_id,
        'user_id': me_id,
    }

    msg = json.dumps(data)
    rabbitmq.publish(msg)

if __name__ == '__main__':
    client.run_until_disconnected()
