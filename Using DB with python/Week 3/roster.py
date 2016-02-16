import json
import sqlite3

connection = sqlite3.connect("roster.sqlite")
cursor = connection.cursor()

cursor.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')


with open("roster_data.json","r") as f:
	str_data = f.read()

json_data = json.loads(str_data)

for entry in json_data:

    name = entry[0];
    title = entry[1];
    role = entry[2];

    #print name, title

    cursor.execute('''INSERT OR IGNORE INTO User (name) 
        VALUES ( ? )''', ( name, ) )
    cursor.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = cursor.fetchone()[0]

    cursor.execute('''INSERT OR IGNORE INTO Course (title) 
        VALUES ( ? )''', ( title, ) )
    cursor.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cursor.fetchone()[0]

    cursor.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ?, ?)''', 
        ( user_id, course_id, role ) )
connection.commit()