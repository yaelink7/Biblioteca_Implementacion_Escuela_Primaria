"""Estilo visual compartido: el diseno «Lapiz», mostaza sobre grafito.

Se concentra aqui para que las pantallas no repitan colores sueltos y para
que cambiar la apariencia del sistema sea tocar un solo archivo. El mostaza
marca solo lo que esta activo y la accion principal; el rojo se queda para lo
urgente. Es la propuesta D de Documentacion/disenos/, la que se eligio.

Los selectores van por propiedad (`[rol="titulo"]`) y no por tipo dentro de
un contenedor: un `QFrame QLabel` le ganaria a la regla de cualquier etiqueta
con rol propio, y esa clase de choque no se ve hasta abrir la pantalla.
"""

from __future__ import annotations

from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QApplication, QTableWidget, QWidget

from biblioteca.ui.apariencia import (
    FAMILIA,
    FAMILIA_MONO,
    cargar_tipografias,
    ruta_para_hoja,
)

# --- Paleta, tomada del prototipo mostaza ---------------------------------
FONDO = "#F6F5F1"
SUPERFICIE = "#FFFFFF"
TEXTO = "#1E2023"
TENUE = "#62666D"
GRIS = "#4A4E55"
APAGADO = "#8A8E95"
MARCADOR = "#80848B"
BORDE = "#E4E2DC"
BORDE_CONTROL = "#D9D6CE"
RAYA = "#EFEDE7"
SOBRE_FILA = "#FAF9F6"

MOSTAZA = "#E0A526"
MOSTAZA_ENCIMA = "#D3981A"
MOSTAZA_SUAVE = "#F9EFD8"
MOSTAZA_MEDIO = "#F2DDA9"
MOSTAZA_TEXTO = "#755C24"

GRAFITO = "#26282C"
GRAFITO_CLARO = "#3A3D42"
TEXTO_RIEL = "#B9BCC2"

ROJO = "#A3261B"
ROJO_OSCURO = "#8F2318"
ROJO_FONDO = "#FBEAE7"
ROJO_BORDE = "#EFC9C3"
VERDE = "#3F6B4A"

# Nombres que las pantallas usan desde antes del rediseno. Siguen sirviendo
# a las que todavia no se pasan al diseno nuevo.
COLOR_PRINCIPAL = TEXTO
COLOR_TENUE = TENUE
COLOR_ERROR = ROJO
COLOR_ALERTA = MOSTAZA_TEXTO
COLOR_OK = VERDE


