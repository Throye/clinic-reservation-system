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
        self.state('zoomed')
        self.mostrar_panel_principal(usuario)

    def mostrar_panel_principal(self, usuario):
        # 1. Limpieza y preparación de ventana
        self.state('zoomed')
        
        # 2. Estructura Principal (Sidebar + Contenido)
        self.sidebar_frame = ctk.CTkFrame(self, width=255, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        self.contenido_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.contenido_frame.pack(side="right", expand=True, fill="both")

        # 3. Llamamos a los constructores del Sidebar
        self._configurar_sidebar(usuario)

    def logout(self):
        if hasattr(self, "sidebar_frame"):
            self.sidebar_frame.destroy()
        if hasattr(self, "contenido_frame"):
            self.contenido_frame.destroy()
        self.state('normal')
        self.geometry("400x500")
        self.mostrar_login()

    def _configurar_sidebar(self, usuario):
        # --- PARTE ARRIBA (Header) ---
        self.sidebar_top = ctk.CTkFrame(self.sidebar_frame, height=93, corner_radius=0, fg_color="transparent")
        self.sidebar_top.pack(side="top", fill="x", padx=20) # Añadimos el padding lateral aquí
        self.sidebar_top.pack_propagate(False)

        # Título alineado a la izquierda (West)
        self.label_titulo = ctk.CTkLabel(self.sidebar_top, text="MediClinic", 
                                         font=("Roboto", 18, "bold"), anchor="w")
        self.label_titulo.pack(side="left", pady=(30, 0))

        # Botón de Ocultar alineado a la derecha (East)
        self.btn_toggle = ctk.CTkButton(self.sidebar_top, text=">", width=30, height=30,
                                        fg_color="transparent", hover_color="#34495E",
                                        command=self._toggle_sidebar)
        self.btn_toggle.pack(side="right", pady=(30, 0))

        # --- PARTE MEDIA (navegacion) ---
        # Le damos un margen superior para separarlo del header
        self.sidebar_middle = ctk.CTkFrame(self.sidebar_frame, corner_radius=0, fg_color="transparent")
        self.sidebar_middle.pack(side="top", fill="both", expand=True, pady=(20, 10))

        self._cargar_botones_navegacion(usuario)

        # --- PARTE ABAJO (Perfil y Cerrar Sesión) ---
        self.sidebar_bottom = ctk.CTkFrame(self.sidebar_frame, corner_radius=0, fg_color="transparent")
        self.sidebar_bottom.pack(side="bottom", fill="x", pady=(15, 20))

        # Info del perfil
        ctk.CTkLabel(self.sidebar_bottom, text=usuario.nombre, font=("Roboto", 14, "bold")).pack()
        ctk.CTkLabel(self.sidebar_bottom, text=usuario.rol.upper(), font=("Roboto", 11), text_color="gray").pack()
        
        # Botón Cerrar Sesión
        ctk.CTkButton(
            self.sidebar_bottom, 
            text="Cerrar Sesión", 
            fg_color="transparent",
            hover_color="#34495E",
            command=self.logout
            ).pack(pady=(15, 0), padx=20,)

        self._cargar_botones_navegacion(usuario)

    def _toggle_sidebar(self):
        current_width = self.sidebar_frame.winfo_width()
        if current_width > 100:
            self.sidebar_frame.configure(width=60)
            self.label_titulo.pack_forget()
            self.btn_toggle.configure(text="<")
        else:
            self.sidebar_frame.configure(width=255)
            self.label_titulo.pack(side="left", pady=(30,0))
            self.btn_toggle.configure(text=">")

    def _cargar_botones_navegacion(self, usuario):
        # Aquí es donde ocurre la magia de los roles
        # Botones comunes para todos
        self._crear_boton_nav("Dashboard", self.mostrar_dashboard)
        self._crear_boton_nav("Citas", self.mostrar_citas)

        # Botones específicos
        if usuario.rol == "admin":
            self._crear_boton_nav("Gestión Médicos", self.mostrar_medicos)
            self._crear_boton_nav("Reportes", self.mostrar_reportes)
        
        if usuario.rol == "recepcionista":
            self._crear_boton_nav("Pacientes", self.mostrar_pacientes)

    def _crear_boton_nav(self, texto, comando):
        """Función auxiliar para no repetir código de estilo de botones"""
        btn = ctk.CTkButton(self.sidebar_middle, text=texto, command=comando,
                            anchor="w", fg_color="transparent", hover_color="#34495E")
        btn.pack(fill="x", padx=10, pady=5)      

from gui.login_frame import LoginFrame # Import circular evitado poniéndolo abajo