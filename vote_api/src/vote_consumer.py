from kafka import KafkaConsumer


def consume():
    c = KafkaConsumer("exemplo", bootstrap_servers='localhost:29092', api_version=(0, 10, 1), group_id='exemplo')
    for message in c:
        print(message.value)
