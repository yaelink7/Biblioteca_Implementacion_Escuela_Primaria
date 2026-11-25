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

# Reglas de negocio del Avance 1
DIAS_DE_PRESTAMO = 7          # REQ-PRE-02
LIBROS_POR_USUARIO = 1        # REQ-PRE-01
