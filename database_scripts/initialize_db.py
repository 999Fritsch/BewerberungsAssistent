import sqlite3
import helper_functions

connection = sqlite3.connect("./data/assessment.db")
connection.execute("PRAGMA foreign_keys = 1")

cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS question (id INTEGER PRIMARY KEY AUTOINCREMENT, skill, grade, FOREIGN KEY (skill) REFERENCES skill (id))")
cursor.execute("CREATE TABLE IF NOT EXISTS skill (id INTEGER PRIMARY KEY AUTOINCREMENT, name)")
cursor.execute("CREATE TABLE IF NOT EXISTS applicant (id INTEGER PRIMARY KEY AUTOINCREMENT, score)")
cursor.execute("CREATE TABLE IF NOT EXISTS skillset (id INTEGER PRIMARY KEY AUTOINCREMENT, skill, grade, FOREIGN KEY (skill) REFERENCES skill (id))")
cursor.execute("CREATE TABLE IF NOT EXISTS position (id INTEGER PRIMARY KEY AUTOINCREMENT, name, description TEXT, skillset, FOREIGN KEY (skillset) REFERENCES skillset (id))")

#cursor.execute("INSERT INTO position (id, name, description) VALUES (1, '"'testposition'"', '"'Dies ist eine Testjobbeschreibung'"')")
#connection.commit()
print(cursor.execute("SELECT id FROM position").fetchall())

