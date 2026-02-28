from modelos import Paciente, Medico, Cita, EstadoCita
from excepciones import AutenticationError, BusquedaInvalidaError, CapacidadMedicoExcedidaError, CitaNotFoundError, ClinicaError, EntidadNotFoundError, EntidadYaExisteError, EstadoCitaError
from utilidades import  formatear_texto, normalizar_rut, validar_y_formatear_fecha
from database import db
import logging
from datetime import datetime


logger = logging.getLogger(__name__)

class Recepcion:
    def __init__(self):
        self.pacientes = {} # {rut: <paciente>}
        self.medicos = {} # {rut: <medico>}
        self.lista_citas = {} # [id: <cita>]

    # ---------- Cargar datos desde db a memoria ----------
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
            id_db, rut_p, rut_m, estado_str, fecha_str = fila
            paciente = self.pacientes.get(rut_p)
            medico = self.medicos.get(rut_m)

            if paciente and medico:
                f_h = datetime.strptime(fecha_str, "%d-%m-%Y %H:%M")
                # crear cita
                nueva_cita = Cita(paciente, medico, f_h)
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
    def generar_cita(self, rut_paciente, rut_medico, fecha_str):
        try:
            # limpiar datos
            rut_p = normalizar_rut(rut_paciente)
            rut_m = normalizar_rut(rut_medico)
            fecha_cita = validar_y_formatear_fecha(fecha_str)
            # Validar instancia en diccionario
            paciente = self.pacientes.get(rut_p)
            medico = self.medicos.get(rut_m)
            if not paciente: raise EntidadNotFoundError("Paciente no registrado")
            if not medico: raise EntidadNotFoundError("Medico no registrado")
            # validar si medico tiene cita en el rango +- 30 mins
            for cita_existe in medico.citas_del_dia:
                diferencia = abs((cita_existe.fecha_hora - fecha_cita).total_seconds() / 60)
                if diferencia < 30 and cita_existe.estado != EstadoCita.CANCELADA:
                    raise ClinicaError(f"El medico ya tiene una cita a las {cita_existe.fecha_hora.strftime('%H:%M')}. "
                    "Debe haber al menos 30 min de diferencia.")
            # Validar que el medico no exceda su limite
            if len(medico.citas_del_dia) >= medico.capacidad_atencion:
                raise CapacidadMedicoExcedidaError(f"Cupos agotados para el médico {medico.nombre}")
            # Generar nueva cita
            nueva_cita = Cita(paciente, medico, fecha_cita)
            # Guardar cita en medico, paciente, memoria y db
            self.lista_citas[nueva_cita.id] = nueva_cita
            paciente.citas.append(nueva_cita)
            medico.citas_del_dia.append(nueva_cita)
            db.insertar_cita(nueva_cita)
            # Registrar en logger y devolver dato
            logger.info(f"Cita [{nueva_cita.id} generada para el {fecha_str}]")
            return nueva_cita
        except Exception as e:
            logger.error(f"Fallo al generar la cita: {e}")
            raise

    # Estados de citas -----
    def confirmar_cita(self, rut_paciente, id_cita):
        try:
            _, cita = self._validar_cita(rut_paciente, id_cita)
            if self._verificar_expiracion_cita(cita):
                raise EstadoCitaError(f"No es posible confirmar: El paciente sobre paso la hora limite "
                f"\nCita programada a las {cita.fecha_hora.strftime('%H:%M')} "
                f"\nHora Actual {datetime.now().strftime('%H:%M')} ")

            estado_nuevo = cita.confirmar()
            db.actualizar_estado_cita(cita.id, estado_nuevo.value)
            logger.info(f"Cita {id_cita} CONFIRMADA para paciente {rut_paciente}")
            return cita
        except EstadoCitaError as e:
            logger.error(f"Error lógico en Cita {id_cita}: {e}")
            raise

    def cancelar_cita(self, rut_paciente, id_cita):
        try:
            _, cita = self._validar_cita(rut_paciente, id_cita)
            cita.cancelar()
            db.actualizar_estado_cita(cita.id, cita.estado.value)
            logger.info(f"Cita {id_cita} CANCELADA para paciente {rut_paciente}")
            return cita
        except EstadoCitaError as e:
            logger.error(f"Error lógico en Cita {id_cita}: {e}")

    def finalizar_cita(self, rut_paciente, id_cita):
        try:
            _, cita = self._validar_cita(rut_paciente, id_cita)
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

    def _verificar_expiracion_cita(self, cita):
        """
        Si la cita está RESERVADA y ya pasó la hora programada, 
        pasa automaticamente a CANCELADA p or atras.
        """
        if cita.estado == EstadoCita.RESERVADA and datetime.now() > cita.fecha_hora:
            cita.estado = EstadoCita.CANCELADA
            db.actualizar_estado_cita(cita.id, cita.estado.value)
            logger.info(f"Cita {cita.id} cancelada automaticamente por inasistencia (Hora: {cita.fecha_hora})")
            return True
        return False

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

    # obtener datos -----
    def obtener_todos_los_pacientes(self):
        try: 
            pacientes = list(self.pacientes.values())
            if not pacientes:
                logger.warning("Consulta de pacientes: La base de datos está vacía")
            logger.debug(f"Se listaron {len(pacientes)} pacientes")
            return pacientes
        except Exception as e:
            logger.error(f"Error al listar pacientes: {e}")
            raise

    def obtener_todos_los_medicos(self):
        try:
            medicos = list(self.medicos.values())
            if not medicos:
                logger.warning("Consulta de medicos: la base de datos está vacía")
            logger.debug(f"Se listaron {len(medicos)} medicos")
            return medicos
        except Exception as e:
            logger.error(f"Error al listar medicos: {e}")
            raise

    def buscar_medicos_por_especialidad(self, especialidad):
        try:
            term = especialidad.lower().strip()

            if not term:
                logger.warning("Intendo de búsqueda con término vacío")
                raise BusquedaInvalidaError("El término de búsqueda no puede estar vacio")

            resultados = [m for m in self.medicos.values() if term in m.especialidad.lower()]

            if not resultados:
                logger.warning(f"Búsqueda sin resultados para especialidad: {term}")
                raise EntidadNotFoundError(f"No se encontraron médicos con la especialidad: {especialidad}")
            
            logger.info(f"Búsqueda exitosa: {len(resultados)} médicos encontrados en {term}")
            return resultados
        except ClinicaError:
            raise
        except Exception as e:
            logger.error(f"Error en búsqueda de especialidad: {e}")
            raise

    def obtener_cita_por_id(self, id_cita):
        try:
            cita = self.lista_citas.get(id_cita)
            if not cita:
                logger.warning(f"Consulta de la cita fallida: ID {id_cita}")
                raise CitaNotFoundError(f"No se encontró la cita con la ID: {id_cita}")
            
            logger.debug(f"Cita {id_cita} consultada con éxito")
            return cita
        except Exception as e:
            logger.error(f"Error al obtener cita {id_cita}: {e}")
            raise