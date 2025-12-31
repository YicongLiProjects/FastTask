-- Active: 1767155769831@@localhost@3306@fasttaskdb
CREATE TABLE IF NOT EXISTS users (
    email VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    username VARCHAR(20) NOT NULL,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    date_of_birth DATE,
    profile_picture_url VARCHAR(255),
    PRIMARY KEY(email)
);

CREATE TABLE IF NOT EXISTS tasks (
    taskID VARCHAR(36) NOT NULL,
    taskName VARCHAR(100) NOT NULL,
    notes TEXT,
    deadline DATETIME,
    remindAt DATETIME,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY(taskID),
    FOREIGN KEY(email) REFERENCES users(email)
);