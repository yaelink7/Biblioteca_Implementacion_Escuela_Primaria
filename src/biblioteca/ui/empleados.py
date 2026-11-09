"""Plantilla de la biblioteca (REQ-EMP-01).

Sustituye a las ventanas de empleados del sistema Java. El requisito pide
que el alta de personal quede "restringida a personal con permisos
administrativos"; esa restriccion la aplican las politicas RLS de Postgres,
y aqui se anticipa para explicar por que el perfil de acceso esta bloqueado
en lugar de dejar que el usuario llene un formulario que va a ser rechazado.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QHeaderView,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from biblioteca.core.errores import mensaje as mensaje_de_error
from biblioteca.core.sesion import sesion_actual
from biblioteca.modelos.persona import Empleado, Rol
from biblioteca.repositorios import personas as repo_personas
from biblioteca.ui.apariencia import icono
from biblioteca.ui.componentes import DelegadoFilaElegida, fuente_mono, poner_icono
from biblioteca.ui.estilo import (
    GRIS,
    TENUE,
    TEXTO,
    repulir,
    rotular,
    rotular_encabezados,
)
from biblioteca.ui.formato import fecha_corta, iniciales, plural
from biblioteca.ui.formulario_empleado import FormularioEmpleado
from biblioteca.ui.generado.ui_empleados import Ui_PantallaEmpleados

NOMBRE_DEL_PERFIL = {Rol.ADMINISTRADOR: "Administrador", Rol.BIBLIOTECARIO: "Bibliotecario"}


class PantallaEmpleados(QWidget):
    def __init__(self, padre: QWidget | None = None) -> None:
        super().__init__(padre)
        self.ui = Ui_PantallaEmpleados()
        self.ui.setupUi(self)

        self._empleados: list[Empleado] = []
        perfil = sesion_actual().perfil
        self._es_administrador = perfil.rol == Rol.ADMINISTRADOR
        self._yo = perfil.id

        self._preparar_aspecto()
        self._preparar_tabla()
        self._preparar_permisos()

        self.ui.tablaEmpleados.itemSelectionChanged.connect(self._cambio_seleccion)
        self.ui.tablaEmpleados.itemDoubleClicked.connect(lambda _: self._modificar())
        self.ui.botonNuevo.clicked.connect(self._registrar)
        self.ui.botonEditar.clicked.connect(self._modificar)

        self.recargar()

    def _preparar_aspecto(self) -> None:
        ui = self.ui
        poner_icono(ui.botonNuevo, "mas", TEXTO)
        poner_icono(ui.botonEditar, "editar", TEXTO)
        ui.iconoAviso.setPixmap(icono("escudo", GRIS, 18).pixmap(18, 18))
        rotular(ui.etiquetaPanel)
        rotular_encabezados(ui.tablaEmpleados)
        ui.tablaEmpleados.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        ui.tablaEmpleados.setItemDelegate(DelegadoFilaElegida(ui.tablaEmpleados))
        ui.etiquetaVacio.hide()

    def _preparar_tabla(self) -> None:
        cabecera = self.ui.tablaEmpleados.horizontalHeader()
        for columna in (1, 3):
            cabecera.setSectionResizeMode(columna, QHeaderView.ResizeMode.Stretch)
        for columna in (0, 2, 4):
            cabecera.setSectionResizeMode(columna, QHeaderView.ResizeMode.ResizeToContents)

    def _preparar_permisos(self) -> None:
        """Dice de entrada quien puede hacer que, en vez de fallar al final."""
        if self._es_administrador:
            self.ui.etiquetaAviso.setText(
                "Como administrador puedes registrar personal y cambiar su "
                "perfil de acceso."
            )
        else:
            self.ui.etiquetaAviso.setText(
                "Puedes registrar y modificar personal. Cambiar el perfil de "
                "acceso de alguien queda reservado al administrador."
            )

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
                mensaje_de_error(error),
            )
            return
        self._pintar()

    def _pintar(self) -> None:
        tabla = self.ui.tablaEmpleados
        tabla.setSortingEnabled(False)
        tabla.setRowCount(len(self._empleados))

        negrita = QFont(tabla.font())
        negrita.setWeight(QFont.Weight.DemiBold)
        mono = fuente_mono(tabla.font())

        for fila, empleado in enumerate(self._empleados):
            nombre = empleado.nombre_completo
            if empleado.id == self._yo:
                nombre += " (tú)"
            celdas = [
                QTableWidgetItem(empleado.codigo),
                QTableWidgetItem(nombre),
                QTableWidgetItem(empleado.tipo_empleado or "—"),
                QTableWidgetItem(empleado.correo or "Sin correo"),
                QTableWidgetItem(NOMBRE_DEL_PERFIL.get(empleado.rol, empleado.rol.value)),
            ]
            celdas[1].setData(Qt.ItemDataRole.UserRole, fila)
            celdas[1].setFont(negrita)
            celdas[0].setFont(mono)
            celdas[3].setFont(mono)
            if not empleado.correo:
                celdas[3].setForeground(QColor(TENUE))
            if empleado.rol == Rol.ADMINISTRADOR:
                celdas[4].setFont(negrita)
            for columna, celda in enumerate(celdas):
                tabla.setItem(fila, columna, celda)

        tabla.setSortingEnabled(True)
        hay = bool(self._empleados)
        tabla.setVisible(hay)
        self.ui.etiquetaVacio.setVisible(not hay)
        self._actualizar_resumen()
        self._cambio_seleccion()

    def _actualizar_resumen(self) -> None:
        total = len(self._empleados)
        admins = sum(1 for e in self._empleados if e.rol == Rol.ADMINISTRADOR)

        partes = [f"{plural(total, 'persona')} en la plantilla"]
        if admins:
            partes.append(f"{admins} con perfil de administrador")
        self.ui.etiquetaResumen.setText(" · ".join(partes))

    # ------------------------------------------------------------------
    # Seleccion y panel
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
        empleado = self._seleccionado()
        self.ui.botonEditar.setEnabled(empleado is not None)
        self._mostrar_panel(empleado)

    def _mostrar_panel(self, empleado: Empleado | None) -> None:
        ui = self.ui
        ui.etiquetaPanelVacio.setHidden(empleado is not None)
        ui.fichaEmpleado.setHidden(empleado is None)
        if empleado is None:
            return

        ui.avatar.setText(iniciales(empleado.nombre, empleado.apellido))
        ui.etiquetaNombre.setText(empleado.nombre_completo)
        ui.etiquetaDetalle.setText(f"{empleado.tipo_empleado or '—'} · {empleado.codigo}")
        ui.valorCorreo.setText(empleado.correo or "Sin correo")
        ui.valorPerfil.setText(NOMBRE_DEL_PERFIL.get(empleado.rol, empleado.rol.value))
        ui.valorTelefono.setText(empleado.telefono or "—")
        ui.valorTelefono.setProperty("mono", bool(empleado.telefono))
        repulir(ui.valorTelefono)
        ui.valorDireccion.setText(empleado.direccion or "—")
        ui.valorIngreso.setText(
            fecha_corta(empleado.fecha_ingreso) if empleado.fecha_ingreso else "—")

    # ------------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------------

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
            self._avisar(f"Se actualizaron los datos de {formulario.guardado.nombre_completo}.")

    def _avisar(self, mensaje: str) -> None:
        """Confirmacion discreta en la linea de resumen, sin cuadros de dialogo."""
        self.ui.etiquetaResumen.setText(mensaje)
        self.ui.etiquetaResumen.setProperty("aviso", True)
        repulir(self.ui.etiquetaResumen)
        QTimer.singleShot(3000, self, self._quitar_aviso)

    def _quitar_aviso(self) -> None:
        self.ui.etiquetaResumen.setProperty("aviso", False)
        repulir(self.ui.etiquetaResumen)
        self._actualizar_resumen()
