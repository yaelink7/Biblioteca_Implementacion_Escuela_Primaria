"""Caja negra · regla de disponibilidad del libro.

**Grupo A.1** de la matriz de casos del sistema Java, casos TC-01 a TC-04.
Allá eran cuatro pruebas sobre `Libro.setDisponible(boolean)`, un método que
guardaba la disponibilidad en una columna aparte. TC-04 reveló el defecto
**D-01**: el método ignoraba su propio parámetro y escribía `true` siempre,
de modo que un libro agotado quedaba anunciado como disponible.

Aquí la columna no existe. `disponible` es una propiedad calculada sobre
`existencias`, así que la disponibilidad **no se puede fijar**: se deduce. El
defecto dejó de ser posible por diseño y no por una comprobación añadida, que
es un cambio de naturaleza distinta y conviene dejarlo probado.
"""

from __future__ import annotations

import pytest

from biblioteca.modelos.libro import Libro, Publicacion


def libro(existencias: int, **extra) -> Libro:
    return Libro(titulo="El Quijote", autor="Cervantes",
                 existencias=existencias, **extra)


# ===========================================================================
# TC-01, TC-02, TC-03 · la disponibilidad sigue a las existencias
# ===========================================================================

def test_tc01_con_ejemplares_esta_disponible():
    assert libro(5).disponible is True


def test_tc02_sin_ejemplares_no_esta_disponible():
    assert libro(0).disponible is False


def test_tc03_existencias_negativas_no_cuentan_como_disponible():
    """Dato corrupto heredado: la base lo impide con un `check`, pero si una
    fila vieja llegara con -3, el modelo no debe anunciarla como disponible."""
    assert libro(-3).disponible is False


@pytest.mark.parametrize("existencias,esperado", [
    (-1, False), (0, False), (1, True), (2, True), (999, True),
])
def test_valores_limite_alrededor_de_cero(existencias, esperado):
    """La frontera de la regla está entre 0 y 1, y es la única que hay."""
    assert libro(existencias).disponible is esperado


# ===========================================================================
# TC-04 · el defecto D-01 ya no se puede reproducir
# ===========================================================================

def test_tc04_la_disponibilidad_no_acepta_que_se_le_imponga_un_valor():
    """El caso que delató a D-01, al revés: aquí no hay setter que ignorar."""
    con_ejemplares = libro(5)

    with pytest.raises(AttributeError):
        con_ejemplares.disponible = False

    assert con_ejemplares.disponible is True


def test_la_disponibilidad_cambia_sola_cuando_cambian_las_existencias():
    """Lo que la columna almacenada del Java no garantizaba.

    Podía quedar en `true` mientras el inventario bajaba a cero: dos fuentes
    de verdad para el mismo hecho.
    """
    ejemplar = libro(1)
    assert ejemplar.disponible is True

    ejemplar.existencias = 0
    assert ejemplar.disponible is False

    ejemplar.existencias = 4
    assert ejemplar.disponible is True


def test_la_regla_vive_en_la_clase_base():
    """`Publicacion` la define y `Libro` la hereda, como en el diseño original."""
    assert "disponible" in vars(Publicacion)
    assert "disponible" not in vars(Libro)
    assert Publicacion(titulo="t", autor="a", existencias=2).disponible is True


# ===========================================================================
# La columna `estado`, que es lo que lee la bibliotecaria
# ===========================================================================

class TestTextoDeEstado:
    """Tres caminos y una concordancia de singular, todos visibles en pantalla."""

    def test_un_solo_ejemplar_va_en_singular(self):
        assert libro(1).estado == "1 disponible"

    def test_varios_ejemplares_van_en_plural(self):
        assert libro(3).estado == "3 disponibles"

    def test_sin_ejemplares_lo_dice_en_lugar_de_mostrar_un_cero(self):
        assert libro(0).estado == "Sin ejemplares"

    def test_un_libro_dado_de_baja_muestra_su_motivo(self):
        ejemplar = libro(2, activo=False, motivo_baja="Extraviado")
        assert ejemplar.estado == "Baja: Extraviado"

    def test_una_baja_sin_motivo_no_deja_el_texto_a_medias(self):
        """La base exige el motivo; el modelo no se rompe si falta."""
        assert libro(2, activo=False).estado == "Baja: sin motivo"

    def test_la_baja_pesa_mas_que_las_existencias(self):
        """Un libro de baja con ejemplares en la fila sigue siendo baja."""
        assert libro(5, activo=False, motivo_baja="Deteriorado").estado.startswith("Baja")


def test_la_etiqueta_junta_titulo_y_autor():
    assert libro(1).etiqueta == "El Quijote — Cervantes"
