"""Ventana principal del sistema.

Sustituye a VentanaMani.java. Aloja las tres pantallas que opera el
bibliotecario: catalogo, prestamos y reporte de deudores.
"""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QMainWindow, QStatusBar, QTabWidget

from biblioteca.core.sesion import Sesion, cerrar_sesion
from biblioteca.ui.catalogo import PantallaCatalogo
from biblioteca.ui.deudores import PantallaDeudores
from biblioteca.ui.prestamos import PantallaPrestamos
from biblioteca.ui.estilo import COLOR_TENUE


class VentanaPrincipal(QMainWindow):
    def __init__(self, sesion: Sesion) -> None:
        super().__init__()
        self.sesion = sesion

        self.setWindowTitle("Biblioteca Escolar Adalberto Tejeda")
        self.resize(960, 620)

        self.pestanas = QTabWidget()
        self.pestanas.addTab(PantallaCatalogo(self), "Catálogo")
        self.pestanas.addTab(PantallaPrestamos(self), "Préstamos")
        self.pestanas.addTab(PantallaDeudores(self), "Deudores")
        self.setCentralWidget(self.pestanas)

        barra = QStatusBar()
        quien = QLabel(f"  {sesion.saludo}")
        quien.setStyleSheet(f"color: {COLOR_TENUE};")
        barra.addWidget(quien)
        self.setStatusBar(barra)

    def closeEvent(self, evento) -> None:  # noqa: N802 (lo nombra Qt)
        cerrar_sesion()
        super().closeEvent(evento)
