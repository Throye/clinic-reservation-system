import re
from excepciones import ClinicaError

class ValidationError(ClinicaError):
    """ Error específico para datos mal formateados """
    pass

def _calcular_dv(cuerpo):
    """ Funcion privada que realiza el algoritmo 11 """
    suma = 0
    multi = 2
    for d in reversed(cuerpo):
        suma += int(d) * multi
        multi = 2 if multi == 7 else multi + 1

    residuos = 11 - (suma % 11)
    if residuos == 11: return '0'
    if residuos == 10: return 'K'
    return str(residuos)

def normalizar_rut(rut_sucio):
    rut_limpio = re.sub(fr'[^0-9kK]', '', str(rut_sucio)).upper() # '12345678k'

    if len(rut_limpio) < 7:
        raise ValidationError("El rut es demasiado corto o inválido")

    cuerpo = rut_limpio[:-1] # '12345678'
    dv = rut_limpio[-1] # 'K'

    if not cuerpo.isdigit() or not (dv.isdigit() or dv == 'K'):
        raise ValidationError("El RUT contiene caracteres no permitidos")

    return f"{cuerpo}-{dv}"

def formatear_texto(texto):
    """ Limpia los espacios y pone un formato de titulo """
    if not texto: return ""
    return " ".join(texto.split()).title()