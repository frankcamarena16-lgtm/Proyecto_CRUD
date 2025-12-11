from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_NAME = os.path.join(BASE_DIR, "dataBase", "database.db")


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def crear_base_de_datos():
    rutaBaseDeDatos = DB_NAME
    # Asegurarse de que la carpeta exista
    os.makedirs(os.path.dirname(rutaBaseDeDatos), exist_ok=True)
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
    # Comprobar si la columna 'en_cartelera' existe; si no, agregarla (para migraciones)
    cursor.execute("PRAGMA table_info(peliculas)")
    cols = [row[1] for row in cursor.fetchall()]
    if 'en_cartelera' not in cols:
        cursor.execute("ALTER TABLE peliculas ADD COLUMN en_cartelera INTEGER DEFAULT 0")
        database.commit()

    database.close()

crear_base_de_datos()
@app.route("/insertar_demo")
def insertar_demo():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO peliculas (titulo, año, genero, en_cartelera)
        VALUES
        ('The Shawshank Redemption', 1994, 'Drama', 1),
        ('The Dark Knight', 2008, 'Acción', 1),
        ('Interstellar', 2014, 'Ciencia Ficción', 0),
        ('Inception', 2010, 'Ciencia Ficción', 0),
        ('Pulp Fiction', 1994, 'Crimen', 1)
    """)
    conn.commit()
    conn.close()
    return "Películas insertadas 👍"

# <-- Página principal -->
@app.route("/")
def inicio():
    conn = get_db_connection()
    

    peliculas_data = conn.execute('SELECT id, titulo, año, genero, en_cartelera FROM peliculas ORDER BY año DESC').fetchall()
    conn.close()

    peliculas = []     
    cartelera = []  
    antiguas = []   

    for p in peliculas_data:

        peliculas.append((p['id'], p['titulo'], p['año'], p['genero'])) 
        if p['en_cartelera'] == 1:
            cartelera.append(p)
        else:
            antiguas.append(p)

    return render_template('index.html', peliculas=peliculas, cartelera=cartelera, antiguas=antiguas)

@app.route('/agregar')
def agregar():
    return render_template('agregar.html')

@app.route('/editar')
def editar():
    return render_template('editar.html')
    
if __name__ == '__main__':
    app.run(debug=True)