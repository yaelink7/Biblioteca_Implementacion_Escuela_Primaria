"""Punto de entrada del sistema de biblioteca.

Sustituye a la ventana principal VentanaMani.java del sistema Java, con una
diferencia: aqui se pide identificarse antes de mostrar nada, porque las
politicas de seguridad de la base no responden a usuarios sin sesion.
"""

import sys

from PySide6.QtWidgets import QApplication

from biblioteca.ui.estilo import aplicar_apariencia
from biblioteca.ui.login import pedir_sesion
from biblioteca.ui.ventana_principal import VentanaPrincipal


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Biblioteca Escolar Adalberto Tejeda")
    aplicar_apariencia(app)

    # «Cerrar sesión» devuelve a la ficha de entrada; cerrar la ventana
    # termina el programa.
    while True:
        sesion = pedir_sesion()
        if sesion is None:
            return 0  # el usuario cerro el dialogo sin entrar

        ventana = VentanaPrincipal(sesion)
        ventana.show()
        codigo = app.exec()
        if not ventana.cerro_sesion:
            return codigo


if __name__ == "__main__":
    sys.exit(main())
