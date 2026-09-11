"""Prestamos y devoluciones. Migra PrestamoDao.java del sistema Java.

La fecha limite y el movimiento de inventario los calcula Postgres, no este
codigo: asi la app movil de los alumnos hereda las mismas reglas.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from typing import Any, Self


class EstadoPrestamo(StrEnum):
    ACTIVO = "activo"
    DEVUELTO = "devuelto"
    VENCIDO = "vencido"


@dataclass
class Prestamo:
    libro_id: int
    usuario_id: str

    fecha_prestamo: date | None = None
    fecha_limite: date | None = None
    fecha_devolucion: date | None = None
    estado: EstadoPrestamo = EstadoPrestamo.ACTIVO
    registrado_por: str | None = None

    id: int | None = None

    # Campos que llegan de la vista de deudores, no de la tabla
    titulo_libro: str | None = None
    nombre_alumno: str | None = None
    salon: str | None = None

    @property
    def dias_de_retraso(self) -> int:
        """Dias vencidos al dia de hoy. Cero si esta en plazo o ya se devolvio."""
        if self.estado == EstadoPrestamo.DEVUELTO or not self.fecha_limite:
            return 0
        atraso = (date.today() - self.fecha_limite).days
        return max(0, atraso)

    @property
    def esta_vencido(self) -> bool:
        return self.dias_de_retraso > 0

    @property
    def resumen(self) -> str:
        """Frase para mostrar al bibliotecario en la lista de prestamos."""
        if self.estado == EstadoPrestamo.DEVUELTO:
            return "Devuelto"
        if self.esta_vencido:
            dias = self.dias_de_retraso
            return f"Vencido hace {dias} día{'s' if dias != 1 else ''}"
        if self.fecha_limite:
            faltan = (self.fecha_limite - date.today()).days
            return f"Vence en {faltan} día{'s' if faltan != 1 else ''}"
        return "Activo"

    @classmethod
    def desde_fila(cls, fila: dict[str, Any]) -> Self:
        def a_fecha(valor: Any) -> date | None:
            return date.fromisoformat(valor[:10]) if valor else None

        return cls(
            id=fila.get("id"),
            libro_id=fila["libro_id"],
            usuario_id=fila["usuario_id"],
            fecha_prestamo=a_fecha(fila.get("fecha_prestamo")),
            fecha_limite=a_fecha(fila.get("fecha_limite")),
            fecha_devolucion=a_fecha(fila.get("fecha_devolucion")),
            estado=EstadoPrestamo(fila.get("estado", EstadoPrestamo.ACTIVO)),
            registrado_por=fila.get("registrado_por"),
            titulo_libro=fila.get("titulo_libro") or fila.get("titulo"),
            nombre_alumno=fila.get("nombre_alumno"),
            salon=fila.get("salon"),
        )
