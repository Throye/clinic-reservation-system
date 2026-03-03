from multiprocessing import Value
from excepciones import ClinicaError

def menu_gestion_personas(recepcion):
    while True:
        print("\n" + "=" * 30)
        print("GESTIÓN DE PERSONAS")
        print("="*30)
        print("1. Registrar Paciente")
        print("2. Registrar Medico")
        print("3. Volver al Menú Principal")

        op = input("\nSeleccione una opción: ")

        if op == "1":
            print("\n--- Registro de Paciente ---")
            rut = input("RUT: ")
            if not rut.strip(): continue
            nombre = input("Nombre: ")
            try:
                edad = int(input("Edad: "))
                recepcion.registrar_paciente(rut, nombre, edad)
                print("Paciente registrado con exito")
            except ValueError: print("Error: Edad debe ser un número")
            except ClinicaError as e: print(f"Error: {e}")

        elif op == "2":
            print("\n--- Registro de Médico ---")
            rut = input("RUT: ")
            if not rut.strip(): continue
            nombre = input("Nombre: ")
            especialidad = input("Especialidad: ")
            try:
                capacidad = int(input("Capacidad diaria: "))
                recepcion.registrar_medico(rut, nombre, especialidad)
                print("Médica registrado con éxito.")
            except ValueError: print("Error: capacidad debe ser número")
            except ClinicaError as e: print(f"Error: {e}")

        elif op == "3":
            break

def menu_citas(recepcion):
    while True:
        print("\n"+"="*30)
        print("GESTION DE CITAS")
        print("="*30)
        print("1. Generar Nueva Cita")
        print("2. Consultar Disponibilidad")
        print("3. Confirmar Asistencia")
        print("4. Cancelar Cita")
        print("5. Finalizar Cita (Atendida)")
        print("6. Volver al Menú principal")
        op = input("\nSeleccione una opción: ")
        try:
            if op == "1":
                rut_p = input("RUT Paciente: ")
                rut_m = input("RUT Medico: ")
                fecha = input("Fecha y Hora (DD-MM-YYY HH:MM): ")
                cita = recepcion.generar_cita(rut_p, rut_m, fecha)
                print(f"Cita ID {cita.id} generada.")

            elif op == "2":
                rut_m = input("RUT Medico: ")
                fecha = input("Fecha (DD-MM-YYYY): ")
                libres = recepcion.obtener_disponibilidad_medico(rut_m, fecha)
                print(f"\n--- Horarios disponibles para el {fecha} ---")
                if not libres: (print("No hay bloques libres para esta fecha"))
                else:
                    for i, hora in enumerate(libres):
                        print(f"[{hora}]", end="\t" if (i+1)%4 != 0 else "\n")
                    print("\n")

            elif op == "3":
                rut_p = input("RUT Paciente: ")
                id_c = int(input("ID de la cita: "))
                recepcion.confirmar_cita(rut_p, id_c)
                print("Cita Confirmada")

            elif op == "4":
                rut_p = input("RUT Paciente: ")
                id_c = int(input("ID de la cita: "))
                recepcion.cancelar_cita(rut_p, id_c)
                print("Cita cancelada")
            
            elif op == "5":
                rut_p = input("RUT Paciente: ")
                id_c = int(input("ID de la cita: "))
                recepcion.finalizar_cita(rut_p, id_c)
                print("Cita finalizada.")
            
            elif op == "6":
                break
        except (ClinicaError, ValueError) as e:
            print(f"Error: {e}")

def menu_reportes(recepcion):
    while True:
        print("\n" + "="*35)
        print("📊 PANEL DE CONSULTAS Y REPORTES")
        print("="*35)
        print("1. Ver Listado de Pacientes")
        print("2. Ver Listado de Médicos")
        print("3. Buscar Médicos por Especialidad")
        print("4. Ver Todas las Citas (General)")
        print("5. Buscar Cita específica (por ID)")
        print("6. Historial por Paciente (RUT)")
        print("7. Historial por Médico (RUT)")
        print("8. Volver al Menú Principal")
        
        op = input("\nSeleccione consulta: ")

        try:
            if op == "1":
                print("\n--- PACIENTES REGISTRADOS ---")
                for p in recepcion.obtener_todos_los_pacientes():
                    print(f"RUT: {p.rut} | Nombre: {p.nombre} | Edad: {p.edad}")

            elif op == "2":
                print("\n--- CUERPO MÉDICO ---")
                for m in recepcion.obtener_todos_los_medicos():
                    print(f"RUT: {m.rut} | Nombre: {m.nombre} | Especialidad: {m.especialidad}")

            elif op == "3":
                esp = input("Ingrese especialidad a buscar: ")
                if not esp.strip(): continue
                try:
                    resultados = recepcion.buscar_medicos_por_especialidad(esp)
                    print(f"\n--- médicos en {esp.title()} ---")
                    for m in resultados:
                        print(f"Médico:{m.nombre} | Especialidad: {m.especialidad} | RUT: {m.rut}")
                except ClinicaError as e:
                    print(f"Error: {e}")

            elif op == "4":
                for c in recepcion.obtener_todas_las_citas(): print(c)

            elif op == "5":
                id_c = int(input("ID de la cita: "))
                print(recepcion.obtener_cita_por_id(id_c))

            elif op == "6":
                rut = input("RUT Paciente: ")
                for c in recepcion.obtener_lista_paciente(rut): print(c)

            elif op == "7":
                rut = input("RUT Médico: ")
                for c in recepcion.obtener_lista_medico(rut): print(c)

            elif op == "8":
                break
        except ClinicaError as e: print(f"\n Aviso: {e}")
        except ValueError: print("\n Error: Por favor, ingrese un número válido")
        except Exception as e: print(f"\n Error inesperado: {e}")


def mostrar_menu(recepcion):
    while True:
        print("\n" + "*"*40)
        print(" SISTEMA CLÍNICO - MENÚ PRINCIPAL")
        print("*"*40)
        print("1. Gestión de Personas")
        print("2. Gestión de Citas")
        print("3. Reportes y Consultas")
        print("4. Salir")

        opcion = input("\nSeleccione un módulo: ")

        if opcion == "1":
            menu_gestion_personas(recepcion)
        elif opcion == "2":
            menu_citas(recepcion)
        elif opcion == "3":
            menu_reportes(recepcion)
        elif opcion == "4":
            print("\nCerrando sistema... Tenga buen día")
            break
        else:
            print("Opción inválida.")