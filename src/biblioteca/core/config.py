"""Configuracion del sistema, leida del archivo .env.

Sustituye a las credenciales que en el proyecto Java estaban escritas
directamente dentro de ConexionBD.java en el sistema Java.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

RAIZ_PROYECTO = Path(__file__).resolve().parents[3]

load_dotenv(RAIZ_PROYECTO / ".env")


def _requerido(nombre: str) -> str:
    valor = os.getenv(nombre)
    if not valor:
        raise RuntimeError(
            f"Falta la variable {nombre}. Copia .env.example como .env "
            f"y pide las llaves al Scrum Master."
        )
    return valor


SUPABASE_URL = _requerido("SUPABASE_URL")
SUPABASE_KEY = _requerido("SUPABASE_KEY")

# Acceso rapido de la copia de pruebas. Con RECORDAR_SESION=1 en el .env, el
# programa guarda la sesion al entrar y la reanuda al abrirse, para no teclear
# correo y contrasena cada vez. Nunca se activa contra la base de la escuela,
# aunque alguien copie la bandera a ese .env.
PROYECTO_DE_LA_ESCUELA = "gibenzgxkbmalljqroxe"
ARCHIVO_DE_SESION = RAIZ_PROYECTO / ".sesion_recordada"


def recordar_sesion_permitido(url: str, bandera: str | None) -> bool:
    return bandera == "1" and PROYECTO_DE_LA_ESCUELA not in url


RECORDAR_SESION = recordar_sesion_permitido(SUPABASE_URL, os.getenv("RECORDAR_SESION"))

# Boton «Entrar rapido» de la copia de pruebas. El correo y la contrasena de la
# cuenta de pruebas los escribe en su .env quien usa esa copia; el repositorio
# no guarda ninguno. Tampoco aparece contra la base de la escuela.
PRUEBAS_CORREO = os.getenv("PRUEBAS_CORREO", "").strip()
PRUEBAS_CONTRASENA = os.getenv("PRUEBAS_CONTRASENA", "")


def acceso_de_pruebas_permitido(url: str, correo: str, contrasena: str) -> bool:
    return bool(correo and contrasena) and PROYECTO_DE_LA_ESCUELA not in url


ACCESO_DE_PRUEBAS = acceso_de_pruebas_permitido(
    SUPABASE_URL, PRUEBAS_CORREO, PRUEBAS_CONTRASENA
)

# Reglas de negocio del Avance 1
DIAS_DE_PRESTAMO = 7          # REQ-PRE-02
LIBROS_POR_USUARIO = 1        # REQ-PRE-01
