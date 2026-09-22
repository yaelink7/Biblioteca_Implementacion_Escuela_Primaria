"""Acceso al catalogo. Migra LibroDao.java del sistema Java."""

from __future__ import annotations

from biblioteca.core.consultas import patron_de_busqueda
from biblioteca.core.errores import causa as causa_del_error
from biblioteca.core.supabase_cliente import obtener_cliente
from biblioteca.modelos.libro import Libro
from biblioteca.servicios import validador_libro

TABLA = "libros"
_COLUMNAS = (
    "id, titulo, autor, tipo_libro, editorial, existencias, "
    "ano_publicacion, num_paginas, activo, motivo_baja, dado_baja_en"
)


class ErrorDeCatalogo(Exception):
    """Una operacion sobre el catalogo fue rechazada por la base de datos."""


def listar(incluir_bajas: bool = False) -> list[Libro]:
    """Todos los libros del acervo, ordenados por titulo."""
    consulta = obtener_cliente().table(TABLA).select(_COLUMNAS)
    if not incluir_bajas:
        consulta = consulta.eq("activo", True)
    filas = consulta.order("titulo").execute()
    return [Libro.desde_fila(f) for f in filas.data]


def buscar(texto: str) -> list[Libro]:
    """Busqueda por coincidencia parcial en titulo, autor o tipo (REQ-BUS-01).

    El usuario no necesita el nombre exacto: "prin" encuentra "El principito".
    """
    texto = texto.strip()
    if not texto:
        return listar()

    patron = patron_de_busqueda(texto)
    filas = (
        obtener_cliente()
        .table(TABLA)
        .select(_COLUMNAS)
        .eq("activo", True)
        .or_(f"titulo.ilike.{patron},autor.ilike.{patron},tipo_libro.ilike.{patron}")
        .order("titulo")
        .execute()
    )
    return [Libro.desde_fila(f) for f in filas.data]


def obtener(libro_id: int) -> Libro | None:
    filas = (
        obtener_cliente().table(TABLA).select(_COLUMNAS).eq("id", libro_id).execute()
    )
    # Una lectura que no encuentra nada no es un error: devuelve None.
    return Libro.desde_fila(filas.data[0]) if filas.data else None


def dar_de_alta(libro: Libro) -> Libro:
    """Registra un libro nuevo (REQ-LIB-01).

    Valida antes de tocar la base: el validador atrapa los defectos D-06,
    D-07 y D-08 del Reporte Tecnico de Calidad y explica los tres de una vez,
    en lugar de que Postgres rechace solo el primero que encuentre.
    """
    revision = validador_libro.validar(libro, es_alta=True)
    if not revision.es_valido:
        raise ErrorDeCatalogo(revision.mensaje)

    datos = libro.a_fila()
    datos.pop("id", None)  # lo genera la base

    try:
        filas = obtener_cliente().table(TABLA).insert(datos).execute()
    except Exception as error:
        raise ErrorDeCatalogo(_mensaje_claro(error)) from error

    if not filas.data:
        # Sin esta guarda, un insert que no devuelve la fila —por ejemplo si
        # RLS deja escribir pero no leer— reventaba con IndexError, que
        # ninguna pantalla atrapa: el diálogo se quedaba colgado sin decir nada.
        raise ErrorDeCatalogo(
            "La base no devolvió el libro después de guardarlo. "
            "Actualiza la pantalla y comprueba si quedó registrado."
        )
    return Libro.desde_fila(filas.data[0])


def modificar(libro: Libro) -> Libro:
    """Actualiza un libro existente (REQ-LIB-02)."""
    if libro.id is None:
        raise ErrorDeCatalogo("No se puede modificar un libro sin identificador.")

    # es_alta=False: un libro ya registrado si puede quedar en cero ejemplares
    # cuando todos estan prestados.
    revision = validador_libro.validar(libro, es_alta=False)
    if not revision.es_valido:
        raise ErrorDeCatalogo(revision.mensaje)

    datos = libro.a_fila()
    datos.pop("id")

    try:
        filas = obtener_cliente().table(TABLA).update(datos).eq("id", libro.id).execute()
    except Exception as error:
        raise ErrorDeCatalogo(_mensaje_claro(error)) from error

    if not filas.data:
        # Sin esta guarda un UPDATE que no afecta filas —id que ya
        # no existe, o fila invisible por RLS— reventaba con
        # IndexError, que ninguna pantalla atrapa.
        raise ErrorDeCatalogo(
            "La base no devolvió el libro después de guardar. "
            "Actualiza la pantalla y comprueba si el cambio quedó."
        )
    return Libro.desde_fila(filas.data[0])


def dar_de_baja(libro_id: int, motivo: str) -> None:
    """Baja logica (REQ-LIB-03).

    Postgres rechaza la baja si el libro tiene prestamos activos; el
    proyecto Java borraba el registro y se llevaba el historial con el.
    """
    if not motivo.strip():
        raise ErrorDeCatalogo("Indica el motivo de la baja.")

    try:
        (
            obtener_cliente()
            .table(TABLA)
            .update(
                {
                    "activo": False,
                    "motivo_baja": motivo.strip(),
                    "dado_baja_en": "now()",
                }
            )
            .eq("id", libro_id)
            .execute()
        )
    except Exception as error:
        raise ErrorDeCatalogo(_mensaje_claro(error)) from error


def _mensaje_claro(error: Exception) -> str:
    """Traduce el error de la base. El traductor vive en core/errores.py.

    Antes cada repositorio tenia su propia lista y se contradecian: el mismo
    `duplicate key` significaba tres cosas distintas segun quien lo atrapara.
    Ademas buscaban textos que los disparadores nunca emiten, asi que las
    reglas mas usadas llegaban al bibliotecario como volcado de Postgres.
    """
    return causa_del_error(error)
