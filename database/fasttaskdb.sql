-- Active: 1767155769831@@localhost@3306@fasttaskdb
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    username VARCHAR(20) NOT NULL,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    date_of_birth DATE,
    profile_picture_url VARCHAR(255),
    user_level INT DEFAULT 1,
    xp_points INT DEFAULT 0,
    PRIMARY KEY(user_id)
);

CREATE TABLE IF NOT EXISTS tasks (
    user_id BIGINT NOT NULL,
    taskID VARCHAR(36) NOT NULL,
    taskName VARCHAR(100) NOT NULL,
    notes TEXT,
    deadline DATETIME NOT NULL,
    remindAt DATETIME,
    PRIMARY KEY(taskID),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

DROP TABLE users;
DROP TABLE tasks;