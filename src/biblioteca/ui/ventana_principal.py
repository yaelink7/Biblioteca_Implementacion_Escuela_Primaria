"""Ventana principal del sistema.

Sustituye a VentanaMani.java. Por ahora aloja el catalogo; las pestanas de
prestamos y deudores se agregan en las siguientes pantallas.
"""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QMainWindow, QStatusBar, QTabWidget

from biblioteca.core.sesion import Sesion, cerrar_sesion
from biblioteca.ui.catalogo import PantallaCatalogo
from biblioteca.ui.estilo import COLOR_TENUE


class VentanaPrincipal(QMainWindow):
    def __init__(self, sesion: Sesion) -> None:
        super().__init__()
        self.sesion = sesion

        self.setWindowTitle("Biblioteca Escolar Adalberto Tejeda")
        self.resize(960, 620)

        self.pestanas = QTabWidget()
        self.pestanas.addTab(PantallaCatalogo(self), "Catálogo")
        self.setCentralWidget(self.pestanas)

        barra = QStatusBar()
        quien = QLabel(f"  {sesion.saludo}")
        quien.setStyleSheet(f"color: {COLOR_TENUE};")
        barra.addWidget(quien)
        self.setStatusBar(barra)

    def closeEvent(self, evento) -> None:  # noqa: N802 (lo nombra Qt)
        cerrar_sesion()
        super().closeEvent(evento)
