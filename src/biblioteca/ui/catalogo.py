"""Pantalla del catalogo: consulta, busqueda, alta, modificacion y baja.

Cubre REQ-LIB-01, REQ-LIB-02, REQ-LIB-03 y REQ-BUS-01.

La busqueda es la funcion que el sistema Java no tenia: el bibliotecario
debia recorrer la lista completa para encontrar un titulo.

En el diseno «Lapiz» la tabla lleva a la derecha la ficha del libro elegido,
con las dos acciones que piden una seleccion: modificar y dar de baja.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QHeaderView,
    QInputDialog,
    QLineEdit,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from biblioteca.core.errores import mensaje as mensaje_de_error
from biblioteca.modelos.libro import Libro
from biblioteca.repositorios import libros as repo_libros
from biblioteca.ui.apariencia import icono
from biblioteca.ui.componentes import DelegadoFilaElegida, poner_icono
from biblioteca.ui.estilo import (
    APAGADO,
    MARCADOR,
    ROJO,
    TEXTO,
    repulir,
    rotular,
    rotular_encabezados,
)
from biblioteca.ui.formato import fecha_corta, inicial
from biblioteca.ui.formulario_libro import FormularioLibro
from biblioteca.ui.generado.ui_catalogo import Ui_PantallaCatalogo

# Espera antes de consultar mientras el usuario sigue escribiendo
MS_ANTES_DE_BUSCAR = 250


class PantallaCatalogo(QWidget):
    """Lista el acervo y permite administrarlo."""

    def __init__(self, padre: QWidget | None = None) -> None:
        super().__init__(padre)
        self.ui = Ui_PantallaCatalogo()
        self.ui.setupUi(self)

        self._libros: list[Libro] = []

        # Un temporizador evita una consulta por cada tecla pulsada
        self._temporizador = QTimer(self)
        self._temporizador.setSingleShot(True)
        self._temporizador.setInterval(MS_ANTES_DE_BUSCAR)
        self._temporizador.timeout.connect(self.recargar)

        self._preparar_aspecto()
        self._preparar_tabla()

        self.ui.campoBusqueda.textChanged.connect(self._temporizador.start)
        self.ui.casillaVerBajas.toggled.connect(self.recargar)
        self.ui.tablaLibros.itemSelectionChanged.connect(self._cambio_seleccion)
        self.ui.tablaLibros.itemDoubleClicked.connect(lambda _: self._modificar())
        self.ui.botonNuevo.clicked.connect(self._registrar)
        self.ui.botonEditar.clicked.connect(self._modificar)
        self.ui.botonBaja.clicked.connect(self._dar_de_baja)

        self.recargar()

    # ------------------------------------------------------------------
    # Tabla
    # ------------------------------------------------------------------

    def _preparar_aspecto(self) -> None:
        """Iconos y rotulos que la hoja de estilo no puede poner por si sola."""
        ui = self.ui
        poner_icono(ui.botonNuevo, "mas", TEXTO)
        poner_icono(ui.botonEditar, "editar", TEXTO)
        poner_icono(ui.botonBaja, "baja", ROJO)
        ui.campoBusqueda.addAction(icono("buscar", MARCADOR),
                                   QLineEdit.ActionPosition.LeadingPosition)
        rotular(ui.etiquetaPanel)
        rotular(ui.etiquetaPista, mayusculas=False, espaciado=0.3)
        rotular_encabezados(ui.tablaLibros)
        ui.tablaLibros.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        ui.tablaLibros.setItemDelegate(DelegadoFilaElegida(ui.tablaLibros))

    def _preparar_tabla(self) -> None:
        cabecera = self.ui.tablaLibros.horizontalHeader()
        cabecera.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        cabecera.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        for columna in (2, 3, 4):
            cabecera.setSectionResizeMode(columna, QHeaderView.ResizeMode.ResizeToContents)

    def recargar(self) -> None:
        """Trae el catalogo aplicando el texto de busqueda que haya."""
        texto = self.ui.campoBusqueda.text().strip()
        ver_bajas = self.ui.casillaVerBajas.isChecked()

        try:
            if texto:
                self._libros = repo_libros.buscar(texto)
            else:
                self._libros = repo_libros.listar(incluir_bajas=ver_bajas)
        except Exception as error:
            QMessageBox.warning(
                self,
                "No se pudo consultar el catálogo",
                mensaje_de_error(error),
            )
            return

        self._pintar()

    def _pintar(self) -> None:
        tabla = self.ui.tablaLibros
        tabla.setSortingEnabled(False)
        tabla.setRowCount(len(self._libros))

        negrita = QFont(tabla.font())
        negrita.setWeight(QFont.Weight.DemiBold)
        punto_rojo = icono("punto", ROJO, 10)

        for fila, libro in enumerate(self._libros):
            celdas = [
                libro.titulo,
                libro.autor,
                libro.tipo_libro or "—",
                str(libro.ano_publicacion) if libro.ano_publicacion else "—",
                libro.estado,
            ]
            for columna, texto in enumerate(celdas):
                celda = QTableWidgetItem(texto)
                if columna == 0:
                    # Guarda el libro en la celda para recuperarlo al seleccionar
                    celda.setData(Qt.ItemDataRole.UserRole, fila)
                    celda.setFont(negrita)
                if not libro.activo:
                    # Fuera del acervo: la fila entera se apaga
                    celda.setForeground(QColor(APAGADO))
                elif columna == 4 and libro.existencias == 0:
                    # Lo unico urgente de la tabla va en rojo, con su punto
                    celda.setForeground(QColor(ROJO))
                    celda.setFont(negrita)
                    celda.setIcon(punto_rojo)
                tabla.setItem(fila, columna, celda)

        tabla.setSortingEnabled(True)
        self._actualizar_resumen()
        self._cambio_seleccion()

    def _actualizar_resumen(self) -> None:
        total = len(self._libros)
        ejemplares = sum(l.existencias for l in self._libros if l.activo)
        disponibles = sum(1 for l in self._libros if l.activo and l.disponible)

        if self.ui.campoBusqueda.text().strip():
            texto = f"{total} resultado{'s' if total != 1 else ''}"
        else:
            texto = (
                f"{total} título{'s' if total != 1 else ''} · "
                f"{ejemplares} ejemplares · {disponibles} con disponibilidad"
            )
        self.ui.etiquetaResumen.setText(texto)

    # ------------------------------------------------------------------
    # Seleccion, ficha y acciones
    # ------------------------------------------------------------------

    def _seleccionado(self) -> Libro | None:
        filas = self.ui.tablaLibros.selectionModel().selectedRows()
        if not filas:
            return None
        celda = self.ui.tablaLibros.item(filas[0].row(), 0)
        if celda is None:
            return None
        indice = celda.data(Qt.ItemDataRole.UserRole)
        return self._libros[indice] if indice is not None else None

    def _cambio_seleccion(self) -> None:
        libro = self._seleccionado()
        self.ui.botonEditar.setEnabled(libro is not None)
        self.ui.botonBaja.setEnabled(libro is not None and libro.activo)
        self._mostrar_ficha(libro)

    def _mostrar_ficha(self, libro: Libro | None) -> None:
        """Llena el panel de la derecha con el libro elegido, o lo deja en espera."""
        ui = self.ui
        ui.etiquetaPanelVacio.setHidden(libro is not None)
        ui.fichaLibro.setHidden(libro is None)
        if libro is None:
            return

        ui.portada.setText(inicial(libro.titulo))
        ui.etiquetaLibroTitulo.setText(libro.titulo)
        ui.etiquetaLibroAutor.setText(libro.autor)
        ui.valorTipo.setText(libro.tipo_libro or "—")
        ui.valorEditorial.setText(libro.editorial or "—")
        ui.valorAno.setText(str(libro.ano_publicacion) if libro.ano_publicacion else "—")
        ui.valorPaginas.setText(str(libro.num_paginas) if libro.num_paginas else "—")

        agotado = libro.activo and libro.existencias == 0
        if not libro.activo:
            disponibles = "—"
        elif agotado:
            disponibles = "Sin ejemplares"
        else:
            disponibles = (f"{libro.existencias} "
                           f"ejemplar{'es' if libro.existencias != 1 else ''}")
        ui.valorDisponibles.setText(disponibles)
        ui.valorDisponibles.setProperty("alerta", agotado)
        repulir(ui.valorDisponibles)

        ui.cajaBaja.setHidden(libro.activo)
        if not libro.activo:
            cuando = f" el {fecha_corta(libro.dado_baja_en)}" if libro.dado_baja_en else ""
            ui.etiquetaBaja.setText(
                f"Dado de baja{cuando}. Motivo: {libro.motivo_baja or 'sin motivo'}."
            )

    def _registrar(self) -> None:
        formulario = FormularioLibro(self)
        if formulario.exec() and formulario.guardado:
            self.ui.campoBusqueda.clear()
            self.recargar()
            self._avisar(f"Se registró «{formulario.guardado.titulo}».")

    def _modificar(self) -> None:
        libro = self._seleccionado()
        if libro is None:
            return
        formulario = FormularioLibro(self, libro=libro)
        if formulario.exec() and formulario.guardado:
            self.recargar()
            self._avisar(f"Se actualizó «{formulario.guardado.titulo}».")

    def _dar_de_baja(self) -> None:
        """Baja logica (REQ-LIB-03).

        Postgres rechaza la baja si el libro tiene prestamos activos; el
        mensaje de ese rechazo es el que se muestra al bibliotecario.
        """
        libro = self._seleccionado()
        if libro is None or libro.id is None:
            return

        motivo, acepto = QInputDialog.getText(
            self,
            "Dar de baja",
            f"¿Por qué se da de baja «{libro.titulo}»?\n"
            "Por ejemplo: extravío, deterioro, donación.",
        )
        if not acepto:
            return
        if not motivo.strip():
            QMessageBox.information(
                self, "Falta el motivo", "Indica por qué se da de baja el libro."
            )
            return

        try:
            repo_libros.dar_de_baja(libro.id, motivo.strip())
        except Exception as error:
            QMessageBox.warning(self, "No se pudo dar de baja", mensaje_de_error(error))
            return

        self.recargar()
        self._avisar(f"«{libro.titulo}» quedó fuera del acervo.")

    def _avisar(self, mensaje: str) -> None:
        """Confirmacion discreta en la linea de resumen, sin cuadros de dialogo."""
        self.ui.etiquetaResumen.setText(mensaje)
        self.ui.etiquetaResumen.setProperty("aviso", True)
        repulir(self.ui.etiquetaResumen)
        # Con la pantalla como contexto: si se cierra antes, el aviso no se
        # intenta quitar de una etiqueta que ya no existe.
        QTimer.singleShot(3000, self, self._quitar_aviso)

    def _quitar_aviso(self) -> None:
        self.ui.etiquetaResumen.setProperty("aviso", False)
        repulir(self.ui.etiquetaResumen)
        self._actualizar_resumen()
