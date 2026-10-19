"""Caja blanca · repositorio del catálogo.

Equivale a lo que en el sistema Java era `LibroDao`, y a los casos TC-14 a
TC-17 del grupo A.5 de la matriz: allá la persistencia era un archivo CSV y
aquí es PostgREST, pero los caminos que hay que recorrer son los mismos —el
feliz, el que no encuentra nada, y el que falla.

A diferencia de las pruebas de caja negra, estas **se diseñaron leyendo el
código**: una por cada rama de cada función, incluidas las guardas que se
agregaron después de la auditoría y que ninguna prueba interrogaba.

No tocan la red. El doble de `tests/conftest.py` sustituye a
`obtener_cliente()` y además anota qué consulta se armó, de modo que se puede
comprobar el filtro sin una base de datos enfrente.
"""

from __future__ import annotations

import pytest

from biblioteca.modelos.libro import Libro
from biblioteca.repositorios import libros
from biblioteca.repositorios.libros import ErrorDeCatalogo

FILA = {
    "id": 7, "titulo": "Momo", "autor": "Michael Ende", "tipo_libro": "Infantil",
    "editorial": "Alfaguara", "existencias": 2, "ano_publicacion": 1973,
    "num_paginas": 272, "activo": True, "motivo_baja": None, "dado_baja_en": None,
}


# ===========================================================================
# listar() · las dos ramas de incluir_bajas
# ===========================================================================

def test_listar_filtra_los_dados_de_baja(monkeypatch, cliente_falso):
    cliente = cliente_falso(monkeypatch, libros, respuesta=[FILA])

    resultado = libros.listar()

    assert len(resultado) == 1 and resultado[0].titulo == "Momo"
    assert cliente.tablas == ["libros"]
    assert ("activo", True) in cliente.consulta.argumentos_de("eq")


def test_listar_con_bajas_no_aplica_el_filtro(monkeypatch, cliente_falso):
    """La otra rama: la casilla «ver bajas» del catálogo."""
    cliente = cliente_falso(monkeypatch, libros, respuesta=[FILA])

    libros.listar(incluir_bajas=True)

    assert "eq" not in cliente.consulta.nombres()


def test_listar_ordena_por_titulo(monkeypatch, cliente_falso):
    cliente = cliente_falso(monkeypatch, libros, respuesta=[])

    assert libros.listar() == []
    assert ("titulo",) in cliente.consulta.argumentos_de("order")


# ===========================================================================
# buscar() · texto vacío, con texto, y el escape del patrón
# ===========================================================================

@pytest.mark.parametrize("texto", ["", "   ", "\t\n"])
def test_buscar_sin_texto_cae_en_listar(monkeypatch, cliente_falso, texto):
    """Rama de salida temprana: no debe armar un `or_` con un patrón vacío."""
    cliente = cliente_falso(monkeypatch, libros, respuesta=[FILA])

    libros.buscar(texto)

    assert "or_" not in cliente.consulta.nombres()


def test_buscar_con_texto_interroga_los_tres_campos(monkeypatch, cliente_falso):
    cliente = cliente_falso(monkeypatch, libros, respuesta=[FILA])

    libros.buscar("prin")

    filtro = cliente.consulta.argumentos_de("or_")[0][0]
    assert filtro.count("ilike") == 3
    assert "titulo.ilike" in filtro
    assert "autor.ilike" in filtro
    assert "tipo_libro.ilike" in filtro


def test_buscar_recorta_los_espacios_de_los_extremos(monkeypatch, cliente_falso):
    cliente = cliente_falso(monkeypatch, libros, respuesta=[])

    libros.buscar("  momo  ")

    assert '"%momo%"' in cliente.consulta.argumentos_de("or_")[0][0]


def test_buscar_una_coma_no_parte_el_filtro(monkeypatch, cliente_falso):
    """El defecto de la auditoría, visto desde el repositorio.

    Dentro de `or_` la coma separa condiciones: «Momo, la niña» armaba cuatro
    condiciones en lugar de tres y PostgREST rechazaba la consulta. Como la
    búsqueda se dispara sola a los 250 ms, el error salía mientras la persona
    seguía escribiendo.
    """
    cliente = cliente_falso(monkeypatch, libros, respuesta=[])

    libros.buscar("Momo, la niña")

    filtro = cliente.consulta.argumentos_de("or_")[0][0]
    assert filtro.count("ilike") == 3, "la coma volvió a partir el filtro"


