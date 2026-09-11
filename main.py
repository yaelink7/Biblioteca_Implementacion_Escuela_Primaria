"""Punto de entrada del sistema de biblioteca.

Sustituye a la ventana principal VentanaMani.java del sistema Java, con una
diferencia: aqui se pide identificarse antes de mostrar nada, porque las
politicas de seguridad de la base no responden a usuarios sin sesion.
"""

import sys

from PySide6.QtWidgets import QApplication

from biblioteca.ui.estilo import HOJA_DE_ESTILO
from biblioteca.ui.login import pedir_sesion
from biblioteca.ui.ventana_principal import VentanaPrincipal


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Biblioteca Escolar Adalberto Tejeda")
    app.setStyleSheet(HOJA_DE_ESTILO)

    sesion = pedir_sesion()
    if sesion is None:
        return 0  # el usuario cerro el dialogo sin entrar

    ventana = VentanaPrincipal(sesion)
    ventana.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
