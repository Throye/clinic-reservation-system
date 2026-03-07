import customtkinter as ctk
from excepciones import AutenticationError

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, recepcion, al_loguear_exito):
        super().__init__(master)
        self.recepcion = recepcion
        self.al_loguear_exito = al_loguear_exito # Función para avisar al "jefe"

        # --- Elementos Visuales ---
        self.label = ctk.CTkLabel(self, text="SISTEMA CLÍNICO", font=("Roboto", 24, "bold"))
        self.label.pack(pady=20)

        self.rut_entry = ctk.CTkEntry(self, placeholder_text="RUT (12.345.678-9)", width=240)
        self.rut_entry.pack(pady=10)

        self.pass_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=240)
        self.pass_entry.pack(pady=10)

        self.btn_login = ctk.CTkButton(self, text="Entrar", command=self._ejecutar_login)
        self.btn_login.pack(pady=20)

        self.error_lbl = ctk.CTkLabel(self, text="", text_color="orange")
        self.error_lbl.pack()

    def _ejecutar_login(self):
        rut = self.rut_entry.get()
        pw = self.pass_entry.get()
        
        try:
            # Usamos el método que ya tienes en servicios.py
            usuario = self.recepcion.autenticar(rut, pw)
            self.al_loguear_exito(usuario) # Avisamos que entramos
        except AutenticationError as e:
            self.error_lbl.configure(text=str(e))