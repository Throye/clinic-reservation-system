import re
from excepciones import ClinicaError

class ValidationError(ClinicaError):
    """ Error específico para datos mal formateados """
    pass

def normalizar_rut(rut_sucio):
    rut_limpio = re.sub(fr'[^0-9kK]', '', str(rut_sucio)).upper()

    if len(rut_limpio) < 7:
        raise ValidationError("El rut es demasiado corto o inválido")

    cuerpo = rut_limpio[:-1]
    dv = rut_limpio[-1]

    if not cuerpo.isdigit() or not (dv.isdigit() or dv == 'K'):
        raise ValidationError("El RUT contiene caracteres no permitidos")

    return f"{cuerpo}-{dv}"

def formatear_texto(texto):
    """ Limpia los espacios y pone un formato de titulo """
    if not texto: return ""
    return " ".join(texto.split()).title()