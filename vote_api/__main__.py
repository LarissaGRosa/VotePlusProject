from vote_api.front.view import *
from vote_api.src.vote_producer import *

app = Flask(__name__)
producer = VoteProducer()


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


if __name__ == '__main__':
    print("a")
    producer.send_vote('exemplo', b'votacao1')
    print("b")
    producer.send_vote('exemplo', b'votacao2')
    print("c")
    producer.send_vote('exemplo', b'votacao1')
    print("d")
    producer.send_vote('exemplo', b'votacao3')
    print("e")
    producer.send_vote('exemplo', b'votacao1')
    app.run(host='0.0.0.0')
