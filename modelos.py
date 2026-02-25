from enum import Enum
from excepciones import EstadoCitaError

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
