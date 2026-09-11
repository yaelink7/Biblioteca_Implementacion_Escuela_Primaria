"""Plantilla de la biblioteca (REQ-EMP-01).

Sustituye a las ventanas de empleados del sistema Java. El requisito pide
que el alta de personal quede "restringida a personal con permisos
administrativos"; esa restriccion la aplican las politicas RLS de Postgres,
y aqui se anticipa para explicar por que el boton esta apagado en lugar de
dejar que el usuario llene un formulario que va a ser rechazado.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QHeaderView,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from biblioteca.core.sesion import sesion_actual
from biblioteca.modelos.persona import Empleado, Rol
from biblioteca.repositorios import personas as repo_personas
from biblioteca.ui.estilo import COLOR_ALERTA, COLOR_PRINCIPAL, COLOR_TENUE
from biblioteca.ui.formulario_empleado import FormularioEmpleado
from biblioteca.ui.generado.ui_empleados import Ui_PantallaEmpleados


class PantallaEmpleados(QWidget):
    def __init__(self, padre: QWidget | None = None) -> None:
        super().__init__(padre)
        self.ui = Ui_PantallaEmpleados()
        self.ui.setupUi(self)

        self._empleados: list[Empleado] = []
        self._es_administrador = sesion_actual().perfil.rol == Rol.ADMINISTRADOR

        self._preparar_tabla()
        self._preparar_permisos()

        self.ui.tablaEmpleados.itemSelectionChanged.connect(self._cambio_seleccion)
        self.ui.botonNuevo.clicked.connect(self._registrar)
        self.ui.botonEditar.clicked.connect(self._modificar)

        self.recargar()

    def _preparar_tabla(self) -> None:
        cabecera = self.ui.tablaEmpleados.horizontalHeader()
        for columna in (1, 3):
            cabecera.setSectionResizeMode(columna, QHeaderView.ResizeMode.Stretch)
        for columna in (0, 2, 4):
            cabecera.setSectionResizeMode(columna, QHeaderView.ResizeMode.ResizeToContents)
        self.ui.etiquetaResumen.setStyleSheet(f"color: {COLOR_TENUE};")

    def _preparar_permisos(self) -> None:
        """Dice de entrada quien puede dar de alta, en vez de fallar al final."""
        if self._es_administrador:
            self.ui.etiquetaAviso.setText(
                "Como administrador puedes registrar personal y cambiar su "
                "perfil de acceso."
            )
            self.ui.etiquetaAviso.setStyleSheet(f"color: {COLOR_PRINCIPAL};")
        else:
            self.ui.etiquetaAviso.setText(
                "Puedes registrar y modificar personal. Cambiar el perfil de "
                "acceso de alguien queda reservado al administrador."
            )
            self.ui.etiquetaAviso.setStyleSheet(f"color: {COLOR_TENUE};")

    # ------------------------------------------------------------------
    # Datos
    # ------------------------------------------------------------------

    def recargar(self) -> None:
        try:
            self._empleados = repo_personas.listar_empleados()
        except Exception as error:
            QMessageBox.warning(
                self,
                "No se pudo consultar la plantilla",
                f"Revisa tu conexión a internet.\n\n{error}",
            )
            return
        self._pintar()

    def _pintar(self) -> None:
        tabla = self.ui.tablaEmpleados
        tabla.setSortingEnabled(False)
        tabla.setRowCount(len(self._empleados))

        for fila, empleado in enumerate(self._empleados):
            celdas = [
                empleado.codigo,
                empleado.nombre_completo,
                empleado.tipo_empleado or "—",
                empleado.correo or "Sin correo",
                empleado.rol.value.capitalize(),
            ]
            for columna, texto in enumerate(celdas):
                celda = QTableWidgetItem(texto)
                if columna in (0, 4):
                    celda.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if columna == 1:
                    celda.setData(Qt.ItemDataRole.UserRole, fila)
                if columna == 4 and empleado.rol == Rol.ADMINISTRADOR:
                    celda.setForeground(Qt.GlobalColor.darkYellow)
                if columna == 3 and not empleado.correo:
                    celda.setForeground(Qt.GlobalColor.darkRed)
                tabla.setItem(fila, columna, celda)

        tabla.setSortingEnabled(True)
        self._actualizar_resumen()
        self._cambio_seleccion()

    def _actualizar_resumen(self) -> None:
        total = len(self._empleados)
        admins = sum(1 for e in self._empleados if e.rol == Rol.ADMINISTRADOR)

        partes = [f"{total} persona{'s' if total != 1 else ''} en la plantilla"]
        if admins:
            partes.append(f"{admins} con perfil de administrador")
        self.ui.etiquetaResumen.setText("   ·   ".join(partes))

    # ------------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------------

    def _seleccionado(self) -> Empleado | None:
        filas = self.ui.tablaEmpleados.selectionModel().selectedRows()
        if not filas:
            return None
        celda = self.ui.tablaEmpleados.item(filas[0].row(), 1)
        if celda is None:
            return None
        indice = celda.data(Qt.ItemDataRole.UserRole)
        return self._empleados[indice] if indice is not None else None

    def _cambio_seleccion(self) -> None:
        self.ui.botonEditar.setEnabled(self._seleccionado() is not None)

    def _registrar(self) -> None:
        formulario = FormularioEmpleado(self)
        if formulario.exec() and formulario.guardado:
            self.recargar()
            self._avisar(f"Se registró a {formulario.guardado.nombre_completo}.")

    def _modificar(self) -> None:
        empleado = self._seleccionado()
        if empleado is None:
            return
        formulario = FormularioEmpleado(self, empleado=empleado)
        if formulario.exec() and formulario.guardado:
            self.recargar()
            self._avisar(f"Se actualizaron los datos de {empleado.nombre_completo}.")

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
