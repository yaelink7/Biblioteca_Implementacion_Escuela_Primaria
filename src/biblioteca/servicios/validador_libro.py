"""Validacion del alta y modificacion de libros.

Responde a la recomendacion de prioridad alta del Reporte Tecnico de Calidad:
"extraer las validaciones de GUILibro a una clase ValidadorLibro independiente
de Swing". En el proyecto Java estas reglas vivian dentro de metodos privados
del formulario, lo que dejaba la cobertura de ramas de la capa grafica en 14 %.

Aqui no dependen de ninguna ventana, asi que se prueban sin abrir la interfaz.

El defecto de fondo que corrige: tres validaciones del original median la
LONGITUD del texto capturado en lugar de su VALOR numerico. Como la regla de
campo obligatorio ya habia descartado las cadenas vacias, esas comprobaciones
nunca se cumplian y el sistema aceptaba justo los datos que sus mensajes de
error decian rechazar.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from biblioteca.modelos.libro import Libro

ANO_MINIMO = 1400


@dataclass
class Resultado:
    """Lo que encontro la validacion. Sin errores significa que pasa."""

    errores: list[str] = field(default_factory=list)

    @property
    def es_valido(self) -> bool:
        return not self.errores

    @property
    def mensaje(self) -> str:
        """Todos los errores en un texto, para mostrarlo en un cuadro de dialogo."""
        if self.es_valido:
            return ""
        if len(self.errores) == 1:
            return self.errores[0]
        return "\n".join(f"• {e}" for e in self.errores)

    def __bool__(self) -> bool:
        return self.es_valido


def validar(libro: Libro, es_alta: bool = True) -> Resultado:
    """Revisa un libro antes de guardarlo.

    es_alta distingue los dos momentos: al registrar un titulo nuevo debe
    haber al menos un ejemplar, pero un libro ya registrado puede quedarse
    en cero cuando todos sus ejemplares estan prestados.
    """
    r = Resultado()

    # Campos obligatorios. El trim es lo que hace que "   " cuente como vacio.
    if not libro.titulo or not libro.titulo.strip():
        r.errores.append("El título es obligatorio.")
    if not libro.autor or not libro.autor.strip():
        r.errores.append("El autor es obligatorio.")

    # D-06: se compara el VALOR, no la longitud del texto.
    if libro.existencias < 0:
        r.errores.append("Las existencias no pueden ser negativas.")
    elif es_alta and libro.existencias == 0:
        r.errores.append(
            "Un libro nuevo debe registrarse con al menos un ejemplar."
        )

    # D-07: mismo error de origen, aplicado al numero de paginas.
    if libro.num_paginas is not None and libro.num_paginas <= 0:
        r.errores.append("El número de páginas debe ser mayor que cero.")

    # D-08: se compara contra el ano actual, no contra la cantidad de digitos.
    # El original aceptaba 9999 porque tiene cuatro caracteres.
    if libro.ano_publicacion is not None:
        ano_actual = date.today().year
        if libro.ano_publicacion > ano_actual:
            r.errores.append(
                f"El año de publicación no puede ser futuro "
                f"(el año actual es {ano_actual})."
            )
        elif libro.ano_publicacion < ANO_MINIMO:
            r.errores.append(
                f"El año de publicación debe ser posterior a {ANO_MINIMO}."
            )

    return r
