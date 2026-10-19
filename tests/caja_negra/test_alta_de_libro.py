"""Caja negra · alta y modificación de libros.

Equivale al **Grupo B** de la matriz de casos de prueba del sistema Java
(`Documentacion/Matriz_Casos_Prueba_Biblioteca.docx`), donde los casos TC-19 a
TC-30 no se pudieron automatizar: la lógica vivía dentro del método privado
`guardarenlista` de `GUILibro`, leía de los componentes Swing y avisaba con
`JOptionPane`. Las pruebas no podían invocarlo, y si lo sorteaban, cada cuadro
de diálogo dejaba la suite colgada esperando un clic.

La matriz recomendaba extraer esa lógica a un `ValidadorLibro` independiente.
Eso es `servicios/validador_libro.py`, y por eso **estos doce casos ya se
pueden ejecutar**.

Técnica: partición de equivalencia y valores límite. Las pruebas se diseñaron
desde las reglas declaradas, sin mirar la implementación: cada una entra por
`validar()` y observa solo lo que sale.
"""

from __future__ import annotations

from datetime import date

import pytest

from biblioteca.modelos.libro import Libro
from biblioteca.servicios import validador_libro
from biblioteca.servicios.validador_libro import ANO_MINIMO


def validar(libro, es_alta=True):
    return validador_libro.validar(libro, es_alta=es_alta)


# ===========================================================================
# TC-19 · camino feliz
# ===========================================================================

def test_tc19_alta_con_todos_los_datos_correctos(libro_valido):
    """Entrada perfecta: el validador no debe encontrar nada."""
    r = validar(libro_valido)

    assert r.es_valido
    assert r.errores == []
    assert r.mensaje == ""


# ===========================================================================
# TC-20, TC-21, TC-22 · campos obligatorios
# ===========================================================================

@pytest.mark.parametrize("campo,esperado", [
    ("titulo", "título"),
    ("autor", "autor"),
])
def test_tc20_un_campo_obligatorio_vacio(libro_valido, campo, esperado):
    setattr(libro_valido, campo, "")

    r = validar(libro_valido)

    assert not r.es_valido
    assert any(esperado in e.lower() for e in r.errores)


def test_tc21_formulario_completamente_vacio():
    """Todos los campos en blanco: debe reportar los dos obligatorios."""
    r = validar(Libro(titulo="", autor="", existencias=0))

    assert not r.es_valido
    assert len(r.errores) >= 2
    assert any("título" in e.lower() for e in r.errores)
    assert any("autor" in e.lower() for e in r.errores)


@pytest.mark.parametrize("relleno", ["   ", "\t", "\n", " \t \n "])
def test_tc22_campo_solo_con_espacios_cuenta_como_vacio(libro_valido, relleno):
    """El recorte es lo que convierte «   » en vacío."""
    libro_valido.titulo = relleno

    assert not validar(libro_valido).es_valido


# ===========================================================================
# TC-23, TC-29 · año de publicación
# ===========================================================================

def test_tc29_ano_futuro_de_cuatro_digitos_se_rechaza(libro_valido):
    """El caso que el sistema Java aceptaba (D-08).

    Aquel medía la cantidad de dígitos, así que 9999 pasaba por tener cuatro.
    """
    libro_valido.ano_publicacion = 9999

    r = validar(libro_valido)

    assert not r.es_valido
    assert any("futuro" in e.lower() for e in r.errores)


def test_tc23_ano_de_mas_de_cuatro_digitos_se_rechaza(libro_valido):
    libro_valido.ano_publicacion = 20255

    assert not validar(libro_valido).es_valido


class TestLimitesDelAno:
    """Valores límite alrededor de las dos fronteras del año."""

    def test_el_ano_actual_se_acepta(self, libro_valido):
        libro_valido.ano_publicacion = date.today().year
        assert validar(libro_valido).es_valido

    def test_el_ano_siguiente_se_rechaza(self, libro_valido):
        libro_valido.ano_publicacion = date.today().year + 1
        assert not validar(libro_valido).es_valido

    def test_el_ano_minimo_se_acepta(self, libro_valido):
        libro_valido.ano_publicacion = ANO_MINIMO
        assert validar(libro_valido).es_valido

    def test_justo_debajo_del_minimo_se_rechaza(self, libro_valido):
        libro_valido.ano_publicacion = ANO_MINIMO - 1
        r = validar(libro_valido)
        assert not r.es_valido
        assert any(str(ANO_MINIMO) in e for e in r.errores)

    def test_sin_ano_se_acepta(self, libro_valido):
        """No es obligatorio: un libro donado puede no traerlo."""
        libro_valido.ano_publicacion = None
        assert validar(libro_valido).es_valido


# ===========================================================================
# TC-26, TC-27 · existencias
# ===========================================================================

def test_tc26_alta_sin_ejemplares_se_rechaza(libro_valido):
    """El sistema Java lo aceptaba (D-06): medía la longitud, no el valor."""
    libro_valido.existencias = 0

    r = validar(libro_valido, es_alta=True)

    assert not r.es_valido
    assert any("ejemplar" in e.lower() for e in r.errores)


@pytest.mark.parametrize("existencias", [-1, -5, -100])
def test_tc27_existencias_negativas_se_rechazan(libro_valido, existencias):
    libro_valido.existencias = existencias

    r = validar(libro_valido)

    assert not r.es_valido
    assert any("negativ" in e.lower() for e in r.errores)


