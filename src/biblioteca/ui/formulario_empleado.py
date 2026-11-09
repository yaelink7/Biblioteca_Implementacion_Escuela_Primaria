"""Alta y modificacion de empleados (REQ-EMP-01).

Cambiar el perfil de acceso esta reservado al administrador. La restriccion
la aplica Postgres (proteger_rol y las politicas RLS), no este codigo: aqui
solo se anticipa, con el candado y una linea que dice por que, para no dejar
que el usuario llene un formulario que sera rechazado.
"""

from __future__ import annotations

from PySide6.QtWidgets import QDialog, QWidget

from biblioteca.core.errores import causa as causa_del_error
from biblioteca.core.sesion import sesion_actual
from biblioteca.modelos.persona import Empleado, Rol
from biblioteca.repositorios import personas as repo_personas
from biblioteca.servicios import validador_persona
from biblioteca.ui.generado.ui_formulario_empleado import Ui_FormularioEmpleado

# Lo que se ve en el desplegable, y el rol que guarda cada opcion
PERFILES = {
    "Bibliotecario": Rol.BIBLIOTECARIO,
    "Administrador": Rol.ADMINISTRADOR,
}

# Los puestos de la biblioteca. La lista se puede escribir: un puesto que no
# este aqui se teclea y se guarda igual.
PUESTOS = ("Bibliotecaria", "Auxiliar", "Docente encargado", "Dirección")

SOLO_ADMINISTRADOR = "Solo un administrador asigna o cambia perfiles de acceso."
PROPIO = "No puedes cambiar tu propio perfil de acceso."
ADMINISTRADOR = "El administrador además puede cambiar perfiles de acceso."


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

        titulo = "Registrar empleado" if self.es_alta else "Modificar empleado"
        self.setWindowTitle(titulo)
        self.ui.etiquetaEncabezado.setText(titulo)
        # En el alta no lleva subtitulo, como el prototipo
        self.ui.etiquetaSubtitulo.setText("" if self.es_alta else empleado.nombre_completo)
        self.ui.etiquetaSubtitulo.setVisible(not self.es_alta)
        self.ui.cajaError.hide()

        self.ui.campoPuesto.setEditable(True)
        self.ui.campoPuesto.addItems(PUESTOS)
        self.ui.campoPuesto.setCurrentIndex(-1)
        self.ui.campoPuesto.lineEdit().setPlaceholderText("Elige o escribe el puesto")

        if empleado is not None:
            self._cargar(empleado)
            self.ui.campoCodigo.setEnabled(False)

        self._bloquear_perfil()

        self.ui.botonGuardar.clicked.connect(self._guardar)
        self.ui.botonCancelar.clicked.connect(self.reject)
        (self.ui.campoCodigo if self.es_alta else self.ui.campoNombre).setFocus()

    def _bloquear_perfil(self) -> None:
        """El candado del perfil de acceso, y la razon debajo.

        Cambiarlo queda reservado al administrador, **tambien al dar de
        alta**: antes la restriccion solo se aplicaba al modificar, de modo
        que cualquiera del personal podia registrar a un administrador nuevo
        y entrar con el. Desde la migracion 10 la base tambien lo rechaza.
        Nadie cambia el suyo: proteger_rol lo rechaza aunque sea administrador.
        """
        yo = sesion_actual().perfil
        es_propio = not self.es_alta and self.empleado.id == yo.id
        if yo.rol != Rol.ADMINISTRADOR:
            self.ui.campoRol.setEnabled(False)
            self.ui.notaRol.setText(SOLO_ADMINISTRADOR)
        elif es_propio:
            self.ui.campoRol.setEnabled(False)
            self.ui.notaRol.setText(PROPIO)
        else:
            self.ui.notaRol.setText(ADMINISTRADOR)

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
            empleado.numero = self.empleado.numero
            empleado.codigo_postal = self.empleado.codigo_postal
            empleado.fecha_ingreso = self.empleado.fecha_ingreso
        return empleado

    def _mostrar_error(self, titulo: str, texto: str) -> None:
        """El recuadro rojo de arriba: que paso y que corregir."""
        self.ui.tituloError.setText(titulo)
        self.ui.etiquetaError.setText(texto)
        self.ui.cajaError.show()

    def _guardar(self) -> None:
        empleado = self._recoger()

        revision = validador_persona.validar_empleado(empleado)
        if not revision.es_valido:
            self._mostrar_error("Revisa estos datos:", revision.mensaje)
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
            self._mostrar_error("No se pudo guardar:", causa_del_error(error))
            self.ui.botonGuardar.setEnabled(True)
            return

        self.accept()
