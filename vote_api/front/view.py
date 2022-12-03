from typing import List, Dict
from flask import Flask, request, jsonify
import mysql.connector
import json
import time
from vote_api.front.vote_producer import VoteProducer
import time

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
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
    election = int(content['idElection'])
    time_now = time.time()
    vote_option = int(content['voteOption'])
    message = {"Election": election,
                "VoteTime": time_now,
                "VoteOption": vote_option}
    vote_producer.send_vote("exemplo", str(message)) #exemplo is the topic and message has the subject of the given election to vote
    return '', 204