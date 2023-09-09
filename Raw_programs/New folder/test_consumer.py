from time import sleep

from rabbitmq.consumer import RabbitConsumer
from . import config


def procces_msg(ch, method, properties, body):
    print(f"message {body} recived")


amqp_url = config.read('rabbitmq', 'CLOUDAMQP_URL')
consumer = RabbitConsumer(amqp_url, "eitaa")
consumer.config_connection()
consumer.start_consuming(procces_msg)
sleep(5)
consumer.stop_consuming()
consumer.stop_connection()
