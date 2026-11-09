"""Interfaz · el diseño «Lápiz» (propuesta D, mostaza sobre grafito).

Comprueba lo que el diseño agregó y que ninguna otra prueba toca: que las
letras y los iconos viajen dentro del paquete, que la hoja de estilo llegue
completa, la columna de iconos que sustituye a las pestañas, la ficha del
libro en el Catálogo, el recuadro de error del formulario y la ficha de
entrada.

Lo visual se comprueba por sus efectos medibles —qué texto, qué color, qué
sección queda abierta— y no por capturas: las capturas se revisan a mano en
el PR, contra el prototipo.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from PySide6.QtCore import QDate, QEvent, QPointF, QSize
from PySide6.QtGui import QColor, QEnterEvent, QFont, QPalette
from PySide6.QtWidgets import QApplication, QLabel

from biblioteca.core import sesion as modulo_sesion
from biblioteca.modelos.libro import Libro
from biblioteca.repositorios import libros as repo_libros
from biblioteca.repositorios import personas as repo_personas
from biblioteca.repositorios import prestamos as repo_prestamos
from biblioteca.ui.apariencia import RECURSOS, cargar_tipografias, icono, ruta_para_hoja
from biblioteca.ui.catalogo import PantallaCatalogo
from biblioteca.ui.componentes import BotonRiel
from biblioteca.ui.deudores import PantallaDeudores
from biblioteca.ui.estilo import (
    FONDO,
    GRAFITO,
    MOSTAZA,
    aplicar_apariencia,
    hoja_de_estilo,
    rotular,
)
from biblioteca.ui.formato import fecha_corta, inicial
from biblioteca.ui.formulario_libro import FormularioLibro
from biblioteca.ui.login import DialogoLogin
from biblioteca.ui.ventana_principal import VentanaPrincipal


@pytest.fixture
def todo_vacio(sin_base, con_sesion):
    """La base contesta vacío a todo: basta para construir la ventana entera."""
    sin_base(repo_libros, listar=[], buscar=[])
    sin_base(repo_personas, listar_alumnos=[], buscar_alumnos=[],
             buscar_alumnos_o_salon=[], listar_empleados=[])
    sin_base(repo_prestamos, activos=[], deudores=[], historial_de=[])


def catalogo_con(sin_base, libros: list[Libro]) -> PantallaCatalogo:
    sin_base(repo_libros, listar=libros, buscar=[])
    return PantallaCatalogo()


# ===========================================================================
# Letras e iconos dentro del paquete
# ===========================================================================

def test_las_tipografias_del_diseno_viajan_en_el_paquete(app):
    """Sin ellas la computadora de la biblioteca dibujaría con Arial."""
    assert {"Manrope", "IBM Plex Mono"} <= cargar_tipografias()


def test_cada_icono_del_paquete_se_puede_dibujar(app):
    archivos = sorted((RECURSOS / "iconos").glob("*.svg"))

    assert archivos
    for archivo in archivos:
        assert not icono(archivo.stem, "#1E2023").isNull(), archivo.name


def test_un_icono_que_no_existe_falla_al_pedirlo(app):
    """Mejor un error claro al programar que un botón vacío en la escuela."""
    with pytest.raises(FileNotFoundError):
        icono("no-existe", "#000000")


def test_la_hoja_de_estilo_recibe_iconos_ya_coloreados(app):
    """La hoja de Qt no sabe teñir un SVG: se le entrega el color puesto."""
    ruta = Path(ruta_para_hoja("abajo", "#62666D"))

    contenido = ruta.read_text(encoding="utf-8")
    assert "#62666D" in contenido
    assert "currentColor" not in contenido


# ===========================================================================
# Hoja de estilo y paleta
# ===========================================================================

def test_la_hoja_de_estilo_lleva_el_mostaza_y_el_grafito(app):
    hoja = hoja_de_estilo()

    assert MOSTAZA in hoja and GRAFITO in hoja
    assert "url(" in hoja and "currentColor" not in hoja


def test_aplicar_la_apariencia_deja_fusion_la_paleta_y_manrope(app):
    """Es lo que hace main.py antes de abrir la primera ventana."""
    antes = (app.style().name(), app.palette(), app.font(), app.styleSheet())
    try:
        aplicar_apariencia(app)

        assert app.palette().color(QPalette.ColorRole.Window) == QColor(FONDO)
        assert app.font().family() == "Manrope"
        assert MOSTAZA in app.styleSheet()
        # Con hoja de estilo, Qt envuelve el estilo base y su nombre sale
        # vacío; sin ella se lee el que quedó debajo.
        app.setStyleSheet("")
        assert app.style().name().lower() == "fusion"
    finally:
        app.setStyleSheet(antes[3])
        app.setFont(antes[2])
        app.setPalette(antes[1])
        app.setStyle(antes[0])


def test_rotular_cambia_como_se_dibuja_y_no_el_texto(app):
    """Las pruebas siguen leyendo «Libro seleccionado», no «LIBRO SELECCIONADO»."""
    rotulo = QLabel("Libro seleccionado")
    pista = QLabel("Doble clic para modificar")

    rotular(rotulo)
    rotular(pista, mayusculas=False, espaciado=0.3)

    assert rotulo.text() == "Libro seleccionado"
    assert rotulo.font().capitalization() == QFont.Capitalization.AllUppercase
    assert pista.font().capitalization() == QFont.Capitalization.MixedCase


# ===========================================================================
# Fechas cortas e inicial de la portada
# ===========================================================================

def test_la_fecha_corta_no_depende_del_idioma_del_equipo():
    assert fecha_corta(date(2026, 11, 3)) == "3 nov 2026"
    assert fecha_corta(date(2026, 1, 15)) == "15 ene 2026"


@pytest.mark.parametrize("titulo,letra", [
    ("El principito", "P"),
    ("Las aventuras de Tom Sawyer", "A"),
    ("Momo", "M"),
    ("¿Dónde viven los monstruos?", "D"),
    ("El", "E"),
    ("", "?"),
])
def test_la_portada_lleva_la_inicial_sin_el_articulo(titulo, letra):
    assert inicial(titulo) == letra


# ===========================================================================
# La columna de iconos, que sustituye a las pestañas
# ===========================================================================

def test_el_menu_tiene_cinco_secciones_y_abre_la_que_se_pulsa(
    todo_vacio, sesion_de_administradora
):
    ventana = VentanaPrincipal(sesion_de_administradora)

    assert ventana.secciones == ["Catálogo", "Préstamos", "Alumnos",
                                 "Deudores", "Empleados"]
    assert ventana.paginas.currentIndex() == 0
    assert ventana.botones[0].isChecked()

    ventana.botones[3].click()

    assert ventana.paginas.currentIndex() == 3
    assert isinstance(ventana.paginas.currentWidget(), PantallaDeudores)
    assert not ventana.botones[0].isChecked()


def test_la_linea_superior_dice_la_fecha_quien_entro_y_su_perfil(
    todo_vacio, sesion_de_administradora
):
    """Sustituye a la barra de estado que decía quién estaba dentro."""
    ventana = VentanaPrincipal(sesion_de_administradora)

    texto = ventana.linea_quien.text()
    assert fecha_corta(QDate.currentDate().toPython()) in texto
    assert "María Hernández" in texto and "administrador" in texto
    assert "Adalberto Tejeda" in ventana.linea_escuela.text()


def test_el_avatar_lleva_las_iniciales_de_quien_entro(
    todo_vacio, sesion_de_administradora
):
    ventana = VentanaPrincipal(sesion_de_administradora)

    assert ventana.avatar.text() == "MH"


def test_cerrar_sesion_desde_el_menu_vuelve_a_pedir_credenciales(
    todo_vacio, sesion_de_administradora
):
    """main.py distingue este cierre del de la ventana con `cerro_sesion`."""
    ventana = VentanaPrincipal(sesion_de_administradora)

    ventana.boton_salir.click()

    assert ventana.cerro_sesion is True
    assert modulo_sesion._sesion_actual is None


def test_cerrar_la_ventana_no_cuenta_como_cerrar_sesion(
    todo_vacio, sesion_de_administradora
):
    ventana = VentanaPrincipal(sesion_de_administradora)

    ventana.close()

    assert ventana.cerro_sesion is False


def test_el_boton_del_menu_se_dibuja_en_cada_estado(app):
    """Normal, con el ratón encima, abierto y con el foco del teclado."""
    boton = BotonRiel("Catálogo", "catalogo")
    boton.resize(boton.sizeHint())

    assert boton.sizeHint() == QSize(80, 64)
    assert not boton.grab().isNull()

    QApplication.sendEvent(boton, QEnterEvent(QPointF(5, 5), QPointF(5, 5),
                                              QPointF(5, 5)))
    assert boton._encima
    assert not boton.grab().isNull()

    QApplication.sendEvent(boton, QEvent(QEvent.Type.Leave))
    assert not boton._encima

    boton.setChecked(True)
    boton.hasFocus = lambda: True   # el foco real exige una ventana activa
    assert not boton.grab().isNull()


# ===========================================================================
# Catálogo: la ficha del libro elegido
# ===========================================================================

def test_sin_libro_elegido_la_ficha_espera(sin_base, libros_de_ejemplo, con_sesion):
    catalogo = catalogo_con(sin_base, libros_de_ejemplo)

    assert not catalogo.ui.etiquetaPanelVacio.isHidden()
    assert catalogo.ui.fichaLibro.isHidden()


def test_al_elegir_un_libro_la_ficha_muestra_sus_datos(
    sin_base, libros_de_ejemplo, con_sesion
):
    catalogo = catalogo_con(sin_base, libros_de_ejemplo)

    catalogo.ui.tablaLibros.selectRow(0)

    ui = catalogo.ui
    assert ui.etiquetaPanelVacio.isHidden() and not ui.fichaLibro.isHidden()
    assert ui.portada.text() == "P"
    assert ui.etiquetaLibroTitulo.text() == "El principito"
    assert ui.valorEditorial.text() == "Salamandra"
    assert ui.valorAno.text() == "1943"
    assert ui.valorPaginas.text() == "96"
    assert ui.valorDisponibles.text() == "3 ejemplares"
    assert ui.cajaBaja.isHidden()


def test_un_solo_ejemplar_se_dice_en_singular(sin_base, con_sesion):
    catalogo = catalogo_con(sin_base, [Libro(id=7, titulo="Matilda",
                                             autor="Roald Dahl", existencias=1)])

    catalogo.ui.tablaLibros.selectRow(0)

    assert catalogo.ui.valorDisponibles.text() == "1 ejemplar"


def test_un_libro_agotado_lo_dice_en_rojo_en_la_ficha(
    sin_base, libros_de_ejemplo, con_sesion
):
    catalogo = catalogo_con(sin_base, libros_de_ejemplo)

    catalogo.ui.tablaLibros.selectRow(1)

    assert catalogo.ui.valorDisponibles.text() == "Sin ejemplares"
    assert catalogo.ui.valorDisponibles.property("alerta") is True


def test_un_libro_dado_de_baja_muestra_cuando_y_por_que(
    sin_base, libros_de_ejemplo, con_sesion
):
    catalogo = catalogo_con(sin_base, libros_de_ejemplo)

    catalogo.ui.tablaLibros.selectRow(2)

    ui = catalogo.ui
    assert not ui.cajaBaja.isHidden()
    assert ui.etiquetaBaja.text() == "Dado de baja el 1 sep 2026. Motivo: Extraviado."
    assert ui.valorDisponibles.text() == "—"
    assert ui.valorTipo.text() == "—" and ui.valorAno.text() == "—"
    assert not ui.botonBaja.isEnabled()


def test_una_baja_sin_fecha_ni_motivo_no_inventa_ninguno(sin_base, con_sesion):
    catalogo = catalogo_con(sin_base, [Libro(id=8, titulo="Pinocho", autor="Collodi",
                                             activo=False)])

    catalogo.ui.tablaLibros.selectRow(0)

    assert catalogo.ui.etiquetaBaja.text() == "Dado de baja. Motivo: sin motivo."


def test_la_fila_elegida_se_dibuja_con_su_raya(sin_base, libros_de_ejemplo, con_sesion):
    """La raya mostaza la pinta el delegado; aquí se comprueba que dibuje."""
    catalogo = catalogo_con(sin_base, libros_de_ejemplo)
    catalogo.resize(1100, 680)

    catalogo.ui.tablaLibros.selectRow(0)

    assert not catalogo.grab().isNull()


def test_el_aviso_vuelve_al_resumen_despues_de_un_rato(
    sin_base, libros_de_ejemplo, con_sesion
):
    catalogo = catalogo_con(sin_base, libros_de_ejemplo)
    resumen = catalogo.ui.etiquetaResumen

    catalogo._avisar("Se registró «Momo».")
    assert resumen.property("aviso") is True

    catalogo._quitar_aviso()   # lo que hace el temporizador a los 3 s

    assert resumen.property("aviso") is False
    assert "títulos" in resumen.text()


def test_los_encabezados_de_la_tabla_se_dibujan_en_mayusculas(
    sin_base, libros_de_ejemplo, con_sesion
):
    """Como en la maqueta, pero sin cambiar el texto que leen las pruebas."""
    catalogo = catalogo_con(sin_base, libros_de_ejemplo)
    tabla = catalogo.ui.tablaLibros

    for columna in range(tabla.columnCount()):
        encabezado = tabla.horizontalHeaderItem(columna)
        assert encabezado.font().capitalization() == QFont.Capitalization.AllUppercase
    assert tabla.horizontalHeaderItem(0).text() == "Título"


# ===========================================================================
# Formulario de libro: el recuadro de error
# ===========================================================================

def test_el_recuadro_de_error_nace_oculto(app):
    assert FormularioLibro().ui.cajaError.isHidden()


def test_un_dato_que_falta_abre_el_recuadro_y_dice_que_revisar(sin_base):
    sin_base(repo_libros, dar_de_alta=Libro(titulo="x", autor="y", existencias=1))
    formulario = FormularioLibro()

    formulario.ui.botonGuardar.click()

    assert not formulario.ui.cajaError.isHidden()
    assert formulario.ui.tituloError.text() == "Revisa estos datos:"


def test_un_corte_de_red_titula_el_recuadro_de_otra_forma(sin_base):
    """No es un dato mal capturado: decir «revisa estos datos» confundiría."""
    sin_base(repo_libros, dar_de_alta=ConnectionError("Connection refused"))
    formulario = FormularioLibro()
    formulario.ui.campoTitulo.setText("Momo")
    formulario.ui.campoAutor.setText("Michael Ende")

    formulario.ui.botonGuardar.click()

    assert formulario.ui.tituloError.text() == "No se pudo guardar:"


def test_el_encabezado_dice_si_es_alta_o_modificacion(libros_de_ejemplo):
    alta = FormularioLibro()
    cambio = FormularioLibro(libro=libros_de_ejemplo[0])

    assert alta.ui.etiquetaEncabezado.text() == "Registrar libro"
    assert "ejemplares" in alta.ui.etiquetaSubtitulo.text()
    assert cambio.ui.etiquetaEncabezado.text() == "Modificar libro"
    assert "Guardar" in cambio.ui.etiquetaSubtitulo.text()


# ===========================================================================
# Inicio de sesión: la ficha sobre el grafito
# ===========================================================================

def test_la_ficha_de_entrada_se_dibuja_sobre_el_grafito(app):
    dialogo = DialogoLogin()
    dialogo.resize(980, 720)

    imagen = dialogo.grab().toImage()

    # La esquina queda entre puntos de la retícula: es grafito liso
    assert imagen.pixelColor(2, 2) == QColor(GRAFITO)


def test_los_campos_de_entrada_llevan_su_icono_y_la_ficha_su_sombra(app):
    dialogo = DialogoLogin()

    assert dialogo.ui.campoCorreo.actions()
    assert dialogo.ui.campoContrasena.actions()
    assert dialogo.ui.ficha.graphicsEffect() is not None
    assert dialogo.ui.botonEntrar.text() == "Entrar"
