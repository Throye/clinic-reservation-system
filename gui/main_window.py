import customtkinter as ctk
from servicios import Recepcion

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Clínica - Gestión de Reservas")
        self.geometry("400x500") # Tamaño para el login
        
        # El cerebro de la app
        self.recepcion = Recepcion()
        self.recepcion.cargar_datos_desde_db()

        # Mostramos el Login al empezar
        self.mostrar_login()

    def mostrar_login(self):
        # Limpiamos ventana y cargamos el Frame de Login
        self.login_frame = LoginFrame(self, self.recepcion, self.on_login_exito)
        self.login_frame.pack(expand=True, fill="both", padx=20, pady=20)

    def on_login_exito(self, usuario):
        # Esta función se ejecuta cuando el LoginFrame dice que todo OK
        print(f"Login exitoso: Bienvenido {usuario.nombre}")
        
        # Borramos el login
        self.login_frame.destroy()
        
        # Aquí es donde cambiaremos el tamaño y mostraremos el menú
        self.geometry("900x600")
        self.mostrar_panel_principal(usuario)

    def mostrar_panel_principal(self, usuario):
        # De momento un saludo para probar
        self.label = ctk.CTkLabel(self, text=f"Hola {usuario.nombre}, eres {usuario.rol}")
        self.label.pack(pady=50)

from gui.login_frame import LoginFrame # Import circular evitado poniéndolo abajo