"""Registro de un prestamo (REQ-PRE-01, REQ-PRE-02).

La Factibilidad Operativa del Avance 1 fija la meta: registrar un prestamo
debe tomar menos de treinta segundos, buscando al alumno por nombre o grupo,
sin llenar mas de tres campos. Por eso el dialogo son dos busquedas y un
boton, y no un formulario.
"""

from __future__ import annotations

from html import escape

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QDialog, QLineEdit, QListWidgetItem, QWidget

from biblioteca.core.config import DIAS_DE_PRESTAMO
from biblioteca.core.errores import causa as causa_del_error
from biblioteca.core.errores import explicar
from biblioteca.core.sesion import sesion_actual
from biblioteca.modelos.libro import Libro
from biblioteca.modelos.persona import Alumno
from biblioteca.repositorios import libros as repo_libros
from biblioteca.repositorios import personas as repo_personas
from biblioteca.repositorios import prestamos as repo_prestamos
from biblioteca.ui.apariencia import icono
from biblioteca.ui.componentes import COLOR_NOTA, DETALLE, NOTA, DelegadoOpcion
from biblioteca.ui.estilo import MARCADOR, ROJO, ROJO_OSCURO, TENUE
from biblioteca.ui.formato import salon
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
        self._con_prestamo = self._prestamos_en_curso()

        self._preparar_aspecto()

        self.ui.campoBuscarAlumno.textChanged.connect(self._temp_alumnos.start)
        self.ui.campoBuscarLibro.textChanged.connect(self._temp_libros.start)
        self.ui.listaAlumnos.itemSelectionChanged.connect(self._elegir_alumno)
        self.ui.listaLibros.itemSelectionChanged.connect(self._elegir_libro)
        self.ui.botonPrestar.clicked.connect(self._prestar)
        self.ui.botonCancelar.clicked.connect(self.reject)

        self._buscar_alumnos()
        self._buscar_libros()
        self.ui.campoBuscarAlumno.setFocus()

    def _preparar_aspecto(self) -> None:
        ui = self.ui
        for campo in (ui.campoBuscarAlumno, ui.campoBuscarLibro):
            campo.addAction(icono("buscar", MARCADOR), QLineEdit.ActionPosition.LeadingPosition)
        for lista in (ui.listaAlumnos, ui.listaLibros):
            lista.setItemDelegate(DelegadoOpcion(lista))
            lista.setMouseTracking(True)
            lista.setSpacing(2)
        ui.iconoError.setPixmap(icono("alerta", ROJO_OSCURO, 18).pixmap(18, 18))
        ui.cajaError.hide()

    def _temporizador(self, funcion) -> QTimer:
        """Evita una consulta por cada tecla mientras el usuario escribe."""
        t = QTimer(self)
        t.setSingleShot(True)
        t.setInterval(MS_ANTES_DE_BUSCAR)
        t.timeout.connect(funcion)
        return t

    def _prestamos_en_curso(self) -> dict[str, str]:
        """Quien ya tiene un libro, para avisarlo antes de intentar el prestamo.

        Es solo un aviso: la regla de un libro por alumno la aplica la base.
        Si la consulta falla, el dialogo sigue sirviendo sin el aviso.
        """
        try:
            return {p.usuario_id: p.titulo_libro or "un libro"
                    for p in repo_prestamos.activos()}
        except Exception:
            return {}

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

        for alumno in sorted(encontrados, key=lambda a: a.nombre_completo):
            item = QListWidgetItem(alumno.nombre_completo)
            item.setData(Qt.ItemDataRole.UserRole, alumno)
            item.setData(DETALLE, f"{salon(alumno.grado, alumno.grupo)} · {alumno.codigo}")
            prestado = self._con_prestamo.get(alumno.id or "")
            if prestado:
                item.setData(NOTA, f" · tiene «{prestado}»")
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
            item = QListWidgetItem(libro.titulo)
            item.setData(Qt.ItemDataRole.UserRole, libro)
            item.setData(DETALLE, libro.autor)
            item.setData(NOTA, f" · {libro.estado}")
            if not libro.disponible:
                # Se muestra pero no se puede elegir: explica por que no esta
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
                item.setData(COLOR_NOTA, ROJO)
            else:
                item.setData(COLOR_NOTA, TENUE)
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
                f"<b>{escape(self.alumno.nombre_completo, quote=False)}</b> "
                f"({salon(self.alumno.grado, self.alumno.grupo)}) "
                f"se lleva <b>{escape(self.libro.titulo, quote=False)}</b>"
            )
            # La fecha limite la calcula la base al registrar (Corolario 2).
            # Anunciarla aqui con date.today() hacia que a partir de las 18:00
            # la pantalla dijera un dia y la base guardara otro.
            self.ui.etiquetaPlazo.setText(
                f"El plazo es de {DIAS_DE_PRESTAMO} días naturales; "
                f"la fecha exacta queda registrada al confirmar."
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
        self.ui.cajaError.hide()
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
            que_hacer = explicar(error).que_hacer
            self._error(str(error), que_hacer)
            self.ui.botonPrestar.setEnabled(True)
            return

        self.registrado = True
        self.accept()

    def _error(self, mensaje: str, que_hacer: str = "") -> None:
        """El recuadro rojo de abajo: que paso, en negrita, y que hacer."""
        texto = f"<b>{escape(mensaje, quote=False)}</b>"
        if que_hacer:
            texto += f"<br>{escape(que_hacer, quote=False)}"
        self.ui.etiquetaError.setText(texto)
        self.ui.cajaError.show()
