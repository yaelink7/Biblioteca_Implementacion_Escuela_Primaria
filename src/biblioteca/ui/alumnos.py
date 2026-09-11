"""Padron de alumnos lectores.

Sustituye a las ventanas de usuarios del sistema Java. Cubre REQ-USU-01 y
REQ-USU-03, y da entrada al historial de cada alumno (REQ-PRE-03).

La columna de situacion cruza con los prestamos activos: saber de un vistazo
quien ya tiene un libro evita intentar un prestamo que la base va a rechazar
por el limite de uno por alumno.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QHeaderView,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from biblioteca.modelos.persona import Alumno
from biblioteca.repositorios import personas as repo_personas
from biblioteca.repositorios import prestamos as repo_prestamos
from biblioteca.ui.estilo import COLOR_ALERTA, COLOR_TENUE
from biblioteca.ui.formulario_alumno import FormularioAlumno
from biblioteca.ui.generado.ui_alumnos import Ui_PantallaAlumnos
from biblioteca.ui.historial_alumno import DialogoHistorial

MS_ANTES_DE_BUSCAR = 250


class PantallaAlumnos(QWidget):
    def __init__(self, padre: QWidget | None = None) -> None:
        super().__init__(padre)
        self.ui = Ui_PantallaAlumnos()
        self.ui.setupUi(self)

        self._alumnos: list[Alumno] = []
        self._con_prestamo: dict[str, str] = {}

        self._temporizador = QTimer(self)
        self._temporizador.setSingleShot(True)
        self._temporizador.setInterval(MS_ANTES_DE_BUSCAR)
        self._temporizador.timeout.connect(self.recargar)

        self._preparar_tabla()
        self.ui.etiquetaResumen.setStyleSheet(f"color: {COLOR_TENUE};")

        self.ui.campoBusqueda.textChanged.connect(self._temporizador.start)
        self.ui.tablaAlumnos.itemSelectionChanged.connect(self._cambio_seleccion)
        self.ui.tablaAlumnos.itemDoubleClicked.connect(lambda _: self._ver_historial())
        self.ui.botonNuevo.clicked.connect(self._registrar)
        self.ui.botonEditar.clicked.connect(self._modificar)
        self.ui.botonHistorial.clicked.connect(self._ver_historial)

        self.recargar()

    def _preparar_tabla(self) -> None:
        cabecera = self.ui.tablaAlumnos.horizontalHeader()
        # Nombre, contacto y situacion se reparten el ancho sobrante; codigo
        # y salon se ajustan a su contenido, que es corto y de tamano fijo.
        for columna in (1, 3, 4):
            cabecera.setSectionResizeMode(columna, QHeaderView.ResizeMode.Stretch)
        for columna in (0, 2):
            cabecera.setSectionResizeMode(columna, QHeaderView.ResizeMode.ResizeToContents)

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
            self._con_prestamo = {
                p.usuario_id: p.titulo_libro or "un libro"
                for p in repo_prestamos.activos()
            }
        except Exception as error:
            QMessageBox.warning(
                self,
                "No se pudo consultar el padrón",
                f"Revisa tu conexión a internet.\n\n{error}",
            )
            return

        self._pintar()

    def _pintar(self) -> None:
        tabla = self.ui.tablaAlumnos
        tabla.setSortingEnabled(False)
        tabla.setRowCount(len(self._alumnos))

        for fila, alumno in enumerate(self._alumnos):
            prestado = self._con_prestamo.get(alumno.id or "")
            celdas = [
                alumno.codigo,
                alumno.nombre_completo,
                alumno.salon,
                alumno.correo or alumno.telefono or "Sin contacto",
                f"Tiene «{prestado}»" if prestado else "Sin préstamos",
            ]
            for columna, texto in enumerate(celdas):
                celda = QTableWidgetItem(texto)
                if columna in (0, 2):
                    celda.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if columna == 1:
                    celda.setData(Qt.ItemDataRole.UserRole, fila)
                if columna == 3 and not (alumno.correo or alumno.telefono):
                    celda.setForeground(Qt.GlobalColor.darkRed)
                if columna == 4 and prestado:
                    celda.setForeground(Qt.GlobalColor.darkYellow)
                tabla.setItem(fila, columna, celda)

        tabla.setSortingEnabled(True)
        self._actualizar_resumen()
        self._cambio_seleccion()

    def _actualizar_resumen(self) -> None:
        total = len(self._alumnos)
        con_libro = sum(1 for a in self._alumnos if a.id in self._con_prestamo)
        sin_contacto = sum(1 for a in self._alumnos if not (a.correo or a.telefono))

        partes = [f"{total} alumno{'s' if total != 1 else ''}"]
        if con_libro:
            partes.append(f"{con_libro} con libro prestado")
        if sin_contacto:
            partes.append(f"{sin_contacto} sin contacto del tutor")
        self.ui.etiquetaResumen.setText("   ·   ".join(partes))

    # ------------------------------------------------------------------
    # Acciones
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
        hay = self._seleccionado() is not None
        self.ui.botonEditar.setEnabled(hay)
        self.ui.botonHistorial.setEnabled(hay)

    def _registrar(self) -> None:
        formulario = FormularioAlumno(self)
        if formulario.exec() and formulario.guardado:
            self.ui.campoBusqueda.clear()
            self.recargar()
            self._avisar(f"Se registró a {formulario.guardado.nombre_completo}.")

    def _modificar(self) -> None:
        alumno = self._seleccionado()
        if alumno is None:
            return
        formulario = FormularioAlumno(self, alumno=alumno)
        if formulario.exec() and formulario.guardado:
            self.recargar()
            self._avisar(f"Se actualizaron los datos de {alumno.nombre_completo}.")

    def _ver_historial(self) -> None:
        alumno = self._seleccionado()
        if alumno is not None:
            DialogoHistorial(self, alumno).exec()

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