def hoja_de_estilo() -> str:
    """La hoja de estilo de toda la aplicacion."""
    flecha_combo = ruta_para_hoja("abajo", TENUE)
    orden_arriba = ruta_para_hoja("arriba", TEXTO)
    orden_abajo = ruta_para_hoja("abajo", TEXTO)
    palomita = ruta_para_hoja("palomita", TEXTO)

    return f"""
/* --- Base --- */
QMainWindow, QDialog, QMessageBox {{ background: {FONDO}; }}
QLabel {{ background: transparent; color: {TEXTO}; }}
QToolTip {{ background: {GRAFITO}; color: #FFFFFF; border: none; padding: 6px 8px; }}

/* --- Columna de iconos --- */
QFrame#riel {{ background: {GRAFITO}; border: none; }}
QLabel#logoRiel {{
    border: 1px dashed #6E727A; border-radius: 12px;
    color: #9DA1A8; font-size: 10px; font-weight: 700;
}}
QLabel#avatarRiel {{
    background: {GRAFITO_CLARO}; color: #FFFFFF; border-radius: 20px;
    font-size: 13px; font-weight: 700;
}}
QToolButton#botonSalir {{ background: transparent; border: none; border-radius: 10px; padding: 8px; }}
QToolButton#botonSalir:hover {{ background: #34373C; }}

/* --- Encabezado de cada pantalla --- */
QLabel[rol="lineaSuperior"] {{ font-family: "{FAMILIA_MONO}"; font-size: 12px; color: {TENUE}; }}
QLabel[rol="titulo"] {{ font-size: 32px; font-weight: 800; }}
QLabel[rol="resumen"] {{ font-family: "{FAMILIA_MONO}"; font-size: 13px; color: {GRIS}; }}
QLabel[rol="resumen"][aviso="true"] {{
    font-family: "{FAMILIA}"; font-size: 15px; font-weight: 700; color: {MOSTAZA_TEXTO};
}}
QLabel[rol="pista"] {{ font-family: "{FAMILIA_MONO}"; font-size: 12px; color: {TENUE}; }}

/* --- Botones. El principal es mostaza con letra oscura: el mostaza no
       aguanta texto blanco. --- */
QPushButton {{
    background: {MOSTAZA}; color: {TEXTO}; border: 1px solid {MOSTAZA};
    border-radius: 8px; padding: 0 18px; min-height: 40px;
    font-size: 14px; font-weight: 800;
}}
QPushButton:hover {{ background: {MOSTAZA_ENCIMA}; border-color: {MOSTAZA_ENCIMA}; }}
QPushButton:disabled {{ background: #EEE8DA; border-color: #EEE8DA; color: #9A968C; }}
QPushButton[secundario="true"] {{
    background: {SUPERFICIE}; border: 1px solid {BORDE_CONTROL}; font-weight: 700;
}}
QPushButton[secundario="true"]:hover {{ background: {SOBRE_FILA}; border-color: #C9C5BB; }}
QPushButton[secundario="true"]:disabled {{
    background: {SUPERFICIE}; border-color: {BORDE}; color: #A9ACB2;
}}
QPushButton[peligro="true"] {{ background: {SUPERFICIE}; color: {ROJO}; border: 1px solid {ROJO_BORDE}; }}
QPushButton[peligro="true"]:hover {{ background: {ROJO_FONDO}; }}
QPushButton[peligro="true"]:disabled {{
    background: {SUPERFICIE}; border-color: #F3E1DE; color: #CFA7A1;
}}
QPushButton:focus, QPushButton[secundario="true"]:focus, QPushButton[peligro="true"]:focus {{
    border: 2px solid {MOSTAZA_TEXTO};
}}

/* --- Campos --- */
QLineEdit, QComboBox, QSpinBox, QDateEdit {{
    background: {SUPERFICIE}; color: {TEXTO};
    border: 1px solid {BORDE_CONTROL}; border-radius: 8px;
    padding: 0 11px; min-height: 40px; font-size: 14px;
    selection-background-color: {MOSTAZA_MEDIO}; selection-color: {TEXTO};
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDateEdit:focus {{
    border: 2px solid {MOSTAZA_TEXTO}; padding: 0 10px;
}}
QLineEdit:disabled, QComboBox:disabled, QSpinBox:disabled, QDateEdit:disabled {{
    background: #F4F3EF; color: {TENUE};
}}
QLineEdit[rol="busqueda"] {{ min-height: 44px; font-size: 15px; }}
QComboBox::drop-down {{ border: none; width: 30px; }}
QComboBox::down-arrow {{ image: url({flecha_combo}); width: 16px; height: 16px; }}
QComboBox QAbstractItemView {{
    background: {SUPERFICIE}; color: {TEXTO}; border: 1px solid {BORDE};
    selection-background-color: {MOSTAZA_SUAVE}; selection-color: {TEXTO}; outline: none;
}}
QSpinBox::up-button, QSpinBox::down-button {{ width: 0; border: none; }}

QCheckBox {{ spacing: 10px; font-size: 14px; font-weight: 600; background: transparent; }}
QCheckBox::indicator {{
    width: 16px; height: 16px; border: 1px solid {MARCADOR}; border-radius: 4px;
    background: {SUPERFICIE};
}}
QCheckBox::indicator:hover {{ border-color: {MOSTAZA_TEXTO}; }}
QCheckBox::indicator:checked {{ background: {MOSTAZA}; border-color: {MOSTAZA}; image: url({palomita}); }}

QListWidget {{
    background: {SUPERFICIE}; color: {TEXTO}; border: 1px solid {BORDE_CONTROL};
    border-radius: 8px; padding: 4px; outline: none;
}}
QListWidget::item {{ padding: 8px 10px; border-radius: 6px; }}
QListWidget::item:selected {{ background: {MOSTAZA_SUAVE}; color: {TEXTO}; }}
QListWidget::item:disabled {{ color: #A9ACB2; }}
QFrame#marcoResumen {{ background: {MOSTAZA_SUAVE}; border: 1px solid {MOSTAZA_MEDIO}; border-radius: 8px; }}

/* --- Tablas --- */
QTableView {{
    background: {SUPERFICIE}; alternate-background-color: {SUPERFICIE}; color: {TEXTO};
    border: none; font-size: 14px; outline: none; qproperty-showGrid: false;
    selection-background-color: {MOSTAZA_SUAVE}; selection-color: {TEXTO};
}}
QTableView::item {{ border-bottom: 1px solid {RAYA}; padding: 0 12px; }}
QTableView::item:hover {{ background: {SOBRE_FILA}; }}
QTableView::item:selected {{ background: {MOSTAZA_SUAVE}; color: {TEXTO}; }}
/* Sin letra en ::section: si la hoja la fija ahi, Qt descarta la fuente de
   cada encabezado, que es donde rotular_encabezados() pone las mayusculas. */
QHeaderView {{ background: {SUPERFICIE}; border: none; font-size: 12px; font-weight: 700; }}
QHeaderView::section {{
    background: {SUPERFICIE}; color: {TENUE}; border: none; border-bottom: 1px solid {RAYA};
    padding: 0 12px; min-height: 40px;
}}
QHeaderView::section:hover {{ color: {TEXTO}; }}
QHeaderView::up-arrow {{ image: url({orden_arriba}); width: 14px; height: 14px; }}
QHeaderView::down-arrow {{ image: url({orden_abajo}); width: 14px; height: 14px; }}
QTableCornerButton::section {{ background: {SUPERFICIE}; border: none; }}

QScrollBar:vertical {{ background: transparent; width: 12px; margin: 2px; }}
QScrollBar:horizontal {{ background: transparent; height: 12px; margin: 2px; }}
QScrollBar::handle:vertical {{ background: {BORDE_CONTROL}; border-radius: 4px; min-height: 32px; }}
QScrollBar::handle:horizontal {{ background: {BORDE_CONTROL}; border-radius: 4px; min-width: 32px; }}
QScrollBar::handle:hover {{ background: #C9C5BB; }}
QScrollBar::add-line, QScrollBar::sub-line {{ width: 0; height: 0; }}
QScrollBar::add-page, QScrollBar::sub-page {{ background: none; }}

/* --- Tarjeta de la tabla y panel de detalle --- */
QFrame[rol="tarjeta"], QFrame[rol="panel"] {{
    background: {SUPERFICIE}; border: 1px solid {BORDE}; border-radius: 12px;
}}
QFrame[rol="barraTabla"] {{ background: transparent; border: none; border-bottom: 1px solid {BORDE}; }}
QLabel[rol="etiquetaPanel"] {{ font-family: "{FAMILIA_MONO}"; font-size: 12px; color: {TENUE}; }}
QLabel[rol="panelVacio"] {{ font-size: 14px; color: {TENUE}; }}
QLabel#portada {{
    background: {GRAFITO}; color: {MOSTAZA}; border-radius: 6px; font-size: 24px; font-weight: 800;
}}
QLabel[rol="nombrePanel"] {{ font-size: 18px; font-weight: 800; }}
QLabel[rol="detallePanel"] {{ font-size: 14px; color: {TENUE}; }}
QLabel[rol="dato"] {{ font-size: 14px; color: {TENUE}; }}
QLabel[rol="valor"] {{ font-size: 14px; }}
QLabel[rol="valor"][mono="true"] {{ font-family: "{FAMILIA_MONO}"; font-size: 13px; }}
QLabel[rol="valor"][alerta="true"] {{ color: {ROJO}; font-weight: 700; }}
QFrame[rol="cajaGris"] {{ background: #F4F3EF; border: none; border-radius: 10px; }}
QLabel[rol="textoCaja"] {{ font-size: 13px; color: {GRIS}; }}

/* --- Dialogos de captura --- */
QLabel[rol="tituloDialogo"] {{ font-size: 24px; font-weight: 800; }}
QLabel[rol="subtituloDialogo"] {{ font-size: 14px; color: {TENUE}; }}
QLabel[rol="etiquetaCampo"] {{ font-size: 14px; font-weight: 700; }}
QLabel[rol="notaCampo"] {{ font-size: 13px; color: {TENUE}; }}
QFrame#cajaError {{ background: {ROJO_FONDO}; border: none; border-radius: 10px; }}
QLabel#tituloError {{ color: {ROJO_OSCURO}; font-size: 14px; font-weight: 800; }}
QFrame#cajaError QLabel#etiquetaError {{ color: {ROJO_OSCURO}; font-size: 14px; }}

/* --- Inicio de sesion: la ficha de biblioteca sobre el grafito --- */
QDialog#DialogoLogin {{ background: {GRAFITO}; }}
QFrame#ficha {{ background: #FBFAF6; border: none; border-radius: 6px; }}
QFrame#franjaFicha {{
    background: {MOSTAZA}; border: none;
    border-top-left-radius: 6px; border-top-right-radius: 6px;
}}
QLabel[rol="rotuloFicha"] {{ font-family: "{FAMILIA_MONO}"; font-size: 12px; color: {TENUE}; }}
QLabel#logoFicha {{
    border: 1px dashed #A3A6AC; border-radius: 12px; color: #6E727A;
    font-size: 10px; font-weight: 700;
}}
QLabel[rol="tituloFicha"] {{ font-size: 24px; font-weight: 800; }}
QLabel[rol="escuelaFicha"] {{ font-size: 14px; color: {GRIS}; }}
QFrame#rayaFicha {{
    background: transparent; border: none;
    border-top: 1px solid {BORDE_CONTROL}; border-bottom: 1px solid {BORDE_CONTROL};
}}
QLabel[rol="rotuloCampo"] {{
    font-family: "{FAMILIA_MONO}"; font-size: 12px; font-weight: 600; color: {GRIS};
}}
QLineEdit[rol="campoFicha"] {{ min-height: 48px; border-radius: 6px; font-size: 15px; }}
QPushButton#botonEntrar {{ min-height: 48px; border-radius: 6px; font-size: 16px; }}
QLabel#perforacion {{ background: {GRAFITO}; border-radius: 9px; }}
"""


