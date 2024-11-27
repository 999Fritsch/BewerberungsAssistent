import sqlite3
import helper_functions

connection = sqlite3.connect("./data/assessment.db")
connection.execute("PRAGMA foreign_keys = 1")

cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS question (id INTEGER PRIMARY KEY AUTOINCREMENT, description, skill, grade, FOREIGN KEY (skill) REFERENCES skill (id))")

cursor.execute("CREATE TABLE IF NOT EXISTS questionset (id INTEGER PRIMARY KEY, question, FOREIGN KEY (question) REFERENCES question (id))")

cursor.execute("CREATE TABLE IF NOT EXISTS skill (id INTEGER PRIMARY KEY AUTOINCREMENT, name)")
cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS skill_idx ON skill(name)")

cursor.execute("CREATE TABLE IF NOT EXISTS answer (id INTEGER PRIMARY KEY AUTOINCREMENT, description, score, application, question, FOREIGN KEY (application) REFERENCES application (id), FOREIGN KEY (question) REFERENCES question (id))")

cursor.execute("CREATE TABLE IF NOT EXISTS application (id INTEGER PRIMARY KEY AUTOINCREMENT, applicant, score)")

cursor.execute("CREATE TABLE IF NOT EXISTS skillset (id INTEGER PRIMARY KEY, skill, grade, FOREIGN KEY (skill) REFERENCES skill (id))")

cursor.execute("CREATE TABLE IF NOT EXISTS position (id INTEGER PRIMARY KEY AUTOINCREMENT, name, description TEXT, skillset, questionset, FOREIGN KEY (skillset) REFERENCES skillset (id), FOREIGN KEY (questionset) REFERENCES questionset (id))")

#cursor.execute("INSERT INTO position (id, name, description) VALUES (1, '"'testposition'"', '"'Dies ist eine Testjobbeschreibung'"')")
#connection.commit()
#print(cursor.execute("SELECT id FROM position").fetchall())

