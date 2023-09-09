from telethon.sync import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel


class PeerType:
    """data class"""

    channel = PeerChannel
    chat = PeerChat
    user = PeerUser


class Client(TelegramClient):
    """the Client class for managing TelegramClient"""

    def __init__(
                self, session_name: str, api_id: int, api_hash: str,
                platform: str = "Linux", proxy: list = None
            ):
        self.session_name = session_name
        self.api_id = api_id
        self.api_hash = api_hash
        self.platform = platform

    def start(self):
        """get proxy config"""

        if self.platform == 'Local':
            if self.proxy is not None:
                self.client = TelegramClient(
                        self.session_name, self.api_id,
                        self.api_hash, proxy=self.proxy
                    )
        else:
            self.client = TelegramClient(
                self.session_name, self.api_id, self.api_hash
                )

        self.client.start()
