"""Modelos del dominio. Migra el paquete ClasesBiblia del proyecto Java."""

from biblioteca.modelos.libro import Libro, Publicacion
from biblioteca.modelos.persona import Alumno, Empleado, Perfil, Rol
from biblioteca.modelos.prestamo import EstadoPrestamo, Prestamo

__all__ = [
    "Alumno",
    "Empleado",
    "EstadoPrestamo",
    "Libro",
    "Perfil",
    "Prestamo",
    "Publicacion",
    "Rol",
]
