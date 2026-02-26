from excepciones import ClinicaError

def mostrar_menu(recepcion):
    print("-" * 80)
    print("Bienvenidos al sistema de reservaciones")
    while True:
        print("\nEliga la acción a realizar: ")
        print("1. Registrar Paciente")
        print("2. Registrar Medico")
        print("3. Generar Cita")
        print("4. Confirmar Cita")
        print("5. Cancelar Cita")
        print("6. Finalizar Cita")
        print("7. Obtener todas las citas")
        print("8. Obtener citas de pacientes")
        print("9. Obtener citas de medicos")
        print("10. Salir")
        try:
            opcion = int(input("Opcion: \n"))
        except ValueError: 
            print("Opción no valida\n")
            continue

        if opcion == 1:
            print("A decidido registrar paciente, si desea cancelar, presione Enter")
            rut = str(input("Porfavor ingrese el RUT: "))
            if not rut.strip(): continue
            nombre = str(input("Ingresar Nombre: "))
            try: edad = int(input("Ingrese la edad: "))
            except ValueError: 
                print("Porfavor ingrese datos validos") 
                continue
            try:
                nuevo_paciente = recepcion.registrar_paciente(rut, nombre, edad)
            except ClinicaError as e:
                print(f"Error: {e}")
                continue
            print(f"Paciente {nuevo_paciente.nombre} agregado correctamente")
            continue

        elif opcion == 2:
            print("A decidido registrar medico, si desea cancelar, presione Enter")

            rut = str(input("RUT:"))
            if not rut: continue
            nombre = str(input("Nombre: "))
            especialidad = str(input("Especialidad: "))

            try:
                capacidad_atencion = int(input("Capacidad de atencion: "))
            except ValueError: 
                print("Error, datos no validos")
                continue

            try:
                nuevo_medico = recepcion.registrar_medico(rut, nombre, especialidad, capacidad_atencion)
            except ClinicaError as e:
                print(f"Error: {e}")
                continue

            print(f"Medico {nuevo_medico.nombre} agregado correctamente")

        elif opcion == 3:
            print("A decidido generar cita, si desea cancelar, presione Enter")
            
            rut_p = str(input("RUT del paciente: "))
            if not rut_p: continue
            rut_m = str(input("RUT del medico: "))
            fecha_input = str(input("Ingrese la fecha y hora (DD-MM-YYYY HH:MM: )"))

            try:
                cita = recepcion.generar_cita(rut_p, rut_m, fecha_input)
                print(f"Cita: [{cita.id}] generada con exito para el {fecha_input}")
            except ClinicaError as e: 
                print(f"Error: {e}")
                continue
            print(f"Cita: [{cita.id}] generada con exito")
            continue  

        elif opcion == 4:
            print("A decidido confirmar cita, si desea cancelar, presione Enter")
            
            rut = str(input("RUT del paciente: "))
            if not rut: continue
            try:
                id_cita = int(input("ID de la cita: "))
            except ValueError: 
                print("Ingrese solo numeros")
                continue
            try:
                cita = recepcion.confirmar_cita(rut, id_cita)
            except ClinicaError as e: 
                print(f"Error: {e}")
                continue
            print(f"Cita: [{cita.id}] confirmada con exito")
            continue

        elif opcion == 5:
            print("A decidido cancelar cita, si desea cancelar, presione Enter")

            rut = str(input("RUT del paciente: "))
            if not rut: continue
            try:
                id_cita = int(input("ID de la cita: "))
            except ValueError: 
                print("Datos invalidos, porfavor ingrese solo numeros")
                continue
            try:
                cita = recepcion.cancelar_cita(rut, id_cita)
            except ClinicaError as e: 
                print(f"Error: {e}")
                continue
            print(f"Cita: [{cita.id}] cancelada con exito")
            continue

        elif opcion == 6:
            print("A decidido finalizar cita, si desea cancelar operación, presione Enter")

            rut = str(input("Rut del paciente: "))
            if not rut: continue
            try:
                id_cita = int(input("ID de la cita: "))
            except ValueError: 
                print("Datos invalidos, porfavor ingrese solo numeros")
                continue
            try:
                cita = recepcion.finalizar_cita(rut, id_cita)
            except ClinicaError as e: 
                print(f"Error: {e}")
                continue
            print(f"Cita: [{cita.id}] finalizada con exito")
            continue

        elif opcion == 7:
            print("Imprimiendo todas las listas: ")
            citas_totales = recepcion.obtener_todas_las_citas()
            if not citas_totales: print("No hay citas registradas en el sistema")
            for cita in citas_totales:
                print(cita)
            continue

        elif opcion == 8:
            print("A decidido obtener cita de pacientes, si desea cancelar operación, presione Enter")
            rut = str(input("ingrese el rut del paciente: "))
            if not rut: continue
            try:
                lista_p = recepcion.obtener_lista_paciente(rut)
            except ClinicaError as e:
                print(f"Error: {e}")
                continue
            print(f"Historial de citas del paciente: {rut}")
            for cita in lista_p:
                print(cita)
            continue

        elif opcion == 9:
            print("A decidido obtener cita de medico, si desea cancelar operación, presione Enter")
            rut = str(input("Ingrese RUT del medico: "))
            if not rut: continue
            try:
                lista_m = recepcion.obtener_lista_medico(rut)
            except ClinicaError as e:
                print(f"Error: {e}")
                continue
            print(f"Historial de citas del medico: {rut}")
            for cita in lista_m:
                print(cita)
            continue

        elif opcion == 10:
            print("--------- Tenga bonito dia. Adios ---------")
            break

        else:
            print("Opcion no valida.")
            continue

