import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'clinica.db')

def conectar():
    """ Establece conexion y activa las llaves foráneas. """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def iniciar_db():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
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
                    capacidad INTEGER NOT NULL,
                    hora_inicio TEXT NOT NULL,
                    hora_fin TEXT NOT NULL,
                    inicio_almuerzo TEXT NOT NULL,
                    fin_almuerzo TEXT NOT NULL
                )
            """)
            # tabla de citas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS citas(
                    id INTEGER PRIMARY KEY,
                    rut_paciente TEXT,
                    rut_medico TEXT,
                    estado TEXT,
                    fecha_hora DATETIME,
                    FOREIGN KEY (rut_paciente) REFERENCES pacientes(rut),
                    FOREIGN KEY (rut_medico) REFERENCES medicos(rut)
                )
            """)
            conn.commit()
            print("Estructura de base de datos preparada con exito")

    except sqlite3.Error as e:
        print(f"Error al crear las tablas: {e}")

# ----- registrar y obtener pacientes -----
def insertar_paciente(paciente):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pacientes VALUES (?,?,?)", 
                        (paciente.rut, paciente.nombre, paciente.edad))

def obtener_todos_los_pacientes():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pacientes")
        return cursor.fetchall()

# ----- registrar y obtener medicos -----
def insertar_medico(medico):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO medicos VALUES (?,?,?,?,?,?,?,?)",
                        (medico.rut, medico.nombre, medico.especialidad, medico.capacidad_atencion,
                        medico.hora_inicio, medico.hora_fin, medico.inicio_almuerzo, medico.fin_almuerzo))

def obtener_todos_los_medicos():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medicos")
        return cursor.fetchall()

# ----- registrar y obtener citas -----
def insertar_cita(cita):
    with conectar() as conn:
        cursor = conn.cursor()
        fecha_iso = cita.fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO citas (id, rut_paciente, rut_medico, estado, fecha_hora) VALUES (?,?,?,?,?)",
                        (cita.id, cita.paciente.rut, cita.medico.rut, cita.estado.value, fecha_iso))

def actualizar_estado_cita(id_cita, nuevo_estado):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE citas SET estado = ? WHERE id = ?", (nuevo_estado, id_cita))

def obtener_citas():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM citas")
        return cursor.fetchall()
