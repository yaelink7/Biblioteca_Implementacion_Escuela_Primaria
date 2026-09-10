"""Configuracion del sistema, leida del archivo .env.

Sustituye a las credenciales que en el proyecto Java estaban escritas
directamente dentro de DAOBiblia/ConexionBD.java.
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

# Reglas de negocio del Avance 1
DIAS_DE_PRESTAMO = 7          # REQ-PRE-02
LIBROS_POR_USUARIO = 1        # REQ-PRE-01
