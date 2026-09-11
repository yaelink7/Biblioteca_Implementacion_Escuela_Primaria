"""Acceso a datos. Migra el paquete DAOBiblia del proyecto Java."""

from biblioteca.repositorios import libros, personas, prestamos

__all__ = ["libros", "personas", "prestamos"]
