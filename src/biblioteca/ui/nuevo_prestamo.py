"""Registro de un prestamo (REQ-PRE-01, REQ-PRE-02).

La Factibilidad Operativa del Avance 1 fija la meta: registrar un prestamo
debe tomar menos de treinta segundos, buscando al alumno por nombre o grupo,
sin llenar mas de tres campos. Por eso el dialogo son dos busquedas y un
boton, y no un formulario.
"""

from __future__ import annotations


from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QDialog, QListWidgetItem, QWidget

from biblioteca.core.errores import causa as causa_del_error
from biblioteca.core.config import DIAS_DE_PRESTAMO
from biblioteca.core.sesion import sesion_actual
from biblioteca.modelos.libro import Libro
from biblioteca.modelos.persona import Alumno
from biblioteca.repositorios import libros as repo_libros
from biblioteca.repositorios import personas as repo_personas
from biblioteca.repositorios import prestamos as repo_prestamos
from biblioteca.ui.estilo import COLOR_ERROR, COLOR_PRINCIPAL, COLOR_TENUE
from biblioteca.ui.generado.ui_nuevo_prestamo import Ui_DialogoNuevoPrestamo

MS_ANTES_DE_BUSCAR = 250


class DialogoNuevoPrestamo(QDialog):
    """Dos busquedas lado a lado: a quien y que libro."""

    def __init__(self, padre: QWidget | None = None) -> None:
        super().__init__(padre)
        self.ui = Ui_DialogoNuevoPrestamo()
        self.ui.setupUi(self)

        self.alumno: Alumno | None = None
        self.libro: Libro | None = None
        self.registrado = False

        self._temp_alumnos = self._temporizador(self._buscar_alumnos)
        self._temp_libros = self._temporizador(self._buscar_libros)

        self.ui.etiquetaError.setStyleSheet(f"color: {COLOR_ERROR};")
        self.ui.etiquetaPlazo.setStyleSheet(f"color: {COLOR_TENUE};")
        self.ui.botonCancelar.setProperty("secundario", True)
        for etiqueta in (self.ui.etiquetaAlumno, self.ui.etiquetaLibro):
            etiqueta.setStyleSheet(f"color: {COLOR_PRINCIPAL}; font-weight: 600;")

        self.ui.campoBuscarAlumno.textChanged.connect(self._temp_alumnos.start)
        self.ui.campoBuscarLibro.textChanged.connect(self._temp_libros.start)
        self.ui.listaAlumnos.itemSelectionChanged.connect(self._elegir_alumno)
        self.ui.listaLibros.itemSelectionChanged.connect(self._elegir_libro)
        self.ui.botonPrestar.clicked.connect(self._prestar)
        self.ui.botonCancelar.clicked.connect(self.reject)

        self._buscar_alumnos()
        self._buscar_libros()
        self.ui.campoBuscarAlumno.setFocus()

    def _temporizador(self, funcion) -> QTimer:
        """Evita una consulta por cada tecla mientras el usuario escribe."""
        t = QTimer(self)
        t.setSingleShot(True)
        t.setInterval(MS_ANTES_DE_BUSCAR)
        t.timeout.connect(funcion)
        return t

    # ------------------------------------------------------------------
    # Busquedas
    # ------------------------------------------------------------------

    def _buscar_alumnos(self) -> None:
        texto = self.ui.campoBuscarAlumno.text()
        try:
            encontrados = repo_personas.buscar_alumnos_o_salon(texto)
        except Exception as error:
            self._error(f"No se pudo buscar el alumno. {causa_del_error(error)}")
            return

        elegido = self.alumno.id if self.alumno else None
        self.ui.listaAlumnos.clear()
        self.alumno = None

        for alumno in encontrados:
            item = QListWidgetItem(f"{alumno.nombre_completo}   ·   {alumno.salon}")
            item.setData(Qt.ItemDataRole.UserRole, alumno)
            self.ui.listaAlumnos.addItem(item)
            # Si quien ya estaba elegido sigue entre los resultados, se
            # conserva: de otro modo una busqueda pendiente borraria la
            # seleccion que el bibliotecario acaba de hacer.
            if elegido and alumno.id == elegido:
                self.ui.listaAlumnos.setCurrentItem(item)

        self._actualizar_resumen()

    def _buscar_libros(self) -> None:
        texto = self.ui.campoBuscarLibro.text().strip()
        try:
            encontrados = repo_libros.buscar(texto) if texto else repo_libros.listar()
        except Exception as error:
            self._error(f"No se pudo buscar el libro. {causa_del_error(error)}")
            return

        elegido = self.libro.id if self.libro else None
        self.ui.listaLibros.clear()
        self.libro = None

        for libro in encontrados:
            item = QListWidgetItem(f"{libro.titulo}   ·   {libro.estado}")
            item.setData(Qt.ItemDataRole.UserRole, libro)
            if not libro.disponible:
                # Se muestra pero no se puede elegir: explica por que no esta
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
            self.ui.listaLibros.addItem(item)
            if elegido and libro.id == elegido and libro.disponible:
                self.ui.listaLibros.setCurrentItem(item)

        self._actualizar_resumen()

    # ------------------------------------------------------------------
    # Seleccion
    # ------------------------------------------------------------------

    def _elegir_alumno(self) -> None:
        item = self.ui.listaAlumnos.currentItem()
        self.alumno = item.data(Qt.ItemDataRole.UserRole) if item else None
        self._actualizar_resumen()

    def _elegir_libro(self) -> None:
        item = self.ui.listaLibros.currentItem()
        self.libro = item.data(Qt.ItemDataRole.UserRole) if item else None
        self._actualizar_resumen()

    def _actualizar_resumen(self) -> None:
        # El error NO se limpia aqui: este metodo lo invocan las busquedas,
        # que pueden dispararse justo despues de un rechazo y borrarian el
        # mensaje antes de que el bibliotecario alcance a leerlo. Se limpia
        # solo al intentar un prestamo nuevo.
        if self.alumno and self.libro:
            self.ui.etiquetaResumen.setText(
                f"<b>{self.alumno.nombre_completo}</b> ({self.alumno.salon}) "
                f"se lleva <b>{self.libro.titulo}</b>"
            )
            # La fecha limite la calcula la base al registrar (Corolario 2).
            # Anunciarla aqui con date.today() hacia que a partir de las 18:00
            # la pantalla dijera un dia y la base guardara otro.
            self.ui.etiquetaPlazo.setText(
                f"El plazo es de {DIAS_DE_PRESTAMO} días naturales; "
                f"la fecha exacta queda registrada al confirmar"
            )
            self.ui.botonPrestar.setEnabled(True)
            return

        if self.alumno:
            falta = "Ahora elige el libro."
        elif self.libro:
            falta = "Ahora elige al alumno."
        else:
            falta = "Elige un alumno y un libro."
        self.ui.etiquetaResumen.setText(falta)
        self.ui.etiquetaPlazo.clear()
        self.ui.botonPrestar.setEnabled(False)

    # ------------------------------------------------------------------
    # Registro
    # ------------------------------------------------------------------

    def _prestar(self) -> None:
        if not (self.alumno and self.libro and self.alumno.id and self.libro.id):
            return

        self.ui.etiquetaError.clear()
        self.ui.botonPrestar.setEnabled(False)
        try:
            repo_prestamos.registrar(
                libro_id=self.libro.id,
                alumno_id=self.alumno.id,
                registrado_por=sesion_actual().perfil.id,
            )
        except repo_prestamos.ErrorDePrestamo as error:
            # Aqui aparece el limite de un libro por alumno, que aplica
            # Postgres mediante un indice unico parcial.
            self._error(str(error))
            self.ui.botonPrestar.setEnabled(True)
            return

        self.registrado = True
        self.accept()

    def _error(self, mensaje: str) -> None:
        self.ui.etiquetaError.setText(mensaje)
