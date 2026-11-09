"""Piezas de interfaz que comparten las pantallas del diseno «Lapiz».

Varias se dibujan a mano porque la hoja de estilo de Qt no alcanza: la
pastilla mostaza abraza solo al icono y no al boton entero, la raya de la
fila elegida va solo en la primera columna, y un boton de Qt no puede llevar
dos letras distintas, como la palabra y el numero de una subpestaña.
"""

from __future__ import annotations

from PySide6.QtCore import QModelIndex, QPointF, QRect, QRectF, QSize, Qt
from PySide6.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen
from PySide6.QtWidgets import (
    QAbstractButton,
    QLabel,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QTableWidgetItem,
    QWidget,
)

from biblioteca.ui.apariencia import FAMILIA_MONO, icono
from biblioteca.ui.estilo import (
    GRIS,
    MOSTAZA,
    MOSTAZA_MEDIO,
    MOSTAZA_SUAVE,
    MOSTAZA_TEXTO,
    ROJO,
    ROJO_OSCURO,
    SUPERFICIE,
    TENUE,
    TEXTO,
    TEXTO_RIEL,
    repulir,
)

BLANCO = "#FFFFFF"
GRAFITO_INSIGNIA = "#26282C"
# Lo que se suma a los cuatro pixeles que Qt deja entre icono y texto
AIRE_DEL_ICONO = 4

# Lo que el delegado de opciones lee de cada renglon de la lista
DETALLE = Qt.ItemDataRole.UserRole + 1
NOTA = Qt.ItemDataRole.UserRole + 2
COLOR_NOTA = Qt.ItemDataRole.UserRole + 3


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
        self.insignia = 0

    def poner_insignia(self, cantidad: int) -> None:
        """El numero sobre el icono, como el de Deudores; cero lo quita."""
        self.insignia = max(0, cantidad)
        nombre = self.text() if not self.insignia else f"{self.text()}, {self.insignia}"
        self.setAccessibleName(nombre)
        self.update()

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

        if self.insignia:
            # Pastilla blanca con el numero en grafito, en la esquina de la
            # del icono: se lee igual sobre el grafito y sobre el mostaza.
            cifra = QFont(self.font())
            cifra.setPixelSize(11)
            cifra.setWeight(QFont.Weight.ExtraBold)
            texto = str(self.insignia) if self.insignia < 100 else "99+"
            ancho = max(18.0, QFontMetrics(cifra).horizontalAdvance(texto) + 10.0)
            caja = QRectF(pastilla.right() - 2 - ancho, pastilla.top() - 2, ancho, 18)
            pintor.setBrush(QColor(BLANCO))
            pintor.drawRoundedRect(caja, 9, 9)
            pintor.setFont(cifra)
            pintor.setPen(QColor(GRAFITO_INSIGNIA))
            pintor.drawText(caja, Qt.AlignmentFlag.AlignCenter, texto)
            pintor.setPen(Qt.PenStyle.NoPen)

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


class PestanaVista(QAbstractButton):
    """Una subpestaña de la barra de la tabla: la palabra y, al lado, su numero.

    El numero va en la letra de maquina y en gris; si `alerta` y hay alguno,
    en rojo, como los vencidos. La elegida lleva la raya mostaza debajo.
    """

    def __init__(self, texto: str, alerta: bool = False, padre: QWidget | None = None) -> None:
        super().__init__(padre)
        self.setText(texto)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.alerta = alerta
        self.cantidad = 0
        self._encima = False
        self.setAccessibleName(texto)

    def poner_cantidad(self, cantidad: int) -> None:
        self.cantidad = cantidad
        self.setAccessibleName(f"{self.text()}, {cantidad}")
        self.updateGeometry()
        self.update()

    def _fuentes(self) -> tuple[QFont, QFont]:
        palabra = QFont(self.font())
        palabra.setPixelSize(15)
        palabra.setWeight(QFont.Weight.ExtraBold if self.isChecked() else QFont.Weight.DemiBold)
        numero = QFont(FAMILIA_MONO)
        numero.setPixelSize(13)
        numero.setWeight(QFont.Weight.DemiBold)
        return palabra, numero

    def sizeHint(self) -> QSize:  # noqa: N802 (lo nombra Qt)
        palabra, numero = self._fuentes()
        # Se mide con la palabra en negrita: asi el ancho no salta al elegirla
        negrita = QFont(palabra)
        negrita.setWeight(QFont.Weight.ExtraBold)
        ancho = (QFontMetrics(negrita).horizontalAdvance(self.text()) + 6
                 + QFontMetrics(numero).horizontalAdvance(str(self.cantidad)) + 24)
        return QSize(ancho, 52)

    def enterEvent(self, evento) -> None:  # noqa: N802
        self._encima = True
        self.update()
        super().enterEvent(evento)

    def leaveEvent(self, evento) -> None:  # noqa: N802
        self._encima = False
        self.update()
        super().leaveEvent(evento)

    def paintEvent(self, evento) -> None:  # noqa: N802
        palabra, numero = self._fuentes()
        pintor = QPainter(self)
        pintor.setRenderHint(QPainter.RenderHint.Antialiasing)
        activa = self.isChecked()

        pintor.setFont(palabra)
        pintor.setPen(QColor(TEXTO if activa or self._encima else GRIS))
        ancho_palabra = QFontMetrics(palabra).horizontalAdvance(self.text())
        caja = QRectF(12, 0, ancho_palabra, self.height() - 3)
        pintor.drawText(caja, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                        self.text())

        pintor.setFont(numero)
        rojo = self.alerta and self.cantidad > 0
        pintor.setPen(QColor(ROJO if rojo else TENUE))
        pintor.drawText(QRectF(caja.right() + 6, 0, self.width(), self.height() - 3),
                        Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                        str(self.cantidad))

        if activa:
            pintor.fillRect(QRectF(0, self.height() - 3, self.width(), 3), QColor(MOSTAZA))
        if self.hasFocus():
            pintor.setPen(QPen(QColor(MOSTAZA_TEXTO), 2))
            pintor.setBrush(Qt.BrushStyle.NoBrush)
            pintor.drawRoundedRect(QRectF(self.rect()).adjusted(2, 6, -2, -6), 6, 6)
        pintor.end()


