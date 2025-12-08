import sqlite3

def crear_base_de_datos():
    database = sqlite3.connect("database.db")
    cursor = database.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS peliculas (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   titulo TEXT NOT NULL,
                   año TEXT NOT NULL,
                   genero TEXT NOT NULL
                   )
                """)
    database.commit()
    database.close()

crear_base_de_datos()
    