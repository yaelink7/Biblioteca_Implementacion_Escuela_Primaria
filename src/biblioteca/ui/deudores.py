"""Reporte de alumnos deudores.

Responde al problema que la propia escuela describio en la entrevista:
generar esta informacion dependia de "una revision manual y exhaustiva del
cuaderno", tiempo que el docente comisionado no siempre tiene.

Todo el calculo lo hace Postgres en la vista v_deudores; esta pantalla solo
lo muestra. Por eso abre ya con el reporte hecho, sin pedir un clic extra.
En el diseno «Lapiz» el reporte es una hoja con su franja mostaza: la cifra
grande, el mas atrasado y la tabla.
"""

from __future__ import annotations

from datetime import datetime
from html import escape

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QHeaderView,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from biblioteca.core.errores import mensaje as mensaje_de_error
from biblioteca.repositorios import prestamos as repo_prestamos
from biblioteca.repositorios.prestamos import Deudor
from biblioteca.ui.apariencia import icono
from biblioteca.ui.componentes import CeldaOrdenada, fuente_mono, poner_icono
from biblioteca.ui.estilo import ROJO, TEXTO, VERDE, repulir, rotular, rotular_encabezados
from biblioteca.ui.formato import fecha_numerica, plural, salon
from biblioteca.ui.generado.ui_deudores import Ui_PantallaDeudores

TODOS_LOS_SALONES = "Todos"

# A partir de dos semanas de retraso la recuperacion se vuelve dificil:
# se marca distinto para que el docente sepa a quien buscar primero.
DIAS_CRITICOS = 14

# Mas alto que esto, la tabla se desliza en vez de crecer
ALTO_MAXIMO_TABLA = 520


class CeldaDeRetraso(CeldaOrdenada):
    """Muestra "12 días" pero ordena por el numero.

    Con el orden alfabetico que trae la tabla por omision, "9 días" quedaria
    despues de "11 días", que es justo lo contrario de lo que necesita quien
    revisa el reporte.
    """

    def __init__(self, texto: str, dias: int) -> None:
        super().__init__(texto, dias)
        self.dias = dias


