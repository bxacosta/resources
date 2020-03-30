import json
import time
from os import environ
from random import randrange
from sys import argv

from pika import BlockingConnection, URLParameters, BasicProperties
from pika.exceptions import AMQPConnectionError, ConnectionClosedByBroker
from retry import retry

SEARCH_QUEUE = 'search'
RESULT_QUEUE = 'result'
PARAMS = URLParameters(environ.get('AMQP_URL', 'amqp://guest:guest@localhost:5672/%2F'))


def publish(message: str):
    connection = BlockingConnection(PARAMS)
    channel = connection.channel()
    channel.queue_declare(queue=SEARCH_QUEUE, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=SEARCH_QUEUE,
        body=json.dumps(message),
        properties=BasicProperties(content_type='application/json'))
    print(f"[x] Sent: {message}")
    connection.close()


@retry(AMQPConnectionError, delay=5, jitter=(1, 3))
def consume(on_message_callback: callable):
    connection = BlockingConnection(PARAMS)
    channel = connection.channel()
    channel.queue_declare(queue=SEARCH_QUEUE, durable=True)
    channel.queue_declare(queue=RESULT_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)

    def callback(ch, method, properties, body):
        print(f"[x] Received: {body} - content_type: {properties.content_type}")
        result = on_message_callback(json.loads(body))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        if result:
            ch.basic_publish(
                exchange='',
                routing_key=RESULT_QUEUE,
                body=json.dumps(result),
                properties=BasicProperties(content_type='application/json'))
            print(f"[x] Sent: {result}")

    channel.basic_consume(queue=SEARCH_QUEUE, on_message_callback=callback)
    print('[*] Waiting for messages. To exit press CTRL+C')

    try:
        channel.start_consuming()
    except (ConnectionClosedByBroker, KeyboardInterrupt):
        pass


if __name__ == '__main__':
    if len(argv) > 1:
        publish(argv[1])
    else:
        def on_message(message):
            size = 40
            total = randrange(3000, 4000)
            for progress in range(0, total + 1):
                x = size * progress // total
                percent = progress / total * 100
                print(
                    f'\r[x] {message}: [{"#" * x}{"." * (size - x)}] {progress // 100:>2}/{total // 100} ({percent:.1f}%)',
                    end='', flush=True)
                time.sleep(0.01)
            print()
            return f'Finished {message} in {total // 100} seconds'


        consume(on_message)
