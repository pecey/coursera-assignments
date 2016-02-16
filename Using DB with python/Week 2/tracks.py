#!/usr/bin/python2
import sqlite3
import xml.etree.ElementTree as ET 

def lookup(entry, key):
	found = False
	for child in entry:
		if found:
			return child.text
		if child.tag == "key" and child.text == key:
			print "Match"
			found = True
	return None


tree = ET.parse("tracks/Library.xml")




# Find all the track nodes
dict_node = tree.findall("dict/dict/dict")

tracksDB = []

# Gather the data required to build the DB
for node in dict_node:
	#print node
	track = {}
	track['title'] = lookup(node, "Name")
	track['length'] = lookup(node, "Total Time")
	track['rating'] = lookup(node, "Rating")
	track['count'] = lookup(node, "Play Count")
	track['artist'] = lookup(node, "Artist")
	track['genre'] = lookup(node, "Genre")
	track['album'] = lookup(node, "Album")
	if track['title'] is None or track['artist'] is None or track['album'] is None or track['genre'] is None:
		continue
	else:
		tracksDB.append(track)

print tracksDB

connection = sqlite3.connect("tracks.sqlite")
cursor = connection.cursor()

# Drop tables if exist
cursor.execute("DROP TABLE IF EXISTS Artist")
cursor.execute("DROP TABLE IF EXISTS Genre")
cursor.execute("DROP TABLE IF EXISTS Album")
cursor.execute("DROP TABLE IF EXISTS Track")

# Create new tables
cursor.execute('''CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
)''')
cursor.execute('''CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
)''')
cursor.execute('''CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
)''')
cursor.execute('''CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
)''')

#print tracksDB
for track in tracksDB:
	# Insert Genre
	cursor.execute("INSERT OR IGNORE INTO Genre(name) VALUES(?)",(track['genre'],))
	cursor.execute("SELECT id FROM Genre WHERE name = ?", (track['genre'],))
	genre_id = cursor.fetchone()[0]

	# Insert artist
	cursor.execute("INSERT OR IGNORE INTO Artist(name) VALUES(?)",(track['artist'],))
	cursor.execute("SELECT id FROM Artist WHERE name = ?", (track['artist'],))
	artist_id = cursor.fetchone()[0]

	# Insert album
	cursor.execute("INSERT OR IGNORE INTO Album(artist_id, title) VALUES(?,?)",(artist_id,track['album'],))
	cursor.execute("SELECT id FROM Album WHERE title = ?", (track['album'],))
	album_id = cursor.fetchone()[0]

	# Insert track
	cursor.execute("INSERT OR IGNORE INTO Track(title, album_id, genre_id, len, rating, count) VALUES(?,?,?,?,?,?)",(track['title'],album_id, genre_id, track['length'], track['rating'], track['count'],))

connection.commit()
cursor.close()