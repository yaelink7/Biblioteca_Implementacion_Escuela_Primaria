"""Piezas de interfaz que comparten las pantallas del diseno «Lapiz».

Las dos se dibujan a mano porque la hoja de estilo de Qt no alcanza: la
pastilla mostaza abraza solo al icono y no al boton entero, y la raya de la
fila elegida va solo en la primera columna.
"""

from __future__ import annotations

from PySide6.QtCore import QRect, QRectF, QSize, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QAbstractButton, QStyle, QStyledItemDelegate, QWidget

from biblioteca.ui.apariencia import icono
from biblioteca.ui.estilo import MOSTAZA, TEXTO, TEXTO_RIEL

BLANCO = "#FFFFFF"
# Lo que se suma a los cuatro pixeles que Qt deja entre icono y texto
AIRE_DEL_ICONO = 4


def poner_icono(boton: QAbstractButton, nombre: str, color: str, tamano: int = 18) -> None:
    """Icono a la izquierda del texto, con el aire del prototipo entre los dos."""
    boton.setIcon(icono(nombre, color, tamano, AIRE_DEL_ICONO))
    boton.setIconSize(QSize(tamano + AIRE_DEL_ICONO, tamano))


class BotonRiel(QAbstractButton):
    """Una seccion de la columna de iconos: el icono en su pastilla y el nombre debajo."""

    def __init__(self, texto: str, nombre_icono: str, padre: QWidget | None = None) -> None:
        super().__init__(padre)
        self.setText(texto)
        self.setCheckable(True)
        self.setToolTip(texto)
        self.setAccessibleName(texto)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        # Solo el tabulador le da el foco: asi el anillo blanco aparece al
        # navegar con teclado y no despues de cada clic.
        self.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.setFixedHeight(64)
        self._icono = nombre_icono
        self._encima = False

    def sizeHint(self) -> QSize:  # noqa: N802 (lo nombra Qt)
        return QSize(80, 64)

    def enterEvent(self, evento) -> None:  # noqa: N802
        self._encima = True
        self.update()
        super().enterEvent(evento)

    def leaveEvent(self, evento) -> None:  # noqa: N802
        self._encima = False
        self.update()
        super().leaveEvent(evento)

    def paintEvent(self, evento) -> None:  # noqa: N802
        activo = self.isChecked()
        pintor = QPainter(self)
        pintor.setRenderHint(QPainter.RenderHint.Antialiasing)
        pintor.setPen(Qt.PenStyle.NoPen)

        if self._encima and not activo:
            pintor.setBrush(QColor(255, 255, 255, 16))
            pintor.drawRoundedRect(QRectF(self.rect()).adjusted(6, 0, -6, 0), 12, 12)

        pastilla = QRectF((self.width() - 48) / 2, 6, 48, 32)
        if activo:
            pintor.setBrush(QColor(MOSTAZA))
            pintor.drawRoundedRect(pastilla, 16, 16)
            color_icono = TEXTO
        else:
            color_icono = BLANCO if self._encima else TEXTO_RIEL
        icono(self._icono, color_icono, 20).paint(pintor, pastilla.toRect())

        fuente = QFont(self.font())
        fuente.setPixelSize(12)
        fuente.setWeight(QFont.Weight.ExtraBold if activo else QFont.Weight.DemiBold)
        pintor.setFont(fuente)
        pintor.setPen(QColor(BLANCO if activo or self._encima else TEXTO_RIEL))
        pintor.drawText(QRectF(0, 42, self.width(), 20),
                        Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, self.text())

        if self.hasFocus():
            pintor.setPen(QPen(QColor(BLANCO), 2))
            pintor.setBrush(Qt.BrushStyle.NoBrush)
            pintor.drawRoundedRect(QRectF(self.rect()).adjusted(5, 1, -5, -1), 12, 12)
        pintor.end()


class DelegadoFilaElegida(QStyledItemDelegate):
    """Raya mostaza a la izquierda de la fila elegida, como el canto de una ficha."""

    def paint(self, pintor: QPainter, opcion, indice) -> None:
        super().paint(pintor, opcion, indice)
        elegida = bool(opcion.state & QStyle.StateFlag.State_Selected)
        if indice.column() == 0 and elegida:
            caja = opcion.rect
            pintor.fillRect(QRect(caja.left(), caja.top(), 3, caja.height()), QColor(MOSTAZA))
