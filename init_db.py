import sqlite3
from config import DB_PATH

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

# Items table
cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    location TEXT NOT NULL
)
''')

# Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    street TEXT NOT NULL,
    state TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

connection.commit()
connection.close()

print("Database initialized successfully.")
