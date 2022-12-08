import json
from urllib import request

from flask import Flask
from kafka import KafkaConsumer, TopicPartition

from vote_api.front.view import *
from vote_api.src.constants import KAFKA_ADDRESS
from vote_api.src.topic_manager import TopicManager
from vote_api.src.vote_consumer import consume

app = Flask(__name__)


@app.route('/listElections', methods=['GET'])
def get_open_elections() -> str:
    return json.dumps({'Elections': search_elections()})


@app.route('/getElectionOptions', methods=['POST'])
def get_options() -> str:
    return json.dumps({'Options': get_election_options(request.get_json())})


@app.route('/createElection', methods=['POST'])
def add_election():
    content = request.get_json()
    return create_election(content)

@app.route('/voteElection', methods=['POST'])
def vote_election():
    content = request.get_json()
    return send_vote(content)

def exemplo():
    TopicManager().create_topic("exemplo", 3)
    example_producer = VoteProducer()
    for i in range(5):
        example_producer.send_vote("exemplo", "ele gosta")
    consume("exemplo")
    TopicManager().delete_topic("exemplo")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
