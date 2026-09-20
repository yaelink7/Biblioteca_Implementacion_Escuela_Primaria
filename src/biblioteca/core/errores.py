"""Explica por que fallo una operacion, en lugar de culpar siempre a internet.

Hasta ahora todas las pantallas respondian lo mismo ante cualquier excepcion:
«Revisa tu conexion a internet». Eso escondia el motivo real. Un permiso que
falta, una regla de la base, una sesion vencida y un error de programacion se
veian identicos, y el bibliotecario no tenia forma de saber si el problema era
suyo, del sistema o del cable de red.

Aqui se clasifica la excepcion y se arma un mensaje con tres partes: que paso,
que hacer al respecto, y el detalle tecnico por si hay que reportarlo. Eso es
lo que pide RNF-USA-03.

El reconocimiento se hace por el nombre de la clase y por el texto del error, no
importando librerias de terceros: asi sigue funcionando aunque supabase-py
cambie sus tipos internos.
"""

from __future__ import annotations

from dataclasses import dataclass

#: Excepciones propias del proyecto. Su texto ya esta escrito para el
#: bibliotecario, asi que se muestra tal cual y no se le agrega nada.
ERRORES_PROPIOS = (
    "ErrorDeAcceso",
    "ErrorDeCatalogo",
    "ErrorDePersona",
    "ErrorDePrestamo",
)

#: Fallos de programacion. Si aparecen, el sistema tiene un defecto: no hay
#: nada que el bibliotecario pueda corregir por su cuenta.
DEFECTOS = (
    "AttributeError",
    "IndexError",
    "KeyError",
    "NameError",
    "TypeError",
    "UnboundLocalError",
    "ZeroDivisionError",
)

_SIN_RED = (
    "connecterror", "connecttimeout", "connectionerror", "connectionreset",
    "readtimeout", "writetimeout", "pooltimeout", "remoteprotocolerror",
    "gaierror", "getaddrinfo", "name or service not known", "connection refused",
    "network is unreachable", "temporary failure in name resolution",
    "max retries", "failed to establish a new connection", "no address associated",
)

_SESION = (
    "jwt expired", "jwt is expired", "invalid jwt", "token is expired",
    "not authenticated", "invalid claim", "401", "unauthorized",
)

_PERMISOS = (
    "row-level security", "row level security", "42501", "permission denied",
    "insufficient privilege", "no tiene permiso",
)

#: Reglas de negocio que viven en Postgres. La llave es lo que la base
#: responde; el valor, lo que el bibliotecario necesita leer.
REGLAS_DE_LA_BASE = {
    "prestamo_unico_activo": (
        "Este alumno ya tiene un préstamo activo.",
        "Solo se permite un libro por alumno. Registra primero la devolución.",
    ),
    "sin ejemplares": (
        "No quedan ejemplares disponibles de este libro.",
        "Espera a que alguien devuelva uno, o revisa las existencias en el catálogo.",
    ),
    "existencias": (
        "El movimiento dejaría el inventario en negativo.",
        "Revisa cuántos ejemplares hay registrados de este libro.",
    ),
    "prestamos activos": (
        "El libro tiene préstamos activos.",
        "No se puede dar de baja hasta que los ejemplares prestados regresen.",
    ),
    "ano_publicacion": (
        "El año de publicación no puede ser futuro.",
        "Corrige el año y vuelve a guardar.",
    ),
    "duplicate key": (
        "Ya existe un registro con ese identificador.",
        "Usa un código distinto: el sistema no admite dos iguales.",
    ),
    "foreign key": (
        "El registro al que haces referencia no existe.",
        "Puede que alguien lo haya dado de baja. Actualiza la pantalla.",
    ),
    "perfil de acceso": (
        "No puedes cambiar ese perfil de acceso.",
        "Solo un administrador cambia perfiles, y nadie cambia el suyo propio.",
    ),
}


@dataclass(frozen=True)
class Explicacion:
    """Lo que hay que decirle a quien esta frente a la pantalla."""

    causa: str
    que_hacer: str
    detalle: str = ""

    @property
    def es_de_red(self) -> bool:
        return self.causa.startswith("No hay conexión")

    def __str__(self) -> str:
        partes = [self.causa, self.que_hacer]
        if self.detalle:
            partes.append(f"Detalle técnico: {self.detalle}")
        return "\n\n".join(partes)


def explicar(error: Exception) -> Explicacion:
    """Clasifica la excepcion y devuelve que decir sobre ella."""
    tipo = type(error).__name__
    texto = str(error)
    buscar = f"{tipo} {texto}".lower()

    # Los errores propios ya traen un mensaje pensado para el bibliotecario.
    if tipo in ERRORES_PROPIOS:
        return Explicacion(texto or "La operación no se pudo completar.", "")

    if any(s in buscar for s in _SIN_RED):
        return Explicacion(
            "No hay conexión con el servidor de la biblioteca.",
            "Revisa que el equipo tenga internet e inténtalo otra vez. "
            "Si la conexión sí funciona, el servicio puede estar caído.",
            f"{tipo}: {texto}" if texto else tipo,
        )

    if any(s in buscar for s in _SESION):
        return Explicacion(
            "Tu sesión ya no es válida.",
            "Cierra sesión y vuelve a entrar con tu correo y contraseña.",
            f"{tipo}: {texto}" if texto else tipo,
        )

    if any(s in buscar for s in _PERMISOS):
        return Explicacion(
            "Tu perfil no tiene permiso para hacer esto.",
            "Pídele a un administrador que realice la operación o que te "
            "asigne el permiso.",
            f"{tipo}: {texto}" if texto else tipo,
        )

    for senal, (causa, que_hacer) in REGLAS_DE_LA_BASE.items():
        if senal in buscar:
            return Explicacion(causa, que_hacer, f"{tipo}: {texto}")

    if tipo in DEFECTOS:
        return Explicacion(
            "El sistema tuvo un error interno. No es un problema de tu conexión.",
            "Avisa al equipo de desarrollo y pásale el detalle de abajo. "
            "Mientras tanto, la información guardada no corre riesgo.",
            f"{tipo}: {texto}" if texto else tipo,
        )

    return Explicacion(
        "La operación no se pudo completar.",
        "Vuelve a intentarlo. Si sigue fallando, pasa el detalle de abajo al "
        "equipo de desarrollo: sirve para saber si es la conexión, un permiso "
        "o un defecto del sistema.",
        f"{tipo}: {texto}" if texto else tipo,
    )


def mensaje(error: Exception) -> str:
    """El texto completo, para el cuadro de diálogo de una pantalla."""
    return str(explicar(error))


def causa(error: Exception) -> str:
    """Solo la primera línea, para una etiqueta de una sola fila."""
    return explicar(error).causa
