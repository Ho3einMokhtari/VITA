import logging
from rabbitmq import RabbitBase

logging.basicConfig()


class RabbitConsumer(RabbitBase):
    def __init__(self, url: str, queue_name: str):
        super().__init__(url, queue_name)

    def start_consuming(self, callback):
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback, auto_ack=True
            )

        logging.info("consuming started")
        self.channel.start_consuming()

    def stop_consuming(self):
        self.channel.stop_consuming()
        logging.info("consuming stoped")
