from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import os
import time

def deduct_from_event(event):
    has_media = False
    if event.message.media:
        has_media = True
    if type(event.message.peer_id) == PeerChannel:
        peer_id = event.message.peer_id.channel_id
    elif type(event.message.peer_id) == PeerChat:
        peer_id = event.message.peer_id.chat_id
    elif type(event.message.peer_id) == PeerUser:
        peer_id = event.message.peer_id.user_id
    else:
        peer_id = 0
    if event.message.from_id is None:
        from_id = None
    else:
        from_id = event.message.from_id.user_id
    return has_media, peer_id, from_id


def is_filtered(filter_list, msg):
    for filter in filter_list:
        if ' ' + filter + ' ' in msg or '\n' + filter + ' ' in msg or \
                ' ' + filter + '\n' in msg or '\n' + filter + '\n' in msg:
            return True
    return False


def prune_msg(msg):
    msg_words = msg.split(' ')
    new_msg = ''
    for word in msg_words:
        if '@' not in word and 'http' not in word:
            new_msg = new_msg + " " + word
    return new_msg


def rename_file(path):
    if path.isascii():
        return path
    else:
        file_array = path.split(os.sep)
        file_name = file_array[-1]
        base_path = path.replace(file_name, '')
        extension = file_name.split('.')[-1]
        new_path = base_path + str(time.time()) + '.' + extension
        os.rename(path, new_path)
        return new_path
