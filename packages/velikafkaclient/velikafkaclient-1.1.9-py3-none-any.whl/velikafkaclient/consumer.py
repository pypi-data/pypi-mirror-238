import json
import logging
import time

from aiokafka import AIOKafkaConsumer
from confluent_kafka import Consumer, KafkaError, KafkaException

from .eventregistration import kafka_topic_events
from .exceptions import InvalidEventTopicException, InvalidEventStructure
from .killer import KafkaClientGracefulKiller


class AsyncKafkaConsumer:

    def __init__(self, bootstrap_servers, group_id=None):
        self.kafka_topic_events = kafka_topic_events
        self.client = None
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.subscriptions = dict()
        self.topics = set()
        self.killer = KafkaClientGracefulKiller(self)

    async def start(self):
        if self.client is not None:
            raise Exception("Consumer already started, stop before starting again <3")
        self.client = AIOKafkaConsumer(
            *list(self.topics),
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id
        )
        await self.client.start()

    async def stop(self):
        if self.client is None:
            raise Exception("Consumer is not started, start before stopping <3")
        await self.client.stop()
        self.client = None

    def subscribe(self, topic, handler):
        self.subscriptions[topic.value] = handler
        self.topics.add(topic.value)

    async def consume(self):
        async for msg in self.client:
            print("consumed: ", msg.topic, msg.partition, msg.offset, msg.value)
            if msg.topic not in self.kafka_topic_events.topic_event_models:
                raise InvalidEventTopicException(f"Topic {msg.topic} not found")
            topic_event_model = self.kafka_topic_events.topic_event_models[msg.topic]
            try:
                decoded_msg = msg.value.decode('utf-8')
                data = json.loads(decoded_msg)
                msg_event = topic_event_model(**data)
                handler = await self.subscriptions[msg.topic](msg_event)
                print(handler)
            except Exception as e:
                # TODO add proper exception handling
                raise InvalidEventStructure(f"Invalid event structure {str(msg.value)} for topic {msg.topic}")


class RateLimit:
    batch_size: int = 1
    batch_waiting_time: int = 3
    units_per_minute: int = 100

    def __init__(self, batch_size=1, batch_waiting_time=3, units_per_minute=10000):
        self.batch_size = batch_size
        self.batch_waiting_time = batch_waiting_time
        self.units_per_minute = units_per_minute


class Batch:

    def __init__(self):
        self.events = dict()

    def add(self, event):
        topic = event.topic()
        if topic not in self.events:
            self.events[topic] = []
        self.events[topic].append(event)

    def reset(self):
        self.events = dict()

    def size(self):
        res = 0
        for t in self.events:
            res += len(self.events[t])
        return res


class EventRate:
    processed_batch_count: int = 0
    batch = Batch()
    session_start_time = time.time()
    batch_session_start_time = time.time()


class KafkaConsumer:

    def __init__(self, bootstrap_servers, rate_limit: RateLimit = None, group_id=None, auto_commit=True):
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.subscriptions = dict()
        self.auto_commit = auto_commit
        conf = {'bootstrap.servers': bootstrap_servers,
                'group.id': group_id,
                'auto.offset.reset': 'earliest',
                'enable.auto.commit': auto_commit,
                'allow.auto.create.topics': True,
                }
        self.client = Consumer(conf)
        self.rate_limit = rate_limit
        self.event_rate = EventRate()

    def process_events(self, time_now):
        try:
            for topic in self.event_rate.batch.events:
                self.subscriptions[topic](self.event_rate.batch.events[topic])

            if not self.auto_commit:
                self.client.commit()

            self.event_rate.batch_session_start_time = time_now
            self.event_rate.processed_batch_count += 1
            self.event_rate.batch.reset()
        except Exception as e:
            # TODO implement
            raise e

    def start(self):
        self.client.subscribe(list(self.subscriptions.keys()))

        try:
            while True:
                event = self.client.poll(timeout=1.0)
                time_now = time.time()
                batch_time_lapse = time_now - self.event_rate.batch_session_start_time

                if event is None:
                    if batch_time_lapse >= self.rate_limit.batch_waiting_time:
                        self.process_events(time_now)
                    continue

                if event.error():
                    if event.error().code() == KafkaError._PARTITION_EOF:
                        logging.info('%% %s [%d] reached end at offset %d\n' %
                                     (event.topic(), event.partition(), event.offset()))
                    elif event.error():
                        # TODO what to do ?
                        raise KafkaException(event.error())
                else:

                    self.event_rate.batch.add(event)

                    if batch_time_lapse >= self.rate_limit.batch_waiting_time or self.event_rate.batch.size() >= self.rate_limit.batch_size:
                        self.process_events(time_now)

                    time_lapse = time_now - self.event_rate.session_start_time
                    if time_lapse >= 60:
                        self.event_rate.processed_batch_count = 0
                        self.event_rate.session_start_time = time_now
                    else:
                        if self.event_rate.processed_batch_count >= self.rate_limit.units_per_minute:
                            time.sleep(60 - time_lapse + 10)
                            self.event_rate.batch_session_start_time = time.time()
                            continue

        finally:
            self.client.close()

    def commit(self):
        self.client.commit()

    def stop(self):
        self.client.close()

    def subscribe(self, topic, handler):
        self.subscriptions[topic] = handler
