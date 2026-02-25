# ------------------ imports ------------------
from database import db
from interfaz import mostrar_menu
from servicios import Recepcion


# ------------------ inicio ------------------
if __name__ == "__main__":
    db.iniciar_db()
    recepcion = Recepcion()
    recepcion.cargar_datos_desde_db()
    mostrar_menu(recepcion)