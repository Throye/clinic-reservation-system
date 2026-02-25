# ------------------ imports ------------------
from enum import Enum
from database import db
from interfaz import mostrar_menu
from excepciones import (CitaNotFoundError, AutenticationError, EstadoCitaError, EntidadYaExisteError, EntidadNotFoundError, CapacidadMedicoExcedidaError)

# ------------------ clases ------------------
class EstadoCita(Enum):
    RESERVADA = "Reservada"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    ATENDIDA = "Atendida"
    AUSENTE = "Ausente"
class Cita:
    contador_id = 1
    def __init__(self, paciente, medico):
        self.id = Cita.contador_id
        self.paciente = paciente
        self.medico = medico
        self.estado = EstadoCita.RESERVADA # Estado por defecto al generar cita
        Cita.contador_id += 1

    def confirmar(self):
        if self.estado == EstadoCita.RESERVADA:
            self.estado = EstadoCita.CONFIRMADA
            return self.estado
        else:
            raise EstadoCitaError(f"No es posible confirmar cita con el estado: {self.estado.value}")

    def cancelar(self):
        if self.estado == EstadoCita.CANCELADA:
            raise EstadoCitaError(f"No es posible cancelar una cita con el estado: {self.estado.value}")
        if self.estado != EstadoCita.ATENDIDA:
            self.estado = EstadoCita.CANCELADA
            return self.estado
        else:
            raise EstadoCitaError("No es posible cancelar una cita ya atendida")

    def finalizar(self):
        if self.estado == EstadoCita.CONFIRMADA:
            self.estado = EstadoCita.ATENDIDA
            return self.estado
        else:
            raise EstadoCitaError("No es posible finalizar una cita que no haya sido confirmada")

    def __str__(self):
        return f"ID: {self.id} | Paciente: {self.paciente.nombre} | Medico: {self.medico.nombre} | Estado: {self.estado.value}"

class Paciente:
    def __init__(self, rut, nombre, edad):
        self.rut = rut
        self.nombre = nombre
        self.edad = edad
        self.citas = []

class Medico:
    def __init__(self, rut, nombre, especialidad, capacidad_atencion):
        self.rut = rut
        self.nombre = nombre
        self.especialidad = especialidad
        self.capacidad_atencion = capacidad_atencion
        self.citas_del_dia = []

class Recepcion:
    def __init__(self):
        self.pacientes = {} # {rut: <paciente>}
        self.medicos = {} # {rut: <medico>}
        self.lista_citas = {} # [id: <cita>]

    # ---------- Cargar datos desde db ----------
    def cargar_datos_desde_db(self):
        self._cargar_pacientes()
        self._cargar_medicos()  
        self._cargar_citas()

    def _cargar_pacientes(self):
        filas = db.obtener_todos_los_pacientes()
        for fila in filas:
            rut, nombre, edad = fila
            self.pacientes[rut] = Paciente(rut, nombre, edad)
    
    def _cargar_medicos(self):
        filas = db.obtener_todos_los_medicos()
        for fila in filas:
            rut, nombre, especialidad, capacidad_atencion = fila
            self.medicos[rut] = Medico(rut, nombre, especialidad, capacidad_atencion)

    def _cargar_citas(self):
        filas_citas = db.obtener_citas()
        max_id = 0
        for fila in filas_citas:
            id_db, rut_p, rut_m, estado_str = fila
            paciente = self.pacientes.get(rut_p)
            medico = self.medicos.get(rut_m)

            if paciente and medico:
                # crear cita
                nueva_cita = Cita(paciente, medico)
                nueva_cita.id = id_db
                nueva_cita.estado = EstadoCita(estado_str)
                # guardar cita
                self.lista_citas[id_db] = nueva_cita
                paciente.citas.append(nueva_cita)
                medico.citas_del_dia.append(nueva_cita)
                # actualizar contador
                if id_db > max_id:
                    max_id = id_db

        Cita.contador_id = max_id + 1


    # ----- Registros -----
    def registrar_paciente(self, rut, nombre, edad):
        if rut in self.pacientes:
            raise EntidadYaExisteError("El RUT ya se encuentra registrado")
        nuevo_paciente = Paciente(rut, nombre, edad)
        db.insertar_paciente(nuevo_paciente)
        self.pacientes[nuevo_paciente.rut] = nuevo_paciente
        return nuevo_paciente

    def registrar_medico(self, rut, nombre, especialidad, capacidad_atencion):

        if rut in self.medicos:
            raise EntidadYaExisteError("El RUT ya se encuentra registrado")
        nuevo_medico = Medico(rut, nombre, especialidad, capacidad_atencion)
        db.insertar_medico(nuevo_medico)
        self.medicos[nuevo_medico.rut] = nuevo_medico
        return nuevo_medico

    # ----- Citas -----
    def generar_cita(self, rut_paciente, rut_medico):
        # Validar instancia en diccionario
        paciente = self.pacientes.get(rut_paciente)
        if not paciente: raise EntidadNotFoundError("Paciente no registrado")
        medico = self.medicos.get(rut_medico)
        if not medico: raise EntidadNotFoundError("Medico no registrado")
        # Validar que el medico no exceda su limite
        if len(medico.citas_del_dia) >= medico.capacidad_atencion:
            raise CapacidadMedicoExcedidaError(f"El medico {medico.nombre} ya no tiene cupos disponibles")
        # Generar nueva cita
        nueva_cita = Cita(paciente, medico)
        self.lista_citas[nueva_cita.id] = nueva_cita
        paciente.citas.append(nueva_cita)
        medico.citas_del_dia.append(nueva_cita)
        db.insertar_cita(nueva_cita)
        return nueva_cita

    # Estados de citas -----
    def confirmar_cita(self, rut_paciente, id_cita):
        _, cita = self._validar_cita(rut_paciente, id_cita)
        cita.confirmar()
        db.actualizar_estado_cita(cita.id, cita.estado.value)
        return cita

    def cancelar_cita(self, rut_paciente, id_cita):
        _, cita = self._validar_cita(rut_paciente, id_cita)
        cita.cancelar()
        db.actualizar_estado_cita(cita.id, cita.estado.value)
        return cita

    def finalizar_cita(self, rut_paciente, id_cita):
        _, cita = self._validar_cita(rut_paciente, id_cita)
        cita.finalizar()
        db.actualizar_estado_cita(cita.id, cita.estado.value)
        return cita

    def _validar_cita(self, rut_paciente, id_cita):
        paciente = self.pacientes.get(rut_paciente)
        if not paciente: raise EntidadNotFoundError("El paciente no se encuentra registrado")
        cita = self.lista_citas.get(id_cita)
        if not cita: raise CitaNotFoundError("Cita no encontrada")

        if cita.paciente != paciente: raise AutenticationError("El rut no coincide con la cita")

        return paciente, cita

    # Listado de citas -----
    def obtener_todas_las_citas(self):
        return list(self.lista_citas.values())

    def obtener_lista_paciente(self, rut):
        paciente = self.pacientes.get(rut)
        if not paciente: raise EntidadNotFoundError("Paciente no registrado")
        return paciente.citas

    def obtener_lista_medico(self, rut):
        medico = self.medicos.get(rut)
        if not medico: raise EntidadNotFoundError("Medico no registrado")
        return medico.citas_del_dia

# ------------------ inicio ------------------
if __name__ == "__main__":
    db.iniciar_db()
    recepcion = Recepcion()
    recepcion.cargar_datos_desde_db()
    mostrar_menu(recepcion)