class CeldaOrdenada(QTableWidgetItem):
    """Muestra un texto pero ordena por otro valor.

    Con el orden alfabetico que trae la tabla, «9 nov» quedaria despues de
    «10 nov» y «Vence hoy» antes que «Vencido»: se ordena por la fecha o por
    los dias, que es lo que la persona espera.
    """

    def __init__(self, texto: str, clave) -> None:
        super().__init__(texto)
        self.clave = clave

    def __lt__(self, otra: QTableWidgetItem) -> bool:
        if isinstance(otra, CeldaOrdenada):
            return self.clave < otra.clave
        return super().__lt__(otra)


class DelegadoOpcion(QStyledItemDelegate):
    """Un renglon de dos lineas en las listas del dialogo de prestamo.

    Arriba el nombre o el titulo, en negrita; abajo el detalle en gris y, si
    hay, una nota en su color: «tiene “El principito”» en ambar, «Sin
    ejemplares» en rojo. El elegido se pinta como una ficha mostaza.
    """

    ALTO = 62

    def sizeHint(self, opcion: QStyleOptionViewItem, indice: QModelIndex) -> QSize:  # noqa: N802
        return QSize(opcion.rect.width(), self.ALTO)

    def paint(self, pintor: QPainter, opcion: QStyleOptionViewItem, indice: QModelIndex) -> None:
        pintor.save()
        pintor.setRenderHint(QPainter.RenderHint.Antialiasing)
        caja = QRectF(opcion.rect).adjusted(4, 2, -4, -2)
        elegida = bool(opcion.state & QStyle.StateFlag.State_Selected)
        encima = bool(opcion.state & QStyle.StateFlag.State_MouseOver)
        if elegida:
            pintor.setPen(QPen(QColor(MOSTAZA_MEDIO), 1))
            pintor.setBrush(QColor(MOSTAZA_SUAVE))
            pintor.drawRoundedRect(caja, 10, 10)
        elif encima:
            pintor.setPen(Qt.PenStyle.NoPen)
            pintor.setBrush(QColor(SUPERFICIE))
            pintor.drawRoundedRect(caja, 10, 10)

        texto = caja.adjusted(12, 9, -12, -9)
        principal = QFont(opcion.font)
        principal.setPixelSize(15)
        principal.setWeight(QFont.Weight.Bold)
        pintor.setFont(principal)
        pintor.setPen(QColor(TEXTO))
        metrica = QFontMetrics(principal)
        pintor.drawText(texto, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
                        metrica.elidedText(indice.data() or "", Qt.TextElideMode.ElideRight,
                                           int(texto.width())))

        detalle = QFont(opcion.font)
        detalle.setPixelSize(13)
        pintor.setFont(detalle)
        pintor.setPen(QColor(TENUE))
        linea = indice.data(DETALLE) or ""
        abajo = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom
        pintor.drawText(texto, abajo, linea)
        nota = indice.data(NOTA)
        if nota:
            # Se mide con la letra que de verdad pinta: QFontMetrics de la
            # fuente suelta redondea distinto y la nota se encimaba al punto.
            avance = pintor.fontMetrics().horizontalAdvance(linea)
            color = indice.data(COLOR_NOTA) or MOSTAZA_TEXTO
            nota_fuente = QFont(detalle)
            if color != TENUE:
                nota_fuente.setWeight(QFont.Weight.DemiBold)
            pintor.setFont(nota_fuente)
            pintor.setPen(QColor(color))
            resto = texto.adjusted(avance, 0, 0, 0)
            pintor.drawText(resto, abajo, pintor.fontMetrics().elidedText(
                nota, Qt.TextElideMode.ElideRight, int(resto.width())))
        pintor.restore()


def mostrar_caja(caja: QWidget, icono_caja: QLabel, titulo: QLabel, texto: QLabel,
                 nombre_icono: str, encabezado: str, detalle: str, rojo: bool = False) -> None:
    """Llena la caja de situacion de un panel: gris para avisar, roja si urge."""
    icono_caja.setPixmap(icono(nombre_icono, ROJO_OSCURO if rojo else TEXTO, 18).pixmap(18, 18))
    titulo.setText(encabezado)
    texto.setText(detalle)
    for widget in (caja, titulo, texto):
        widget.setProperty("tono", "rojo" if rojo else "gris")
        repulir(widget)


def fuente_mono(base: QFont, tamano: int = 13) -> QFont:
    """La letra de maquina para codigos, salones, fechas y telefonos."""
    fuente = QFont(base)
    fuente.setFamily(FAMILIA_MONO)
    fuente.setPixelSize(tamano)
    return fuente
