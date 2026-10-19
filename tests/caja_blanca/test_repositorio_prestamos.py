"""Caja blanca · repositorio de préstamos, devoluciones y deudores.

Equivale a `PrestamoDao` del sistema Java, que no tenía pruebas: la matriz de
casos no llegó a cubrirlo porque el préstamo no aplicaba ninguna regla, así
que no había qué interrogar.

Aquí las reglas existen, pero **no viven en este archivo**: el límite de un
libro por alumno es un índice único, el plazo de siete días es el disparador
`calcular_fecha_limite` y el movimiento de inventario es `mover_inventario`.
Por eso estas pruebas no comprueban que Python aplique la regla —no debe—,
sino tres cosas distintas:

1. que **no** calcule lo que le toca a la base (el defecto del PR #55),
2. que mande exactamente los datos que la base espera,
3. que traduzca cada rechazo a algo que el bibliotecario entienda.
"""

from __future__ import annotations

import pytest

from biblioteca.core.config import DIAS_DE_PRESTAMO
from biblioteca.modelos.prestamo import EstadoPrestamo
from biblioteca.repositorios import prestamos
from biblioteca.repositorios.prestamos import Deudor, ErrorDePrestamo

FILA = {
    "id": 1, "libro_id": 7, "usuario_id": "a-1",
    "fecha_prestamo": "2026-09-15", "fecha_limite": "2026-09-22",
    "fecha_devolucion": None, "estado": "activo", "dias_restantes": 3,
    "titulo_libro": "Momo", "nombre_alumno": "Ana Martínez",
}


def fila_deudor(**cambios) -> dict:
    fila = {
        "prestamo_id": 1, "codigo": "A-001", "alumno": "Ana Martínez",
        "grado": 4, "grupo": "B", "correo": None, "telefono": "2281234567",
        "libro": "Momo", "fecha_prestamo": "2026-09-01",
        "fecha_limite": "2026-09-08", "dias_de_retraso": 11,
    }
    fila.update(cambios)
    return fila


# ===========================================================================
# registrar() · lo que se envía, y lo que deliberadamente no
# ===========================================================================

def test_el_prestamo_manda_solo_dos_datos(monkeypatch, cliente_falso):
    """Dos datos y nada más. El resto lo resuelven los disparadores.

    Es la decisión que ordena el proyecto: si Python mandara la fecha límite,
    la app móvil planeada tendría que reimplementar el plazo.
    """
    cliente = cliente_falso(monkeypatch, prestamos, respuesta=[FILA])

    prestamos.registrar(libro_id=7, alumno_id="a-1")

    assert cliente.consulta.argumentos_de("insert")[0][0] == {
        "libro_id": 7, "usuario_id": "a-1"}


def test_el_prestamo_no_manda_la_fecha_limite(monkeypatch, cliente_falso):
    """El defecto del PR #55, cerrado por partida doble.

    La pantalla anunciaba una fecha calculada con `date.today()` que la base
    no iba a guardar. Desde la migración 10, `calcular_fecha_limite` además
    ignora la fecha que mande el cliente: `REQ-PRE-02` pasó de valor por
    omisión a regla.
    """
    cliente = cliente_falso(monkeypatch, prestamos, respuesta=[FILA])

    prestamos.registrar(libro_id=7, alumno_id="a-1")

    enviado = cliente.consulta.argumentos_de("insert")[0][0]
    assert "fecha_limite" not in enviado
    assert "fecha_prestamo" not in enviado


def test_el_prestamo_no_descuenta_el_inventario_desde_python(
    monkeypatch, cliente_falso
):
    """`mover_inventario` lo hace en la misma transacción que el INSERT."""
    cliente = cliente_falso(monkeypatch, prestamos, respuesta=[FILA])

    prestamos.registrar(libro_id=7, alumno_id="a-1")

    assert cliente.tablas == ["prestamos"], "se tocó la tabla libros"


def test_quien_captura_se_registra_si_se_sabe(monkeypatch, cliente_falso):
    cliente = cliente_falso(monkeypatch, prestamos, respuesta=[FILA])

    prestamos.registrar(libro_id=7, alumno_id="a-1", registrado_por="e-1")

    assert cliente.consulta.argumentos_de("insert")[0][0]["registrado_por"] == "e-1"


