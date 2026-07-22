import sqlite3

with open("schema.sql", "r") as f:
    schema = f.read()

connection = sqlite3.connect("tracker.db")
connection.execute("PRAGMA foreign_keys = ON")
connection.executescript(schema)
connection.commit()
connection.close()

print("Database created successfully.")
