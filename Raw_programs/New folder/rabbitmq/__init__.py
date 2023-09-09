import pika
import logging
logging.basicConfig()


class RabbitBase:
    """Rabbit base class for control the connections and configs"""

    def __init__(self, url: str, queue_name: str):
        self.url = url
        self.queue_name = queue_name
        self.params = pika.URLParameters(url)
        self.params.socket_timeout = 5

    def config_connection(self):
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)
        logging.info("Rabbitmq connected")

    def stop_connection(self):
        self.connection.close()
        logging.info("Rabbitmq disconnected")