def paleta() -> QPalette:
    """Colores para lo que la hoja de estilo no nombra.

    Sin esto Windows en tema oscuro pinta los encabezados de tabla con texto
    claro sobre fondo claro, y no se leen.
    """
    colores = {
        QPalette.ColorRole.Window: FONDO,
        QPalette.ColorRole.WindowText: TEXTO,
        QPalette.ColorRole.Base: SUPERFICIE,
        QPalette.ColorRole.AlternateBase: SOBRE_FILA,
        QPalette.ColorRole.Text: TEXTO,
        QPalette.ColorRole.Button: SUPERFICIE,
        QPalette.ColorRole.ButtonText: TEXTO,
        QPalette.ColorRole.Highlight: MOSTAZA_SUAVE,
        QPalette.ColorRole.HighlightedText: TEXTO,
        QPalette.ColorRole.PlaceholderText: MARCADOR,
        QPalette.ColorRole.ToolTipBase: GRAFITO,
        QPalette.ColorRole.ToolTipText: "#FFFFFF",
        QPalette.ColorRole.Link: MOSTAZA_TEXTO,
    }
    resultado = QPalette()
    for rol, color in colores.items():
        resultado.setColor(rol, QColor(color))
    return resultado


def aplicar_apariencia(app: QApplication) -> None:
    """Deja la aplicacion con las letras, la paleta y la hoja del diseno.

    Fusion es el estilo base porque se dibuja igual en cualquier version de
    Windows; el de Windows 11 interpreta parte de la hoja a su manera.
    """
    cargar_tipografias()
    app.setStyle("Fusion")
    app.setPalette(paleta())
    fuente = QFont(FAMILIA)
    fuente.setPixelSize(14)
    app.setFont(fuente)
    app.setStyleSheet(hoja_de_estilo())


