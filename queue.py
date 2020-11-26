import sys
import time
import json
import configparser
from argparse import ArgumentParser

import pika


class RabbitMQ:

    def __init__(self,
                 account,
                 password,
                 url,
                 vhost):

        self.params = pika.URLParameters(
            f"amqps://{account}:{password}@{url}/{vhost}"
        )

    @classmethod
    def from_dict(cls, d):
        return RabbitMQ(
            account=d.get("ACCOUNT", "asd"),
            password=d.get("PASSWORD"),
            url=d.get("QUEUE_URL"),
            vhost=d.get("VIRTUAL_HOST")
        )

    @classmethod
    def from_file(cls, filepath):
        try:
            with open(filepath) as f:
                config = cls.from_string(f.read())
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {filepath}")
        else:
            return cls.from_dict(config)

    @classmethod
    def from_string(cls, string):
        config = configparser.ConfigParser(allow_no_value=True)

        try:
            config.read_string(string)
        except configparser.ParsingError as err:
            raise configparser.ParsingError(err)
        else:
            return config["RABBITMQ_INFO"]

    def _connect(self):
        return pika.BlockingConnection(self.params)

    def publish(self, queue, data):
        connection = self._connect()
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(data)
        )
        print(f" [x] Sent 'data {data}'")
        connection.close()

    def consume(self, queue, callback):
        connection = self._connect()
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        print(' [*] Waiting for messages. To exit press CTRL+C')

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=queue,
            on_message_callback=callback
        )
        channel.start_consuming()


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(5)
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument(
        "-p",
        "--path",
        default="./config.ini",
        help="Path to the config file"
    )
    parser.add_argument(
        "opt",
        help="Operation to perform (publish/consume)"
    )
    parser.add_argument(
        "queue",
        help="Queue to be performed"
    )
    parser.add_argument(
        "-n",
        "--number",
        type=int,
        default=10,
        help="Number of messages to be published to queue"
    )
    args = parser.parse_args()

    queue = RabbitMQ.from_file(args.path)

    if args.opt == "publish":
        for i in range(args.number):
            data = {
                f"data{i}": {
                    "bucket": {"name": "BUCKET NAME"},
                    "object": {"key": i}
                }
            }
            queue.publish(args.queue, data)

    elif args.opt == "consume":
        queue.consume(args.queue, callback)

    else:
        parser.print_help()
        sys.exit(1)
