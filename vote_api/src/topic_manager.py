from kafka.admin import KafkaAdminClient, NewTopic

from vote_api.src.constants import KAFKA_ADDRESS


class TopicManager:
    def __init__(self):
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=KAFKA_ADDRESS,
            client_id='test'
        )

    def create_topic(self, name: str, partitions: int):
        topic_list = [NewTopic(name=name,
                               num_partitions=partitions,
                               replication_factor=len(KAFKA_ADDRESS))]
        self.admin_client.create_topics(new_topics=topic_list, validate_only=False)

    def delete_topic(self, topic_name: str):
        self.admin_client.delete_topics(topics=[topic_name])
