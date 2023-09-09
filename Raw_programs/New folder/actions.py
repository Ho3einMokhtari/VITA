import os
import time

from .classes import PeerType


def deduct_from_event(event):
    peer_data = event.message.peer_id
    peer_type = type(peer_data)

    match peer_type:
        case PeerType.channel:
            peer_id = peer_data.channel_id
        case PeerType.chat:
            peer_id = peer_data.chat_id
        case PeerType.user:
            peer_id = event.message.peer_id.user_id
        case _:
            peer_id = 0

    has_media = True if event.message.media else False

    from_id = None if event.message.from_id is None else event.message.from_id.user_id

    return has_media, peer_id, from_id


def is_filtered(func, filter_list, event, *args, **kwargs):
    def wrapper(*args, **kwargs):
        result = any(filter in event.message.message for filter in filter_list)

        if not result:
            return func(event, args, kwargs)

    return wrapper


def prune_msg(msg):
    msg_words = msg.split(' ')

    for word in msg_words:
        if '@' in word and 'http' in word:
            del word

    return " ".join(msg_words)


def rename_file(path):
    if not path.isascii():
        file_array = path.split(os.sep)
        file_name = file_array[-1]
        base_path = path.replace(file_name, '')
        extension = file_name.split('.')[-1]
        new_path = base_path + str(time.time()) + '.' + extension
        os.rename(path, new_path)

    return path
