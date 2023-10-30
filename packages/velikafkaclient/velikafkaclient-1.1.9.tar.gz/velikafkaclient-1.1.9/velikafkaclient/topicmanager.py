from confluent_kafka.admin import AdminClient, NewTopic


class KafkaTopicManager:

    def __init__(self, bootstrap_servers):
        self.bootstrap_servers = bootstrap_servers
        self.client = AdminClient({
            "bootstrap.servers": bootstrap_servers
        })

    def create_topic(self, topic_name: str, num_partitions=1, replication_factor=1):
        topics_list = [NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]
        return self.client.create_topics(topics_list)

    def create_topics(self, topic_names: [str], num_partitions=1, replication_factor=1):
        topics_list = [NewTopic(tn, num_partitions=num_partitions, replication_factor=replication_factor) for tn in
                       topic_names]
        return self.client.create_topics(topics_list)

    def list_topics(self) -> [str]:
        return list(self.client.list_topics().topics.keys())

    def topic_exists(self, topic_name) -> bool:
        return self.client.list_topics().topics.get(topic_name) is not None

    def delete_topic(self, topic_name):
        self.client.delete_topics(topics=[topic_name])

    def delete_topics(self, topic_names):
        self.client.delete_topics(topics=topic_names)
