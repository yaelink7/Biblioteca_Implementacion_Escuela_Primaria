"""Punto unico de acceso a Supabase.

Equivale a ConexionBD.java del sistema Java, pero en lugar de abrir una conexion
nueva en cada llamada se reutiliza un solo cliente.
"""

from functools import lru_cache

from supabase import Client, create_client

from biblioteca.core.config import SUPABASE_KEY, SUPABASE_URL


@lru_cache(maxsize=1)
def obtener_cliente() -> Client:
    """Devuelve el cliente de Supabase, creandolo la primera vez."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)
