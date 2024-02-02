from flask import Flask, render_template, request, redirect
import requests
import psycopg2
from dotenv import load_dotenv
import os
import sys

# Obtener la ruta al directorio 'main' (un nivel arriba de donde se encuentra este archivo)
basedir = os.path.abspath(os.path.dirname(__file__))
main_dir = os.path.join(basedir, '..')
sys.path.append(main_dir)

# Cargar las variables de entorno desde .env (dentro del directorio 'main')
load_dotenv(os.path.join(main_dir, 'main', '.env'))

# Importar funciones desde models.contact después de cargar las variables de entorno
from models.contact import crear_tabla_si_no_existe

app = Flask(__name__, template_folder='.')

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.environ['DATABASE_URL']

# Llamar a la función para crear la tabla
crear_tabla_si_no_existe()


def insertar_datos(nombre, apellido, email, telefono):
    # Conexión a la base de datos
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    # Ejecutar la consulta SQL
    cur.execute("INSERT INTO datos_usuario (nombre, apellido, email, telefono) VALUES (%s, %s, %s, %s)", 
                (nombre, apellido, email, telefono))
    conn.commit()
    cur.close()
    conn.close()

def enviar_datos_al_sistema_central(nombre, apellido, email, telefono):
    # URL del sistema central (reemplazar con la URL real)
    url_sistema_central = 'http://url_del_sistema_central.com/api'
    datos = {
        'nombre': nombre,
        'apellido': apellido,
        'email': email,
        'telefono': telefono
    }
    # Enviar los datos al sistema central
    response = requests.post(url_sistema_central, json=datos)
    return response.status_code

@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/submit', methods=['POST'])
def submit():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    telefono = request.form['telefono']

    # Insertar datos en la base de datos
    insertar_datos(nombre, apellido, email, telefono)

    # Enviar datos al sistema central
    status = enviar_datos_al_sistema_central(nombre, apellido, email, telefono)
    print("Estado del envío:", status)

    # Redirigir a la página de confirmación
    return render_template('datos_recibidos.html')

if __name__ == '__main__':
    app.run(debug=True)