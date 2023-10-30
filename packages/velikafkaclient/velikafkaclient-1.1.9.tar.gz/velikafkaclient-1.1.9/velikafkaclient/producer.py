import json

from aiokafka import AIOKafkaProducer
from confluent_kafka import Producer

from .eventregistration import kafka_topic_events
from .exceptions import InvalidEventTopicException, InvalidEventModelForTopic
from .topics.topics import KafkaTopic
from .events.base import KafkaEvent
from velilogger import get_tracing_id


class AsyncKafkaEventProducer:

    def __init__(self, bootstrap_servers):
        self.kafka_topic_events = kafka_topic_events
        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers
        )

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.flush()
        await self.producer.stop()

    async def produce_event(self, topic: KafkaTopic, event: KafkaEvent):
        if topic not in self.kafka_topic_events.topic_event_models:
            raise InvalidEventTopicException(f"Topic {topic} not found")
        topic_event_model = self.kafka_topic_events.topic_event_models[topic]
        if not isinstance(event, topic_event_model):
            raise InvalidEventModelForTopic(f"event: {str(event)} topic model: {str(topic_event_model)}")
        event.tracing_id = get_tracing_id()
        await self.producer.send(topic.value, json.dumps(event.dict()).encode())

    async def produce_easy_event(self, topic_name, event_data):
        await self.producer.send(topic_name, json.dumps(event_data).encode())


class KafkaEventProducer:

    def __init__(self, bootstrap_servers):
        self.kafka_topic_events = kafka_topic_events
        self.producer = Producer({'bootstrap.servers': bootstrap_servers})

    def produce_event(self, topic: KafkaTopic, event: KafkaEvent):
        if topic not in self.kafka_topic_events.topic_event_models:
            raise InvalidEventTopicException(f"Topic {topic} not found")
        topic_event_model = self.kafka_topic_events.topic_event_models[topic]
        if not isinstance(event, topic_event_model):
            raise InvalidEventModelForTopic(f"event: {str(event)} topic model: {str(topic_event_model)}")
        event.tracing_id = get_tracing_id()
        self.producer.produce(topic.value, json.dumps(event.dict()).encode())

    def produce_easy_event(self, topic_name, event_data):
        self.producer.produce(topic_name, json.dumps(event_data).encode())

    def flush(self, timeout=1):
        return self.producer.flush(timeout)
