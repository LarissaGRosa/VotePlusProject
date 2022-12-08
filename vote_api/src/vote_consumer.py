from kafka import KafkaConsumer

from vote_api.src.constants import KAFKA_ADDRESS


def consume(election):
    consumer = KafkaConsumer(election,
                             bootstrap_servers=KAFKA_ADDRESS,
                             api_version=(0, 10, 1),
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             consumer_timeout_ms=500)
    for message in consumer:
        #TODO contar candidatos
        print(message.value)
