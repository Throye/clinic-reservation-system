# ------------------ excepciones ------------------
class ClinicaError(Exception):
    """Clase base para Excepciones del sistema"""
    pass

class CitaNotFoundError(ClinicaError): pass
class AutenticationError(ClinicaError): pass
class EstadoCitaError(ClinicaError): pass
class EntidadYaExisteError(ClinicaError): pass
class EntidadNotFoundError(ClinicaError): pass
class CapacidadMedicoExcedidaError(ClinicaError): pass
