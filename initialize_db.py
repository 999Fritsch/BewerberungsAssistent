import sqlite3

connection = sqlite3.connect("data/assessment.db")
connection.execute("PRAGMA foreign_keys = 1")

cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS question (id INTEGER PRIMARY KEY, skill, grade, FOREIGN KEY (skill) REFERENCES skill (id))")
cursor.execute("CREATE TABLE IF NOT EXISTS skill (id INTEGER PRIMARY KEY, name)")
cursor.execute("CREATE TABLE IF NOT EXISTS applicant (id INTEGER PRIMARY KEY, score)")
cursor.execute("CREATE TABLE IF NOT EXISTS skillset (id INTEGER PRIMARY KEY, skill, grade, FOREIGN KEY (skill) REFERENCES skill (id))")
cursor.execute("CREATE TABLE IF NOT EXISTS position (id INTEGER PRIMARY KEY, name, description, skillset, FOREIGN KEY (skillset) REFERENCES skillset (id))")

result = cursor.execute("SELECT name FROM sqlite_master")
print(result.fetchall())
