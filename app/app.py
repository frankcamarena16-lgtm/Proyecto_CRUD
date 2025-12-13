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
                    año DATE NOT NULL,
                    genero TEXT NOT NULL,
                    en_cartelera INTEGER DEFAULT 0
                    )
                """)
    database.commit()
    # Comprobar si la columna 'en_cartelera' existe; si no, agregarla
    cursor.execute("PRAGMA table_info(peliculas)")
    cols = [row[1] for row in cursor.fetchall()]
    if 'en_cartelera' not in cols:
        cursor.execute("ALTER TABLE peliculas ADD COLUMN en_cartelera INTEGER DEFAULT 0")
        database.commit()

    database.close()

crear_base_de_datos()

# <-- Página principal -->
@app.route("/")
def inicio():
    conn = get_db_connection()
    peliculas_data = conn.execute('SELECT id, titulo, año, genero, en_cartelera FROM peliculas').fetchall()
    conn.close()

    cartelera = []
    antiguas = []

    for p in peliculas_data:
        if p['en_cartelera'] == 1:
            cartelera.append(p)
        else:
            antiguas.append(p)

    return render_template(
        'index.html',
        peliculas=peliculas_data,  # TODAS solo para la tabla
        cartelera=cartelera,       # Solo cartelera
        antiguas=antiguas          # Solo antiguas
    )


@app.route('/agregar')
def agregar():
    return render_template('agregar.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    titulo = request.form['titulo']
    año = request.form['año']
    genero = request.form['genero']
    en_cartelera = 1 if 'en_cartelera' in request.form else 0
    
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO peliculas (titulo, año, genero, en_cartelera) 
        VALUES (?, ?, ?, ?)
    """, (titulo, año, genero, en_cartelera))
    conn.commit()
    conn.close()
    
    return redirect('/')

@app.route('/editar/<int:id>')
def editar(id):
    conn = get_db_connection()
    pelicula = conn.execute('SELECT * FROM peliculas WHERE id = ?', (id,)).fetchone()
    conn.close()
    if pelicula is None:
        return "Película no encontrada", 404

    return render_template('editar.html', pelicula=pelicula)

@app.route('/editar/<int:id>', methods=['POST'])
def actualizar(id):
    titulo = request.form['titulo']
    año = request.form['año']
    genero = request.form['genero']
    en_cartelera = 1 if 'en_cartelera' in request.form else 0

    conn = get_db_connection()
    conn.execute("""
        UPDATE peliculas 
        SET titulo = ?, año = ?, genero = ?, en_cartelera = ?
        WHERE id = ?
    """, (titulo, año, genero, en_cartelera, id))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM peliculas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    reorganizar_ids()
    return redirect('/')


def reorganizar_ids():
    conn = get_db_connection()
    peliculas = conn.execute('SELECT titulo, año, genero, en_cartelera FROM peliculas ORDER BY id').fetchall()
    conn.execute('DELETE FROM peliculas')
    conn.execute("DELETE FROM sqlite_sequence WHERE name='peliculas'")
    for p in peliculas:
        conn.execute('INSERT INTO peliculas (titulo, año, genero, en_cartelera) VALUES (?, ?, ?, ?)', p)
    conn.commit()
    conn.close()
    

    
if __name__ == '__main__':
    app.run(debug=True)