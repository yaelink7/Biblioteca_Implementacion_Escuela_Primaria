"""Maestros de grupo: uno por salon, y lo heredan sus alumnos (USU-09, #76).

Se edita aqui y no en la ficha de cada nino: al empezar otro ciclo escolar
basta con corregir un renglon por salon. Lo decidio Yael el 27 de octubre
para el prototipo, y la migracion 11 lo aplica con la tabla
maestros_de_grupo.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QTableWidgetItem,
    QWidget,
)

from biblioteca.core.errores import causa as causa_del_error
from biblioteca.repositorios import personas as repo_personas
from biblioteca.ui.estilo import TENUE
from biblioteca.ui.formato import plural, salon
from biblioteca.ui.generado.ui_maestros_de_grupo import Ui_DialogoMaestros


class DialogoMaestros(QDialog):
    """Una tabla de salones: el maestro de cada uno se escribe en su renglon."""

    def __init__(self, padre: QWidget | None = None) -> None:
        super().__init__(padre)
        self.ui = Ui_DialogoMaestros()
        self.ui.setupUi(self)

        self.guardado = False
        self._originales: dict[tuple[int, str], str] = {}
        self.campos: dict[tuple[int, str], QLineEdit] = {}

        self.ui.cajaError.hide()
        cabecera = self.ui.tablaMaestros.horizontalHeader()
        cabecera.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        cabecera.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        cabecera.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        cabecera.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        self.ui.botonGuardar.clicked.connect(self._guardar)
        self.ui.botonCancelar.clicked.connect(self.reject)
        self._cargar()

    def _cargar(self) -> None:
        try:
            self._originales = repo_personas.listar_maestros()
            alumnos = repo_personas.listar_alumnos()
        except Exception as error:
            self._error(causa_del_error(error), "No se pudo consultar:")
            self.ui.botonGuardar.setEnabled(False)
            return

        cuantos: dict[tuple[int, str], int] = {}
        for alumno in alumnos:
            if alumno.grado and alumno.grupo:
                clave = (alumno.grado, alumno.grupo)
                cuantos[clave] = cuantos.get(clave, 0) + 1
        # Los salones con alumnos y los que ya tienen maestro, aunque hoy
        # esten vacios: si no, un maestro asignado se volveria invisible.
        salones = sorted(set(cuantos) | set(self._originales))

        tabla = self.ui.tablaMaestros
        tabla.setRowCount(len(salones))
        negrita = QFont(tabla.font())
        negrita.setWeight(QFont.Weight.DemiBold)
        for fila, clave in enumerate(salones):
            nombre = QTableWidgetItem(salon(*clave))
            nombre.setFont(negrita)
            tabla.setItem(fila, 0, nombre)

            campo = QLineEdit(self._originales.get(clave, ""))
            campo.setPlaceholderText("Sin asignar")
            campo.setAccessibleName(f"Maestro de {salon(*clave)}")
            self.campos[clave] = campo
            # El campo con aire alrededor, como en el prototipo, y no pegado
            # a la raya de la fila
            celda = QWidget()
            margen = QHBoxLayout(celda)
            margen.setContentsMargins(4, 8, 12, 8)
            margen.addWidget(campo)
            tabla.setCellWidget(fila, 1, celda)

            numero = QTableWidgetItem(plural(cuantos.get(clave, 0), "alumno"))
            numero.setForeground(QColor(TENUE))
            tabla.setItem(fila, 2, numero)

        if salones:
            self.campos[salones[0]].setFocus()

    def cambios(self) -> dict[tuple[int, str], str]:
        """Solo los salones que se tocaron: los demas no se reescriben."""
        return {
            clave: campo.text().strip()
            for clave, campo in self.campos.items()
            if campo.text().strip() != self._originales.get(clave, "")
        }

    def _guardar(self) -> None:
        cambios = self.cambios()
        if not cambios:
            self.accept()
            return

        self.ui.botonGuardar.setEnabled(False)
        try:
            repo_personas.guardar_maestros(cambios)
        except Exception as error:
            self._error(causa_del_error(error))
            self.ui.botonGuardar.setEnabled(True)
            return

        self.guardado = True
        self.accept()

    def _error(self, texto: str, titulo: str = "No se pudo guardar:") -> None:
        self.ui.tituloError.setText(titulo)
        self.ui.etiquetaError.setText(texto)
        self.ui.cajaError.show()
