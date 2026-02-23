import sqlite3

def conectar():
    return sqlite3.connect('database/clinica.db')


def iniciar_db():
    cursor.execute("PRAGMA foreign_keys = ON")
    try:
        with sqlite3.connect('database/clinica.db') as conn:
            cursor = conn.cursor()
            # tabla de pacientes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pacientes(
                    rut TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    edad INTEGER
                )
            """)
            # tabla de medicos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS medicos(
                    rut TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    especialidad TEXT NOT NULL,
                    capacidad INTEGER NOT NULL
                )
            """)
            # tabla de citas
            cursor.execute("""
                CREATE TABLE IF NOT EXIST citas(
                    id INTEGER PRIMARY KEY,
                    rut_paciente TEXT,
                    rut_medico TEXT,
                    estado TEXT,
                    FOREIGN KEY (rut_paciente) REFERENCES pacientes(rut),
                    FOREIGN KEY (rut_medico) REFERENCES (medicos(rut))
                )
            """)
            conn.commit()
            print("Estructura de base de datos preparada con exito")

    except sqlite3.Error as e:
        print(f"Error al crear las tablas: {e}")