def rotular(widget: QWidget, mayusculas: bool = True, espaciado: float = 1.0) -> None:
    """Letra de ficha de biblioteca: mayusculas con aire entre las letras.

    La hoja de estilo de Qt no sabe de mayusculas ni de espaciado, asi que se
    le ponen a la fuente del control. El texto se queda como se escribio y
    las pruebas lo siguen leyendo igual: solo cambia como se dibuja.
    """
    fuente = widget.font()
    if mayusculas:
        fuente.setCapitalization(QFont.Capitalization.AllUppercase)
    fuente.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, espaciado)
    widget.setFont(fuente)


def rotular_encabezados(tabla: QTableWidget, espaciado: float = 0.6) -> None:
    """Encabezados de tabla en mayusculas, sin cambiar el texto de cada columna.

    Va en cada encabezado y no en la fuente del encabezado entero: al dibujar
    las secciones, Qt solo respeta la fuente que trae cada una.
    """
    for columna in range(tabla.columnCount()):
        encabezado = tabla.horizontalHeaderItem(columna)
        fuente = QFont(encabezado.font())
        fuente.setPixelSize(12)
        fuente.setWeight(QFont.Weight.Bold)
        fuente.setCapitalization(QFont.Capitalization.AllUppercase)
        fuente.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, espaciado)
        encabezado.setFont(fuente)


def repulir(widget: QWidget) -> None:
    """Vuelve a aplicar la hoja de estilo despues de cambiar una propiedad."""
    widget.style().unpolish(widget)
    widget.style().polish(widget)
