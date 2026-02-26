import os
from database import db
from servicios import Recepcion
from modelos import EstadoCita
from excepciones import ClinicaError
from configuracion import configurar_logs
from datetime import datetime, timedelta

def ejecutar_pruebas():
    configurar_logs()
    print("\n🚀 INICIANDO PRUEBAS DE CHOQUE Y CONSISTENCIA TEMPORAL\n")

    # 1. Limpieza de entorno
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    db.iniciar_db()

    recepcion = Recepcion()

    try:
        # 2. Setup de datos con RUTS MATEMÁTICAMENTE VÁLIDOS
        print("--- Fase 1: Registro de Entidades (RUTs Válidos) ---")
        # RUTs reales: 19.141.061-0 (Válido), 12.345.678-5 (Inválido -> el real es K)
        p1 = recepcion.registrar_paciente("19.141.061-0", "Juan Perez", 30)
        p2 = recepcion.registrar_paciente("21.072.613-6", "Maria Lopez", 25)
        m1 = recepcion.registrar_medico("24.360.785-K", "Dr. Simi", "General", 5)
        print(f"✅ Registrados: {p1.nombre}, {p2.nombre} y {m1.nombre}")

        # 3. Prueba de Choque (Intervalos de 30 min)
        print("\n--- Fase 2: Prueba de Choque (Bloqueo de 30 min) ---")
        
        # Cita 1: 10:00 AM
        hora_base = "20-05-2026 10:00"
        recepcion.generar_cita(p1.rut, m1.rut, hora_base)
        print(f"✅ Cita 1 agendada exitosamente a las {hora_base}")

        # Intento de Cita 2: 10:15 AM (DEBE FALLAR: Está a solo 15 min de la anterior)
        hora_choque = "20-05-2026 10:15"
        print(f"⏳ Intentando agendar a las {hora_choque} (Choque esperado)...")
        try:
            recepcion.generar_cita(p2.rut, m1.rut, hora_choque)
            print("❌ ERROR: El sistema permitió un sobrecupo en el mismo intervalo.")
        except ClinicaError as e:
            print(f"✅ Éxito: Bloqueo de intervalo activo. Motivo: {e}")

        # Cita 3: 10:45 AM (DEBE FUNCIONAR: Hay justo 45 min de diferencia)
        hora_ok = "20-05-2026 10:45"
        cita3 = recepcion.generar_cita(p2.rut, m1.rut, hora_ok)
        print(f"✅ Cita 2 agendada exitosamente a las {hora_ok}")

        # 4. Prueba de Fecha Pasada
        print("\n--- Fase 3: Validación de Fecha Actual ---")
        try:
            # Intentar agendar en el año 2020
            recepcion.generar_cita(p1.rut, m1.rut, "01-01-2020 08:00")
        except ClinicaError as e:
            print(f"✅ Éxito: El sistema no vive en el pasado. Motivo: {e}")
            
        # test_automatizado.py (Fragmento de la Fase de Atraso)

        print("\n--- Fase 4: Prueba de Atraso (10:01 Rule) ---")

        # 1. Creamos una cita manualmente en la DB que sea de hace 5 minutos
        # Nota: Para el test, simulamos que la cita era hace poco para que la validación dispare
        hora_pasada = (datetime.now() - timedelta(minutes=5)).strftime("%d-%m-%Y %H:%M")

        try:
            # Intentamos generar una cita "en el pasado" (esto fallará por tu validación en utilidades)
            # Así que para el test, vamos a crear una cita válida y LUEGO manipularemos su hora
            cita_tardia = recepcion.generar_cita(p1.rut, m1.rut, "25-12-2026 10:00") # Futuro

            print("Simulando que el tiempo pasó y ahora la cita es antigua...")
            cita_tardia.fecha_hora = datetime.now() - timedelta(minutes=1) # Hace un minuto

            print(f"Intentando confirmar cita de las {cita_tardia.fecha_hora.strftime('%H:%M')} "
                  f"siendo las {datetime.now().strftime('%H:%M')}...")

            recepcion.confirmar_cita(p1.rut, cita_tardia.id)
            print("❌ ERROR: El sistema permitió confirmar una cita atrasada.")
        except ClinicaError as e:
            print(f"✅ Éxito: El sistema canceló la cita por atraso. Motivo: {e}")

        # 5. Visualización de la Agenda del Médico
        print("\n" + "="*65)
        print(f"📅 AGENDA DEL DÍA - {m1.nombre} ({m1.especialidad})")
        print("="*65)
        
        # Confirmamos la segunda cita para variar los estados
        recepcion.confirmar_cita(p2.rut, cita3.id)
        
        # Obtenemos las citas del médico y las ordenamos por hora
        agenda = sorted(m1.citas_del_dia, key=lambda x: x.fecha_hora)


        for c in agenda:
            check = " [CONFIRMADA] " if c.estado == EstadoCita.CONFIRMADA else " [RESERVADA]  "
            print(f"{c.fecha_hora.strftime('%H:%M')} | {check} | Paciente: {c.paciente.nombre.ljust(15)} | ID: {c.id}")

    except Exception as e:
        print(f"❌ Error crítico en el test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    ejecutar_pruebas()