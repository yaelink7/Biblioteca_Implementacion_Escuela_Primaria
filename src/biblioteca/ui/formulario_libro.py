"""Alta y modificacion de un libro (REQ-LIB-01, REQ-LIB-02).

La validacion no vive aqui: la hace servicios.validador_libro, que se prueba
sin abrir ninguna ventana. Esta clase solo recoge lo que el usuario escribio
y muestra lo que el validador conteste.
"""

from __future__ import annotations

from datetime import date

from PySide6.QtWidgets import QDialog, QWidget

from biblioteca.core.errores import causa as causa_del_error
from biblioteca.modelos.libro import Libro
from biblioteca.repositorios import libros as repo_libros
from biblioteca.servicios import validador_libro
from biblioteca.ui.estilo import COLOR_ERROR
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

        self.setWindowTitle("Registrar libro" if self.es_alta else "Modificar libro")
        self.ui.campoAno.setMaximum(date.today().year)  # D-08: el tope es hoy
        self.ui.etiquetaError.setStyleSheet(f"color: {COLOR_ERROR};")

        if libro is not None:
            self._cargar(libro)

        self.ui.botonCancelar.setProperty("secundario", True)
        self.ui.botonGuardar.clicked.connect(self._guardar)
        self.ui.botonCancelar.clicked.connect(self.reject)
        self.ui.campoTitulo.setFocus()

    def _cargar(self, libro: Libro) -> None:
        self.ui.campoTitulo.setText(libro.titulo)
        self.ui.campoAutor.setText(libro.autor)
        self.ui.campoTipo.setCurrentText(libro.tipo_libro or "")
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
            tipo_libro=self.ui.campoTipo.currentText().strip() or None,
            editorial=self.ui.campoEditorial.text().strip() or None,
            existencias=self.ui.campoExistencias.value(),
            ano_publicacion=None if ano == SIN_ANO else ano,
            num_paginas=None if paginas == SIN_PAGINAS else paginas,
        )

    def _guardar(self) -> None:
        libro = self._recoger()

        # Se valida antes de llamar a la base: el usuario ve todos los
        # errores juntos en lugar de uno por intento, como en el Java.
        revision = validador_libro.validar(libro, es_alta=self.es_alta)
        if not revision.es_valido:
            self.ui.etiquetaError.setText(revision.mensaje)
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
            self.ui.etiquetaError.setText(causa_del_error(error))
            self.ui.botonGuardar.setEnabled(True)
            return

        self.accept()
