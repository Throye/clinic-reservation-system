# ------------------ imports ------------------
from database import db
from interfaz import mostrar_menu
from servicios import Recepcion
from configuracion import configurar_logs


# ------------------ inicio ------------------
if __name__ == "__main__":
    configurar_logs()
    db.iniciar_db()

    recepcion = Recepcion()
    recepcion.cargar_datos_desde_db()
    
    mostrar_menu(recepcion)