@pytest.mark.parametrize("registrado_por", [None, ""])
def test_sin_quien_captura_la_columna_no_se_envia(
    monkeypatch, cliente_falso, registrado_por
):
    """La columna admite nulo; mandarla vacía sería mandar una cadena vacía."""
    cliente = cliente_falso(monkeypatch, prestamos, respuesta=[FILA])

    prestamos.registrar(7, "a-1", registrado_por)

    assert "registrado_por" not in cliente.consulta.argumentos_de("insert")[0][0]


def test_el_prestamo_feliz_devuelve_el_plazo_que_calculo_la_base(
    monkeypatch, cliente_falso
):
    cliente_falso(monkeypatch, prestamos, respuesta=[FILA])

    prestamo = prestamos.registrar(7, "a-1")

    assert prestamo.fecha_limite.isoformat() == "2026-09-22"
    assert prestamo.dias_restantes == 3


def test_el_plazo_de_la_base_y_el_del_archivo_de_configuracion_coinciden():
    """Si alguien cambia uno sin el otro, la pantalla miente.

    La base es la que manda: `DIAS_DE_PRESTAMO` solo sirve para redactar el
    aviso «se vence en N días» que se muestra al confirmar.
    """
    assert DIAS_DE_PRESTAMO == 7, (
        "la migración 03 calcula fecha_prestamo + 7; si el plazo cambió, "
        "debe cambiar en una migración nueva y aquí al mismo tiempo"
    )


# ===========================================================================
# registrar() · cada rechazo de la base, traducido
# ===========================================================================

@pytest.mark.parametrize("texto_de_la_base,fragmento", [
    ('duplicate key value violates unique constraint '
     '"prestamo_unico_activo_por_usuario"', "préstamo activo"),
    ('No hay ejemplares disponibles de "Momo".', "ejemplares"),
    ('El libro "Momo" esta dado de baja del acervo.', "dado de baja"),
])
def test_cada_rechazo_del_prestamo_llega_traducido(
    monkeypatch, cliente_falso, texto_de_la_base, fragmento
):
    """Las tres reglas que el bibliotecario encuentra a diario.

    Antes de la auditoría los patrones del traductor no coincidían con estos
    textos, así que «no quedan ejemplares» llegaba como volcado de Postgres.
    """
    cliente_falso(monkeypatch, prestamos, error=Exception(texto_de_la_base))

    with pytest.raises(ErrorDePrestamo) as fallo:
        prestamos.registrar(7, "a-1")

    assert fragmento in str(fallo.value).lower()


def test_un_libro_que_no_existe_se_explica_sin_jerga(monkeypatch, cliente_falso):
    cliente_falso(
        monkeypatch, prestamos,
        error=Exception('insert or update on table "prestamos" violates foreign '
                        'key constraint "prestamos_libro_id_fkey"'),
    )

    with pytest.raises(ErrorDePrestamo) as fallo:
        prestamos.registrar(999, "a-1")

    assert "foreign key" not in str(fallo.value)


def test_el_prestamo_sin_fila_de_respuesta_revienta_sin_mensaje(
    monkeypatch, cliente_falso
):
    """Defecto en pie: `registrar()` no tiene la guarda que sí tienen los demás.

    `filas.data[0]` sobre una respuesta vacía levanta `IndexError`, que no es
    `ErrorDePrestamo` y por lo tanto **ninguna pantalla atrapa**: el diálogo
    de préstamo se queda colgado sin decir nada. Pasa si RLS deja escribir
    pero no leer la fila, que es exactamente el caso que ya se corrigió en
    `libros.dar_de_alta` y en `libros.modificar`.

    La prueba fija el comportamiento de hoy. Cuando se agregue la guarda,
    falla y hay que cambiarla por la que espera el mensaje.
    """
    cliente_falso(monkeypatch, prestamos, respuesta=[])

    with pytest.raises(IndexError):
        prestamos.registrar(7, "a-1")


# ===========================================================================
# devolver()
# ===========================================================================

