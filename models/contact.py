import psycopg2
import os

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.environ['DATABASE_URL']

def crear_tabla_si_no_existe():
    try:
        # Conexión a la base de datos
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Verificar si la tabla existe
        cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'datos_usuario')")
        table_exists = cur.fetchone()[0]

        if not table_exists:
            # La tabla no existe, crearla
            cur.execute("""
                CREATE TABLE datos_usuario (
                    id serial PRIMARY KEY,
                    nombre VARCHAR(255),
                    apellido VARCHAR(255),
                    email VARCHAR(255),
                    telefono VARCHAR(255)
                )
            """)
            conn.commit()

        cur.close()
        conn.close()
    except Exception as e:
        print("Error al crear la tabla:", e)