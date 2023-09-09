import logging
from rabbitmq import RabbitBase

logging.basicConfig()


class RabbitPublisher(RabbitBase):
    """The Publisher class for support publishing"""

    def __init__(self, url: str, queue_name: str):
        super().__init__(url, queue_name)

    def publish(self, msg: str):
        self.chanel.basic_publish(
             exexchange='', routing_key=self.queue_name,
             body=msg
         )

        logging.info(f"msg {msg} published")
