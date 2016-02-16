#!/usr/bin/python2
import sqlite3

connection = sqlite3.connect('emaildb.sqlite')
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS Counts")

cursor.execute("CREATE TABLE Counts(org TEXT, count INTEGER) ")

with open("../mbox.txt", "r") as f:
	lines = f.readlines()

emails = {}

for line in lines:
	if line.startswith("From: "):
		pieces = line.split()
		email = pieces[1]
		#print email
		domain = email.split("@")[1]
		user = email.split("@")[0]
		if domain in emails.keys():
			emails[domain] += 1
		else:
			emails[domain] = 1

for key in emails.keys():
	print key, emails[key]
	cursor.execute("INSERT INTO Counts (org, count) VALUES (?,?)", (key, emails[key]));

connection.commit()
cursor.close()