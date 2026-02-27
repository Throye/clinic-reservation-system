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
        print("2. Confirmar Asistencia")
        print("3. Cancelar Cita")
        print("4. Finalizar Cita (Atendida)")
        print("5. Volver al Menú principal")
        op = input("\nSeleccione una opción: ")
        try:
            if op == "1":
                rut_p = input("RUT Paciente: ")
                rut_m = input("RUT Medico: ")
                fecha = input("Fecha y Hora (DD-MM-YYY HH:MM): ")
                cita = recepcion.generar_cita(rut_p, rut_m, fecha)
                print(f"Cita ID {cita.id} generada.")
            elif op == "2":
                rut_p = input("RUT Paciente: ")
                id_c = int(input("ID de la cita: "))
                recepcion.confirmar_cita(rut_p, id_c)
                print("Cita Confirmada")
            elif op == "3":
                rut_p = input("RUT Paciente: ")
                id_c = int(input("ID de la cita: "))
                recepcion.cancelar_cita(rut_p, id_c)
                print("Cita cancelada")
            
            elif op == "4":
                rut_p = input("RUT Paciente: ")
                id_c = int(input("ID de la cita: "))
                recepcion.finalizar_cita(rut_p, id_c)
                print("Cita finalizada.")
            
            elif op == "5":
                break
        except (ClinicaError, ValueError) as e:
            print(f"Error: {e}")

def menu_reportes(recepcion):
    while True:
        print("\n"+"="*30)
        print("CONSULTAS Y REPORTES")
        print("="*30)
        print("1. Ver Todas las Citas")
        print("2. Buscar Citas por Paciente")
        print("3. Buscar Citas por Médico")
        print("4. Volver al Menú Principal")

        op = input("\nSeleccione una opción: ")

        if op == "1":
            citas = recepcion.obtener_todas_las_citas()
            for c in citas: print(c)

        elif op == "2":
            rut = input("RUT Paciente: ")
            try:
                for c in recepcion.obtener_lista_paciente(rut): print(c)
            except ClinicaError as e: print(e)

        elif op == "3":
            rut = input("RUT Médico: ")
            try:
                for c in recepcion.obtener_lista_medico(rut): print(c)
            except ClinicaError as e: print(e)

        elif op == "4":
            break


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