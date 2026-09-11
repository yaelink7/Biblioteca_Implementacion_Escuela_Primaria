"""Acceso al catalogo. Migra DAOBiblia/LibroDao.java."""

from __future__ import annotations

from biblioteca.core.supabase_cliente import obtener_cliente
from biblioteca.modelos.libro import Libro

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

    patron = f"%{texto}%"
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
    return Libro.desde_fila(filas.data[0]) if filas.data else None


def dar_de_alta(libro: Libro) -> Libro:
    """Registra un libro nuevo (REQ-LIB-01).

    Postgres valida el ano de publicacion y los campos obligatorios; aqui
    solo se traduce el error a algo que el bibliotecario entienda.
    """
    datos = libro.a_fila()
    datos.pop("id", None)  # lo genera la base

    try:
        filas = obtener_cliente().table(TABLA).insert(datos).execute()
    except Exception as error:
        raise ErrorDeCatalogo(_mensaje_claro(error)) from error

    return Libro.desde_fila(filas.data[0])


def modificar(libro: Libro) -> Libro:
    """Actualiza un libro existente (REQ-LIB-02)."""
    if libro.id is None:
        raise ErrorDeCatalogo("No se puede modificar un libro sin identificador.")

    datos = libro.a_fila()
    datos.pop("id")

    try:
        filas = obtener_cliente().table(TABLA).update(datos).eq("id", libro.id).execute()
    except Exception as error:
        raise ErrorDeCatalogo(_mensaje_claro(error)) from error

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
    """Traduce el error crudo de Postgres a algo accionable."""
    texto = str(error)

    if "ano_publicacion" in texto or "futuro" in texto:
        return "El año de publicación no puede ser futuro."
    if "prestamos activos" in texto or "prestamo activo" in texto:
        return "No se puede dar de baja: el libro tiene préstamos activos."
    if "existencias" in texto:
        return "Las existencias no pueden quedar en negativo."
    if "duplicate key" in texto or "unique" in texto:
        return "Ya existe un libro con ese identificador."
    if "violates row-level security" in texto or "42501" in texto:
        return "Tu perfil no tiene permiso para modificar el catálogo."
    return f"La base de datos rechazó la operación: {texto}"
