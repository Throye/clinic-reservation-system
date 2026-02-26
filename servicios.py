from modelos import Paciente, Medico, Cita, EstadoCita
from excepciones import AutenticationError, CapacidadMedicoExcedidaError, CitaNotFoundError, ClinicaError, EntidadNotFoundError, EntidadYaExisteError, EstadoCitaError
from utilidades import  formatear_texto, normalizar_rut
from database import db
import logging


logger = logging.getLogger(__name__)

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
        try:
            # limpiar datos
            rut_f = normalizar_rut(rut)
            nombre_f = formatear_texto(nombre)
            # validar duplicidad
            if rut_f in self.pacientes:
                raise EntidadYaExisteError("El RUT ya se encuentra registrado")
            # agregar a memoria y db
            nuevo_paciente = Paciente(rut_f, nombre_f, edad)
            db.insertar_paciente(nuevo_paciente)
            self.pacientes[nuevo_paciente.rut] = nuevo_paciente
            # registrar en logger y devolver dato
            logger.info(f"paciente registrado: {nombre} (RUT: {rut})")
            return nuevo_paciente
            # manejo de exepcion
        except Exception as e:
            logger.error(f"fallo al registrar paciente {rut}: {e}")
            raise

    def registrar_medico(self, rut, nombre, especialidad, capacidad_atencion):
        try:
            # limpiar datos
            rut_f = normalizar_rut(rut)
            nombre_f = formatear_texto(nombre)
            especialidad_f = formatear_texto(especialidad)
            # validar duplicidad
            if rut_f in self.medicos:
                raise EntidadYaExisteError("El RUT ya se encuentra registrado")
            # agregar a memoria y a db
            nuevo_medico = Medico(rut_f, nombre_f, especialidad_f, capacidad_atencion)
            db.insertar_medico(nuevo_medico)
            self.medicos[nuevo_medico.rut] = nuevo_medico
            # registrar en logger y devolver medico
            logger.info(f"Medico registrado: {nombre} (RUT: {rut})")
            return nuevo_medico
            # manejo de exepcion
        except Exception as e:
            logger.error(f"Fallo al registrar medico {rut}: {e}")
            raise

    # ----- Citas -----
    def generar_cita(self, rut_paciente, rut_medico):
        try:
            # limpiar datos
            rut_p = normalizar_rut(rut_paciente)
            rut_m = normalizar_rut(rut_medico)
            # Validar instancia en diccionario
            paciente = self.pacientes.get(rut_p)
            if not paciente: raise EntidadNotFoundError("Paciente no registrado")
            medico = self.medicos.get(rut_m)
            if not medico: raise EntidadNotFoundError("Medico no registrado")
            # Validar que el medico no exceda su limite
            if len(medico.citas_del_dia) >= medico.capacidad_atencion:
                raise CapacidadMedicoExcedidaError(f"El medico {medico.nombre} ya no tiene cupos disponibles")
            # Generar nueva cita
            nueva_cita = Cita(paciente, medico)
            # Guardar cita en medico, paciente, memoria y db
            self.lista_citas[nueva_cita.id] = nueva_cita
            paciente.citas.append(nueva_cita)
            medico.citas_del_dia.append(nueva_cita)
            db.insertar_cita(nueva_cita)
            # Registrar en logger y devolver dato
            logger.info(f"Cita generada [{nueva_cita.id}] entre: Paciente: {paciente.nombre} - Medico: {medico.nombre}")
            return nueva_cita
        except Exception as e:
            logger.error(f"Fallo al generar la cita: {e}")
            raise

    # Estados de citas -----
    def confirmar_cita(self, rut_paciente, id_cita):
        _, cita = self._validar_cita(rut_paciente, id_cita)
        try:
            cita.confirmar()
            db.actualizar_estado_cita(cita.id, cita.estado.value)
            logger.info(f"Cita {id_cita} CONFIRMADA para paciente {rut_paciente}")
            return cita
        except EstadoCitaError as e:
            logger.error(f"Error lógico en Cita {id_cita}: {e}")
            raise

    def cancelar_cita(self, rut_paciente, id_cita):
        _, cita = self._validar_cita(rut_paciente, id_cita)
        try:
            cita.cancelar()
            db.actualizar_estado_cita(cita.id, cita.estado.value)
            logger.info(f"Cita {id_cita} CANCELADA para paciente {rut_paciente}")
            return cita
        except EstadoCitaError as e:
            logger.error(f"Error lógico en Cita {id_cita}: {e}")

    def finalizar_cita(self, rut_paciente, id_cita):
        _, cita = self._validar_cita(rut_paciente, id_cita)
        try:
            cita.finalizar()
            db.actualizar_estado_cita(cita.id, cita.estado.value)
            logger.info(f"Cita {id_cita} FINALIZADA para paciente {rut_paciente}")
            return cita
        except ClinicaError as e:
            logger.error(f"Error lógico en cita {id_cita}: {e}")
            raise

    def _validar_cita(self, rut_paciente, id_cita):
        try:
            # limpiar datos
            rut_p = normalizar_rut(rut_paciente)

            paciente = self.pacientes.get(rut_p)
            if not paciente: raise EntidadNotFoundError("El paciente no se encuentra registrado")

            cita = self.lista_citas.get(id_cita)
            if not cita: raise CitaNotFoundError("Cita no encontrada")

            if cita.paciente != paciente: raise AutenticationError("El rut no coincide con la cita")

            return paciente, cita
        except ClinicaError as e:
            logger.error(f"Fallo de validacion: {e}")
            raise

    # Listado de citas -----
    def obtener_todas_las_citas(self):
        return list(self.lista_citas.values())

    def obtener_lista_paciente(self, rut):
        try:
            rut_p = normalizar_rut(rut)
            paciente = self.pacientes.get(rut_p)
            if not paciente: 
                logger.warning(f"Consulta fallida: RUT de paciente no encontrado ({rut_p})")
                raise EntidadNotFoundError("Paciente no registrado")
            logger.debug(f"Listado de citas consultado para paciente: {rut_p}")
            return paciente.citas
        except Exception as e:
            logger.error(f"Error al obtener lista de pacientes {rut_p}: {e}")
            raise

    def obtener_lista_medico(self, rut):
        try:
            medico = self.medicos.get(rut)
            if not medico: 
                logger.warning(f"Consulta fallida: RUT de medico no encontrado ({rut})")
                raise EntidadNotFoundError("Medico no registrado")
            logger.debug(f"Listado de citas consultado para medico: {rut}")
            return medico.citas_del_dia
        except Exception as e:
            logger.error(f"Error al obtener lista de medico {rut}: {e}")
            raise