def test_buscar_tambien_excluye_las_bajas(monkeypatch, cliente_falso):
    cliente = cliente_falso(monkeypatch, libros, respuesta=[])

    libros.buscar("momo")

    assert ("activo", True) in cliente.consulta.argumentos_de("eq")


# ===========================================================================
# obtener() · encontrado y no encontrado
# ===========================================================================

def test_obtener_devuelve_el_libro(monkeypatch, cliente_falso):
    cliente_falso(monkeypatch, libros, respuesta=[FILA])

    assert libros.obtener(7).id == 7


def test_obtener_lo_que_no_existe_devuelve_none(monkeypatch, cliente_falso):
    """Una lectura vacía no es un error: por eso el contrato es `Libro | None`."""
    cliente_falso(monkeypatch, libros, respuesta=[])

    assert libros.obtener(999) is None


# ===========================================================================
# dar_de_alta() · validación, error de la base, respuesta vacía, feliz
# ===========================================================================

def test_alta_valida_antes_de_tocar_la_base(monkeypatch, cliente_falso):
    """Primera rama: si el validador falla, no se envía nada."""
    cliente = cliente_falso(monkeypatch, libros, respuesta=[FILA])

    with pytest.raises(ErrorDeCatalogo, match="título"):
        libros.dar_de_alta(Libro(titulo="", autor="Ende", existencias=1))

    assert cliente.tablas == [], "se llamó a la base con datos ya rechazados"


def test_el_alta_no_manda_el_id(monkeypatch, cliente_falso):
    """Lo genera la base; mandarlo sería imponer un identificador."""
    cliente = cliente_falso(monkeypatch, libros, respuesta=[FILA])

    libros.dar_de_alta(Libro(id=99, titulo="Momo", autor="Ende", existencias=1))

    enviado = cliente.consulta.argumentos_de("insert")[0][0]
    assert "id" not in enviado


def test_el_alta_traduce_el_error_de_la_base(monkeypatch, cliente_falso):
    """Rama del `except`: el bibliotecario no debe leer el volcado de Postgres."""
    cliente_falso(
        monkeypatch, libros,
        error=Exception('duplicate key value violates unique constraint '
                        '"perfiles_codigo_key"'),
    )

    with pytest.raises(ErrorDeCatalogo) as fallo:
        libros.dar_de_alta(Libro(titulo="Momo", autor="Ende", existencias=1))

    assert "duplicate key" not in str(fallo.value)


def test_el_alta_sin_fila_de_respuesta_avisa_en_lugar_de_reventar(
    monkeypatch, cliente_falso
):
    """La guarda que la auditoría agregó, y que nadie probaba.

    Si RLS deja escribir pero no leer, `filas.data` llega vacío y el
    `filas.data[0]` de antes levantaba `IndexError`, que ninguna pantalla
    atrapa: el diálogo quedaba colgado sin decir nada.
    """
    cliente_falso(monkeypatch, libros, respuesta=[])

    with pytest.raises(ErrorDeCatalogo, match="Actualiza la pantalla"):
        libros.dar_de_alta(Libro(titulo="Momo", autor="Ende", existencias=1))


def test_el_alta_feliz_devuelve_el_libro_con_su_id(monkeypatch, cliente_falso):
    cliente_falso(monkeypatch, libros, respuesta=[FILA])

    guardado = libros.dar_de_alta(Libro(titulo="Momo", autor="Ende", existencias=2))

    assert guardado.id == 7


# ===========================================================================
# modificar() · sin id, validación, error, respuesta vacía, feliz
# ===========================================================================

def test_modificar_sin_id_se_rechaza_antes_de_salir(monkeypatch, cliente_falso):
    cliente = cliente_falso(monkeypatch, libros, respuesta=[FILA])

    with pytest.raises(ErrorDeCatalogo, match="identificador"):
        libros.modificar(Libro(titulo="Momo", autor="Ende", existencias=1))

    assert cliente.tablas == []


def test_modificar_admite_cero_ejemplares(monkeypatch, cliente_falso):
    """La rama `es_alta=False` del validador, vista desde aquí.

    Un libro ya registrado puede quedar en cero cuando todos están prestados.
    """
    cliente_falso(monkeypatch, libros, respuesta=[FILA])

    assert libros.modificar(Libro(id=7, titulo="Momo", autor="Ende",
                                  existencias=0)).id == 7


