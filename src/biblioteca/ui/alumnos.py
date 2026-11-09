"""Padron de alumnos lectores.

Sustituye a las ventanas de usuarios del sistema Java. Cubre REQ-USU-01 y
REQ-USU-03, y da entrada al historial de cada alumno (REQ-PRE-03).

La columna de situacion cruza con los prestamos activos: saber de un vistazo
quien ya tiene un libro evita intentar un prestamo que la base va a rechazar
por el limite de uno por alumno. El panel de la derecha junta lo que pidio la
escuela (#74 a #76): la CURP, el maestro del salon y el telefono del tutor.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QHeaderView,
    QLineEdit,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from biblioteca.core.errores import mensaje as mensaje_de_error
from biblioteca.modelos.persona import Alumno
from biblioteca.modelos.prestamo import Prestamo
from biblioteca.repositorios import personas as repo_personas
from biblioteca.repositorios import prestamos as repo_prestamos
from biblioteca.ui.apariencia import icono
from biblioteca.ui.componentes import (
    CeldaOrdenada,
    DelegadoFilaElegida,
    fuente_mono,
    mostrar_caja,
    poner_icono,
    volver_a_elegir,
)
from biblioteca.ui.estilo import (
    MARCADOR,
    ROJO,
    TENUE,
    TEXTO,
    repulir,
    rotular,
    rotular_encabezados,
)
from biblioteca.ui.formato import iniciales, plural, salon
from biblioteca.ui.formulario_alumno import FormularioAlumno
from biblioteca.ui.generado.ui_alumnos import Ui_PantallaAlumnos
from biblioteca.ui.historial_alumno import DialogoHistorial
from biblioteca.ui.maestros_de_grupo import DialogoMaestros

MS_ANTES_DE_BUSCAR = 250


class PantallaAlumnos(QWidget):
    # El telefono o el salon de un alumno tambien se ven en Prestamos y Deudores
    alumnos_cambiaron = Signal()

    def __init__(self, padre: QWidget | None = None) -> None:
        super().__init__(padre)
        self.ui = Ui_PantallaAlumnos()
        self.ui.setupUi(self)

        self._alumnos: list[Alumno] = []
        self._con_prestamo: dict[str, Prestamo] = {}
        self._maestros: dict[tuple[int, str], str] = {}

        self._temporizador = QTimer(self)
        self._temporizador.setSingleShot(True)
        self._temporizador.setInterval(MS_ANTES_DE_BUSCAR)
        self._temporizador.timeout.connect(self.recargar)

        self._preparar_aspecto()
        self._preparar_tabla()

        self.ui.campoBusqueda.textChanged.connect(self._temporizador.start)
        self.ui.tablaAlumnos.itemSelectionChanged.connect(self._cambio_seleccion)
        self.ui.tablaAlumnos.itemDoubleClicked.connect(lambda _: self._modificar())
        self.ui.botonNuevo.clicked.connect(self._registrar)
        self.ui.botonEditar.clicked.connect(self._modificar)
        self.ui.botonHistorial.clicked.connect(self._ver_historial)
        self.ui.botonMaestros.clicked.connect(self._editar_maestros)

        self.recargar()

    def _preparar_aspecto(self) -> None:
        ui = self.ui
        poner_icono(ui.botonNuevo, "mas", TEXTO)
        poner_icono(ui.botonMaestros, "maestro", TEXTO)
        poner_icono(ui.botonEditar, "editar", TEXTO)
        poner_icono(ui.botonHistorial, "historial", TEXTO)
        ui.campoBusqueda.addAction(icono("buscar", MARCADOR),
                                   QLineEdit.ActionPosition.LeadingPosition)
        rotular(ui.etiquetaPanel)
        rotular_encabezados(ui.tablaAlumnos)
        ui.tablaAlumnos.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        ui.tablaAlumnos.setItemDelegate(DelegadoFilaElegida(ui.tablaAlumnos))
        ui.etiquetaVacio.hide()

    def _preparar_tabla(self) -> None:
        cabecera = self.ui.tablaAlumnos.horizontalHeader()
        # Nombre y situacion se reparten el ancho sobrante; codigo, salon y
        # telefono se ajustan a su contenido, que es corto y de tamano fijo.
        for columna in (1, 4):
            cabecera.setSectionResizeMode(columna, QHeaderView.ResizeMode.Stretch)
        for columna in (0, 2, 3):
            cabecera.setSectionResizeMode(columna, QHeaderView.ResizeMode.ResizeToContents)
        # Por nombre, como el prototipo
        cabecera.setSortIndicator(1, Qt.SortOrder.AscendingOrder)

    # ------------------------------------------------------------------
    # Datos
    # ------------------------------------------------------------------

    def recargar(self) -> None:
        texto = self.ui.campoBusqueda.text().strip()
        try:
            self._alumnos = (
                repo_personas.buscar_alumnos_o_salon(texto)
                if texto
                else repo_personas.listar_alumnos()
            )
            # Una sola consulta para todos: pedir el estado alumno por alumno
            # multiplicaria las peticiones sin necesidad.
            self._con_prestamo = {p.usuario_id: p for p in repo_prestamos.activos()}
            self._maestros = repo_personas.listar_maestros()
        except Exception as error:
            QMessageBox.warning(
                self,
                "No se pudo consultar el padrón",
                mensaje_de_error(error),
            )
            return

        self._pintar()

    def _pintar(self) -> None:
        anterior = self._seleccionado()
        tabla = self.ui.tablaAlumnos
        tabla.blockSignals(True)
        tabla.clearSelection()
        tabla.setSortingEnabled(False)
        tabla.setRowCount(len(self._alumnos))

        negrita = QFont(tabla.font())
        negrita.setWeight(QFont.Weight.DemiBold)
        mono = fuente_mono(tabla.font())

        for fila, alumno in enumerate(self._alumnos):
            prestamo = self._con_prestamo.get(alumno.id or "")
            celdas = [
                QTableWidgetItem(alumno.codigo),
                QTableWidgetItem(alumno.nombre_completo),
                CeldaOrdenada(salon(alumno.grado, alumno.grupo),
                              f"{alumno.grado or 9}{alumno.grupo or 'z'}"),
                CeldaOrdenada(alumno.telefono or "Sin contacto", 0 if alumno.telefono else 1),
                QTableWidgetItem(f"Tiene «{prestamo.titulo_libro}»" if prestamo
                                 else "Sin préstamos"),
            ]
            celdas[1].setData(Qt.ItemDataRole.UserRole, fila)
            celdas[1].setFont(negrita)
            celdas[0].setFont(mono)
            celdas[2].setFont(mono)
            if alumno.telefono:
                celdas[3].setFont(mono)
            else:
                celdas[3].setForeground(QColor(ROJO))
                celdas[3].setFont(negrita)
            if prestamo is None:
                celdas[4].setForeground(QColor(TENUE))
            elif prestamo.esta_vencido:
                celdas[4].setForeground(QColor(ROJO))
                celdas[4].setFont(negrita)
            for columna, celda in enumerate(celdas):
                tabla.setItem(fila, columna, celda)

        tabla.setSortingEnabled(True)
        if anterior is not None:
            volver_a_elegir(tabla, 1, lambda i: i is not None and self._alumnos[i].id == anterior.id)
        tabla.blockSignals(False)
        hay = bool(self._alumnos)
        tabla.setVisible(hay)
        self.ui.etiquetaVacio.setVisible(not hay)
        texto = self.ui.campoBusqueda.text().strip()
        self.ui.etiquetaVacio.setText(
            f"Nadie coincide con «{texto}»." if texto else "No hay alumnos registrados.")
        self._actualizar_resumen()
        self._cambio_seleccion()

    def _actualizar_resumen(self) -> None:
        total = len(self._alumnos)
        con_libro = sum(1 for a in self._alumnos if a.id in self._con_prestamo)
        # El correo ya no cuenta como contacto: la escuela confirmo que no
        # funciona con las familias (USU-08). Sin telefono no hay a quien llamar.
        sin_contacto = sum(1 for a in self._alumnos if not a.telefono)

        partes = [plural(total, "alumno")]
        if con_libro:
            partes.append(f"{con_libro} con libro prestado")
        if sin_contacto:
            partes.append(f"{sin_contacto} sin contacto del tutor")
        self.ui.etiquetaResumen.setText(" · ".join(partes))

    # ------------------------------------------------------------------
    # Seleccion y panel
    # ------------------------------------------------------------------

    def _seleccionado(self) -> Alumno | None:
        filas = self.ui.tablaAlumnos.selectionModel().selectedRows()
        if not filas:
            return None
        celda = self.ui.tablaAlumnos.item(filas[0].row(), 1)
        if celda is None:
            return None
        indice = celda.data(Qt.ItemDataRole.UserRole)
        return self._alumnos[indice] if indice is not None else None

    def _cambio_seleccion(self) -> None:
        alumno = self._seleccionado()
        self.ui.botonEditar.setEnabled(alumno is not None)
        self.ui.botonHistorial.setEnabled(alumno is not None)
        self._mostrar_panel(alumno)

    def maestro_de(self, alumno: Alumno) -> str:
        if not (alumno.grado and alumno.grupo):
            return ""
        return self._maestros.get((alumno.grado, alumno.grupo), "")

    def _mostrar_panel(self, alumno: Alumno | None) -> None:
        ui = self.ui
        ui.etiquetaPanelVacio.setHidden(alumno is not None)
        ui.fichaAlumno.setHidden(alumno is None)
        if alumno is None:
            return

        ui.avatar.setText(iniciales(alumno.nombre, alumno.apellido))
        ui.etiquetaNombre.setText(alumno.nombre_completo)
        ui.etiquetaDetalle.setText(f"{salon(alumno.grado, alumno.grupo)} · {alumno.codigo}")

        prestamo = self._con_prestamo.get(alumno.id or "")
        cajas = (ui.cajaSituacion, ui.iconoCaja, ui.tituloCaja, ui.textoCaja)
        if prestamo is None:
            mostrar_caja(*cajas, "catalogo", "Sin préstamos en curso", "Puede llevarse un libro.")
        elif prestamo.esta_vencido:
            mostrar_caja(*cajas, "alerta", f"Tiene «{prestamo.titulo_libro}»",
                         f"Vencido hace {plural(prestamo.dias_de_retraso, 'día')}; ya "
                         "aparece en el reporte de deudores.", rojo=True)
        else:
            mostrar_caja(*cajas, "reloj", f"Tiene «{prestamo.titulo_libro}»",
                         f"{prestamo.resumen}.")

        ui.valorCurp.setText(alumno.curp or "—")
        maestro = self.maestro_de(alumno)
        ui.valorMaestro.setText(maestro or "Sin asignar")
        ui.valorMaestro.setProperty("tenue", not maestro)
        repulir(ui.valorMaestro)

        ui.valorTelefono.setText(alumno.telefono or "Sin contacto")
        ui.valorTelefono.setProperty("mono", bool(alumno.telefono))
        ui.valorTelefono.setProperty("alerta", not alumno.telefono)
        repulir(ui.valorTelefono)
        ui.valorDireccion.setText(alumno.direccion or "—")

    # ------------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------------

    def _registrar(self) -> None:
        formulario = FormularioAlumno(self, maestros=self._maestros)
        if formulario.exec() and formulario.guardado:
            self.ui.campoBusqueda.clear()
            self.recargar()
            self._avisar(f"Se registró a {formulario.guardado.nombre_completo}.")
            self.alumnos_cambiaron.emit()

    def _modificar(self) -> None:
        alumno = self._seleccionado()
        if alumno is None:
            return
        formulario = FormularioAlumno(self, alumno=alumno, maestros=self._maestros)
        if formulario.exec() and formulario.guardado:
            self.recargar()
            self._avisar(f"Se actualizaron los datos de {formulario.guardado.nombre_completo}.")
            self.alumnos_cambiaron.emit()

    def _ver_historial(self) -> None:
        alumno = self._seleccionado()
        if alumno is not None:
            DialogoHistorial(self, alumno).exec()

    def _editar_maestros(self) -> None:
        dialogo = DialogoMaestros(self)
        if dialogo.exec() and dialogo.guardado:
            self.recargar()
            self._avisar("Se guardaron los maestros de grupo.")

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
