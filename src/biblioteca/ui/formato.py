"""Textos cortos que muestran las pantallas: fechas, salones, plurales.

No dependen del idioma configurado en la computadora: la de la biblioteca
puede estar en ingles y la fecha tiene que salir igual.
"""

from __future__ import annotations

import re
import unicodedata
from datetime import date

MESES = ("ene", "feb", "mar", "abr", "may", "jun",
         "jul", "ago", "sep", "oct", "nov", "dic")

# Se saltan al elegir la letra de la portada: «El principito» va en la P
ARTICULOS = ("el ", "la ", "los ", "las ", "un ", "una ")


def fecha_corta(fecha: date) -> str:
    """«3 nov 2026»."""
    return f"{fecha.day} {MESES[fecha.month - 1]} {fecha.year}"


def dia_y_mes(fecha: date) -> str:
    """«3 nov», para las tablas: el año casi siempre es el actual."""
    return f"{fecha.day} {MESES[fecha.month - 1]}"


def fecha_numerica(fecha: date | None) -> str:
    """«03/11/2026», o una raya si no hay fecha."""
    return fecha.strftime("%d/%m/%Y") if fecha else "—"


def plural(cantidad: int, singular: str, plural_: str | None = None) -> str:
    """«1 día», «3 días»; el plural irregular se pasa aparte."""
    return f"{cantidad} {singular if cantidad == 1 else (plural_ or singular + 's')}"


def salon(grado: int | None, grupo: str | None) -> str:
    """«4.º B», como lo escribe la escuela; «Sin salón» si falta algo."""
    if grado and grupo:
        return f"{grado}.º {grupo}"
    return "Sin salón"


def iniciales(nombre: str, apellido: str = "") -> str:
    """Las dos letras del avatar: la del nombre y la del primer apellido."""
    return f"{nombre.strip()[:1]}{apellido.strip()[:1]}".upper() or "?"


def sin_acentos(texto: str) -> str:
    """Minusculas y sin acentos: «Martínez» y «martinez» se encuentran igual."""
    descompuesto = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")


def es_salon(texto: str, grado: int | None, grupo: str | None) -> bool:
    """Si lo que se escribio es el salon: «4B», «4b» y «4.º B» valen igual."""
    if not (grado and grupo):
        return False
    clave = re.sub(r"[^0-9a-z]", "", sin_acentos(texto).replace("º", ""))
    return 2 <= len(clave) <= 3 and clave == f"{grado}{grupo}".lower()


def inicial(titulo: str) -> str:
    """La letra que va en la portada del libro, sin el articulo inicial."""
    texto = titulo.strip().lstrip("¿¡«\"'(")
    for articulo in ARTICULOS:
        if texto.lower().startswith(articulo) and len(texto) > len(articulo):
            texto = texto[len(articulo):]
            break
    return texto[:1].upper() or "?"