def test_la_devolucion_solo_cambia_el_estado(monkeypatch, cliente_falso):
    """La fecha la pone `sellar_devolucion`, con el reloj de la base."""
    cliente = cliente_falso(monkeypatch, prestamos, respuesta=[
        FILA | {"estado": "devuelto", "fecha_devolucion": "2026-09-20"}])

    prestamos.devolver(1)

    enviado = cliente.consulta.argumentos_de("update")[0][0]
    assert enviado == {"estado": "devuelto"}
    assert "fecha_devolucion" not in enviado


def test_la_devolucion_filtra_por_el_prestamo(monkeypatch, cliente_falso):
    cliente = cliente_falso(monkeypatch, prestamos, respuesta=[
        FILA | {"estado": "devuelto"}])

    prestamos.devolver(1)

    assert ("id", 1) in cliente.consulta.argumentos_de("eq")


def test_devolver_un_prestamo_que_no_existe_avisa(monkeypatch, cliente_falso):
    """Esta sí tiene guarda: devuelve un mensaje, no un `IndexError`."""
    cliente_falso(monkeypatch, prestamos, respuesta=[])

    with pytest.raises(ErrorDePrestamo, match="No se encontró ese préstamo"):
        prestamos.devolver(999)


def test_la_devolucion_traduce_el_error_de_la_base(monkeypatch, cliente_falso):
    cliente_falso(
        monkeypatch, prestamos,
        error=Exception('violates check constraint "devolucion_coherente"'),
    )

    with pytest.raises(ErrorDePrestamo, match="fecha de devolución"):
        prestamos.devolver(1)


def test_la_devolucion_devuelve_el_prestamo_ya_cerrado(monkeypatch, cliente_falso):
    cliente_falso(monkeypatch, prestamos, respuesta=[
        FILA | {"estado": "devuelto", "fecha_devolucion": "2026-09-20"}])

    cerrado = prestamos.devolver(1)

    assert cerrado.estado is EstadoPrestamo.DEVUELTO
    assert cerrado.fecha_devolucion.isoformat() == "2026-09-20"
    assert cerrado.dias_de_retraso == 0, "un préstamo cerrado no acumula retraso"


# ===========================================================================
# activos() e historial_de()
# ===========================================================================

def test_los_activos_salen_de_la_vista_y_no_de_la_tabla(monkeypatch, cliente_falso):
    """Corolario 2: `dias_restantes` lo calcula la vista, no Python."""
    cliente = cliente_falso(monkeypatch, prestamos, respuesta=[FILA])

    prestamos.activos()

    assert cliente.tablas == ["v_prestamos"]


def test_los_activos_incluyen_los_vencidos(monkeypatch, cliente_falso):
    """Un préstamo vencido sigue sin devolverse: tiene que aparecer.

    Si el filtro fuera solo `activo`, los vencidos desaparecerían de la
    pantalla justo cuando más importan.
    """
    cliente = cliente_falso(monkeypatch, prestamos, respuesta=[FILA])

    prestamos.activos()

    estados = cliente.consulta.argumentos_de("in_")[0][1]
    assert set(estados) == {"activo", "vencido"}
    assert "devuelto" not in estados


def test_los_activos_se_ordenan_por_fecha_limite(monkeypatch, cliente_falso):
    """Lo más urgente arriba."""
    cliente = cliente_falso(monkeypatch, prestamos, respuesta=[])

    prestamos.activos()

    assert ("fecha_limite",) in cliente.consulta.argumentos_de("order")


def test_el_historial_trae_tambien_lo_ya_concluido(monkeypatch, cliente_falso):
    """REQ-PRE-03: el historial completo, sin filtro de estado."""
    cliente = cliente_falso(monkeypatch, prestamos, respuesta=[
        FILA, FILA | {"id": 2, "estado": "devuelto"}])

    historial = prestamos.historial_de("a-1")

    assert len(historial) == 2
    assert "in_" not in cliente.consulta.nombres()
    assert ("usuario_id", "a-1") in cliente.consulta.argumentos_de("eq")


def test_el_historial_va_del_mas_reciente_al_mas_viejo(monkeypatch, cliente_falso):
    cliente = cliente_falso(monkeypatch, prestamos, respuesta=[])

    prestamos.historial_de("a-1")

    assert ("fecha_prestamo",) in cliente.consulta.argumentos_de("order")
    assert cliente.consulta.llamadas[-2][2] == {"desc": True}


