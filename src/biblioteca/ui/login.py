"""Pantalla de inicio de sesion (REQ-USU-02).

El sistema Java abria directo en el menu principal. Aqui esta pantalla es
obligatoria: sin sesion las politicas RLS de Supabase no devuelven ni un
libro, asi que no hay forma de saltarsela.

En el diseno «Lapiz» es una ficha de biblioteca sobre el grafito punteado:
la franja mostaza, los rotulos a maquina y la perforacion de abajo.
"""

from __future__ import annotations

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QGraphicsDropShadowEffect,
    QLineEdit,
    QWidget,
)

from biblioteca.core.errores import causa as causa_del_error
from biblioteca.core.sesion import ErrorDeAcceso, Sesion, iniciar_sesion
from biblioteca.ui.apariencia import icono
from biblioteca.ui.estilo import COLOR_ERROR, GRAFITO, GRAFITO_CLARO, TENUE, TEXTO, rotular
from biblioteca.ui.generado.ui_login import Ui_DialogoLogin

# Distancia entre los puntos del fondo, como la reticula del prototipo
PASO_DE_PUNTOS = 24


class DialogoLogin(QDialog):
    """Pide las credenciales y deja lista la sesion del bibliotecario."""

    def __init__(self, padre: QWidget | None = None) -> None:
        super().__init__(padre)
        self.ui = Ui_DialogoLogin()
        self.ui.setupUi(self)

        self.sesion: Sesion | None = None

        self._preparar_aspecto()
        self.ui.etiquetaError.setStyleSheet(f"color: {COLOR_ERROR};")

        self.ui.botonEntrar.clicked.connect(self._entrar)
        self.ui.campoCorreo.returnPressed.connect(self._entrar)
        self.ui.campoContrasena.returnPressed.connect(self._entrar)

        self.ui.campoCorreo.setFocus()

    def _preparar_aspecto(self) -> None:
        ui = self.ui
        for etiqueta in (ui.etiquetaRotulo, ui.etiquetaCorreo, ui.etiquetaContrasena):
            rotular(etiqueta)
        posicion = QLineEdit.ActionPosition.LeadingPosition
        ui.campoCorreo.addAction(icono("correo", TENUE), posicion)
        ui.campoContrasena.addAction(icono("candado", TENUE), posicion)
        # La flecha va despues de la palabra, como en el prototipo
        ui.botonEntrar.setIcon(icono("flecha", TEXTO))
        ui.botonEntrar.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        sombra = QGraphicsDropShadowEffect(ui.ficha)
        sombra.setBlurRadius(60)
        sombra.setOffset(0, 24)
        sombra.setColor(QColor(0, 0, 0, 170))
        ui.ficha.setGraphicsEffect(sombra)

    def paintEvent(self, evento) -> None:  # noqa: N802 (lo nombra Qt)
        """El grafito con su reticula de puntos, detras de la ficha."""
        pintor = QPainter(self)
        pintor.fillRect(self.rect(), QColor(GRAFITO))
        pintor.setRenderHint(QPainter.RenderHint.Antialiasing)
        pintor.setPen(Qt.PenStyle.NoPen)
        pintor.setBrush(QColor(GRAFITO_CLARO))
        mitad = PASO_DE_PUNTOS / 2
        for x in range(0, self.width(), PASO_DE_PUNTOS):
            for y in range(0, self.height(), PASO_DE_PUNTOS):
                pintor.drawEllipse(QPointF(x + mitad, y + mitad), 1.2, 1.2)
        pintor.end()

    def _entrar(self) -> None:
        correo = self.ui.campoCorreo.text().strip()
        contrasena = self.ui.campoContrasena.text()

        if not correo or not contrasena:
            self._mostrar_error("Escribe tu correo y tu contraseña.")
            return

        self._ocupado(True)
        try:
            self.sesion = iniciar_sesion(correo, contrasena)
        except ErrorDeAcceso as error:
            self._mostrar_error(str(error))
            self.ui.campoContrasena.clear()
            self.ui.campoContrasena.setFocus()
            return
        except Exception as error:
            # Un correo mal escrito, una sesion caida y un servidor apagado
            # no son el mismo problema: decir cual es evita que la persona
            # revise el cable cuando lo que falla es otra cosa.
            self._mostrar_error(causa_del_error(error))
            return
        finally:
            self._ocupado(False)

        self.accept()

    def _mostrar_error(self, mensaje: str) -> None:
        self.ui.etiquetaError.setText(mensaje)

    def _ocupado(self, ocupado: bool) -> None:
        """Evita dobles clics mientras se valida contra el servidor."""
        self.ui.botonEntrar.setEnabled(not ocupado)
        self.ui.botonEntrar.setText("Verificando…" if ocupado else "Entrar")
        if ocupado:
            self.ui.etiquetaError.clear()
        QApplication.processEvents()


def pedir_sesion(padre: QWidget | None = None) -> Sesion | None:
    """Muestra el dialogo y devuelve la sesion, o None si se cancelo."""
    dialogo = DialogoLogin(padre)
    if dialogo.exec() == QDialog.DialogCode.Accepted:
        return dialogo.sesion
    return None
