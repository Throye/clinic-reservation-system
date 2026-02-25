from main import Recepcion
from database import db
import random

def poblar_sistema():
    print("🚀 Iniciando carga de datos de prueba...")
    
    # 1. Asegurar que la base de datos esté lista
    db.iniciar_db()
    
    recepcion = Recepcion()
    # No cargamos desde DB porque queremos insertar datos nuevos y limpios
    
    # --- 3 Médicos ---
    medicos_data = [
        ("11.111.111-1", "Dr. Hannibal Lecter", "Psiquiatría", 15),
        ("22.222.222-2", "Dra. Dana Scully", "Patología", 10),
        ("33.333.333-3", "Dr. Stephen Strange", "Neurocirugía", 8)
    ]
    
    print("🩺 Registrando médicos...")
    for m in medicos_data:
        try:
            recepcion.registrar_medico(*m)
        except Exception as e:
            print(f"Nota: Medico {m[1]} ya existía o hubo error: {e}")

    # --- 10 Pacientes ---
    pacientes_data = [
        ("1-1", "Paciente Uno", 20), ("2-2", "Paciente Dos", 25),
        ("3-3", "Paciente Tres", 30), ("4-4", "Paciente Cuatro", 35),
        ("5-5", "Paciente Cinco", 40), ("6-6", "Paciente Seis", 45),
        ("7-7", "Paciente Siete", 50), ("8-8", "Paciente Ocho", 55),
        ("9-9", "Paciente Nueve", 60), ("10-10", "Paciente Diez", 65)
    ]
    
    print("👤 Registrando pacientes...")
    for p in pacientes_data:
        try:
            recepcion.registrar_paciente(*p)
        except Exception as e:
            print(f"Nota: Paciente {p[1]} ya existía o hubo error: {e}")

    # --- Citas (3 a 5 por paciente) ---
    print("📅 Generando citas masivas...")
    medicos_ruts = [m[0] for m in medicos_data]
    
    for p_rut, _, _ in pacientes_data:
        cantidad_citas = random.randint(3, 5)
        for _ in range(cantidad_citas):
            m_rut = random.choice(medicos_ruts)
            try:
                recepcion.generar_cita(p_rut, m_rut)
            except Exception as e:
                print(f"No se pudo crear cita para {p_rut}: {e}")

    print(f"\n✅ Carga completada.")
    print(f"Total en memoria: {len(recepcion.pacientes)} pacientes, {len(recepcion.medicos)} médicos.")

if __name__ == "__main__":
    poblar_sistema()