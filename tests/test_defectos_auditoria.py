"""Comprueba que la migracion corrige los defectos del Reporte Tecnico de Calidad.

Cada prueba cita el defecto que cierra y el caso de prueba original de la
matriz. No tocan la base de datos: se ejecutan sin red ni credenciales, que
era una de las carencias senaladas en la auditoria (DAOBiblia quedo en 36 %
de cobertura porque sus pruebas exigian MySQL activo).

    pytest tests/test_defectos_auditoria.py -v
"""

from datetime import date

import pytest

from biblioteca.modelos.libro import Libro
from biblioteca.servicios import validador_libro


def libro_valido(**cambios) -> Libro:
    """Un libro que pasa todas las reglas, para alterarle un campo a la vez."""
    base = {
        "titulo": "El Quijote",
        "autor": "Cervantes",
        "tipo_libro": "Novela",
        "editorial": "Planeta",
        "existencias": 3,
        "ano_publicacion": 1605,
        "num_paginas": 863,
    }
    return Libro(**{**base, **cambios})


# --------------------------------------------------------------------------
# D-01 y D-09 (severidad alta)
# El original tenia setDisponible(boolean) que ignoraba su parametro, y al
# construir el libro fijaba disponible=true sin mirar las existencias.
# --------------------------------------------------------------------------


def test_d01_disponibilidad_no_se_puede_forzar():
    """TC-04: marcar como disponible un libro sin ejemplares no debe funcionar."""
    agotado = libro_valido(existencias=0)
    assert agotado.disponible is False

    # En el Java se llamaba setDisponible(False) y no pasaba nada.
    # Aqui no existe el setter: disponible se deduce, no se asigna.
    with pytest.raises(AttributeError):
        agotado.disponible = True


def test_d09_libro_sin_ejemplares_nace_no_disponible():
    """TC-30: la disponibilidad sigue a las existencias, no al reves."""
    assert libro_valido(existencias=0).disponible is False
    assert libro_valido(existencias=1).disponible is True


# --------------------------------------------------------------------------
# D-06 (severidad alta)
# La validacion media len("0") == 1 en lugar del valor 0, asi que aceptaba
# altas con cero ejemplares y con existencias negativas.
# --------------------------------------------------------------------------


def test_d06_alta_con_cero_ejemplares_se_rechaza():
    """TC-26: el original aceptaba el registro; ahora lo rechaza."""
    r = validador_libro.validar(libro_valido(existencias=0), es_alta=True)
    assert not r.es_valido
    assert "al menos un ejemplar" in r.mensaje


def test_d06_existencias_negativas_se_rechazan():
    """TC-27: el original registraba el libro con existencias en -5."""
    r = validador_libro.validar(libro_valido(existencias=-5), es_alta=True)
    assert not r.es_valido
    assert "negativas" in r.mensaje


def test_d06_libro_existente_si_puede_quedar_en_cero():
    """Un titulo ya registrado llega a cero cuando se presta el ultimo ejemplar."""
    r = validador_libro.validar(libro_valido(existencias=0), es_alta=False)
    assert r.es_valido


# --------------------------------------------------------------------------
# D-07 (severidad media): aceptaba libros de cero paginas.
# --------------------------------------------------------------------------


def test_d07_cero_paginas_se_rechaza():
    """TC-28."""
    r = validador_libro.validar(libro_valido(num_paginas=0))
    assert not r.es_valido
    assert "páginas" in r.mensaje


# --------------------------------------------------------------------------
# D-08 (severidad media)
# Contaba digitos: "2077" y "9999" tienen cuatro, asi que pasaban. La captura
# del libro publicado en 2077 quedo como evidencia en el reporte.
# --------------------------------------------------------------------------


def test_d08_ano_futuro_se_rechaza():
    """TC-29: el caso exacto documentado en la Figura 6 del reporte."""
    for ano in (2077, 9999, date.today().year + 1):
        r = validador_libro.validar(libro_valido(ano_publicacion=ano))
        assert not r.es_valido, f"el año {ano} deberia rechazarse"
        assert "futuro" in r.mensaje


def test_d08_ano_actual_se_acepta():
    """El limite es el ano en curso, no un numero fijo que envejece."""
    assert validador_libro.validar(
        libro_valido(ano_publicacion=date.today().year)
    ).es_valido


# --------------------------------------------------------------------------
# D-03 (severidad baja): la clase exponia getPublicacion y getAnoPublicacion
# para el mismo atributo.
# --------------------------------------------------------------------------


def test_d03_un_solo_nombre_para_el_ano():
    """TC-10: ya no hay dos formas de leer lo mismo."""
    libro = libro_valido(ano_publicacion=1999)
    assert libro.ano_publicacion == 1999
    assert not hasattr(libro, "getPublicacion")
    assert not hasattr(libro, "publicacion")


# --------------------------------------------------------------------------
# Reglas de campos obligatorios que el original si cumplia: se conservan.
# --------------------------------------------------------------------------


@pytest.mark.parametrize("titulo", ["", "   ", "\t"])
def test_tc20_tc22_titulo_vacio_o_en_blanco_se_rechaza(titulo):
    """TC-20 y TC-22: el trim hace que los espacios cuenten como vacio."""
    r = validador_libro.validar(libro_valido(titulo=titulo))
    assert not r.es_valido
    assert "título" in r.mensaje


def test_tc19_camino_feliz():
    """TC-19: con los siete campos correctos, pasa."""
    assert validador_libro.validar(libro_valido()).es_valido


def test_varios_errores_se_reportan_juntos():
    """El original avisaba de uno a la vez; asi el bibliotecario los ve todos."""
    r = validador_libro.validar(
        libro_valido(titulo="", existencias=-1, num_paginas=0, ano_publicacion=3000)
    )
    assert len(r.errores) == 4
