import database.db as db
from modelos import Medico, Paciente
from utilidades import normalizar_rut
import os

def poblar():
    
    # 1. Asegurar que la DB esté iniciada
    db.iniciar_db()

    print("--- Iniciando carga de datos de prueba ---")

    # 2. Insertar Usuarios (Login)
    # Formato: rut, nombre, password_plana, rol
    try:
        rut_admin = normalizar_rut("12.345.678-5")
        rut_recep = normalizar_rut("19.876.543-0")

        db.insertar_usuario(rut_admin, "Admin Supremo", "admin123", "admin")
        db.insertar_usuario(rut_recep, "Ana Recepción", "recep123", "recepcionista")
        print("[OK] Usuarios creados (Admin y Recepcionista)")
    except Exception as e:
        print(f"[!] Nota: Usuarios ya existían o error: {e}")

    # 3. Insertar Médicos
    # Usamos la clase Medico de tu modelos.py y normalizamos RUT
    medicos_test = [
        Medico(
            normalizar_rut("15.667.889-9"),
            "Dr. Pérez",
            "Cardiología",
            10,
            "09:00",
            "18:00",
            "13:00",
            "14:00",
        ),
        Medico(
            normalizar_rut("10.223.445-6"),
            "Dra. García",
            "Pediatría",
            8,
            "08:30",
            "17:30",
            "14:00",
            "15:00",
        ),
    ]
    
    for m in medicos_test:
        try:
            db.insertar_medico(m)
            print(f"[OK] Médico {m.nombre} registrado.")
        except Exception as e:
            print(f"[!] Error médico {m.nombre}: {e}")

    # 4. Insertar Pacientes
    # Normalizamos RUT igual que en la lógica de negocio
    pacientes_test = [
        Paciente(normalizar_rut("20.112.334-8"), "Juan Probeta", 25),
        Paciente(normalizar_rut("11.556.778-0"), "Maria Curitas", 65),
    ]

    for p in pacientes_test:
        try:
            db.insertar_paciente(p)
            print(f"[OK] Paciente {p.nombre} registrado.")
        except Exception as e:
            print(f"[!] Error paciente {p.nombre}: {e}")

    print("--- Carga finalizada ---")

if __name__ == "__main__":
    poblar()