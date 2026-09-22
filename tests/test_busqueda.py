"""Comprueba que un nombre corriente no rompa la busqueda.

Nace de un defecto que la auditoria encontro: el texto que el bibliotecario
escribe se interpolaba crudo en la sintaxis de filtros de PostgREST. Dentro
de `or_` la coma separa condiciones, asi que buscar «Momo, la nina» o un
alumno como «Garcia, Ana» partia el filtro en dos y la consulta fallaba —y
como la busqueda se dispara sola a los 250 ms, el error salia mientras la
persona seguia escribiendo.

Estas pruebas no tocan la base: solo verifican como queda armado el valor.
"""

import pytest

from biblioteca.core.consultas import patron_de_busqueda


def test_el_texto_normal_se_envuelve_en_comodines():
    assert patron_de_busqueda("principito") == '"%principito%"'


@pytest.mark.parametrize("texto", [
    "Momo, la niña",
    "García, Ana",
    "Cuentos (varios)",
    "El principito, de Saint-Exupéry",
])
def test_los_separadores_de_postgrest_viajan_dentro_del_valor(texto):
    """La coma y el parentesis deben quedar dentro de las comillas."""
    patron = patron_de_busqueda(texto)

    assert patron.startswith('"%') and patron.endswith('%"')
    assert texto in patron


def test_la_comilla_doble_se_escapa():
    """Sin escapar cerraria el valor y lo que siguiera seria sintaxis."""
    patron = patron_de_busqueda('El libro "raro"')

    assert '\\"raro\\"' in patron
    assert patron.count('"') - patron.count('\\"') == 2   # solo las de fuera


def test_la_barra_invertida_se_escapa_antes_que_la_comilla():
    """Si se escapara al reves, la barra propia anularia el escape siguiente."""
    assert patron_de_busqueda('a\\"b') == '"%a\\\\\\"b%"'


def test_un_texto_vacio_no_produce_un_filtro_invalido():
    assert patron_de_busqueda("") == '"%%"'


def test_el_patron_se_puede_importar_sin_credenciales():
    """Vive en core/consultas.py justamente por esto.

    `core/config.py` lee las variables de entorno al importarse y revienta si
    faltan, y los repositorios lo arrastran. Por eso ni sus funciones puras se
    podian probar en una maquina sin `.env`. Este modulo no debe heredarlo:
    se comprueba en un proceso aparte, con el entorno limpio.
    """
    import sys

    import biblioteca.core.consultas  # noqa: F401

    assert "biblioteca.core.config" not in sys.modules, (
        "core/consultas.py arrastro core/config.py, que exige las variables "
        "de entorno al importarse"
    )
    assert "biblioteca.core.supabase_cliente" not in sys.modules
