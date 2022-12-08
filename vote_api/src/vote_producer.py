from kafka import KafkaProducer
from vote_api.src.constants import KAFKA_ADDRESS


class VoteProducer:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=KAFKA_ADDRESS,
                                      api_version=(0, 10, 1))

    def send_vote(self, election, msg):
        self.producer.send(election, bytes(msg, encoding='utf-8'))

    def wait_for_message_delivery(self):
        self.producer.flush()
