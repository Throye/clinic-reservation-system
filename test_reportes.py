from servicios import Recepcion
from excepciones import ClinicaError, EntidadNotFoundError, BusquedaInvalidaError, CitaNotFoundError
import os
from database import db
from configuracion import configurar_logs

def ejecutar_pruebas():
    configurar_logs()
    # 1. Limpieza de entorno
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    db.iniciar_db()

    print("🔧 INICIANDO ENTORNO DE PRUEBAS AUTOMATIZADO...")
    
    # 1. Al crear una nueva instancia, la base de datos parte limpia
    recepcion = Recepcion() 

    print("\n💉 1. POBLANDO DATOS DE PRUEBA...")
    
    # --- Agregando 5 Pacientes (Con RUTs Válidos) ---
    recepcion.registrar_paciente("12345678-5", "Juan Perez", 30)
    recepcion.registrar_paciente("19876543-0", "Maria Lopez", 25)
    recepcion.registrar_paciente("20123456-5", "Carlos Pinto", 40)
    recepcion.registrar_paciente("15678901-1", "Ana Soto", 15)
    recepcion.registrar_paciente("17283945-2", "Luis Jara", 55)

    # --- Agregando 3 Médicos (Con RUTs Válidos) ---
    recepcion.registrar_medico("10987654-2", "Dr. Simi", "Medicina General", 10)
    recepcion.registrar_medico("21999888-0", "Dra. Polo", "Pediatria", 8)
    recepcion.registrar_medico("13579246-2", "Dr. House", "Cardiologia", 5)

    # --- Agregando 2 Citas ---
    # Usamos los RUTs válidos que acabamos de crear
    cita1 = recepcion.generar_cita("12345678-5", "10987654-2", "01-03-2026 10:00")
    cita2 = recepcion.generar_cita("19876543-0", "21999888-0", "01-03-2026 11:30")

    print("✅ Base de datos poblada con éxito.")
    print("="*50)
    print("🧪 2. EJECUTANDO CASOS DE PRUEBA (REPORTES)")
    print("="*50)

    # ---------------------------------------------------------
    # PRUEBA A: Listar Datos Correctamente (ÉXITO)
    # ---------------------------------------------------------
    print("\n▶️ PRUEBA A: Obtener todos los médicos")
    medicos = recepcion.obtener_todos_los_medicos()
    for m in medicos: 
        print(f"  - {m.nombre} ({m.especialidad})")

    # ---------------------------------------------------------
    # PRUEBA B: Búsqueda Exitosa
    # ---------------------------------------------------------
    print("\n▶️ PRUEBA B: Buscar Especialidad 'Pediatria'")
    try:
        resultados = recepcion.buscar_medicos_por_especialidad("Pediatria")
        for m in resultados: 
            print(f"  ✅ Encontrado: {m.nombre}")
    except ClinicaError as e:
        print(f"  ❌ Falló la prueba: {e}")

    # ---------------------------------------------------------
    # PRUEBA C: Búsqueda de Especialidad Inexistente (ERROR ESPERADO)
    # ---------------------------------------------------------
    print("\n▶️ PRUEBA C: Buscar Especialidad 'Neurologia'")
    try:
        recepcion.buscar_medicos_por_especialidad("Neurologia")
        print("  ❌ Falló: Debería haber lanzado un error, pero no lo hizo.")
    except EntidadNotFoundError as e:
        print(f"  ✅ Error capturado correctamente: {e}")

    # ---------------------------------------------------------
    # PRUEBA D: Búsqueda Vacía (ERROR ESPERADO)
    # ---------------------------------------------------------
    print("\n▶️ PRUEBA D: Buscar Especialidad vacía '   '")
    try:
        recepcion.buscar_medicos_por_especialidad("   ")
        print("  ❌ Falló: Debería haber lanzado un error, pero no lo hizo.")
    except BusquedaInvalidaError as e:
        print(f"  ✅ Error capturado correctamente: {e}")

    # ---------------------------------------------------------
    # PRUEBA E: Buscar Cita que no existe (ERROR ESPERADO)
    # ---------------------------------------------------------
    print("\n▶️ PRUEBA E: Buscar Cita ID 999")
    try:
        recepcion.obtener_cita_por_id(999)
        print("  ❌ Falló: Debería haber lanzado un error, pero no lo hizo.")
    except CitaNotFoundError as e:
        print(f"  ✅ Error capturado correctamente: {e}")

    print("\n🎉 PRUEBAS FINALIZADAS. REVISA EL ARCHIVO CLINICA.LOG PARA VER LOS REGISTROS.")

if __name__ == "__main__":
    ejecutar_pruebas()