def test_modificar_con_datos_invalidos_no_toca_la_base(monkeypatch, cliente_falso):
    cliente = cliente_falso(monkeypatch, libros, respuesta=[FILA])

    with pytest.raises(ErrorDeCatalogo):
        libros.modificar(Libro(id=7, titulo="Momo", autor="", existencias=1))

    assert cliente.tablas == []


def test_modificar_filtra_por_el_id_del_libro(monkeypatch, cliente_falso):
    """Sin el `eq`, un UPDATE alcanzaría toda la tabla."""
    cliente = cliente_falso(monkeypatch, libros, respuesta=[FILA])

    libros.modificar(Libro(id=7, titulo="Momo", autor="Ende", existencias=1))

    assert ("id", 7) in cliente.consulta.argumentos_de("eq")


def test_modificar_traduce_el_error_de_la_base(monkeypatch, cliente_falso):
    cliente_falso(monkeypatch, libros,
                  error=Exception("El año de publicacion (3000) no puede ser futuro."))

    with pytest.raises(ErrorDeCatalogo, match="futuro"):
        libros.modificar(Libro(id=7, titulo="Momo", autor="Ende", existencias=1))


def test_modificar_sin_fila_de_respuesta_avisa(monkeypatch, cliente_falso):
    """Un id que ya no existe, o una fila que RLS esconde."""
    cliente_falso(monkeypatch, libros, respuesta=[])

    with pytest.raises(ErrorDeCatalogo, match="Actualiza la pantalla"):
        libros.modificar(Libro(id=7, titulo="Momo", autor="Ende", existencias=1))


def test_modificar_no_manda_el_id_entre_los_datos(monkeypatch, cliente_falso):
    """Va en el filtro, no en el cuerpo: la llave primaria no se actualiza."""
    cliente = cliente_falso(monkeypatch, libros, respuesta=[FILA])

    libros.modificar(Libro(id=7, titulo="Momo", autor="Ende", existencias=1))

    assert "id" not in cliente.consulta.argumentos_de("update")[0][0]


# ===========================================================================
# dar_de_baja() · motivo obligatorio, error, feliz
# ===========================================================================

@pytest.mark.parametrize("motivo", ["", "   ", "\n"])
def test_la_baja_exige_motivo(monkeypatch, cliente_falso, motivo):
    """REQ-LIB-03. La base lo exige con `baja_con_motivo`; aquí se avisa antes."""
    cliente = cliente_falso(monkeypatch, libros, respuesta=[FILA])

    with pytest.raises(ErrorDeCatalogo, match="motivo"):
        libros.dar_de_baja(7, motivo)

    assert cliente.tablas == []


def test_la_baja_es_logica_y_no_borra_la_fila(monkeypatch, cliente_falso):
    """El sistema Java borraba el registro y se llevaba el historial con él."""
    cliente = cliente_falso(monkeypatch, libros, respuesta=[FILA])

    libros.dar_de_baja(7, "Extraviado")

    assert "delete" not in cliente.consulta.nombres()
    enviado = cliente.consulta.argumentos_de("update")[0][0]
    assert enviado["activo"] is False
    assert enviado["motivo_baja"] == "Extraviado"


def test_la_baja_recorta_el_motivo(monkeypatch, cliente_falso):
    cliente = cliente_falso(monkeypatch, libros, respuesta=[FILA])

    libros.dar_de_baja(7, "  Extraviado  ")

    assert cliente.consulta.argumentos_de("update")[0][0]["motivo_baja"] == "Extraviado"


def test_la_fecha_de_baja_la_pone_la_base(monkeypatch, cliente_falso):
    """Corolario 2: las fechas no las calcula Python.

    La base corre en UTC y los equipos en hora de Veracruz; seis horas de cada
    día los dos relojes no coinciden.
    """
    cliente = cliente_falso(monkeypatch, libros, respuesta=[FILA])

    libros.dar_de_baja(7, "Extraviado")

    assert cliente.consulta.argumentos_de("update")[0][0]["dado_baja_en"] == "now()"


def test_la_baja_traduce_el_rechazo_del_disparador(monkeypatch, cliente_falso):
    """`validar_baja_de_libro` impide dar de baja un libro prestado."""
    cliente_falso(
        monkeypatch, libros,
        error=Exception('No se puede dar de baja "Momo": tiene 2 prestamo(s) '
                        'sin devolver.'),
    )

    with pytest.raises(ErrorDeCatalogo) as fallo:
        libros.dar_de_baja(7, "Extraviado")

    assert "ejemplares prestados" in str(fallo.value)
