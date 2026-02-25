import os
from database import db
from servicios import Recepcion
from modelos import EstadoCita, Cita
from excepciones import ClinicaError
from configuracion import configurar_logs

def ejecutar_pruebas():
    configurar_logs()
    print("🧪 INICIANDO AUTOMATIZACIÓN DE PRUEBAS\n")

    # 1. Preparación del entorno (Limpiamos la DB para una prueba limpia)
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    db.iniciar_db()

    recepcion = Recepcion()

    try:
        # 2. Registro de Entidades
        print("--- Fase 1: Registro ---")
        recepcion.registrar_paciente("1-1", "Test Paciente", 25)
        recepcion.registrar_medico("10-10", "Test Medico", "General", 2)
        print("✅ Paciente y Médico registrados.")

        # 3. Flujo de Citas
        print("\n--- Fase 2: Flujo de Citas ---")
        cita = recepcion.generar_cita("1-1", "10-10")
        print(f"✅ Cita generada (ID: {cita.id}) - Estado inicial: {cita.estado.value}")

        recepcion.confirmar_cita("1-1", cita.id)
        print(f"✅ Cita confirmada - Estado: {cita.estado.value}")

        # 4. Prueba de Inconsistencias (Forzar errores)
        print("\n--- Fase 3: Pruebas de Error (Inconsistencias) ---")
        try:
            # Intentar confirmar algo ya confirmado debería dar error según tu lógica
            recepcion.confirmar_cita("1-1", cita.id)
        except ClinicaError as e:
            print(f"✅ Error capturado correctamente (Inconsistencia prevenida): {e}")

        # 5. Forzado de Estados (Solo para Test)
        # Aquí manipulamos el objeto directamente sin pasar por métodos de validación
        print("\n--- Fase 4: Forzado de Estados (Reset a Reservada) ---")
        print(f"Estado antes del reset: {cita.estado.value}")
        cita.estado = EstadoCita.RESERVADA # Forzado manual
        db.actualizar_estado_cita(cita.id, cita.estado.value)
        print(f"✅ Estado forzado manualmente a: {cita.estado.value}")

        # 6. Reportes Detallados
        print("\n" + "="*40)
        print("📊 REPORTE DE CONSISTENCIA FINAL")
        print("="*40)
        
        # Lista total
        print(f"Total citas en sistema: {len(recepcion.obtener_todas_las_citas())}")
        
        # Lista por paciente
        citas_p = recepcion.obtener_lista_paciente("1-1")
        print(f"Citas del paciente 1-1: {len(citas_p)}")
        for c in citas_p:
            print(f"  - [{c.id}] Medico: {c.medico.nombre} | Estado: {c.estado.value}")

        # Lista por médico
        citas_m = recepcion.obtener_lista_medico("10-10")
        print(f"Citas del médico 10-10: {len(citas_m)}")

    except Exception as e:
        print(f"❌ Error crítico en las pruebas: {e}")
        

if __name__ == "__main__":
    ejecutar_pruebas()