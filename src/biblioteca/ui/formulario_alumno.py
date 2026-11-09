"""Alta y modificacion de alumnos (REQ-USU-01, REQ-USU-03).

No crea cuenta de acceso: la bibliotecaria registra la ficha de un nino de
primaria sin darle correo ni contrasena. Desde la reunion con la escuela el
formulario lleva la CURP (USU-07) y los datos del tutor (USU-08), y ya no
pide correo: la escuela confirmo que no funciona con las familias. El
maestro de grupo no se escribe aqui: se hereda del salon (USU-09).
"""

from __future__ import annotations

from html import escape

from PySide6.QtWidgets import QDialog, QWidget

from biblioteca.core.errores import causa as causa_del_error
from biblioteca.modelos.persona import Alumno
from biblioteca.repositorios import personas as repo_personas
from biblioteca.servicios import validador_persona
from biblioteca.ui.apariencia import ruta_para_hoja
from biblioteca.ui.estilo import TENUE
from biblioteca.ui.generado.ui_formulario_alumno import Ui_FormularioAlumno

GRADOS = (1, 2, 3, 4, 5, 6)
GRUPOS = ("A", "B", "C", "D")
SIN_GRADO = "Sin asignar"
SIN_GRUPO = "—"


class FormularioAlumno(QDialog):
    def __init__(
        self,
        padre: QWidget | None = None,
        alumno: Alumno | None = None,
        maestros: dict[tuple[int, str], str] | None = None,
    ) -> None:
        super().__init__(padre)
        self.ui = Ui_FormularioAlumno()
        self.ui.setupUi(self)

        self.alumno = alumno
        self.es_alta = alumno is None
        self.guardado: Alumno | None = None
        self.texto_maestro = ""
        self.maestros = maestros if maestros is not None else self._consultar_maestros()

        titulo = "Registrar alumno" if self.es_alta else "Modificar alumno"
        self.setWindowTitle(titulo)
        self.ui.etiquetaEncabezado.setText(titulo)
        self.ui.etiquetaSubtitulo.setText(
            "Sin correo: la escuela se comunica con el tutor por teléfono."
            if self.es_alta else alumno.nombre_completo
        )
        self.ui.cajaError.hide()
        self._preparar_listas()

        if alumno is not None:
            self._cargar(alumno)
            # El codigo identifica al alumno en los prestamos ya registrados
            self.ui.campoCodigo.setEnabled(False)

        self.ui.campoCurp.textEdited.connect(self._curp_en_mayusculas)
        self.ui.campoGrado.currentIndexChanged.connect(self._mostrar_maestro)
        self.ui.campoGrupo.currentIndexChanged.connect(self._mostrar_maestro)
        self.ui.botonGuardar.clicked.connect(self._guardar)
        self.ui.botonCancelar.clicked.connect(self.reject)
        self._mostrar_maestro()
        (self.ui.campoCodigo if self.es_alta else self.ui.campoNombre).setFocus()

    def _consultar_maestros(self) -> dict[tuple[int, str], str]:
        """Sin la pantalla de Alumnos detras, el formulario los pide solo.

        Es informativo: si la consulta falla, el formulario sigue sirviendo y
        el maestro simplemente no se muestra.
        """
        try:
            return repo_personas.listar_maestros()
        except Exception:
            return {}

    def _preparar_listas(self) -> None:
        self.ui.campoGrado.addItem(SIN_GRADO, None)
        for grado in GRADOS:
            self.ui.campoGrado.addItem(f"{grado}.º", grado)
        self.ui.campoGrupo.addItem(SIN_GRUPO, None)
        for grupo in GRUPOS:
            self.ui.campoGrupo.addItem(grupo, grupo)

    def _cargar(self, alumno: Alumno) -> None:
        self.ui.campoCodigo.setText(alumno.codigo)
        self.ui.campoCurp.setText(alumno.curp or "")
        self.ui.campoNombre.setText(alumno.nombre)
        self.ui.campoApellido.setText(alumno.apellido)
        self.poner_grado(alumno.grado)
        self.poner_grupo(alumno.grupo)
        self.ui.campoTelefono.setText(alumno.telefono or "")
        self.ui.campoCalle.setText(alumno.calle or "")
        self.ui.campoColonia.setText(alumno.colonia or "")

    def poner_grado(self, grado: int | None) -> None:
        indice = self.ui.campoGrado.findData(grado)
        self.ui.campoGrado.setCurrentIndex(max(0, indice))

    def poner_grupo(self, grupo: str | None) -> None:
        """Elige el grupo; uno fuera de la lista (como una E) se agrega.

        La lista trae los cuatro grupos de la escuela, pero la base acepta
        cualquier letra: un alumno ya registrado en otro grupo no lo pierde
        al abrir su ficha.
        """
        if grupo and self.ui.campoGrupo.findData(grupo) < 0:
            self.ui.campoGrupo.addItem(grupo, grupo)
        self.ui.campoGrupo.setCurrentIndex(max(0, self.ui.campoGrupo.findData(grupo)))

    def _curp_en_mayusculas(self, texto: str) -> None:
        """La CURP se escribe en mayusculas, como en el acta."""
        if texto != texto.upper():
            posicion = self.ui.campoCurp.cursorPosition()
            self.ui.campoCurp.setText(texto.upper())
            self.ui.campoCurp.setCursorPosition(posicion)

    def _mostrar_maestro(self) -> None:
        """El maestro del salon elegido: se hereda, no se captura aqui."""
        grado = self.ui.campoGrado.currentData()
        grupo = self.ui.campoGrupo.currentData()
        if not (grado and grupo):
            texto = "Se muestra al elegir grado y grupo."
        else:
            texto = self.maestros.get((grado, grupo)) or (
                "Este salón aún no tiene maestro. Se asigna en «Maestros de grupo».")
        self.texto_maestro = texto
        # El birrete del prototipo va dentro del texto: una etiqueta de Qt no
        # lleva imagen y texto a la vez si no es como texto enriquecido.
        birrete = ruta_para_hoja("maestro", TENUE)
        self.ui.valorMaestro.setText(
            f'<img src="{birrete}" width="16" height="16"> &nbsp;{escape(texto, quote=False)}')

    def _recoger(self) -> Alumno:
        alumno = Alumno(
            codigo=self.ui.campoCodigo.text().strip(),
            nombre=self.ui.campoNombre.text().strip(),
            apellido=self.ui.campoApellido.text().strip(),
            telefono=self.ui.campoTelefono.text().strip() or None,
            calle=self.ui.campoCalle.text().strip() or None,
            colonia=self.ui.campoColonia.text().strip() or None,
        )
        alumno.curp = self.ui.campoCurp.text().strip().upper() or None
        alumno.grado = self.ui.campoGrado.currentData()
        alumno.grupo = self.ui.campoGrupo.currentData()
        if self.alumno is not None:
            alumno.id = self.alumno.id
            # El formulario ya no muestra el correo, pero tampoco lo borra: si
            # una ficha vieja lo tiene, se queda como estaba.
            alumno.correo = self.alumno.correo
            alumno.numero = self.alumno.numero
            alumno.codigo_postal = self.alumno.codigo_postal
        return alumno

    def _mostrar_error(self, titulo: str, texto: str) -> None:
        """El recuadro rojo de arriba: que paso y que corregir."""
        self.ui.tituloError.setText(titulo)
        self.ui.etiquetaError.setText(texto)
        self.ui.cajaError.show()

    def _guardar(self) -> None:
        alumno = self._recoger()

        revision = validador_persona.validar_alumno(alumno)
        if not revision.es_valido:
            self._mostrar_error("Revisa estos datos:", revision.mensaje)
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
            self._mostrar_error("No se pudo guardar:", causa_del_error(error))
            self.ui.botonGuardar.setEnabled(True)
            return

        self.accept()

