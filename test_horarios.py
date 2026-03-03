import os
from datetime import datetime, timedelta

# Importamos los módulos de tu sistema
from database import db
from servicios import Recepcion
from excepciones import ClinicaError

def ejecutar_pruebas():
    print("="*50)
    print("🚀 INICIANDO PRUEBAS DE DISPONIBILIDAD DE HORARIOS")
    print("="*50)

    # 1. Limpiar la base de datos (Eliminamos el archivo si existe)
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
        print("[✔] Base de datos anterior eliminada para prueba limpia.")

    # 2. Iniciar base de datos y sistema
    db.iniciar_db()
    recepcion = Recepcion()
    # Aunque esté vacía, es buena práctica llamar a la carga
    recepcion.cargar_datos_desde_db() 
    print("[✔] Sistema inicializado correctamente.\n")

    # 3. Preparar Datos de Prueba
    rut_paciente = "19.141.061-0"
    rut_medico = "24.360.785-K"
    
    # Usamos la fecha de mañana para asegurar que los bloques no hayan pasado
    fecha_dt = datetime.now() + timedelta(days=1)
    fecha_str = fecha_dt.strftime("%d-%m-%Y")

    print("--- REGISTRANDO ENTIDADES ---")
    recepcion.registrar_paciente(rut_paciente, "Juan Perez", 30)
    # Médico con jornada de 08:00 a 17:00 y almuerzo de 13:00 a 14:00
    recepcion.registrar_medico(rut_medico, "Dr. House", "Medicina General", 10)
    print("[✔] Paciente y Médico registrados con éxito.\n")

    # ---------------------------------------------------------
    # PRUEBA 1: Consultar disponibilidad inicial
    # ---------------------------------------------------------
    print(f"--- PRUEBA 1: Disponibilidad inicial para el {fecha_str} ---")
    libres = recepcion.obtener_disponibilidad_medico(rut_medico, fecha_str)
    print(f"Bloques libres: {len(libres)}")
    print(f"Primeros bloques: {libres[:4]} ...")
    assert "10:00" in libres, "El bloque de las 10:00 debería estar libre."
    assert "13:30" not in libres, "El bloque de las 13:30 (almuerzo) NO debería estar libre."
    print("✅ PRUEBA 1 SUPERADA\n")

    # ---------------------------------------------------------
    # PRUEBA 2: Agendar una cita válida
    # ---------------------------------------------------------
    print("--- PRUEBA 2: Agendar cita válida a las 10:00 ---")
    try:
        fecha_cita_str = f"{fecha_str} 10:00"
        cita = recepcion.generar_cita(rut_paciente, rut_medico, fecha_cita_str)
        print(f"[✔] Cita generada exitosamente. ID: {cita.id}")
        print("✅ PRUEBA 2 SUPERADA\n")
    except ClinicaError as e:
        print(f"❌ Falló la Prueba 2: {e}")

    # ---------------------------------------------------------
    # PRUEBA 3: Validar que el bloque ya no está disponible
    # ---------------------------------------------------------
    print("--- PRUEBA 3: Consultar disponibilidad post-agendamiento ---")
    libres_actualizados = recepcion.obtener_disponibilidad_medico(rut_medico, fecha_str)
    if "10:00" not in libres_actualizados:
        print("[✔] El bloque de las 10:00 ya no aparece en la lista de disponibles.")
        print("✅ PRUEBA 3 SUPERADA\n")
    else:
        print("❌ Falló la Prueba 3: Las 10:00 sigue apareciendo disponible.")

    # ---------------------------------------------------------
    # PRUEBA 4: Intentar agendar en un bloque ocupado
    # ---------------------------------------------------------
    print("--- PRUEBA 4: Intentar chocar horarios (Agendar a las 10:00 de nuevo) ---")
    try:
        recepcion.generar_cita(rut_paciente, rut_medico, f"{fecha_str} 10:00")
        print("❌ Falló la Prueba 4: El sistema permitió agendar sobre una hora ocupada.")
    except ClinicaError as e:
        print(f"[✔] El sistema bloqueó la cita correctamente. Mensaje: {e}")
        print("✅ PRUEBA 4 SUPERADA\n")

    # ---------------------------------------------------------
    # PRUEBA 5: Intentar agendar en hora de almuerzo
    # ---------------------------------------------------------
    print("--- PRUEBA 5: Intentar agendar en colación (13:30) ---")
    try:
        recepcion.generar_cita(rut_paciente, rut_medico, f"{fecha_str} 13:30")
        print("❌ Falló la Prueba 5: El sistema permitió agendar en hora de almuerzo.")
    except ClinicaError as e:
        print(f"[✔] El sistema bloqueó la cita correctamente. Mensaje: {e}")
        print("✅ PRUEBA 5 SUPERADA\n")

    # ---------------------------------------------------------
    # PRUEBA 6: Intentar agendar fuera de jornada
    # ---------------------------------------------------------
    print("--- PRUEBA 6: Intentar agendar fuera de horario (18:30) ---")
    try:
        recepcion.generar_cita(rut_paciente, rut_medico, f"{fecha_str} 18:30")
        print("❌ Falló la Prueba 6: El sistema permitió agendar fuera de turno.")
    except ClinicaError as e:
        print(f"[✔] El sistema bloqueó la cita correctamente. Mensaje: {e}")
        print("✅ PRUEBA 6 SUPERADA\n")

    print("="*50)
    print("🎉 TODAS LAS PRUEBAS FINALIZADAS 🎉")
    print("="*50)

if __name__ == "__main__":
    ejecutar_pruebas()