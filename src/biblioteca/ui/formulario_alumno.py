"""Alta y modificacion de alumnos (REQ-USU-01, REQ-USU-03).

No crea cuenta de acceso: la bibliotecaria registra la ficha de un nino de
primaria sin darle correo ni contrasena. El correo que se pide es el del
tutor, para los avisos de prestamos vencidos.
"""

from __future__ import annotations

from PySide6.QtWidgets import QDialog, QWidget

from biblioteca.core.errores import causa as causa_del_error
from biblioteca.modelos.persona import Alumno
from biblioteca.repositorios import personas as repo_personas
from biblioteca.servicios import validador_persona
from biblioteca.ui.estilo import COLOR_ERROR, COLOR_TENUE
from biblioteca.ui.generado.ui_formulario_alumno import Ui_FormularioAlumno

SIN_GRADO = 0


class FormularioAlumno(QDialog):
    def __init__(self, padre: QWidget | None = None, alumno: Alumno | None = None) -> None:
        super().__init__(padre)
        self.ui = Ui_FormularioAlumno()
        self.ui.setupUi(self)

        self.alumno = alumno
        self.es_alta = alumno is None
        self.guardado: Alumno | None = None

        self.setWindowTitle("Registrar alumno" if self.es_alta else "Modificar alumno")
        self.ui.etiquetaError.setStyleSheet(f"color: {COLOR_ERROR};")
        self.ui.etiquetaAviso.setStyleSheet(f"color: {COLOR_TENUE};")
        self.ui.botonCancelar.setProperty("secundario", True)

        if alumno is not None:
            self._cargar(alumno)
            # El codigo identifica al alumno en los prestamos ya registrados
            self.ui.campoCodigo.setEnabled(False)

        self.ui.botonGuardar.clicked.connect(self._guardar)
        self.ui.botonCancelar.clicked.connect(self.reject)
        self.ui.campoCodigo.setFocus() if self.es_alta else self.ui.campoNombre.setFocus()

    def _cargar(self, alumno: Alumno) -> None:
        self.ui.campoCodigo.setText(alumno.codigo)
        self.ui.campoNombre.setText(alumno.nombre)
        self.ui.campoApellido.setText(alumno.apellido)
        self.ui.campoGrado.setValue(alumno.grado or SIN_GRADO)
        self.ui.campoGrupo.setCurrentText(alumno.grupo or "")
        self.ui.campoCorreo.setText(alumno.correo or "")
        self.ui.campoTelefono.setText(alumno.telefono or "")
        self.ui.campoCalle.setText(alumno.calle or "")
        self.ui.campoColonia.setText(alumno.colonia or "")

    def _recoger(self) -> Alumno:
        grado = self.ui.campoGrado.value()
        alumno = Alumno(
            codigo=self.ui.campoCodigo.text().strip(),
            nombre=self.ui.campoNombre.text().strip(),
            apellido=self.ui.campoApellido.text().strip(),
            correo=self.ui.campoCorreo.text().strip() or None,
            telefono=self.ui.campoTelefono.text().strip() or None,
            calle=self.ui.campoCalle.text().strip() or None,
            colonia=self.ui.campoColonia.text().strip() or None,
        )
        alumno.grado = None if grado == SIN_GRADO else grado
        alumno.grupo = (self.ui.campoGrupo.currentText().strip() or None)
        if alumno.grupo:
            alumno.grupo = alumno.grupo.upper()
        if self.alumno is not None:
            alumno.id = self.alumno.id
        return alumno

    def _guardar(self) -> None:
        alumno = self._recoger()

        revision = validador_persona.validar_alumno(alumno)
        if not revision.es_valido:
            self.ui.etiquetaError.setText(revision.mensaje)
            return

        self.ui.botonGuardar.setEnabled(False)
        try:
            if self.es_alta:
                self.guardado = repo_personas.dar_de_alta_alumno(alumno)
            else:
                repo_personas.actualizar_alumno(alumno)
                self.guardado = alumno
        except Exception as error:
            # Cualquier fallo, no solo el que rechaza la base: sin esto
            # un corte de red se leia como «la base rechazo la operacion».
            self.ui.etiquetaError.setText(causa_del_error(error))
            self.ui.botonGuardar.setEnabled(True)
            return

        self.accept()
