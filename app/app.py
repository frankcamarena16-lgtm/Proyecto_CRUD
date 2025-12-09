from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

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
    
if __name__ == '__main__':
    app.run(debug=True)