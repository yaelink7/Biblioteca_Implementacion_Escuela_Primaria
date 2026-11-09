"""Alta y modificacion de un libro (REQ-LIB-01, REQ-LIB-02).

La validacion no vive aqui: la hace servicios.validador_libro, que se prueba
sin abrir ninguna ventana. Esta clase solo recoge lo que el usuario escribio
y muestra lo que el validador conteste.

Desde la reunion con la escuela el libro se clasifica por su coleccion de
Libros del Rincon, con sus grados (LIB-06), y por su asignatura (LIB-07), en
lugar del «tipo o genero» libre de antes. Las listas son las de
modelos/libro.py, que son las mismas que acepta la base.
"""

from __future__ import annotations

from datetime import date

from PySide6.QtWidgets import QDialog, QWidget

from biblioteca.core.errores import causa as causa_del_error
from biblioteca.modelos.libro import ASIGNATURAS, COLECCIONES, Libro
from biblioteca.repositorios import libros as repo_libros
from biblioteca.servicios import validador_libro
from biblioteca.ui.generado.ui_formulario_libro import Ui_FormularioLibro

# El QSpinBox usa su valor minimo como "sin especificar"
SIN_ANO = 1399
SIN_PAGINAS = 0


class FormularioLibro(QDialog):
    """Sirve para registrar un libro nuevo o modificar uno existente."""

    def __init__(self, padre: QWidget | None = None, libro: Libro | None = None) -> None:
        super().__init__(padre)
        self.ui = Ui_FormularioLibro()
        self.ui.setupUi(self)

        self.libro = libro
        self.es_alta = libro is None
        self.guardado: Libro | None = None

        titulo = "Registrar libro" if self.es_alta else "Modificar libro"
        self.setWindowTitle(titulo)
        self.ui.etiquetaEncabezado.setText(titulo)
        self.ui.etiquetaSubtitulo.setText(
            "Se agrega al catálogo con los ejemplares que indiques."
            if self.es_alta
            else libro.titulo
        )
        self.ui.campoAno.setMaximum(date.today().year)  # D-08: el tope es hoy
        self.ui.cajaError.hide()
        # Lo que hay en el estante solo se aclara al modificar
        self.ui.notaExistencias.setVisible(not self.es_alta)
        self._preparar_listas()

        if libro is not None:
            self._cargar(libro)

        self.ui.botonGuardar.clicked.connect(self._guardar)
        self.ui.botonCancelar.clicked.connect(self.reject)
        self.ui.campoTitulo.setFocus()

    def _preparar_listas(self) -> None:
        """Coleccion con sus grados, y asignatura; las dos se pueden dejar vacias."""
        self.ui.campoColeccion.addItem("Sin colección", None)
        for nombre, grados in COLECCIONES.items():
            self.ui.campoColeccion.addItem(f"{nombre} · {grados}", nombre)
        self.ui.campoAsignatura.addItem("Sin asignatura", None)
        for asignatura in ASIGNATURAS:
            self.ui.campoAsignatura.addItem(asignatura, asignatura)

    @staticmethod
    def _elegir(combo, valor: str | None) -> None:
        """Elige el valor guardado; uno que ya no este en la lista se conserva."""
        if valor and combo.findData(valor) < 0:
            combo.addItem(valor, valor)
        combo.setCurrentIndex(max(0, combo.findData(valor)))

    def _cargar(self, libro: Libro) -> None:
        self.ui.campoTitulo.setText(libro.titulo)
        self.ui.campoAutor.setText(libro.autor)
        self._elegir(self.ui.campoColeccion, libro.coleccion)
        self._elegir(self.ui.campoAsignatura, libro.asignatura)
        self.ui.campoEditorial.setText(libro.editorial or "")
        self.ui.campoExistencias.setValue(libro.existencias)
        self.ui.campoAno.setValue(libro.ano_publicacion or SIN_ANO)
        self.ui.campoPaginas.setValue(libro.num_paginas or SIN_PAGINAS)

    def _recoger(self) -> Libro:
        ano = self.ui.campoAno.value()
        paginas = self.ui.campoPaginas.value()

        return Libro(
            id=self.libro.id if self.libro else None,
            titulo=self.ui.campoTitulo.text().strip(),
            autor=self.ui.campoAutor.text().strip(),
            # El «tipo o genero» ya no se captura, pero el de los libros que
            # ya lo tienen no se borra al modificarlos.
            tipo_libro=self.libro.tipo_libro if self.libro else None,
            coleccion=self.ui.campoColeccion.currentData(),
            asignatura=self.ui.campoAsignatura.currentData(),
            editorial=self.ui.campoEditorial.text().strip() or None,
            existencias=self.ui.campoExistencias.value(),
            ano_publicacion=None if ano == SIN_ANO else ano,
            num_paginas=None if paginas == SIN_PAGINAS else paginas,
        )

    def _mostrar_error(self, titulo: str, texto: str) -> None:
        """El recuadro rojo de arriba: que paso y que corregir."""
        self.ui.tituloError.setText(titulo)
        self.ui.etiquetaError.setText(texto)
        self.ui.cajaError.show()

    def _guardar(self) -> None:
        libro = self._recoger()

        # Se valida antes de llamar a la base: el usuario ve todos los
        # errores juntos en lugar de uno por intento, como en el Java.
        revision = validador_libro.validar(libro, es_alta=self.es_alta)
        if not revision.es_valido:
            self._mostrar_error("Revisa estos datos:", revision.mensaje)
            return

        self.ui.botonGuardar.setEnabled(False)
        try:
            if self.es_alta:
                self.guardado = repo_libros.dar_de_alta(libro)
            else:
                self.guardado = repo_libros.modificar(libro)
        except Exception as error:
            # Cualquier fallo, no solo el que rechaza la base: sin esto
            # un corte de red se leia como «la base rechazo la operacion».
            self._mostrar_error("No se pudo guardar:", causa_del_error(error))
            self.ui.botonGuardar.setEnabled(True)
            return

        self.accept()