class TestExistenciasSegunElMomento:
    """La regla cambia entre registrar y modificar, y hay que probar ambas.

    Un título nuevo necesita al menos un ejemplar; uno ya registrado puede
    quedar en cero cuando todos están prestados.
    """

    def test_cero_al_dar_de_alta_se_rechaza(self, libro_valido):
        libro_valido.existencias = 0
        assert not validar(libro_valido, es_alta=True).es_valido

    def test_cero_al_modificar_se_acepta(self, libro_valido):
        libro_valido.existencias = 0
        assert validar(libro_valido, es_alta=False).es_valido

    def test_negativas_se_rechazan_en_los_dos_momentos(self, libro_valido):
        libro_valido.existencias = -1
        assert not validar(libro_valido, es_alta=True).es_valido
        assert not validar(libro_valido, es_alta=False).es_valido

    def test_uno_es_el_minimo_que_pasa_al_dar_de_alta(self, libro_valido):
        libro_valido.existencias = 1
        assert validar(libro_valido, es_alta=True).es_valido


# ===========================================================================
# TC-28 · número de páginas
# ===========================================================================

@pytest.mark.parametrize("paginas", [0, -1, -50])
def test_tc28_paginas_no_positivas_se_rechazan(libro_valido, paginas):
    """El sistema Java aceptaba cero páginas (D-07), por el mismo motivo."""
    libro_valido.num_paginas = paginas

    r = validar(libro_valido)

    assert not r.es_valido
    assert any("página" in e.lower() for e in r.errores)


def test_una_pagina_es_el_minimo_valido(libro_valido):
    libro_valido.num_paginas = 1
    assert validar(libro_valido).es_valido


def test_sin_numero_de_paginas_se_acepta(libro_valido):
    libro_valido.num_paginas = None
    assert validar(libro_valido).es_valido


# ===========================================================================
# TC-24, TC-25 · campos numéricos capturados como texto
# ===========================================================================

def test_tc24_y_tc25_las_cantidades_no_pueden_llegar_como_texto(libro_valido):
    """En el sistema Java esto reventaba con `NumberFormatException`.

    Aquí no hay conversión que falle: los dos campos son `QSpinBox` en el
    formulario, así que nunca entra texto, y el modelo los declara `int`. La
    prueba deja constancia de que la comparación trata números y no cadenas:
    si alguien sustituyera el control por una caja de texto sin convertir,
    falla aquí y no delante de la bibliotecaria.
    """
    libro_valido.existencias = "5"

    with pytest.raises(TypeError):
        validar(libro_valido)


# ===========================================================================
# TC-30 · coherencia entre disponibilidad y existencias
# ===========================================================================

def test_tc30_un_libro_sin_ejemplares_no_nace_disponible():
    """El sistema Java fijaba `disponible = true` sin mirar las existencias.

    Aquí no hay columna que fijar: la disponibilidad se deduce. El defecto
    D-09 dejó de ser posible por diseño, no por una comprobación añadida.
    """
    agotado = Libro(titulo="Momo", autor="Ende", existencias=0)
    con_ejemplares = Libro(titulo="Momo", autor="Ende", existencias=2)

    assert agotado.disponible is False
    assert con_ejemplares.disponible is True


def test_la_disponibilidad_no_se_puede_forzar():
    """Sin setter que ignore su parámetro, D-01 tampoco puede repetirse."""
    libro = Libro(titulo="Momo", autor="Ende", existencias=0)

    with pytest.raises(AttributeError):
        libro.disponible = True


# ===========================================================================
# Varios errores a la vez
# ===========================================================================

def test_se_reportan_todos_los_errores_de_una_vez():
    """El validador no se detiene en el primero.

    Importa para la operación: la bibliotecaria corrige una vez en lugar de
    descubrir los problemas de uno en uno.
    """
    r = validar(Libro(
        titulo="", autor="", existencias=-1, num_paginas=0, ano_publicacion=3000,
    ))

    assert len(r.errores) == 5


def test_con_varios_errores_el_mensaje_los_lista_con_viñetas():
    r = validar(Libro(titulo="", autor="", existencias=1))

    assert r.mensaje.count("•") == len(r.errores)


def test_con_un_solo_error_el_mensaje_no_lleva_viñeta(libro_valido):
    libro_valido.titulo = ""

    r = validar(libro_valido)

    assert "•" not in r.mensaje
    assert r.mensaje == r.errores[0]


# ===========================================================================
# TC-06 · exportación a CSV (grupos A.2 y A.5, aún sin implementar)
# ===========================================================================

@pytest.mark.xfail(
    reason="REP-03 (#38) sin implementar: cierra los defectos D-02, D-04 y D-05",
    raises=(ImportError, AttributeError), strict=True,
)
def test_tc06_un_titulo_con_coma_no_debe_romper_el_csv():
    """Los tres defectos de CSV del sistema Java siguen sin cerrarse.

    La prueba está escrita y marcada como fallo esperado: el día que alguien
    implemente la exportación, deja de fallar y avisa sola.
    """
    from biblioteca.servicios import exportador  # noqa: F401

    linea = exportador.libro_a_csv(
        Libro(titulo="Cien años, edición especial", autor="García Márquez",
              existencias=1)
    )
    assert linea.count(",") == 1 or '"' in linea
