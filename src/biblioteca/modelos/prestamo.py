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

    # Campos que llegan de las vistas, no de la tabla
    titulo_libro: str | None = None
    nombre_alumno: str | None = None
    salon: str | None = None

    # Lo calcula la base, no este codigo: positivo si faltan dias, negativo
    # si ya vencio, cero si vence hoy. Antes se calculaba aqui con el reloj
    # del equipo mientras la base usaba el suyo, que corre en UTC; durante
    # seis horas cada dia las dos respuestas diferian en uno.
    dias_restantes: int = 0

    @property
    def dias_de_retraso(self) -> int:
        """Dias vencidos. Cero si esta en plazo o ya se devolvio."""
        if self.estado == EstadoPrestamo.DEVUELTO:
            return 0
        return max(0, -self.dias_restantes)

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
        if self.dias_restantes == 0:
            return "Vence hoy"
        faltan = self.dias_restantes
        return f"Vence en {faltan} día{'s' if faltan != 1 else ''}"

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
            salon=_salon(fila),
            dias_restantes=fila.get("dias_restantes", 0),
        )


def _salon(fila: dict[str, Any]) -> str | None:
    """Arma el salon cuando la vista trae grado y grupo por separado."""
    if fila.get("salon"):
        return fila["salon"]
    grado, grupo = fila.get("grado"), fila.get("grupo")
    return f"{grado}{grupo}" if grado and grupo else None
