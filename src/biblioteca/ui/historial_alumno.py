"""Historial de prestamos de un alumno (REQ-PRE-03).

El requisito exige que la informacion se conserve "incluso despues de
concluida la transaccion". Por eso la tabla prestamos usa ON DELETE RESTRICT
y no CASCADE como el esquema original: alli, dar de baja un libro borraba
todo rastro de quien lo habia tenido.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QDialog,
    QHeaderView,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from biblioteca.core.errores import mensaje as mensaje_de_error
from biblioteca.modelos.persona import Alumno
from biblioteca.modelos.prestamo import EstadoPrestamo
from biblioteca.repositorios import prestamos as repo_prestamos
from biblioteca.ui.estilo import COLOR_PRINCIPAL, COLOR_TENUE
from biblioteca.ui.generado.ui_historial_alumno import Ui_DialogoHistorial


class DialogoHistorial(QDialog):
    def __init__(self, padre: QWidget | None, alumno: Alumno) -> None:
        super().__init__(padre)
        self.ui = Ui_DialogoHistorial()
        self.ui.setupUi(self)

        self.alumno = alumno
        self.setWindowTitle(f"Historial · {alumno.nombre_completo}")

        titulo = QFont()
        titulo.setPointSize(14)
        titulo.setBold(True)
        self.ui.etiquetaAlumno.setFont(titulo)
        self.ui.etiquetaAlumno.setStyleSheet(f"color: {COLOR_PRINCIPAL};")
        self.ui.etiquetaAlumno.setText(
            f"{alumno.nombre_completo}  ·  {alumno.salon}  ·  {alumno.codigo}"
        )
        self.ui.etiquetaResumen.setStyleSheet(f"color: {COLOR_TENUE};")
        self.ui.etiquetaNota.setStyleSheet(f"color: {COLOR_TENUE};")

        cabecera = self.ui.tablaHistorial.horizontalHeader()
        cabecera.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

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
                p.titulo_libro or "—",
                p.fecha_prestamo.strftime("%d/%m/%Y") if p.fecha_prestamo else "—",
                p.fecha_limite.strftime("%d/%m/%Y") if p.fecha_limite else "—",
                p.fecha_devolucion.strftime("%d/%m/%Y") if p.fecha_devolucion else "—",
                p.resumen,
            ]
            for columna, texto in enumerate(celdas):
                celda = QTableWidgetItem(texto)
                if columna:
                    celda.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if columna == 4 and p.esta_vencido:
                    celda.setForeground(Qt.GlobalColor.darkRed)
                tabla.setItem(fila, columna, celda)

        tabla.setSortingEnabled(True)
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

        partes = [f"{len(movimientos)} préstamo{'s' if len(movimientos) != 1 else ''}"]
        if devueltos:
            partes.append(f"{devueltos} devuelto{'s' if devueltos != 1 else ''}")
        if activos:
            partes.append(f"{activos} sin devolver")
        if vencidos:
            partes.append(f"{vencidos} vencido{'s' if vencidos != 1 else ''}")

        self.ui.etiquetaResumen.setText("   ·   ".join(partes))
