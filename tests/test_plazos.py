"""Comprueba que el plazo de un prestamo se lee de la base y no se recalcula.

Nace de un defecto encontrado en la auditoria interna: los dias de retraso
se calculaban en Python con el reloj del equipo y en la vista de deudores
con el de la base, que corre en UTC. Durante seis horas de cada dia las dos
respuestas diferian en uno, asi que la pantalla de prestamos podia decir
"vencido hace 11 dias" y el reporte de deudores "12", para el mismo prestamo.

Estas pruebas no tocan la base: verifican que el modelo respeta el numero
que se le entrega en lugar de volver a calcularlo.
"""

from datetime import date, timedelta

import pytest

from biblioteca.modelos.prestamo import EstadoPrestamo, Prestamo


def prestamo(dias_restantes: int, estado=EstadoPrestamo.ACTIVO) -> Prestamo:
    """Un prestamo cuyo plazo ya viene resuelto por la base."""
    return Prestamo(
        libro_id=1,
        usuario_id="x",
        fecha_prestamo=date(2026, 9, 1),
        fecha_limite=date(2026, 9, 8),
        estado=estado,
        dias_restantes=dias_restantes,
    )


# --------------------------------------------------------------------------
# El dato de la base manda
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "dias_restantes, retraso_esperado",
    [(-12, 12), (-1, 1), (0, 0), (5, 0), (30, 0)],
)
def test_el_retraso_sale_del_dato_de_la_base(dias_restantes, retraso_esperado):
    assert prestamo(dias_restantes).dias_de_retraso == retraso_esperado


def test_no_se_recalcula_con_el_reloj_del_equipo():
    """La fecha limite dice una cosa y la base otra: manda la base.

    Si el modelo recalculara a partir de fecha_limite, esta prueba fallaria
    en cuanto cambiara el dia, que es justo el defecto que se corrigio.
    """
    p = prestamo(dias_restantes=3)
    p.fecha_limite = date.today() - timedelta(days=99)  # contradice al dato
    assert p.dias_de_retraso == 0
    assert not p.esta_vencido
    assert "Vence en 3 días" == p.resumen


# --------------------------------------------------------------------------
# Lo que lee el bibliotecario
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "dias_restantes, texto",
    [
        (-12, "Vencido hace 12 días"),
        (-1, "Vencido hace 1 día"),
        (0, "Vence hoy"),
        (1, "Vence en 1 día"),
        (7, "Vence en 7 días"),
    ],
)
def test_resumen_legible(dias_restantes, texto):
    assert prestamo(dias_restantes).resumen == texto


def test_un_prestamo_devuelto_no_tiene_retraso():
    """Aunque su fecha limite haya pasado hace meses."""
    p = prestamo(dias_restantes=-40, estado=EstadoPrestamo.DEVUELTO)
    assert p.dias_de_retraso == 0
    assert not p.esta_vencido
    assert p.resumen == "Devuelto"


# --------------------------------------------------------------------------
# Lectura de la vista
# --------------------------------------------------------------------------


def test_desde_fila_toma_los_dias_de_la_vista():
    p = Prestamo.desde_fila({
        "id": 1, "libro_id": 2, "usuario_id": "x",
        "fecha_prestamo": "2026-09-01", "fecha_limite": "2026-09-08",
        "estado": "activo", "dias_restantes": -4,
        "titulo_libro": "El principito", "nombre_alumno": "Ana Sofia Martinez",
        "grado": 4, "grupo": "B",
    })
    assert p.dias_de_retraso == 4
    assert p.esta_vencido
    assert p.salon == "4B"
    assert p.titulo_libro == "El principito"


def test_sin_dias_restantes_no_se_inventa_un_retraso():
    """Una fila sin el campo (por ejemplo, recien insertada) no debe
    aparecer como vencida."""
    p = Prestamo.desde_fila({
        "id": 1, "libro_id": 2, "usuario_id": "x", "estado": "activo",
    })
    assert p.dias_de_retraso == 0
    assert not p.esta_vencido
