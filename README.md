# 🏥 Clinic Reservation System

Sistema de gestión de reservas médicas desarrollado en **Python** como proyecto de práctica técnica, con un enfoque central en el **diseño orientado a objetos** y una **arquitectura incremental**.

---

## 🎯 Objetivo
Simular el flujo integral de reservas en un entorno clínico, abarcando los siguientes pilares:

* **Registro de Usuarios:** Gestión de pacientes y médicos.
* **Asignación Inteligente:** Citas basadas en la especialidad médica.
* **Control de Capacidad:** Validación de disponibilidad y límites diarios.
* **Ciclo de Vida de Citas:** Gestión de estados:
    * `Reservada`
    * `Confirmada`
    * `Cancelada`
    * `Atendida`

---

## 🏗️ Arquitectura
El sistema aplica una separación de responsabilidades para facilitar el mantenimiento y la escalabilidad:



* **Dominio:** Clases núcleo (`Paciente`, `Medico`, `Cita`).
* **Servicio Principal:** Clase `Recepcion`, encargada de coordinar las reservas y la lógica de negocio.
* **Persistencia:** Lógica implementada inicialmente **en memoria** (sin base de datos) para validar el diseño antes de escalar.

> **Nota:** El proyecto sigue un desarrollo por versiones (`v1`, `v2`, etc.) bajo un enfoque incremental.

---

## 🛠️ Tecnologías
* **Lenguaje:** Python 3
* **Paradigma:** Programación Orientada a Objetos (POO)
* **Control de Versiones:** GitFlow

---

## 📈 Estado Actual
**🟡 En desarrollo**
Actualmente en la **Versión 1**, que incluye el núcleo funcional operativo a través de la consola.

---
