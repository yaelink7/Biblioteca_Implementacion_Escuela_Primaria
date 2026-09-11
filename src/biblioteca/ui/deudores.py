"""Reporte de alumnos deudores.

Responde al problema que la propia escuela describio en la entrevista:
generar esta informacion dependia de "una revision manual y exhaustiva del
cuaderno", tiempo que el docente comisionado no siempre tiene.

Todo el calculo lo hace Postgres en la vista v_deudores; esta pantalla solo
lo muestra. Por eso abre ya con el reporte hecho, sin pedir un clic extra.
"""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHeaderView,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from biblioteca.repositorios.prestamos import Deudor
from biblioteca.repositorios import prestamos as repo_prestamos
from biblioteca.ui.estilo import COLOR_ERROR, COLOR_OK, COLOR_PRINCIPAL, COLOR_TENUE
from biblioteca.ui.generado.ui_deudores import Ui_PantallaDeudores

TODOS_LOS_SALONES = "Todos"

# A partir de dos semanas de retraso la recuperacion se vuelve dificil:
# se marca distinto para que el docente sepa a quien buscar primero.
DIAS_CRITICOS = 14


class CeldaDeRetraso(QTableWidgetItem):
    """Muestra "12 días" pero ordena por el numero.

    Con el orden alfabetico que trae la tabla por omision, "9 días" quedaria
    despues de "11 días", que es justo lo contrario de lo que necesita quien
    revisa el reporte.
    """

    def __init__(self, texto: str, dias: int) -> None:
        super().__init__(texto)
        self.dias = dias

    def __lt__(self, otra: QTableWidgetItem) -> bool:
        if isinstance(otra, CeldaDeRetraso):
            return self.dias < otra.dias
        return super().__lt__(otra)


class PantallaDeudores(QWidget):
    """Quien no ha devuelto, desde cuando, y como localizar a su tutor."""

    def __init__(self, padre: QWidget | None = None) -> None:
        super().__init__(padre)
        self.ui = Ui_PantallaDeudores()
        self.ui.setupUi(self)

        self._deudores: list[Deudor] = []

        self._preparar_tabla()
        self._preparar_estilos()

        self.ui.botonActualizar.clicked.connect(self.recargar)
        self.ui.campoSalon.currentTextChanged.connect(self._pintar)

        self.recargar()

    def _preparar_tabla(self) -> None:
        cabecera = self.ui.tablaDeudores.horizontalHeader()
        cabecera.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        cabecera.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        for columna in (1, 3, 4):
            cabecera.setSectionResizeMode(columna, QHeaderView.ResizeMode.ResizeToContents)

    def _preparar_estilos(self) -> None:
        grande = QFont()
        grande.setPointSize(17)
        grande.setBold(True)
        self.ui.etiquetaTotal.setFont(grande)

        self.ui.etiquetaMasAtrasado.setStyleSheet(f"color: {COLOR_TENUE};")
        self.ui.etiquetaGenerado.setStyleSheet(f"color: {COLOR_TENUE};")
        self.ui.etiquetaNota.setStyleSheet(f"color: {COLOR_TENUE};")

    # ------------------------------------------------------------------
    # Datos
    # ------------------------------------------------------------------

    def recargar(self) -> None:
        """Una sola consulta a la vista y el reporte esta listo."""
        try:
            self._deudores = repo_prestamos.deudores()
        except Exception as error:
            QMessageBox.warning(
                self,
                "No se pudo generar el reporte",
                f"Revisa tu conexión a internet.\n\n{error}",
            )
            return

        self._llenar_salones()
        self.ui.etiquetaGenerado.setText(
            f"Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}"
        )
        self._pintar()

    def _llenar_salones(self) -> None:
        """Solo ofrece los salones que realmente tienen deudores."""
        salones = sorted({d.salon for d in self._deudores if d.salon != "-"})
        actual = self.ui.campoSalon.currentText()

        self.ui.campoSalon.blockSignals(True)
        self.ui.campoSalon.clear()
        self.ui.campoSalon.addItem(TODOS_LOS_SALONES)
        self.ui.campoSalon.addItems(salones)
        if actual in [TODOS_LOS_SALONES, *salones]:
            self.ui.campoSalon.setCurrentText(actual)
        self.ui.campoSalon.blockSignals(False)

    def _visibles(self) -> list[Deudor]:
        salon = self.ui.campoSalon.currentText()
        if not salon or salon == TODOS_LOS_SALONES:
            return self._deudores
        return [d for d in self._deudores if d.salon == salon]

    def _pintar(self) -> None:
        visibles = self._visibles()
        tabla = self.ui.tablaDeudores
        tabla.setSortingEnabled(False)
        tabla.setRowCount(len(visibles))

        for fila, deudor in enumerate(visibles):
            celdas = [
                deudor.alumno,
                deudor.salon,
                deudor.libro,
                deudor.fecha_limite.strftime("%d/%m/%Y") if deudor.fecha_limite else "—",
                deudor.retraso,
                deudor.correo or deudor.telefono or "Sin contacto registrado",
            ]
            for columna, texto in enumerate(celdas):
                if columna == 4:
                    celda = CeldaDeRetraso(texto, deudor.dias_de_retraso)
                    celda.setForeground(
                        Qt.GlobalColor.darkRed
                        if deudor.dias_de_retraso >= DIAS_CRITICOS
                        else Qt.GlobalColor.darkYellow
                    )
                else:
                    celda = QTableWidgetItem(texto)

                if columna in (1, 3, 4):
                    celda.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                tabla.setItem(fila, columna, celda)

        tabla.setSortingEnabled(True)
        self._actualizar_totales(visibles)

    def _actualizar_totales(self, visibles: list[Deudor]) -> None:
        total = len(visibles)

        if total == 0:
            self.ui.etiquetaTotal.setText("Sin deudores")
            self.ui.etiquetaTotal.setStyleSheet(f"color: {COLOR_OK};")
            self.ui.etiquetaMasAtrasado.setText(
                "Todos los préstamos están dentro de su plazo."
            )
            return

        self.ui.etiquetaTotal.setText(
            f"{total} alumno{'s' if total != 1 else ''} con adeudo"
        )
        criticos = sum(1 for d in visibles if d.dias_de_retraso >= DIAS_CRITICOS)
        color = COLOR_ERROR if criticos else COLOR_PRINCIPAL
        self.ui.etiquetaTotal.setStyleSheet(f"color: {color};")

        peor = max(visibles, key=lambda d: d.dias_de_retraso)
        detalle = f"El más atrasado: {peor.alumno}, {peor.retraso}"
        if criticos:
            detalle += (
                f"   ·   {criticos} con más de {DIAS_CRITICOS} días"
            )
        self.ui.etiquetaMasAtrasado.setText(detalle)
