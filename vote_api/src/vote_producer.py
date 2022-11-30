from kafka import KafkaProducer
from vote_api.src.constants import KAFKA_ADDRESS


class VoteProducer:
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=KAFKA_ADDRESS,
                                      api_version=(0, 10, 1))
        self.count = 0

    def send_vote(self, election, msg):
        self.producer.send(election, bytes(msg))
        self.count += 1
        if self.count > 5:
            self.producer.flush()
            self.count = 0
