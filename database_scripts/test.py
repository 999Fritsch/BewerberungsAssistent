import sqlite3

connection = sqlite3.connect("./data/assessment.db")

cursor = connection.cursor()

cursor.execute("SELECT * FROM skillset")

print(cursor.fetchall())