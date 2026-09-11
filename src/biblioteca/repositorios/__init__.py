"""Acceso a datos. Sustituye al paquete de acceso a datos del sistema Java."""

from biblioteca.repositorios import libros, personas, prestamos

__all__ = ["libros", "personas", "prestamos"]
