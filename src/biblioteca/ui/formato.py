"""Textos cortos que muestran las pantallas: fechas y la inicial de un libro.

No dependen del idioma configurado en la computadora: la de la biblioteca
puede estar en ingles y la fecha tiene que salir igual.
"""

from __future__ import annotations

from datetime import date

MESES = ("ene", "feb", "mar", "abr", "may", "jun",
         "jul", "ago", "sep", "oct", "nov", "dic")

# Se saltan al elegir la letra de la portada: «El principito» va en la P
ARTICULOS = ("el ", "la ", "los ", "las ", "un ", "una ")


def fecha_corta(fecha: date) -> str:
    """«3 nov 2026»."""
    return f"{fecha.day} {MESES[fecha.month - 1]} {fecha.year}"


def inicial(titulo: str) -> str:
    """La letra que va en la portada del libro, sin el articulo inicial."""
    texto = titulo.strip().lstrip("¿¡«\"'(")
    for articulo in ARTICULOS:
        if texto.lower().startswith(articulo) and len(texto) > len(articulo):
            texto = texto[len(articulo):]
            break
    return texto[:1].upper() or "?"
