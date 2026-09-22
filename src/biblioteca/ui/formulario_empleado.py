"""Alta y modificacion de empleados (REQ-EMP-01).

El alta esta restringida al perfil administrador. La restriccion la aplica
Postgres mediante las politicas RLS, no este codigo: aqui solo se anticipa
para no dejar que el usuario llene un formulario que sera rechazado.
"""

from __future__ import annotations

from PySide6.QtWidgets import QDialog, QWidget

from biblioteca.core.errores import causa as causa_del_error
from biblioteca.core.sesion import sesion_actual
from biblioteca.modelos.persona import Empleado, Rol
from biblioteca.repositorios import personas as repo_personas
from biblioteca.servicios import validador_persona
from biblioteca.ui.estilo import COLOR_ERROR, COLOR_TENUE
from biblioteca.ui.generado.ui_formulario_empleado import Ui_FormularioEmpleado

# Lo que se ve en el desplegable, y el rol que guarda cada opcion
PERFILES = {
    "Bibliotecario": Rol.BIBLIOTECARIO,
    "Administrador": Rol.ADMINISTRADOR,
}


class FormularioEmpleado(QDialog):
    def __init__(
        self, padre: QWidget | None = None, empleado: Empleado | None = None
    ) -> None:
        super().__init__(padre)
        self.ui = Ui_FormularioEmpleado()
        self.ui.setupUi(self)

        self.empleado = empleado
        self.es_alta = empleado is None
        self.guardado: Empleado | None = None

        self.setWindowTitle(
            "Registrar empleado" if self.es_alta else "Modificar empleado"
        )
        self.ui.etiquetaError.setStyleSheet(f"color: {COLOR_ERROR};")
        self.ui.etiquetaAviso.setStyleSheet(f"color: {COLOR_TENUE};")
        self.ui.botonCancelar.setProperty("secundario", True)

        if empleado is not None:
            self._cargar(empleado)
            self.ui.campoCodigo.setEnabled(False)

        # Cambiar el perfil de acceso queda reservado al administrador,
        # **tambien al dar de alta**. Antes la restriccion solo se aplicaba al
        # modificar, de modo que cualquiera del personal podia registrar a un
        # administrador nuevo y entrar con el. La base todavia lo permite
        # (proteger_rol solo vigila el UPDATE): falta la migracion 10.
        if sesion_actual().perfil.rol != Rol.ADMINISTRADOR:
            self.ui.campoRol.setEnabled(False)
            self.ui.etiquetaRol.setText("Perfil en el sistema (solo administrador)")

        self.ui.botonGuardar.clicked.connect(self._guardar)
        self.ui.botonCancelar.clicked.connect(self.reject)
        (self.ui.campoCodigo if self.es_alta else self.ui.campoNombre).setFocus()

    def _cargar(self, empleado: Empleado) -> None:
        self.ui.campoCodigo.setText(empleado.codigo)
        self.ui.campoNombre.setText(empleado.nombre)
        self.ui.campoApellido.setText(empleado.apellido)
        self.ui.campoPuesto.setCurrentText(empleado.tipo_empleado or "")
        self.ui.campoCorreo.setText(empleado.correo or "")
        self.ui.campoTelefono.setText(empleado.telefono or "")
        self.ui.campoCalle.setText(empleado.calle or "")
        self.ui.campoColonia.setText(empleado.colonia or "")

        for etiqueta, rol in PERFILES.items():
            if rol == empleado.rol:
                self.ui.campoRol.setCurrentText(etiqueta)
                break

    def _recoger(self) -> Empleado:
        empleado = Empleado(
            codigo=self.ui.campoCodigo.text().strip(),
            nombre=self.ui.campoNombre.text().strip(),
            apellido=self.ui.campoApellido.text().strip(),
            correo=self.ui.campoCorreo.text().strip() or None,
            telefono=self.ui.campoTelefono.text().strip() or None,
            calle=self.ui.campoCalle.text().strip() or None,
            colonia=self.ui.campoColonia.text().strip() or None,
        )
        empleado.tipo_empleado = self.ui.campoPuesto.currentText().strip()
        empleado.rol = PERFILES.get(
            self.ui.campoRol.currentText(), Rol.BIBLIOTECARIO
        )
        if self.empleado is not None:
            empleado.id = self.empleado.id
        return empleado

    def _guardar(self) -> None:
        empleado = self._recoger()

        revision = validador_persona.validar_empleado(empleado)
        if not revision.es_valido:
            self.ui.etiquetaError.setText(revision.mensaje)
            return

        self.ui.botonGuardar.setEnabled(False)
        try:
            if self.es_alta:
                self.guardado = repo_personas.dar_de_alta_empleado(empleado)
            else:
                repo_personas.actualizar_empleado(empleado)
                self.guardado = empleado
        except Exception as error:
            # Cualquier fallo, no solo el que rechaza la base: sin esto
            # un corte de red se leia como «la base rechazo la operacion».
            self.ui.etiquetaError.setText(causa_del_error(error))
            self.ui.botonGuardar.setEnabled(True)
            return

        self.accept()
