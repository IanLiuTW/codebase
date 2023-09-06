import asyncio

from confluent_kafka import Consumer, KafkaError
from loguru import logger as lo


def commit_completed(err, partitions):
    if err:
        lo.error(str(err))
    else:
        lo.info("Committed partition offsets: " + str(partitions))


KAFKA_CONSUMER_CONFIG = {
    'bootstrap.servers': "localhost:9094",
    'group.id': "sample_group",
    'default.topic.config': {'auto.offset.reset': 'smallest'},
    'on_commit': commit_completed,
}
KAFKA_CONSUMER_TOPICS = []


class KafkaConsumer:
    def __init__(self, msg_process):
        self.running = False
        self.consumer = Consumer(KAFKA_CONSUMER_CONFIG)
        self.msg_process = msg_process
        lo.info("Kafka consumer created")

    async def consume_loop(self):
        while self.running:
            try:
                self.consumer.subscribe(KAFKA_CONSUMER_TOPICS)
                while self.running:
                    msg = self.consumer.poll(timeout=1.0)
                    if msg:
                        if msg.error():
                            if msg.error().code() == KafkaError._PARTITION_EOF:
                                lo.error(f"{msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}")
                            elif msg.error():
                                lo.error(f"Error occurred: {str(msg.error())}")
                        else:
                            self.msg_process(msg)
                            self.__commit()
                    await asyncio.sleep(0.1)
            except Exception as e:
                lo.error(f"Error occurred: {e}")
            finally:
                self.consumer.close()
                lo.info("Kafka consumer connection closed")

    def __commit(self):
        self.consumer.commit(asynchronous=False)
        lo.info("Committed offsets")

    def start(self):
        self.running = True
        asyncio.create_task(self.consume_loop())
        lo.info("Kafka consumer loop started")

    def shutdown(self):
        self.running = False
        lo.info("Kafka consumer stopped")