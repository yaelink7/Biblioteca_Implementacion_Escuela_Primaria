"""Explica por que fallo una operacion, en lugar de culpar siempre a internet.

Antes cada pantalla respondia lo mismo ante cualquier excepcion: «Revisa tu
conexion a internet». Un permiso que falta, una sesion vencida, una regla de
la base y un defecto de programacion se veian identicos, y el bibliotecario no
tenia forma de saber si el problema era suyo, del sistema o del cable de red.

Aqui se clasifica la excepcion y se arma un mensaje con tres partes: que paso,
que hacer al respecto, y el detalle tecnico por si hay que reportarlo. Eso es
lo que pide RNF-USA-03.

**Este es el unico traductor de errores del proyecto.** Los repositorios lo
invocan desde su `_mensaje_claro()`; no deben mantener sus propias listas. Hubo
tres y se contradecian entre si: el mismo `duplicate key` significaba «ya
existe un libro», «este alumno ya tiene un prestamo activo» o «ya existe un
registro», segun que modulo atrapara el error.

Las señales de REGLAS_DE_LA_BASE **estan copiadas de los `raise exception` de
`database/migraciones/`**. Si se cambia el texto de un disparador, hay que
cambiarlo aqui: una señal que no coincide deja al bibliotecario leyendo el
volcado crudo de Postgres. Antes pasaba con tres de las reglas mas usadas.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field

#: Excepciones propias del proyecto. Envuelven al error de la base, asi que se
#: desenvuelven antes de clasificar: el original dice mucho mas que el envoltorio.
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

#: Credenciales que no corresponden. No es lo mismo que una sesion vencida.
_CREDENCIALES = ("invalid login credentials", "invalid_credentials")

#: Sesion caducada. **Sin «401» ni «unauthorized» a secas**: son subcadenas que
#: aparecen dentro de cualquier identificador o cantidad —un libro con id 1401—
#: y mandaban al bibliotecario a reiniciar sesion ante un error de inventario.
_SESION = (
    "jwt expired", "jwt is expired", "invalid jwt", "token is expired",
    "token has expired", "not authenticated", "invalid claim",
    "session_not_found", "refresh_token_not_found",
)

_PERMISOS = (
    "row-level security", "row level security", "42501", "permission denied",
    "insufficient privilege",
)

#: Reglas de negocio que viven en Postgres, en orden de especificidad. La llave
#: es lo que la base responde **literalmente**; el valor, lo que el
#: bibliotecario necesita leer y hacer.
REGLAS_DE_LA_BASE = (
    # database/migraciones/03_prestamos_y_reglas.sql
    ("prestamo_unico_activo",
     "Este alumno ya tiene un préstamo activo.",
     "Solo se permite un libro por alumno. Registra primero la devolución."),
    ("no hay ejemplares disponibles",
     "No quedan ejemplares disponibles de este libro.",
     "Espera a que alguien devuelva uno, o revisa las existencias en el catálogo."),
    ("esta dado de baja del acervo",
     "Ese libro está dado de baja del acervo.",
     "No se puede prestar. Si volvió a la biblioteca, reactívalo en el catálogo."),
    ("sin devolver",
     "El libro tiene ejemplares prestados.",
     "No se puede dar de baja hasta que regresen. Revísalos en Préstamos."),
    ("devolucion_coherente",
     "La fecha de devolución no corresponde al estado del préstamo.",
     "Marca el préstamo como devuelto en lugar de escribir la fecha a mano."),
    # database/migraciones/02_catalogo_y_bitacora.sql
    ("no puede ser futuro",
     "El año de publicación no puede ser futuro.",
     "Corrige el año y vuelve a guardar."),
    ("ano de publicacion",
     "El año de publicación no es válido.",
     "Escribe un año entre 1400 y el actual."),
    ("baja_con_motivo",
     "Falta indicar el motivo de la baja.",
     "Escribe por qué se da de baja el libro y vuelve a guardar."),
    # database/migraciones/06 y 07 — altas y cambios de personas
    ("no puede tener perfil de alumno",
     "Un empleado no puede quedar con perfil de alumno.",
     "Elige Bibliotecario o Administrador en el perfil de acceso."),
    ("no se encontro el alumno",
     "Ese alumno ya no existe en el padrón.",
     "Puede que alguien lo haya dado de baja. Actualiza la pantalla."),
    # database/migraciones/09 — proteccion del perfil de acceso
    ("tu propio perfil de acceso",
     "No puedes cambiar tu propio perfil de acceso.",
     "Pídeselo a un administrador."),
    ("solo un administrador puede cambiar",
     "Solo un administrador cambia el perfil de acceso de alguien.",
     "Pídele a un administrador que haga el cambio."),
    # Restricciones genericas
    ("perfiles_codigo_key",
     "Ya existe una persona registrada con ese código.",
     "Usa un código distinto: el sistema no admite dos iguales."),
    ("duplicate key",
     "Ya existe un registro con ese identificador.",
     "Usa un código distinto: el sistema no admite dos iguales."),
    ("foreign key",
     "El registro al que haces referencia no existe.",
     "Puede que alguien lo haya dado de baja. Actualiza la pantalla."),
    ("existencias",
     "El movimiento dejaría el inventario en negativo.",
     "Revisa cuántos ejemplares hay registrados de este libro."),
)


def _normalizar(texto: str) -> str:
    """Minusculas y sin acentos.

    Los mensajes de las migraciones se escribieron sin acentos («ano», «esta»)
    y los de las funciones de personas con ellos («No se encontró»). Comparar
    sobre el texto normalizado evita que una tilde decida si el bibliotecario
    entiende el error o lee un volcado de Postgres.
    """
    sin_acentos = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in sin_acentos if unicodedata.category(c) != "Mn")


@dataclass(frozen=True)
class Explicacion:
    """Lo que hay que decirle a quien esta frente a la pantalla."""

    causa: str
    que_hacer: str = ""
    detalle: str = ""
    tipo: str = field(default="desconocido")

    @property
    def es_de_red(self) -> bool:
        return self.tipo == "red"

    def __str__(self) -> str:
        partes = [p for p in (self.causa, self.que_hacer) if p]
        if self.detalle:
            partes.append(f"Detalle técnico: {self.detalle}")
        return "\n\n".join(partes)


def _detalle(tipo: str, texto: str) -> str:
    return f"{tipo}: {texto}" if texto else tipo


def explicar(error: Exception) -> Explicacion:
    """Clasifica la excepcion y devuelve que decir sobre ella."""
    tipo = type(error).__name__

    # Un error propio envuelve al de la base. El original trae la señal que
    # permite decir «no quedan ejemplares» en vez de repetir el envoltorio.
    if tipo in ERRORES_PROPIOS:
        origen = error.__cause__
        if origen is not None:
            interpretacion = explicar(origen)
            if interpretacion.tipo != "desconocido":
                return interpretacion
        return Explicacion(
            str(error) or "La operación no se pudo completar.",
            "Vuelve a intentarlo. Si sigue fallando, avisa al equipo.",
            tipo="propio",
        )

    texto = str(error)
    buscar = _normalizar(f"{tipo} {texto}")

    if any(s in buscar for s in _SIN_RED):
        return Explicacion(
            "No hay conexión con el servidor de la biblioteca.",
            "Revisa que el equipo tenga internet e inténtalo otra vez. "
            "Si la conexión sí funciona, el servicio puede estar caído.",
            _detalle(tipo, texto), "red",
        )

    # Las reglas del negocio van antes que sesion y permisos: son las señales
    # mas especificas, y su texto puede contener cualquier cosa.
    for senal, causa, que_hacer in REGLAS_DE_LA_BASE:
        if senal in buscar:
            return Explicacion(causa, que_hacer, _detalle(tipo, texto), "regla")

    if any(s in buscar for s in _CREDENCIALES):
        return Explicacion(
            "Correo o contraseña incorrectos.",
            "Revisa que el correo esté bien escrito y vuelve a intentarlo.",
            _detalle(tipo, texto), "credenciales",
        )

    if any(s in buscar for s in _PERMISOS):
        return Explicacion(
            "Tu perfil no tiene permiso para hacer esto.",
            "Pídele a un administrador que realice la operación o que te "
            "asigne el permiso.",
            _detalle(tipo, texto), "permisos",
        )

    if any(s in buscar for s in _SESION):
        return Explicacion(
            "Tu sesión ya no es válida.",
            "Cierra sesión y vuelve a entrar con tu correo y contraseña.",
            _detalle(tipo, texto), "sesion",
        )

    if tipo in DEFECTOS:
        return Explicacion(
            "El sistema tuvo un error interno. No es un problema de tu conexión.",
            "Avisa al equipo de desarrollo y pásale el detalle de abajo. "
            "Mientras tanto, la información guardada no corre riesgo.",
            _detalle(tipo, texto), "defecto",
        )

    return Explicacion(
        "La operación no se pudo completar.",
        "Vuelve a intentarlo. Si sigue fallando, pasa el detalle de abajo al "
        "equipo de desarrollo: sirve para saber si es la conexión, un permiso "
        "o un defecto del sistema.",
        _detalle(tipo, texto),
    )


def mensaje(error: Exception) -> str:
    """El texto completo, para el cuadro de diálogo de una pantalla."""
    return str(explicar(error))


def causa(error: Exception) -> str:
    """Solo la primera línea, para una etiqueta de una sola fila."""
    return explicar(error).causa
