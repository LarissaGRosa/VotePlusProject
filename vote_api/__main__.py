from vote_api.front.view import *

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


if __name__ == '__main__':
    app.run(host='0.0.0.0')
