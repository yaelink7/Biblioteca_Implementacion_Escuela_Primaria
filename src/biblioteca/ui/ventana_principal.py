"""Ventana principal del sistema.

Sustituye a VentanaMani.java. Aloja las cinco pantallas que opera el personal
de la biblioteca: catalogo, prestamos, alumnos, deudores y empleados.

La navegacion es la columna de iconos del diseno «Lapiz»: en grafito, con el
mostaza solo en la seccion abierta. Encima de cada pantalla va una linea con
la escuela, la fecha y quien esta dentro, que sustituye a la barra de estado.
"""

from __future__ import annotations

from PySide6.QtCore import QDate, QSize, Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QStackedWidget,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from biblioteca.core.sesion import Sesion, cerrar_sesion
from biblioteca.ui.alumnos import PantallaAlumnos
from biblioteca.ui.apariencia import icono
from biblioteca.ui.catalogo import PantallaCatalogo
from biblioteca.ui.componentes import BotonRiel
from biblioteca.ui.deudores import PantallaDeudores
from biblioteca.ui.empleados import PantallaEmpleados
from biblioteca.ui.estilo import TEXTO_RIEL, rotular
from biblioteca.ui.formato import fecha_corta
from biblioteca.ui.prestamos import PantallaPrestamos

# Cada seccion: el nombre que se lee, su icono de Lucide y la pantalla que abre
SECCIONES = (
    ("Catálogo", "catalogo", PantallaCatalogo),
    ("Préstamos", "prestamos", PantallaPrestamos),
    ("Alumnos", "alumnos", PantallaAlumnos),
    ("Deudores", "deudores", PantallaDeudores),
    ("Empleados", "empleados", PantallaEmpleados),
)


class VentanaPrincipal(QMainWindow):
    def __init__(self, sesion: Sesion) -> None:
        super().__init__()
        self.sesion = sesion
        # Distingue «cerrar sesion» de cerrar la ventana: main.py vuelve a
        # pedir credenciales en el primer caso y termina en el segundo.
        self.cerro_sesion = False

        self.setWindowTitle("Biblioteca Escolar Adalberto Tejeda")
        self.resize(1280, 800)
        self.setMinimumSize(1024, 640)

        self.paginas = QStackedWidget()
        self.menu = QButtonGroup(self)
        self.botones: list[BotonRiel] = []
        for indice, (nombre, nombre_icono, pantalla) in enumerate(SECCIONES):
            self.paginas.addWidget(pantalla(self))
            boton = BotonRiel(nombre, nombre_icono)
            self.menu.addButton(boton, indice)
            self.botones.append(boton)
        self.botones[0].setChecked(True)
        self.menu.idClicked.connect(self.paginas.setCurrentIndex)

        marco = QWidget()
        disposicion = QHBoxLayout(marco)
        disposicion.setContentsMargins(0, 0, 0, 0)
        disposicion.setSpacing(0)
        disposicion.addWidget(self._riel())
        disposicion.addWidget(self._principal(), 1)
        self.setCentralWidget(marco)

    @property
    def secciones(self) -> list[str]:
        """Los nombres del menu, en el orden en que aparecen."""
        return [boton.text() for boton in self.botones]

    def _riel(self) -> QFrame:
        riel = QFrame()
        riel.setObjectName("riel")
        riel.setFixedWidth(96)
        columna = QVBoxLayout(riel)
        columna.setContentsMargins(8, 20, 8, 18)
        columna.setSpacing(6)

        logo = QLabel("LOGO")
        logo.setObjectName("logoRiel")
        logo.setFixedSize(54, 54)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        columna.addWidget(logo, 0, Qt.AlignmentFlag.AlignHCenter)
        columna.addSpacing(20)
        for boton in self.botones:
            columna.addWidget(boton)
        columna.addStretch(1)

        perfil = self.sesion.perfil
        self.avatar = QLabel(f"{perfil.nombre[:1]}{perfil.apellido[:1]}".upper())
        self.avatar.setObjectName("avatarRiel")
        self.avatar.setFixedSize(40, 40)
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar.setToolTip(self.sesion.saludo)
        columna.addWidget(self.avatar, 0, Qt.AlignmentFlag.AlignHCenter)

        self.boton_salir = QToolButton()
        self.boton_salir.setObjectName("botonSalir")
        self.boton_salir.setIcon(icono("salir", TEXTO_RIEL, 20))
        self.boton_salir.setIconSize(QSize(20, 20))
        self.boton_salir.setToolTip("Cerrar sesión")
        self.boton_salir.setAccessibleName("Cerrar sesión")
        self.boton_salir.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_salir.clicked.connect(self.salir)
        columna.addWidget(self.boton_salir, 0, Qt.AlignmentFlag.AlignHCenter)
        return riel

    def _principal(self) -> QWidget:
        principal = QWidget()
        columna = QVBoxLayout(principal)
        columna.setContentsMargins(34, 26, 34, 34)
        columna.setSpacing(18)

        perfil = self.sesion.perfil
        hoy = fecha_corta(QDate.currentDate().toPython())
        self.linea_escuela = QLabel("Biblioteca escolar · Esc. Prim. Adalberto Tejeda")
        self.linea_quien = QLabel(f"{hoy} · {perfil.nombre_completo} · {perfil.rol.value}")
        linea = QHBoxLayout()
        for etiqueta in (self.linea_escuela, self.linea_quien):
            etiqueta.setProperty("rol", "lineaSuperior")
            rotular(etiqueta)
        linea.addWidget(self.linea_escuela)
        linea.addStretch(1)
        linea.addWidget(self.linea_quien)

        columna.addLayout(linea)
        columna.addWidget(self.paginas, 1)
        return principal

    def salir(self) -> None:
        """Cierra la sesion; main.py vuelve a mostrar el inicio de sesion."""
        self.cerro_sesion = True
        self.close()

    def closeEvent(self, evento) -> None:  # noqa: N802 (lo nombra Qt)
        cerrar_sesion()
        super().closeEvent(evento)