class PantallaDeudores(QWidget):
    """Quien no ha devuelto, desde cuando, y como localizar a su tutor."""

    # El numero de la columna de iconos: las filas de v_deudores
    total_cambio = Signal(int)

    def __init__(self, padre: QWidget | None = None) -> None:
        super().__init__(padre)
        self.ui = Ui_PantallaDeudores()
        self.ui.setupUi(self)

        self._deudores: list[Deudor] = []

        self._preparar_aspecto()
        self._preparar_tabla()

        self.ui.botonActualizar.clicked.connect(self.recargar)
        self.ui.campoSalon.currentTextChanged.connect(self._pintar)

        self.recargar()

    @property
    def total(self) -> int:
        """Cuantos prestamos vencidos hay, sin filtro de salon."""
        return len(self._deudores)

    def _preparar_aspecto(self) -> None:
        ui = self.ui
        poner_icono(ui.botonActualizar, "actualizar", TEXTO)
        ui.etiquetaCriterio.setText(f"En rojo, {DIAS_CRITICOS} días o más")
        rotular_encabezados(ui.tablaDeudores)
        rotular(ui.etiquetaCriterio, mayusculas=False, espaciado=0.3)
        ui.tablaDeudores.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        ui.iconoTotal.setPixmap(icono("listo", VERDE, 26).pixmap(26, 26))

    def _preparar_tabla(self) -> None:
        cabecera = self.ui.tablaDeudores.horizontalHeader()
        cabecera.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        cabecera.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        for columna in (1, 3, 4, 5):
            cabecera.setSectionResizeMode(columna, QHeaderView.ResizeMode.ResizeToContents)
        # El mas atrasado arriba, como lo entrega la base
        cabecera.setSortIndicator(4, Qt.SortOrder.DescendingOrder)

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
                mensaje_de_error(error),
            )
            return

        self._llenar_salones()
        self.ui.etiquetaGenerado.setText(
            f"Generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}"
        )
        self._pintar()
        self.total_cambio.emit(self.total)

    @staticmethod
    def _salon(deudor: Deudor) -> str:
        return salon(deudor.grado, deudor.grupo)

    def _llenar_salones(self) -> None:
        """Solo ofrece los salones que realmente tienen deudores."""
        salones = sorted({self._salon(d) for d in self._deudores if d.grado and d.grupo})
        actual = self.ui.campoSalon.currentText()

        self.ui.campoSalon.blockSignals(True)
        self.ui.campoSalon.clear()
        self.ui.campoSalon.addItem(TODOS_LOS_SALONES)
        self.ui.campoSalon.addItems(salones)
        if actual in [TODOS_LOS_SALONES, *salones]:
            self.ui.campoSalon.setCurrentText(actual)
        self.ui.campoSalon.blockSignals(False)

    def _visibles(self) -> list[Deudor]:
        elegido = self.ui.campoSalon.currentText()
        if not elegido or elegido == TODOS_LOS_SALONES:
            return self._deudores
        return [d for d in self._deudores if self._salon(d) == elegido]

    def _pintar(self) -> None:
        visibles = self._visibles()
        tabla = self.ui.tablaDeudores
        tabla.setSortingEnabled(False)
        tabla.setRowCount(len(visibles))

        negrita = QFont(tabla.font())
        negrita.setWeight(QFont.Weight.DemiBold)
        mono = fuente_mono(tabla.font())
        mono_negrita = QFont(mono)
        mono_negrita.setWeight(QFont.Weight.Bold)

        for fila, deudor in enumerate(visibles):
            critico = deudor.dias_de_retraso >= DIAS_CRITICOS
            celdas = [
                QTableWidgetItem(deudor.alumno),
                QTableWidgetItem(self._salon(deudor)),
                QTableWidgetItem(deudor.libro),
                CeldaOrdenada(fecha_numerica(deudor.fecha_limite),
                              deudor.fecha_limite.isoformat() if deudor.fecha_limite else ""),
                CeldaDeRetraso(deudor.retraso, deudor.dias_de_retraso),
                # El correo ya no es contacto del tutor: la escuela confirmo
                # que no funciona (USU-08). Queda el telefono.
                QTableWidgetItem(deudor.telefono or "Sin contacto registrado"),
            ]
            celdas[0].setFont(negrita)
            for celda in (celdas[1], celdas[3]):
                celda.setFont(mono)
            celdas[4].setFont(mono_negrita)
            if critico:
                celdas[4].setForeground(QColor(ROJO))
            if deudor.telefono:
                celdas[5].setFont(mono)
            else:
                celdas[5].setForeground(QColor(ROJO))
            for columna, celda in enumerate(celdas):
                tabla.setItem(fila, columna, celda)

        tabla.setSortingEnabled(True)
        self._ajustar_alto(len(visibles))
        self._actualizar_totales(visibles)

    def _ajustar_alto(self, filas: int) -> None:
        """La hoja mide lo que su contenido, como un reporte impreso."""
        tabla = self.ui.tablaDeudores
        tabla.setVisible(filas > 0)
        alto = (tabla.horizontalHeader().sizeHint().height()
                + filas * tabla.verticalHeader().defaultSectionSize() + 4)
        tabla.setFixedHeight(min(alto, ALTO_MAXIMO_TABLA))

    def _actualizar_totales(self, visibles: list[Deudor]) -> None:
        ui = self.ui
        total = len(visibles)
        ui.iconoTotal.setVisible(total == 0)

        if total == 0:
            ui.etiquetaTotal.setText("")
            ui.etiquetaTotal.hide()
            ui.etiquetaTotalTexto.setText("Sin deudores")
            ui.etiquetaMasAtrasado.setText("Todos los préstamos están dentro de su plazo.")
            return

        criticos = sum(1 for d in visibles if d.dias_de_retraso >= DIAS_CRITICOS)
        ui.etiquetaTotal.show()
        ui.etiquetaTotal.setText(str(total))
        ui.etiquetaTotal.setProperty("alerta", criticos > 0)
        repulir(ui.etiquetaTotal)
        ui.etiquetaTotalTexto.setText(
            "alumno con adeudo" if total == 1 else "alumnos con adeudo")

        peor = max(visibles, key=lambda d: d.dias_de_retraso)
        detalle = (f"El más atrasado: <b style='color:{TEXTO}'>"
                   f"{escape(peor.alumno, quote=False)}, {peor.retraso}</b>")
        if criticos:
            detalle += f" · {criticos} con más de {DIAS_CRITICOS} días"
        ui.etiquetaMasAtrasado.setText(detalle)
