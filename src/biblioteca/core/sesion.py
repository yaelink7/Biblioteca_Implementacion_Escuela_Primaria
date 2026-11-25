"""Sesion del usuario que opera el sistema.

Cubre REQ-USU-02. El proyecto Java abria directo en el menu principal sin
validar quien entraba; aqui nada se puede leer sin iniciar sesion, porque
las politicas RLS de Supabase solo responden a usuarios autenticados.
"""

from __future__ import annotations

from dataclasses import dataclass

from biblioteca.core.errores import causa as causa_del_error
from biblioteca.core.errores import causa as causa_del_error
from biblioteca.core.errores import causa as causa_del_error
from biblioteca.core import config
from biblioteca.core.supabase_cliente import obtener_cliente
from biblioteca.modelos.persona import Perfil, Rol
from supabase_auth.errors import AuthApiError


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
        # Antes cualquier excepcion salia como credenciales malas: sin
        # internet la bibliotecaria tecleaba su contrasena cinco veces y
        # terminaba cambiandola. El traductor distingue la causa, y para
        # credenciales sigue sin decir cual de los dos campos fallo
        # (REQ-USU-02).
        raise ErrorDeAcceso(causa_del_error(error)) from error

    if not respuesta.user:
        raise ErrorDeAcceso("Correo o contraseña incorrectos.")

    sesion = _cargar_perfil(cliente, respuesta.user.id)
    _recordar(getattr(respuesta, "session", None))
    return sesion


def _cargar_perfil(cliente, auth_id: str) -> Sesion:
    """Busca el perfil de la cuenta y deja la sesion lista para el programa."""
    global _sesion_actual
    filas = (
        cliente.table("perfiles")
        .select("*")
        .eq("auth_id", auth_id)
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


# ---------------------------------------------------------------------------
# Acceso rapido de la copia de pruebas (config.RECORDAR_SESION)
#
# Se guarda el permiso de renovacion que da Supabase, nunca la contrasena.
# En la base de la escuela nada de esto corre: la bandera no se activa ahi.
# ---------------------------------------------------------------------------

_escucha_activa = False


def restaurar_sesion_recordada() -> Sesion | None:
    """Reanuda la sesion guardada, o devuelve None para pedir entrar.

    Si el permiso guardado ya no sirve (vencio o se cerro sesion), se olvida.
    Sin internet se conserva para la proxima vez y el programa pide entrar
    como siempre, que es donde se explica la falta de conexion.
    """
    if not config.RECORDAR_SESION:
        return None
    try:
        guardado = config.ARCHIVO_DE_SESION.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    if not guardado:
        return None

    cliente = obtener_cliente()
    try:
        respuesta = cliente.auth.refresh_session(guardado)
    except AuthApiError:
        _olvidar_sesion_guardada()
        return None
    except Exception:
        return None
    if not respuesta.user:
        _olvidar_sesion_guardada()
        return None

    try:
        sesion = _cargar_perfil(cliente, respuesta.user.id)
    except Exception:
        return None  # sin perfil, _cargar_perfil ya cerro y olvido la sesion
    _recordar(getattr(respuesta, "session", None))
    return sesion


def _recordar(sesion_de_auth) -> None:
    """Guarda el permiso de la sesion para reanudarla al abrir de nuevo."""
    if not config.RECORDAR_SESION or sesion_de_auth is None:
        return
    _guardar_permiso(getattr(sesion_de_auth, "refresh_token", None))
    _escuchar_renovaciones()


def _guardar_permiso(permiso: str | None) -> None:
    if not permiso:
        return
    try:
        config.ARCHIVO_DE_SESION.write_text(permiso, encoding="utf-8")
    except OSError:
        pass  # sin poder guardarlo, la proxima vez solo se vuelve a pedir entrar


def _escuchar_renovaciones() -> None:
    """Supabase cambia el permiso cada vez que renueva la sesion.

    El archivo tiene que seguir al ultimo: uno ya usado no sirve para la
    proxima apertura.
    """
    global _escucha_activa
    if _escucha_activa:
        return

    def al_cambiar(evento, sesion_de_auth) -> None:
        if evento == "TOKEN_REFRESHED" and sesion_de_auth is not None:
            _guardar_permiso(sesion_de_auth.refresh_token)

    try:
        obtener_cliente().auth.on_auth_state_change(al_cambiar)
        _escucha_activa = True
    except Exception:
        pass


def _olvidar_sesion_guardada() -> None:
    try:
        config.ARCHIVO_DE_SESION.unlink(missing_ok=True)
    except OSError:
        pass


def cerrar_sesion(olvidar: bool = True) -> None:
    """Termina la sesion.

    En la copia de pruebas, cerrar la ventana (olvidar=False) solo suelta la
    sesion en memoria: sign_out revoca en Supabase el permiso guardado, y la
    proxima apertura volveria a pedir la contrasena. «Cerrar sesión» si la
    olvida, para poder entrar con otra cuenta.
    """
    global _sesion_actual
    _sesion_actual = None
    if config.RECORDAR_SESION:
        if not olvidar:
            return
        _olvidar_sesion_guardada()
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
    "restaurar_sesion_recordada",
    "sesion_actual",
]
