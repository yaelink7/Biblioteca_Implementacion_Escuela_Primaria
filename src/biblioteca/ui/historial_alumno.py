"""Historial de prestamos de un alumno (REQ-PRE-03).

El requisito exige que la informacion se conserve "incluso despues de
concluida la transaccion". Por eso la tabla prestamos usa ON DELETE RESTRICT
y no CASCADE como el esquema original: alli, dar de baja un libro borraba
todo rastro de quien lo habia tenido.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QDialog,
    QHeaderView,
    QMessageBox,
    QWidget,
)

from biblioteca.core.errores import mensaje as mensaje_de_error
from biblioteca.modelos.persona import Alumno
from biblioteca.modelos.prestamo import EstadoPrestamo
from biblioteca.repositorios import prestamos as repo_prestamos
from biblioteca.ui.componentes import CeldaOrdenada
from biblioteca.ui.estilo import ROJO
from biblioteca.ui.formato import fecha_numerica, plural, salon
from biblioteca.ui.generado.ui_historial_alumno import Ui_DialogoHistorial


ALTO_MAXIMO = 340


def _orden(fecha) -> str:
    """Las fechas se ordenan como fechas, no como «dd/mm/aaaa»."""
    return fecha.isoformat() if fecha else ""


class DialogoHistorial(QDialog):
    def __init__(self, padre: QWidget | None, alumno: Alumno) -> None:
        super().__init__(padre)
        self.ui = Ui_DialogoHistorial()
        self.ui.setupUi(self)

        self.alumno = alumno
        self.setWindowTitle(f"Historial · {alumno.nombre_completo}")
        partes = [alumno.nombre_completo, salon(alumno.grado, alumno.grupo)]
        if alumno.codigo:
            partes.append(alumno.codigo)
        self.ui.etiquetaAlumno.setText(" · ".join(partes))

        cabecera = self.ui.tablaHistorial.horizontalHeader()
        cabecera.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        cabecera.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for columna in (1, 2, 3, 4):
            cabecera.setSectionResizeMode(columna, QHeaderView.ResizeMode.ResizeToContents)
        # Lo mas reciente arriba, como lo entrega la base
        cabecera.setSortIndicator(1, Qt.SortOrder.DescendingOrder)

        self.ui.botonCerrar.clicked.connect(self.accept)
        self._cargar()

    def _cargar(self) -> None:
        if not self.alumno.id:
            return

        try:
            movimientos = repo_prestamos.historial_de(self.alumno.id)
        except Exception as error:
            QMessageBox.warning(
                self,
                "No se pudo consultar el historial",
                mensaje_de_error(error),
            )
            return

        tabla = self.ui.tablaHistorial
        tabla.setSortingEnabled(False)
        tabla.setRowCount(len(movimientos))

        for fila, p in enumerate(movimientos):
            celdas = [
                CeldaOrdenada(p.titulo_libro or "—", p.titulo_libro or ""),
                CeldaOrdenada(fecha_numerica(p.fecha_prestamo), _orden(p.fecha_prestamo)),
                CeldaOrdenada(fecha_numerica(p.fecha_limite), _orden(p.fecha_limite)),
                CeldaOrdenada(fecha_numerica(p.fecha_devolucion), _orden(p.fecha_devolucion)),
                CeldaOrdenada(p.resumen, p.dias_restantes),
            ]
            if p.esta_vencido:
                celdas[4].setForeground(QColor(ROJO))
            for columna, celda in enumerate(celdas):
                tabla.setItem(fila, columna, celda)

        tabla.setSortingEnabled(True)
        self.ui.marcoTabla.setVisible(bool(movimientos))
        # La tabla mide lo que sus filas, hasta un tope; despues se desliza
        alto = (tabla.horizontalHeader().sizeHint().height()
                + len(movimientos) * tabla.verticalHeader().defaultSectionSize() + 4)
        tabla.setFixedHeight(min(alto, ALTO_MAXIMO))
        self.adjustSize()
        self._resumir(movimientos)

    def _resumir(self, movimientos: list) -> None:
        if not movimientos:
            self.ui.etiquetaResumen.setText(
                "Este alumno todavía no ha pedido ningún libro."
            )
            return

        devueltos = sum(
            1 for p in movimientos if p.estado == EstadoPrestamo.DEVUELTO
        )
        activos = len(movimientos) - devueltos
        vencidos = sum(1 for p in movimientos if p.esta_vencido)

        partes = [plural(len(movimientos), "préstamo")]
        if devueltos:
            partes.append(plural(devueltos, "devuelto"))
        if activos:
            partes.append(f"{activos} sin devolver")
        if vencidos:
            partes.append(plural(vencidos, "vencido"))

        self.ui.etiquetaResumen.setText(" · ".join(partes))
