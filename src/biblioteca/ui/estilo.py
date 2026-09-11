"""Estilo visual compartido por las ventanas.

Se concentra aqui para que las pantallas no repitan colores sueltos y para
que cambiar la apariencia del sistema sea tocar un solo archivo.
"""

from __future__ import annotations

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel

# Paleta: azul de sello de biblioteca, con ambar para lo que necesita atencion
COLOR_PRINCIPAL = "#2D4B73"
COLOR_TENUE = "#6A7386"
COLOR_ERROR = "#B3261E"
COLOR_ALERTA = "#A8621B"
COLOR_OK = "#3F6B4A"

# Colores de superficie. Se declaran explicitos para que el sistema se vea
# igual en cualquier equipo: sin esto, Windows en tema oscuro pinta los
# encabezados de tabla con texto claro sobre fondo claro y no se leen.
FONDO = "#F7F7F5"
SUPERFICIE = "#FFFFFF"
TEXTO = "#1C2536"
BORDE = "#C8CCD4"
BORDE_TENUE = "#DCDFE4"

HOJA_DE_ESTILO = f"""
QWidget {{
    font-size: 14px;
    background-color: {FONDO};
    color: {TEXTO};
}}
QMainWindow, QDialog, QStatusBar {{
    background-color: {FONDO};
}}
QTabWidget::pane {{
    border: 1px solid {BORDE_TENUE};
    background: {FONDO};
}}
QTabBar::tab {{
    background: #E7E9EC;
    color: {COLOR_TENUE};
    padding: 8px 20px;
    border: 1px solid {BORDE_TENUE};
    border-bottom: none;
}}
QTabBar::tab:selected {{
    background: {FONDO};
    color: {COLOR_PRINCIPAL};
    font-weight: 600;
}}
QPushButton {{
    background-color: {COLOR_PRINCIPAL};
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 18px;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: #3A5D8A;
}}
QPushButton:disabled {{
    background-color: #C8CCD4;
    color: #8A9099;
}}
QLineEdit, QComboBox, QSpinBox {{
    border: 1px solid {BORDE};
    border-radius: 4px;
    padding: 4px 8px;
    background: {SUPERFICIE};
    color: {TEXTO};
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
    border: 1px solid {COLOR_PRINCIPAL};
}}
QComboBox QAbstractItemView {{
    background: {SUPERFICIE};
    color: {TEXTO};
    selection-background-color: {COLOR_PRINCIPAL};
    selection-color: white;
}}
QTableWidget {{
    border: 1px solid {BORDE_TENUE};
    background-color: {SUPERFICIE};
    alternate-background-color: #FAFAFA;
    gridline-color: #ECEEF1;
    color: {TEXTO};
}}
QTableWidget::item {{
    padding: 4px;
    color: {TEXTO};
}}
QTableWidget::item:selected {{
    background-color: {COLOR_PRINCIPAL};
    color: white;
}}
QHeaderView::section {{
    background-color: #EDEFF2;
    color: {TEXTO};
    border: none;
    border-bottom: 1px solid {BORDE_TENUE};
    padding: 8px;
    font-weight: 600;
}}
QCheckBox {{
    color: {TEXTO};
}}
QListWidget {{
    background-color: {SUPERFICIE};
    color: {TEXTO};
    border: 1px solid {BORDE};
    border-radius: 4px;
    padding: 2px;
}}
QListWidget::item {{
    padding: 7px 8px;
    border-radius: 3px;
}}
QListWidget::item:selected {{
    background-color: {COLOR_PRINCIPAL};
    color: white;
}}
QListWidget::item:disabled {{
    color: #A8ADB5;
}}
/* Recuadro del resumen antes de confirmar un prestamo.
   Se apunta por nombre y no por frameShape: QListWidget tambien es un
   QFrame y el selector generico le robaba el fondo blanco. */
QFrame#marcoResumen {{
    background-color: #EEF2F7;
    border: 1px solid {BORDE_TENUE};
    border-radius: 4px;
}}
QFrame#marcoResumen QLabel {{
    background: transparent;
}}
/* Boton secundario: acompana a la accion principal sin competir con ella */
QPushButton[secundario="true"] {{
    background-color: transparent;
    color: {COLOR_TENUE};
    border: 1px solid {BORDE};
}}
QPushButton[secundario="true"]:hover {{
    background-color: #E7E9EC;
    color: {TEXTO};
}}
QMessageBox, QInputDialog {{
    background-color: {FONDO};
}}
"""


def aplicar_estilo_titulo(titulo: QLabel, subtitulo: QLabel | None = None) -> None:
    """Jerarquia tipografica del encabezado de una pantalla."""
    fuente = QFont()
    fuente.setPointSize(20)
    fuente.setBold(True)
    titulo.setFont(fuente)
    titulo.setStyleSheet(f"color: {COLOR_PRINCIPAL};")

    if subtitulo is not None:
        menor = QFont()
        menor.setPointSize(11)
        subtitulo.setFont(menor)
        subtitulo.setStyleSheet(f"color: {COLOR_TENUE};")
