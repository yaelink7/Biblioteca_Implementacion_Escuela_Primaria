"""Prestamos, devoluciones y reporte de deudores.

Migra PrestamoDao.java del sistema Java. Las reglas de negocio (limite de un libro
por alumno, plazo de siete dias, movimiento de inventario) las aplica
Postgres mediante disparadores; aqui solo se invocan y se traducen sus
errores a mensajes que el bibliotecario entienda.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from biblioteca.core.errores import causa as causa_del_error
from biblioteca.core.supabase_cliente import obtener_cliente
from biblioteca.modelos.prestamo import EstadoPrestamo, Prestamo

TABLA = "prestamos"
VISTA = "v_prestamos"   # incluye el plazo calculado por la base


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


@dataclass
class DetallePrestamo:
    """Lo que el panel de Prestamos muestra y la vista v_prestamos no trae."""

    codigo_alumno: str | None = None
    telefono_tutor: str | None = None
    autor: str | None = None
    registro: str | None = None   # quien lo registro, por su nombre
    nombre_alumno: str | None = None
    apellido_alumno: str | None = None


# prestamos tiene dos llaves hacia perfiles —el alumno y quien registro—, asi
# que cada una se nombra por su restriccion para que PostgREST sepa cual es.
_DETALLE = (
    "id, libros(autor), "
    "alumno:perfiles!prestamos_usuario_id_fkey(codigo, telefono, nombre, apellido), "
    "registro:perfiles!prestamos_registrado_por_fkey(nombre, apellido)"
)


def detalles(ids: list[int]) -> dict[int, DetallePrestamo]:
    """El detalle de varios prestamos en una sola consulta, por su id.

    Sirve al panel de Prestamos: el telefono del tutor y quien registro el
    prestamo, que aprobo Yael el 8 de noviembre. Los prestamos cargados a
    mano no tienen registrado_por y su registro queda vacio.
    """
    if not ids:
        return {}
    filas = obtener_cliente().table(TABLA).select(_DETALLE).in_("id", ids).execute()

    resultado = {}
    for fila in filas.data:
        alumno = fila.get("alumno") or {}
        libro = fila.get("libros") or {}
        quien = fila.get("registro") or {}
        nombre = f"{quien.get('nombre', '')} {quien.get('apellido', '')}".strip()
        resultado[fila["id"]] = DetallePrestamo(
            codigo_alumno=alumno.get("codigo"),
            telefono_tutor=alumno.get("telefono"),
            autor=libro.get("autor"),
            registro=nombre or None,
            nombre_alumno=alumno.get("nombre"),
            apellido_alumno=alumno.get("apellido"),
        )
    return resultado


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
    """Cierra un prestamo y reintegra el ejemplar al inventario.

    Solo se marca como devuelto: la fecha la pone el disparador de la base,
    con el mismo reloj que calculo el plazo. Enviarla desde aqui la ponia
    con la hora del equipo, que no coincide con la de la base.
    """
    try:
        filas = (
            obtener_cliente()
            .table(TABLA)
            .update({"estado": str(EstadoPrestamo.DEVUELTO)})
            .eq("id", prestamo_id)
            .execute()
        )
    except Exception as error:
        raise ErrorDePrestamo(_mensaje_claro(error)) from error

    if not filas.data:
        raise ErrorDePrestamo("No se encontró ese préstamo.")
    return Prestamo.desde_fila(filas.data[0])


def activos() -> list[Prestamo]:
    """Prestamos sin devolver, con el titulo, el nombre y el plazo resueltos.

    Va por la vista v_prestamos para que los dias de retraso los calcule la
    base: si se calcularan aqui, el reloj del equipo y el de la base darian
    respuestas distintas seis horas de cada dia.
    """
    filas = (
        obtener_cliente()
        .table(VISTA)
        .select("*")
        .in_("estado", [str(EstadoPrestamo.ACTIVO), str(EstadoPrestamo.VENCIDO)])
        .order("fecha_limite")
        .execute()
    )
    return [Prestamo.desde_fila(f) for f in filas.data]


def historial_de(alumno_id: str) -> list[Prestamo]:
    """Todos los movimientos de un alumno, incluso los ya concluidos (REQ-PRE-03)."""
    filas = (
        obtener_cliente()
        .table(VISTA)
        .select("*")
        .eq("usuario_id", alumno_id)
        .order("fecha_prestamo", desc=True)
        .execute()
    )
    return [Prestamo.desde_fila(f) for f in filas.data]


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
    """Traduce el error de la base. El traductor vive en core/errores.py.

    Antes cada repositorio tenia su propia lista y se contradecian: el mismo
    `duplicate key` significaba tres cosas distintas segun quien lo atrapara.
    Ademas buscaban textos que los disparadores nunca emiten, asi que las
    reglas mas usadas llegaban al bibliotecario como volcado de Postgres.
    """
    return causa_del_error(error)
