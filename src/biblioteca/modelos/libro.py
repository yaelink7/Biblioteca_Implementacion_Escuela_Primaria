"""Catalogo de la biblioteca.

Migra Publicacion.java y Libro.java del sistema Java, conservando la herencia
del diseno original: Libro extiende Publicacion.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Self

# Colecciones de Libros del Rincon, con los grados que acordo la escuela
# (LIB-06). Son las mismas que acepta la restriccion libros_coleccion_valida
# de la migracion 11: agregar una aqui sin agregarla alla no la deja guardar.
COLECCIONES: dict[str, str] = {
    "Al sol solito": "1.º",
    "Pasos de luna": "1.º y 2.º",
    "Astrolabio": "3.º y 4.º",
    "Espejo de Urania": "5.º y 6.º",
    "Cometas convidados": "sin grado asignado",
}

# Asignaturas tradicionales (LIB-07), las de libros_asignatura_valida
ASIGNATURAS: tuple[str, ...] = (
    "Español",
    "Matemáticas",
    "Ciencias Naturales",
    "Historia",
    "Geografía",
    "Formación Cívica y Ética",
    "Artes",
    "Inglés",
)


@dataclass
class Publicacion:
    """Datos comunes de cualquier material del acervo."""

    titulo: str
    autor: str
    ano_publicacion: int | None = None
    existencias: int = 0

    id: int | None = None

    @property
    def disponible(self) -> bool:
        """En el Java esto era una columna aparte que podia contradecir al
        inventario. Aqui se deduce, que es la unica forma de que no mienta."""
        return self.existencias > 0


@dataclass
class Libro(Publicacion):
    """Un titulo del acervo. Migra Libro.java del sistema Java."""

    tipo_libro: str | None = None
    editorial: str | None = None
    num_paginas: int | None = None
    coleccion: str | None = None
    asignatura: str | None = None

    activo: bool = True
    motivo_baja: str | None = None
    dado_baja_en: date | None = None

    @property
    def etiqueta(self) -> str:
        """Como se nombra el libro en listas y mensajes al usuario."""
        return f"{self.titulo} — {self.autor}"

    @property
    def estado(self) -> str:
        """Texto corto para la columna de estado en la tabla del catalogo."""
        if not self.activo:
            return f"Baja: {self.motivo_baja or 'sin motivo'}"
        if self.existencias == 0:
            return "Sin ejemplares"
        return f"{self.existencias} disponible{'s' if self.existencias != 1 else ''}"

    @classmethod
    def desde_fila(cls, fila: dict[str, Any]) -> Self:
        baja = fila.get("dado_baja_en")
        return cls(
            id=fila.get("id"),
            titulo=fila["titulo"],
            autor=fila["autor"],
            ano_publicacion=fila.get("ano_publicacion"),
            existencias=fila.get("existencias", 0),
            tipo_libro=fila.get("tipo_libro"),
            editorial=fila.get("editorial"),
            num_paginas=fila.get("num_paginas"),
            coleccion=fila.get("coleccion"),
            asignatura=fila.get("asignatura"),
            activo=fila.get("activo", True),
            motivo_baja=fila.get("motivo_baja"),
            dado_baja_en=date.fromisoformat(baja[:10]) if baja else None,
        )

    def a_fila(self) -> dict[str, Any]:
        """Columnas de la tabla libros. El id lo genera Postgres en el alta."""
        fila: dict[str, Any] = {
            "titulo": self.titulo,
            "autor": self.autor,
            "tipo_libro": self.tipo_libro,
            "editorial": self.editorial,
            "existencias": self.existencias,
            "ano_publicacion": self.ano_publicacion,
            "num_paginas": self.num_paginas,
            "coleccion": self.coleccion,
            "asignatura": self.asignatura,
        }
        if self.id is not None:
            fila["id"] = self.id
        return fila
