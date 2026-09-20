"""Pantalla de prestamos activos y devoluciones.

Cubre REQ-PRE-01, REQ-PRE-02 y REQ-PRE-03. Es el reemplazo directo del
cuaderno: aqui se ve de un vistazo quien tiene cada ejemplar y cuales ya
se pasaron de la fecha.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QHeaderView,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from biblioteca.core.errores import mensaje as mensaje_de_error
from biblioteca.modelos.prestamo import Prestamo
from biblioteca.repositorios import prestamos as repo_prestamos
from biblioteca.ui.estilo import COLOR_ALERTA, COLOR_TENUE
from biblioteca.ui.generado.ui_prestamos import Ui_PantallaPrestamos
from biblioteca.ui.nuevo_prestamo import DialogoNuevoPrestamo


class PantallaPrestamos(QWidget):
    """Lista lo que esta prestado y permite cerrar cada prestamo."""

    def __init__(self, padre: QWidget | None = None) -> None:
        super().__init__(padre)
        self.ui = Ui_PantallaPrestamos()
        self.ui.setupUi(self)

        self._prestamos: list[Prestamo] = []

        self._preparar_tabla()
        self.ui.etiquetaResumen.setStyleSheet(f"color: {COLOR_TENUE};")

        self.ui.campoFiltro.textChanged.connect(self._pintar)
        self.ui.casillaSoloVencidos.toggled.connect(self._pintar)
        self.ui.tablaPrestamos.itemSelectionChanged.connect(self._cambio_seleccion)
        self.ui.botonNuevo.clicked.connect(self._registrar)
        self.ui.botonDevolver.clicked.connect(self._devolver)

        self.recargar()

    def _preparar_tabla(self) -> None:
        cabecera = self.ui.tablaPrestamos.horizontalHeader()
        cabecera.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        cabecera.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        for columna in (2, 3, 4):
            cabecera.setSectionResizeMode(columna, QHeaderView.ResizeMode.ResizeToContents)

    # ------------------------------------------------------------------
    # Datos
    # ------------------------------------------------------------------

    def recargar(self) -> None:
        try:
            self._prestamos = repo_prestamos.activos()
        except Exception as error:
            QMessageBox.warning(
                self,
                "No se pudieron consultar los préstamos",
                mensaje_de_error(error),
            )
            return
        self._pintar()

    def _visibles(self) -> list[Prestamo]:
        """Aplica el filtro de texto y la casilla de vencidos en memoria.

        Son pocos registros y ya estan cargados: filtrar aqui responde al
        instante y evita una consulta por cada tecla.
        """
        filtro = self.ui.campoFiltro.text().strip().lower()
        solo_vencidos = self.ui.casillaSoloVencidos.isChecked()

        resultado = []
        for p in self._prestamos:
            if solo_vencidos and not p.esta_vencido:
                continue
            if filtro:
                texto = f"{p.nombre_alumno or ''} {p.titulo_libro or ''}".lower()
                if filtro not in texto:
                    continue
            resultado.append(p)
        return resultado

    def _pintar(self) -> None:
        visibles = self._visibles()
        tabla = self.ui.tablaPrestamos
        tabla.setSortingEnabled(False)
        tabla.setRowCount(len(visibles))

        for fila, prestamo in enumerate(visibles):
            celdas = [
                prestamo.nombre_alumno or "—",
                prestamo.titulo_libro or "—",
                prestamo.fecha_prestamo.strftime("%d/%m/%Y") if prestamo.fecha_prestamo else "—",
                prestamo.fecha_limite.strftime("%d/%m/%Y") if prestamo.fecha_limite else "—",
                prestamo.resumen,
            ]
            for columna, texto in enumerate(celdas):
                celda = QTableWidgetItem(texto)
                if columna in (2, 3, 4):
                    celda.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if columna == 0:
                    celda.setData(Qt.ItemDataRole.UserRole, prestamo)
                if columna == 4 and prestamo.esta_vencido:
                    celda.setForeground(Qt.GlobalColor.darkRed)
                tabla.setItem(fila, columna, celda)

        tabla.setSortingEnabled(True)
        self._actualizar_resumen()
        self._cambio_seleccion()

    def _actualizar_resumen(self) -> None:
        total = len(self._prestamos)
        vencidos = sum(1 for p in self._prestamos if p.esta_vencido)

        if total == 0:
            texto = "No hay préstamos activos."
        elif vencidos:
            texto = (
                f"{total} préstamo{'s' if total != 1 else ''} activo"
                f"{'s' if total != 1 else ''} · "
                f"{vencidos} vencido{'s' if vencidos != 1 else ''}"
            )
        else:
            texto = (
                f"{total} préstamo{'s' if total != 1 else ''} activo"
                f"{'s' if total != 1 else ''} · ninguno vencido"
            )
        self.ui.etiquetaResumen.setText(texto)

    # ------------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------------

    def _seleccionado(self) -> Prestamo | None:
        filas = self.ui.tablaPrestamos.selectionModel().selectedRows()
        if not filas:
            return None
        celda = self.ui.tablaPrestamos.item(filas[0].row(), 0)
        return celda.data(Qt.ItemDataRole.UserRole) if celda else None

    def _cambio_seleccion(self) -> None:
        self.ui.botonDevolver.setEnabled(self._seleccionado() is not None)

    def _registrar(self) -> None:
        dialogo = DialogoNuevoPrestamo(self)
        if dialogo.exec() and dialogo.registrado:
            self.recargar()
            self._avisar(
                f"{dialogo.alumno.nombre_completo} se llevó «{dialogo.libro.titulo}»."
            )

    def _devolver(self) -> None:
        prestamo = self._seleccionado()
        if prestamo is None or prestamo.id is None:
            return

        confirmar = QMessageBox.question(
            self,
            "Registrar devolución",
            f"¿{prestamo.nombre_alumno} devolvió «{prestamo.titulo_libro}»?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirmar != QMessageBox.StandardButton.Yes:
            return

        try:
            repo_prestamos.devolver(prestamo.id)
        except repo_prestamos.ErrorDePrestamo as error:
            QMessageBox.warning(self, "No se pudo registrar la devolución", str(error))
            return

        self.recargar()
        self._avisar(f"«{prestamo.titulo_libro}» volvió al acervo.")

    def _avisar(self, mensaje: str) -> None:
        self.ui.etiquetaResumen.setText(mensaje)
        self.ui.etiquetaResumen.setStyleSheet(f"color: {COLOR_ALERTA}; font-weight: 600;")
        QTimer.singleShot(
            3000,
            lambda: (
                self.ui.etiquetaResumen.setStyleSheet(f"color: {COLOR_TENUE};"),
                self._actualizar_resumen(),
            ),
        )
