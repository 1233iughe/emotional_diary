--Here we eliminate previous tables with the same name and create our new tables
DROP TABLE IF EXISTS users;
DROP TABlE IF EXISTS settings;
DROP TABLE IF EXISTS register;

--Base table contains basic information about each user (username, password hash and security phrase hash)
CREATE TABLE users( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    hash TEXT NOT NULL,
    security_phrase TEXT NOT NULL
);

--This table is connected to 'users' by user_id column. There should be a row and only
--a row per user. Here we store the user configurationf of emotion-color pairs as strings
--to be converted back in dictionaries using json module function json.loads().
CREATE TABLE settings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    colors TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

--In this table we register the emotion-color values set by the users to each day.
--This table is connected to 'users' by user_id column. 
CREATE TABLE register(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    value TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);