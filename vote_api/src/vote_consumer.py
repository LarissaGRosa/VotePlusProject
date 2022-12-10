from kafka import KafkaConsumer
import json
import mysql.connector

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'vote_db'
}

from vote_api.src.constants import KAFKA_ADDRESS


def consume(election):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    consumer = KafkaConsumer(election,
                             bootstrap_servers=KAFKA_ADDRESS,
                             api_version=(0, 10, 1),
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             consumer_timeout_ms=500)
    election_info = dict()
    for message in consumer:

        dict = json.loads(message.decode('utf-8'))
        if dict["VoteOption"] not in list(election_info.keys()):
            election_info[dict["VoteOption"]] = 1
        else:
            election_info[dict["VoteOption"]] += 1

    for vote_option in list(election_info.key()):
        val = (election_info[vote_option], vote_option)
        sql = '''INSERT INTO Votes(votes, idVoteOption) VALUES (%d, %d)''' % val
    
    cursor.execute(sql)
    connection.commit()
    cursor.close()
    connection.close()
    