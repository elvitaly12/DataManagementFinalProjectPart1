CREATE DATABASE beautipoll;

CREATE TABLE Users (
    username VARCHAR (20) PRIMARY KEY,
    chat_id INT NOT NULL,
    active BOOLEAN NOT NULL,
);

CREATE TABLE Admins (
    username VARCHAR (20) PRIMARY KEY,
    password VARCHAR (20) NOT NULL,
);

CREATE TABLE Polls (
    poll_id INT PRIMARY KEY,
);

CREATE TABLE Questions (
    question_id INT PRIMARY KEY,
    poll_id INT NOT NULL,
    description VARCHAR (300) NOT NULL,
    FOREIGN KEY (poll_id) REFERENCES Polls (poll_id)
);

CREATE TABLE Answers (
    answer_id INT PRIMARY KEY,
    question_id INT NOT NUL,
    description VARCHAR (150) NOT NULL,
    FOREIGN KEY (question_id) REFERENCES Questions (question_id)
);

CREATE TABLE PollsAnswers (
    username VARCHAR (20) PRIMARY KEY,
    poll_id INT PRIMARY KEY,
    question_id INT PRIMARY KEY,
    answer_id INT PRIMARY KEY,
    FOREIGN KEY (username) REFERENCES Users (username)
    FOREIGN KEY (poll_id) REFERENCES Polls (poll_id)
    FOREIGN KEY (question_id) REFERENCES Questions (question_id)
    FOREIGN KEY (answer_id) REFERENCES Answers (answer_id)
);

----CREATE VIEW ActiveUsers (
----    username VARCHAR (20) PRIMARY KEY,
----    FOREIGN KEY (username) REFERENCES Users (username)
----);
--
--CREATE VIEW ActiveUsers AS
--SELECT username
--FROM Users
--WHERE active=TRUE;