import sqlite3 as sql

PATH_DB = 'bot_mem.db'

def db_connection():
    connection = sql.Connection(PATH_DB)
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                    (id_user INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name_user TEXT, 
                    surname_user TEXT,
                    telegram_id INTEGER)''')
    connection.commit()

