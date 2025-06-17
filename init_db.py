import sqlite3

connection = sqlite3.connect('warehouse.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    location TEXT NOT NULL
)
''')

connection.commit()
connection.close()