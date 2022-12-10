create database if not exists vote_db;
use vote_db;

CREATE TABLE if not EXISTS Election(
id INT(10) PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(100),
timestampEnd INT(30),
description VARCHAR(500)
);

CREATE TABLE if not EXISTS VoteOption(
id INT(10) PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(100),
description VARCHAR(500),
idElection INT(10),
FOREIGN KEY (idElection) REFERENCES Election(id)
);

CREATE TABLE if not EXISTS Votes(
id INT(10) PRIMARY KEY AUTO_INCREMENT,
votes INT(10),
idVoteOption INT(10),
FOREIGN KEY (idVoteOption) REFERENCES VoteOption(id)
);

INSERT INTO Election(name, timestampEnd, description) VALUES ("Melhor filme", 1670696286, "Vote no seu filme favorito entre as opções de voto");
INSERT INTO Election(name, timestampEnd, description) VALUES ("Cor mais amada", 1670696286, "Conte para gente qual cor você gosta mais");

INSERT INTO VoteOption(name, description, idElection) VALUES ("Harry Potter e a camara secreta", "Segundo filme da saga Harry Potter", 1);
INSERT INTO VoteOption(name, description, idElection) VALUES ("O iluminado", "Filme de terror", 1);
INSERT INTO VoteOption(name, description, idElection) VALUES ("Enola Holmes", "Filme sobre a irmã do Sherlock", 1);

INSERT INTO VoteOption(name, description, idElection) VALUES ("Azul", "A cor do céu", 2);
INSERT INTO VoteOption(name, description, idElection) VALUES ("Vermelho", "A cor do sangue", 2);
INSERT INTO VoteOption(name, description, idElection) VALUES ("Amarelo", "A cor do girassol", 2);