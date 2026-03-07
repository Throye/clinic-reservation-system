import customtkinter as ctk
from configuracion import configurar_logs
from database.db import iniciar_db
from gui.main_window import MainWindow

def main():
    configurar_logs()
    # Iniciamos la base de datos
    iniciar_db()
    
    # Configuramos el estilo visual
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Arrancamos la App
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()