def test_un_alumno_sin_prestamos_no_es_un_error(monkeypatch, cliente_falso):
    cliente_falso(monkeypatch, prestamos, respuesta=[])

    assert prestamos.historial_de("a-9") == []


# ===========================================================================
# deudores() · el reporte que reemplaza al cuaderno
# ===========================================================================

def test_el_reporte_sale_de_la_vista_en_una_consulta(monkeypatch, cliente_falso):
    """Es el reemplazo directo de revisar el cuaderno hoja por hoja."""
    cliente = cliente_falso(monkeypatch, prestamos, respuesta=[fila_deudor()])

    reporte = prestamos.deudores()

    assert cliente.tablas == ["v_deudores"]
    assert len(reporte) == 1
    assert reporte[0].alumno == "Ana Martínez"


def test_el_reporte_ordena_por_los_dias_de_retraso(monkeypatch, cliente_falso):
    cliente = cliente_falso(monkeypatch, prestamos, respuesta=[])

    prestamos.deudores()

    assert ("dias_de_retraso",) in cliente.consulta.argumentos_de("order")
    assert cliente.consulta.llamadas[-2][2] == {"desc": True}


def test_el_reporte_trae_el_contacto_del_tutor(monkeypatch, cliente_falso):
    """Sin él, saber quién debe no sirve para avisarle a nadie."""
    cliente_falso(monkeypatch, prestamos, respuesta=[fila_deudor()])

    deudor = prestamos.deudores()[0]

    assert deudor.telefono == "2281234567"
    assert deudor.salon == "4B"


class TestFilasDelReporte:
    """Las columnas opcionales de la vista, y las fechas."""

    def test_las_fechas_se_recortan_a_dia(self, monkeypatch, cliente_falso):
        cliente_falso(monkeypatch, prestamos, respuesta=[
            fila_deudor(fecha_prestamo="2026-09-01T06:00:00+00:00")])

        assert prestamos.deudores()[0].fecha_prestamo.isoformat() == "2026-09-01"

    def test_una_fecha_nula_no_revienta(self, monkeypatch, cliente_falso):
        cliente_falso(monkeypatch, prestamos,
                      respuesta=[fila_deudor(fecha_prestamo=None)])

        assert prestamos.deudores()[0].fecha_prestamo is None

    def test_sin_dias_de_retraso_no_se_inventa_uno(self, monkeypatch, cliente_falso):
        fila = fila_deudor()
        del fila["dias_de_retraso"]
        cliente_falso(monkeypatch, prestamos, respuesta=[fila])

        assert prestamos.deudores()[0].dias_de_retraso == 0

    def test_un_alumno_sin_salon_asignado(self, monkeypatch, cliente_falso):
        cliente_falso(monkeypatch, prestamos,
                      respuesta=[fila_deudor(grado=None, grupo=None)])

        assert prestamos.deudores()[0].salon == "-"


class TestTextoDelRetraso:
    """Concordancia de singular: se lee en el reporte impreso."""

    def _deudor(self, dias):
        return Deudor(prestamo_id=1, codigo="A-1", alumno="Ana", grado=4,
                      grupo="B", correo=None, telefono=None, libro="Momo",
                      fecha_prestamo=None, fecha_limite=None,
                      dias_de_retraso=dias)

    def test_un_dia_va_en_singular(self):
        assert self._deudor(1).retraso == "1 día"

    @pytest.mark.parametrize("dias", [0, 2, 11, 30])
    def test_los_demas_van_en_plural(self, dias):
        assert self._deudor(dias).retraso.endswith("días")

    @pytest.mark.parametrize("grado,grupo,esperado", [
        (4, "B", "4B"), (None, "B", "-"), (4, None, "-"), (None, None, "-"),
    ])
    def test_el_salon_necesita_los_dos_datos(self, grado, grupo, esperado):
        deudor = self._deudor(1)
        deudor.grado, deudor.grupo = grado, grupo

        assert deudor.salon == esperado


def test_sin_deudores_el_reporte_abre_vacio_y_no_falla(monkeypatch, cliente_falso):
    """El caso que la escuela querría: nadie debe nada."""
    cliente_falso(monkeypatch, prestamos, respuesta=[])

    assert prestamos.deudores() == []
