from typing import List, Dict
import mysql.connector
import hashlib
from vote_api.src.topic_manager import TopicManager
from vote_api.src.vote_producer import VoteProducer
import time
from multiprocessing import Process
from vote_api.src.vote_consumer import consume
from vote_api.src.constants import KAFKA_ADDRESS

config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '3306',
    'database': 'vote_db'
}
vote_producer = VoteProducer()

# TODO: Arrumar para ter apenas uma conexão com db sempre ativa

def search_elections() -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    time_now = time.time()
    cursor.execute(f'SELECT * FROM Election WHERE timestampEnd >= {time_now}')
    election_list = cursor.fetchall()
    results = [{"id": x[0], "name": x[1], "description": x[2]} for x in election_list]
    cursor.close()
    connection.close()
    return results


def get_election_options(content) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    election = content['idElection']
    cursor.execute(f'SELECT * FROM VoteOption WHERE idElection = {election}')
    option_list = cursor.fetchall()
    results = [{"id": x[0], "name": x[1], "description": x[3]} for x in option_list]
    cursor.close()
    connection.close()
    return results


def create_election(content):
    manager = TopicManager()
    hash_name = hashlib.sha256(content['name'].encode('UTF-8'))
    manager.create_topic(hash_name.hexdigest(), len(KAFKA_ADDRESS))
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    val = (content['name'], content['timeEnd'], content['description'])
    sql = '''INSERT INTO Election(name, timestampEnd, description) VALUES (\"%s\", %d, \"%s\")''' % val
    try:
        cursor.execute(sql)

        if cursor.lastrowid:
            election = cursor.lastrowid
            print('last insert id', cursor.lastrowid)
            for i in content['options']:
                v = (i['name'], i['description'], election)
                s = '''INSERT INTO VoteOption(name, description, idElection) VALUES (\"%s\", \"%s\", %d)''' % v
                cursor.execute(s)
        else:
            print('last insert id not found')

        connection.commit()
    except Error as error:
        print(error)
        return error, 500

    finally:
        cursor.close()
        connection.close()
        return '', 204

def send_vote(content):
    hash_name = hashlib.sha256(content['name'].encode('UTF-8'))
    vote_option = int(content['voteOption'])
    vote_producer.send_vote(hash_name.hexdigest(), vote_option)
    return '', 204

def get_election_result(content):
    election = content['name']
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute(f'SELECT timestampEnd FROM Election WHERE Election.name = "{election}"')
    election_time = cursor.fetchall()
    time_now = time.time()

    if (election_time and election_time[0][0] > time_now):
        return "Eleição em andamento"

    cursor.execute(f'SELECT v.votes, vo.description FROM Election e, VoteOption vo, Votes v WHERE e.id = vo.idElection and vo.id = v.idVoteOption and e.name = "{election}"')
    option_list = cursor.fetchall()
    option_size = cursor.rowcount
    cursor.close()
    connection.close()

    if(option_size == 0):
        hash_name = hashlib.sha256(content['name'].encode('UTF-8'))
        p = Process(target=consume, args=(hash_name.hexdigest(),))
        p.start()
        return "Eleição está em contagem"

    results = [{"votes": x[0], "description": x[1]} for x in option_list]
   
    return results
    