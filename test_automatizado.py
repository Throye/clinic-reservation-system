import os
from database import db
from servicios import Recepcion
from modelos import EstadoCita
from excepciones import ClinicaError, EntidadYaExisteError
from configuracion import configurar_logs

def ejecutar_pruebas():
    configurar_logs()
    print("\n🧪 INICIANDO AUTOMATIZACIÓN DE PRUEBAS (CON NORMALIZACIÓN)\n")

    # 1. Preparación del entorno
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    db.iniciar_db()

    recepcion = Recepcion()

    try:
        # 2. Registro con datos "sucios"
        print("--- Fase 1: Registro con datos sucios ---")
        # Enviamos RUT con puntos, espacios y nombre en minúsculas
        p = recepcion.registrar_paciente("  12.345.678 - k  ", "juan perez", 30)
        m = recepcion.registrar_medico("11111111-1", "DR. simon", "CARDIOLOGÍA", 1)
        
        print(f"✅ Paciente normalizado: '{p.rut}' | Nombre: '{p.nombre}'")
        print(f"✅ Médico normalizado: '{m.rut}' | Nombre: '{m.nombre}'")

        # 3. Validar duplicidad con formatos distintos
        print("\n--- Fase 2: Validar prevención de duplicados ---")
        try:
            # Aunque el formato sea distinto, el sistema debería detectar que es el mismo RUT
            recepcion.registrar_paciente("12345678-K", "Juan", 30)
        except EntidadYaExisteError:
            print("✅ Éxito: El sistema detectó el duplicado correctamente a pesar del formato.")

        # 4. Flujo de Citas con datos inconsistentes
        print("\n--- Fase 3: Flujo de Citas (Normalización en búsqueda) ---")
        # El usuario pide cita usando un RUT sucio para un paciente que ya existe
        cita = recepcion.generar_cita(" 12345678k ", "11.111.111-1")
        print(f"✅ Cita [{cita.id}] generada usando RUTs sucios en la búsqueda.")

        # 5. Confirmación y Validación
        recepcion.confirmar_cita("12345678-K", cita.id)
        print(f"✅ Cita {cita.id} confirmada exitosamente.")

        # 6. Reporte Final
        print("\n" + "="*40)
        print("📊 REPORTE DE CONSISTENCIA FINAL")
        print("="*40)
        
        citas_p = recepcion.obtener_lista_paciente(" 12.345.678-k ")
        print(f"Total citas recuperadas para el paciente: {len(citas_p)}")
        for c in citas_p:
            print(f"  - {c}")

    except Exception as e:
        print(f"❌ Error inesperado en las pruebas: {e}")

if __name__ == "__main__":
    ejecutar_pruebas()