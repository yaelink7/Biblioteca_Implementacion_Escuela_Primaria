"""Sesion del usuario que opera el sistema.

Cubre REQ-USU-02. El proyecto Java abria directo en el menu principal sin
validar quien entraba; aqui nada se puede leer sin iniciar sesion, porque
las politicas RLS de Supabase solo responden a usuarios autenticados.
"""

from __future__ import annotations

from dataclasses import dataclass

from biblioteca.core.supabase_cliente import obtener_cliente
from biblioteca.modelos.persona import Perfil, Rol


class ErrorDeAcceso(Exception):
    """Las credenciales no sirven, o la cuenta no tiene perfil asignado."""


@dataclass
class Sesion:
    """Quien esta usando el sistema en este momento."""

    perfil: Perfil

    @property
    def es_personal(self) -> bool:
        return self.perfil.rol.es_personal

    @property
    def saludo(self) -> str:
        return f"{self.perfil.nombre_completo} · {self.perfil.rol.value.capitalize()}"


_sesion_actual: Sesion | None = None


def iniciar_sesion(correo: str, contrasena: str) -> Sesion:
    """Valida las credenciales y carga el perfil de quien entra.

    El mensaje de error es el mismo para correo inexistente y contrasena
    incorrecta: REQ-USU-02 pide no revelar cual de los dos fallo.
    """
    global _sesion_actual
    cliente = obtener_cliente()

    try:
        respuesta = cliente.auth.sign_in_with_password(
            {"email": correo, "password": contrasena}
        )
    except Exception as error:
        raise ErrorDeAcceso("Correo o contraseña incorrectos.") from error

    if not respuesta.user:
        raise ErrorDeAcceso("Correo o contraseña incorrectos.")

    filas = (
        cliente.table("perfiles")
        .select("*")
        .eq("auth_id", respuesta.user.id)
        .limit(1)
        .execute()
    )
    if not filas.data:
        cerrar_sesion()
        raise ErrorDeAcceso(
            "La cuenta existe pero no tiene un perfil asignado. "
            "Pide al administrador que te registre."
        )

    _sesion_actual = Sesion(perfil=Perfil.desde_fila(filas.data[0]))
    return _sesion_actual


def cerrar_sesion() -> None:
    global _sesion_actual
    _sesion_actual = None
    try:
        obtener_cliente().auth.sign_out()
    except Exception:
        pass  # cerrar sesion nunca debe impedir salir de la aplicacion


def sesion_actual() -> Sesion:
    """Sesion en curso. Falla si nadie ha iniciado sesion."""
    if _sesion_actual is None:
        raise ErrorDeAcceso("No hay una sesión iniciada.")
    return _sesion_actual


def hay_sesion() -> bool:
    return _sesion_actual is not None


def exigir_personal() -> Sesion:
    """Para operaciones que solo el personal de la biblioteca puede hacer."""
    sesion = sesion_actual()
    if not sesion.es_personal:
        raise ErrorDeAcceso(
            "Esta operación solo la puede realizar el personal de la biblioteca."
        )
    return sesion


__all__ = [
    "ErrorDeAcceso",
    "Rol",
    "Sesion",
    "cerrar_sesion",
    "exigir_personal",
    "hay_sesion",
    "iniciar_sesion",
    "sesion_actual",
]
