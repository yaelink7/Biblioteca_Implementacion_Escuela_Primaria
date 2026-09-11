"""Prestamos, devoluciones y reporte de deudores.

Migra PrestamoDao.java del sistema Java. Las reglas de negocio (limite de un libro
por alumno, plazo de siete dias, movimiento de inventario) las aplica
Postgres mediante disparadores; aqui solo se invocan y se traducen sus
errores a mensajes que el bibliotecario entienda.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from biblioteca.core.supabase_cliente import obtener_cliente
from biblioteca.modelos.prestamo import EstadoPrestamo, Prestamo

TABLA = "prestamos"


class ErrorDePrestamo(Exception):
    """La base rechazo el prestamo o la devolucion."""


@dataclass
class Deudor:
    """Una fila del reporte de deudores (vista v_deudores)."""

    prestamo_id: int
    codigo: str
    alumno: str
    grado: int | None
    grupo: str | None
    correo: str | None
    telefono: str | None
    libro: str
    fecha_prestamo: date | None
    fecha_limite: date | None
    dias_de_retraso: int

    @property
    def salon(self) -> str:
        return f"{self.grado}{self.grupo}" if self.grado and self.grupo else "-"

    @property
    def retraso(self) -> str:
        d = self.dias_de_retraso
        return f"{d} día{'s' if d != 1 else ''}"


def registrar(libro_id: int, alumno_id: str, registrado_por: str | None = None) -> Prestamo:
    """Presta un libro a un alumno (REQ-PRE-01, REQ-PRE-02).

    No se calcula aqui la fecha limite ni se descuenta el inventario: de eso
    se encargan los disparadores, para que la app movil herede las reglas.
    """
    datos = {"libro_id": libro_id, "usuario_id": alumno_id}
    if registrado_por:
        datos["registrado_por"] = registrado_por

    try:
        filas = obtener_cliente().table(TABLA).insert(datos).execute()
    except Exception as error:
        raise ErrorDePrestamo(_mensaje_claro(error)) from error

    return Prestamo.desde_fila(filas.data[0])


def devolver(prestamo_id: int) -> Prestamo:
    """Cierra un prestamo y reintegra el ejemplar al inventario."""
    try:
        filas = (
            obtener_cliente()
            .table(TABLA)
            .update(
                {
                    "estado": str(EstadoPrestamo.DEVUELTO),
                    "fecha_devolucion": date.today().isoformat(),
                }
            )
            .eq("id", prestamo_id)
            .execute()
        )
    except Exception as error:
        raise ErrorDePrestamo(_mensaje_claro(error)) from error

    if not filas.data:
        raise ErrorDePrestamo("No se encontró ese préstamo.")
    return Prestamo.desde_fila(filas.data[0])


def activos() -> list[Prestamo]:
    """Prestamos sin devolver, con el titulo y el nombre ya resueltos."""
    filas = (
        obtener_cliente()
        .table(TABLA)
        .select("*, libros(titulo), perfiles!prestamos_usuario_id_fkey(nombre, apellido)")
        .in_("estado", [str(EstadoPrestamo.ACTIVO), str(EstadoPrestamo.VENCIDO)])
        .order("fecha_limite")
        .execute()
    )

    prestamos = []
    for fila in filas.data:
        libro = fila.pop("libros", None) or {}
        persona = fila.pop("perfiles", None) or {}
        fila["titulo_libro"] = libro.get("titulo")
        fila["nombre_alumno"] = (
            f"{persona.get('nombre', '')} {persona.get('apellido', '')}".strip() or None
        )
        prestamos.append(Prestamo.desde_fila(fila))
    return prestamos


def historial_de(alumno_id: str) -> list[Prestamo]:
    """Todos los movimientos de un alumno, incluso los ya concluidos (REQ-PRE-03)."""
    filas = (
        obtener_cliente()
        .table(TABLA)
        .select("*, libros(titulo)")
        .eq("usuario_id", alumno_id)
        .order("fecha_prestamo", desc=True)
        .execute()
    )

    prestamos = []
    for fila in filas.data:
        libro = fila.pop("libros", None) or {}
        fila["titulo_libro"] = libro.get("titulo")
        prestamos.append(Prestamo.desde_fila(fila))
    return prestamos


def deudores() -> list[Deudor]:
    """Reporte de alumnos con prestamos vencidos, en una sola consulta.

    Es el reemplazo directo de revisar el cuaderno hoja por hoja.
    """
    filas = (
        obtener_cliente()
        .table("v_deudores")
        .select("*")
        .order("dias_de_retraso", desc=True)
        .execute()
    )

    def a_fecha(valor) -> date | None:
        return date.fromisoformat(valor[:10]) if valor else None

    return [
        Deudor(
            prestamo_id=f["prestamo_id"],
            codigo=f["codigo"],
            alumno=f["alumno"],
            grado=f.get("grado"),
            grupo=f.get("grupo"),
            correo=f.get("correo"),
            telefono=f.get("telefono"),
            libro=f["libro"],
            fecha_prestamo=a_fecha(f.get("fecha_prestamo")),
            fecha_limite=a_fecha(f.get("fecha_limite")),
            dias_de_retraso=f.get("dias_de_retraso", 0),
        )
        for f in filas.data
    ]


def _mensaje_claro(error: Exception) -> str:
    texto = str(error)

    if "prestamo_unico_activo" in texto or "duplicate key" in texto:
        return (
            "Este alumno ya tiene un préstamo activo. "
            "Solo se permite un libro por alumno."
        )
    if "existencias" in texto or "sin ejemplares" in texto:
        return "No quedan ejemplares disponibles de este libro."
    if "violates row-level security" in texto or "42501" in texto:
        return "Tu perfil no tiene permiso para registrar préstamos."
    if "foreign key" in texto:
        return "El libro o el alumno indicado no existe."
    return f"La base de datos rechazó la operación: {texto}"
