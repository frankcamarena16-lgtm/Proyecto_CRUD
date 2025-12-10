from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os

app = Flask(__name__)

def crear_base_de_datos():
    rutaCarpetaProyecto = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    rutaBaseDeDatos = os.path.join(rutaCarpetaProyecto, "dataBase", "database.db")
    database = sqlite3.connect(rutaBaseDeDatos)
    cursor = database.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS peliculas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    año TEXT NOT NULL,
                    genero TEXT NOT NULL,
                    en_cartelera INTEGER DEFAULT 0
                    )
                """)
    database.commit()
    database.close()

crear_base_de_datos()

# <-- Página principal -->
@app.route("/")
def inicio():
    return render_template("index.html")
    
if __name__ == '__main__':
    app.run(debug=True)