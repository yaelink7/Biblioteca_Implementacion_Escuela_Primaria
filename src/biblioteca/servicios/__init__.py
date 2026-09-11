"""Reglas de negocio independientes de la interfaz.

Capa nueva que no existia en el proyecto Java: alli las validaciones vivian
dentro de los formularios Swing, lo que dejaba la cobertura de ramas de
la capa grafica en 14 %. El Reporte Tecnico de Calidad lo senala como la
recomendacion de prioridad mas alta.
"""

from biblioteca.servicios import validador_libro, validador_persona

__all__ = ["validador_libro", "validador_persona"]
