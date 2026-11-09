"""Pantalla de prestamos activos y devoluciones.

Cubre REQ-PRE-01, REQ-PRE-02 y REQ-PRE-03. Es el reemplazo directo del
cuaderno: aqui se ve de un vistazo quien tiene cada ejemplar y cuales ya
se pasaron de la fecha.

En el diseno «Lapiz» la tabla tiene tres vistas —todos, por vencer y
vencidos— y a la derecha el panel del prestamo elegido, con el telefono del
tutor y quien lo registro. Las cuatro piezas las aprobo Yael el 8 de
noviembre de 2026. Los dias que faltan o sobran los calcula la base.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from biblioteca.core.config import DIAS_DE_PRESTAMO
from biblioteca.core.errores import mensaje as mensaje_de_error
from biblioteca.modelos.persona import Alumno
from biblioteca.modelos.prestamo import Prestamo
from biblioteca.repositorios import prestamos as repo_prestamos
from biblioteca.repositorios.prestamos import DetallePrestamo
from biblioteca.ui.apariencia import icono
from biblioteca.ui.componentes import (
    CeldaOrdenada,
    DelegadoFilaElegida,
    fuente_mono,
    PestanaVista,
    volver_a_elegir,
    mostrar_caja,
    poner_icono,
)
from biblioteca.ui.estilo import (
    MARCADOR,
    ROJO,
    TEXTO,
    TENUE,
    repulir,
    rotular,
    rotular_encabezados,
)
from biblioteca.ui.formato import (
    dia_y_mes,
    es_salon,
    fecha_corta,
    iniciales,
    plural,
    salon,
    sin_acentos,
)
from biblioteca.ui.generado.ui_prestamos import Ui_PantallaPrestamos
from biblioteca.ui.historial_alumno import DialogoHistorial
from biblioteca.ui.nuevo_prestamo import DialogoNuevoPrestamo

TODOS, POR_VENCER, VENCIDOS = "todos", "por_vencer", "vencidos"

SIN_RESULTADOS = {
    TODOS: "No hay préstamos activos.",
    POR_VENCER: "Ningún préstamo vence en los próximos tres días.",
    VENCIDOS: "No hay préstamos vencidos.",
}


def situacion(prestamo: Prestamo) -> str:
    """La frase corta de la columna Situacion."""
    if prestamo.esta_vencido:
        return f"Vencido · {plural(prestamo.dias_de_retraso, 'día')}"
    if prestamo.dias_restantes == 0:
        return "Vence hoy"
    return f"En {plural(prestamo.dias_restantes, 'día')}"


class PantallaPrestamos(QWidget):
    """Lista lo que esta prestado y permite cerrar cada prestamo."""

    # Se avisa a la ventana para que Deudores y Alumnos no queden atrasados
    prestamos_cambiaron = Signal()

    def __init__(self, padre: QWidget | None = None) -> None:
        super().__init__(padre)
        self.ui = Ui_PantallaPrestamos()
        self.ui.setupUi(self)

        self._prestamos: list[Prestamo] = []
        self._visibles: list[Prestamo] = []
        self._detalles: dict[int, DetallePrestamo] = {}

        self._preparar_vistas()
        self._preparar_aspecto()
        self._preparar_tabla()

        self.ui.campoFiltro.textChanged.connect(self._pintar)
        self.ui.tablaPrestamos.itemSelectionChanged.connect(self._cambio_seleccion)
        self.ui.botonNuevo.clicked.connect(self._registrar)
        self.ui.botonDevolver.clicked.connect(self._devolver)
        self.ui.botonHistorial.clicked.connect(self._ver_historial)

        self.recargar()

    # ------------------------------------------------------------------
    # Aspecto
    # ------------------------------------------------------------------

    def _preparar_vistas(self) -> None:
        """Las tres subpestañas de la barra: todos, por vencer y vencidos."""
        self.vistas = {
            TODOS: PestanaVista("Todos"),
            POR_VENCER: PestanaVista("Por vencer"),
            VENCIDOS: PestanaVista("Vencidos", alerta=True),
        }
        self._grupo_vistas = QButtonGroup(self)
        for posicion, (clave, pestana) in enumerate(self.vistas.items()):
            pestana.setObjectName(f"vista_{clave}")
            self._grupo_vistas.addButton(pestana)
            self.ui.disposicionBarra.insertWidget(posicion, pestana)
        self.vistas[TODOS].setChecked(True)
        # Solo la que se enciende repinta: la que se apaga tambien avisa
        for pestana in self.vistas.values():
            pestana.toggled.connect(lambda encendida: encendida and self._pintar())

    def _preparar_aspecto(self) -> None:
        ui = self.ui
        poner_icono(ui.botonNuevo, "mas", TEXTO)
        poner_icono(ui.botonDevolver, "devolver", TEXTO)
        poner_icono(ui.botonHistorial, "historial", TEXTO)
        ui.campoFiltro.addAction(icono("buscar", MARCADOR),
                                 QLineEdit.ActionPosition.LeadingPosition)
        rotular(ui.etiquetaPanel)
        rotular_encabezados(ui.tablaPrestamos)
        ui.tablaPrestamos.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        ui.tablaPrestamos.setItemDelegate(DelegadoFilaElegida(ui.tablaPrestamos))
        ui.valorLibro.setProperty("fuerte", True)
        ui.etiquetaVacio.hide()

    def _preparar_tabla(self) -> None:
        cabecera = self.ui.tablaPrestamos.horizontalHeader()
        cabecera.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        cabecera.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        for columna in (1, 3, 4):
            cabecera.setSectionResizeMode(columna, QHeaderView.ResizeMode.ResizeToContents)
        # Lo mas urgente arriba: ordenado por la fecha limite, como el prototipo
        cabecera.setSortIndicator(3, Qt.SortOrder.AscendingOrder)

    # ------------------------------------------------------------------
    # Datos
    # ------------------------------------------------------------------

    def recargar(self) -> None:
        try:
            self._prestamos = repo_prestamos.activos()
            self._detalles = repo_prestamos.detalles(
                [p.id for p in self._prestamos if p.id is not None])
        except Exception as error:
            QMessageBox.warning(
                self,
                "No se pudieron consultar los préstamos",
                mensaje_de_error(error),
            )
            return
        self._pintar()

    def vista(self) -> str:
        return next((clave for clave, p in self.vistas.items() if p.isChecked()), TODOS)

    def _coincide(self, prestamo: Prestamo, texto: str) -> bool:
        """Por alumno, codigo, libro, autor o salon («4B»), sin importar acentos."""
        if not texto:
            return True
        detalle = self._detalles.get(prestamo.id or -1, DetallePrestamo())
        campos = (prestamo.nombre_alumno, prestamo.titulo_libro,
                  detalle.codigo_alumno, detalle.autor)
        buscado = sin_acentos(texto)
        return (any(buscado in sin_acentos(c) for c in campos if c)
                or es_salon(texto, prestamo.grado, prestamo.grupo))

    def _filtrar(self) -> list[Prestamo]:
        """Aplica el texto y la vista en memoria.

        Son pocos registros y ya estan cargados: filtrar aqui responde al
        instante y evita una consulta por cada tecla.
        """
        texto = self.ui.campoFiltro.text().strip()
        vista = self.vista()
        resultado = []
        for p in self._prestamos:
            if vista == VENCIDOS and not p.esta_vencido:
                continue
            if vista == POR_VENCER and not p.por_vencer:
                continue
            if self._coincide(p, texto):
                resultado.append(p)
        return resultado

    def _pintar(self) -> None:
        anterior = self._seleccionado()
        elegido = anterior.id if anterior else None
        self._visibles = self._filtrar()
        tabla = self.ui.tablaPrestamos
        tabla.blockSignals(True)
        tabla.clearSelection()
        tabla.setSortingEnabled(False)
        tabla.setRowCount(len(self._visibles))

        negrita = QFont(tabla.font())
        negrita.setWeight(QFont.Weight.DemiBold)
        punto_rojo = icono("punto", ROJO, 10)
        reloj = icono("reloj", TEXTO, 15)

        for fila, p in enumerate(self._visibles):
            celdas = [
                QTableWidgetItem(p.nombre_alumno or "—"),
                CeldaOrdenada(salon(p.grado, p.grupo), f"{p.grado or 9}{p.grupo or 'z'}"),
                QTableWidgetItem(p.titulo_libro or "—"),
                CeldaOrdenada(dia_y_mes(p.fecha_limite) if p.fecha_limite else "—",
                              p.dias_restantes),
                CeldaOrdenada(situacion(p), p.dias_restantes),
            ]
            celdas[0].setData(Qt.ItemDataRole.UserRole, fila)
            celdas[0].setFont(negrita)
            for mono in (celdas[1], celdas[3]):
                mono.setFont(fuente_mono(tabla.font()))
            estado = celdas[4]
            if p.esta_vencido:
                estado.setForeground(QColor(ROJO))
                estado.setFont(negrita)
                estado.setIcon(punto_rojo)
            elif p.por_vencer:
                estado.setFont(negrita)
                estado.setIcon(reloj)
            else:
                estado.setForeground(QColor(TENUE))
            for columna, celda in enumerate(celdas):
                tabla.setItem(fila, columna, celda)

        tabla.setSortingEnabled(True)
        if elegido is not None:
            volver_a_elegir(tabla, 0, lambda i: i is not None and self._visibles[i].id == elegido)
        tabla.blockSignals(False)
        hay = bool(self._visibles)
        tabla.setVisible(hay)
        self.ui.etiquetaVacio.setVisible(not hay)
        texto = self.ui.campoFiltro.text().strip()
        self.ui.etiquetaVacio.setText(
            f"Ningún préstamo coincide con «{texto}»." if texto else SIN_RESULTADOS[self.vista()])
        self._actualizar_resumen()
        self._cambio_seleccion()

    def _actualizar_resumen(self) -> None:
        total = len(self._prestamos)
        por_vencer = sum(1 for p in self._prestamos if p.por_vencer)
        vencidos = sum(1 for p in self._prestamos if p.esta_vencido)

        self.vistas[TODOS].poner_cantidad(total)
        self.vistas[POR_VENCER].poner_cantidad(por_vencer)
        self.vistas[VENCIDOS].poner_cantidad(vencidos)

        if total == 0:
            self.ui.etiquetaResumen.setText("No hay préstamos activos.")
            return
        cola = (f'<span style="color:{ROJO}">{plural(vencidos, "vencido")}</span>'
                if vencidos else "ninguno vencido")
        self.ui.etiquetaResumen.setText(
            f"{plural(total, 'activo')} · {por_vencer} por vencer · {cola}")

    # ------------------------------------------------------------------
    # Seleccion y panel
    # ------------------------------------------------------------------

    def _seleccionado(self) -> Prestamo | None:
        filas = self.ui.tablaPrestamos.selectionModel().selectedRows()
        if not filas:
            return None
        celda = self.ui.tablaPrestamos.item(filas[0].row(), 0)
        if celda is None:
            return None
        indice = celda.data(Qt.ItemDataRole.UserRole)
        return self._visibles[indice] if indice is not None else None

    def _cambio_seleccion(self) -> None:
        prestamo = self._seleccionado()
        self.ui.botonDevolver.setEnabled(prestamo is not None)
        self.ui.botonHistorial.setEnabled(prestamo is not None)
        self._mostrar_panel(prestamo)

    def _mostrar_panel(self, p: Prestamo | None) -> None:
        ui = self.ui
        ui.etiquetaPanelVacio.setHidden(p is not None)
        ui.fichaPrestamo.setHidden(p is None)
        if p is None:
            return

        detalle = self._detalles.get(p.id or -1, DetallePrestamo())
        nombre = p.nombre_alumno or "—"
        if detalle.nombre_alumno:
            # Las mismas iniciales que en Alumnos: nombre y primer apellido
            ui.avatar.setText(iniciales(detalle.nombre_alumno, detalle.apellido_alumno or ""))
        else:
            partes = nombre.split(" ", 1)
            ui.avatar.setText(iniciales(partes[0], partes[1] if len(partes) > 1 else ""))
        ui.etiquetaNombre.setText(nombre)
        codigo = f" · {detalle.codigo_alumno}" if detalle.codigo_alumno else ""
        ui.etiquetaDetalle.setText(f"{salon(p.grado, p.grupo)}{codigo}")

        if p.esta_vencido:
            mostrar_caja(ui.cajaSituacion, ui.iconoCaja, ui.tituloCaja, ui.textoCaja,
                         "alerta", f"Venció hace {plural(p.dias_de_retraso, 'día')}",
                         "Ya aparece en el reporte de deudores.", rojo=True)
        else:
            mostrar_caja(ui.cajaSituacion, ui.iconoCaja, ui.tituloCaja, ui.textoCaja,
                         "reloj", p.resumen,
                         f"Plazo de {DIAS_DE_PRESTAMO} días que calcula la base.")

        ui.valorLibro.setText(p.titulo_libro or "—")
        ui.valorAutor.setText(detalle.autor or "—")
        ui.valorPrestado.setText(fecha_corta(p.fecha_prestamo) if p.fecha_prestamo else "—")
        ui.datoVence.setText("Vencía" if p.esta_vencido else "Vence")
        ui.valorVence.setText(fecha_corta(p.fecha_limite) if p.fecha_limite else "—")
        # Los prestamos cargados a mano no tienen quien los registro
        ui.valorRegistro.setText(detalle.registro or "—")

        telefono = detalle.telefono_tutor
        ui.valorTelefono.setText(telefono or "Sin contacto")
        ui.valorTelefono.setProperty("mono", bool(telefono))
        ui.valorTelefono.setProperty("alerta", not telefono)
        repulir(ui.valorTelefono)

    # ------------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------------

    def _registrar(self) -> None:
        dialogo = DialogoNuevoPrestamo(self)
        if dialogo.exec() and dialogo.registrado:
            # Vuelve a «Todos» y sin filtro, para que el prestamo nuevo se vea
            self.ui.campoFiltro.blockSignals(True)
            self.ui.campoFiltro.clear()
            self.ui.campoFiltro.blockSignals(False)
            self.vistas[TODOS].setChecked(True)
            self.ui.tablaPrestamos.clearSelection()
            self.recargar()
            self.prestamos_cambiaron.emit()
            self._avisar(
                f"{dialogo.alumno.nombre_completo} se llevó «{dialogo.libro.titulo}»."
            )

    def _devolver(self) -> None:
        prestamo = self._seleccionado()
        if prestamo is None or prestamo.id is None:
            return

        if not DialogoDevolucion(self, prestamo).exec():
            return

        try:
            repo_prestamos.devolver(prestamo.id)
        except Exception as error:
            QMessageBox.warning(self, "No se pudo registrar la devolución", mensaje_de_error(error))
            return

        self.ui.tablaPrestamos.clearSelection()
        self.recargar()
        self.prestamos_cambiaron.emit()
        self._avisar(f"«{prestamo.titulo_libro}» volvió al acervo.")

    def _ver_historial(self) -> None:
        prestamo = self._seleccionado()
        if prestamo is None:
            return
        detalle = self._detalles.get(prestamo.id or -1, DetallePrestamo())
        nombre = prestamo.nombre_alumno or ""
        alumno = Alumno(id=prestamo.usuario_id, codigo=detalle.codigo_alumno or "",
                        nombre=nombre, apellido="")
        alumno.grado, alumno.grupo = prestamo.grado, prestamo.grupo
        DialogoHistorial(self, alumno).exec()

    def _avisar(self, mensaje: str) -> None:
        """Confirmacion discreta en la linea de resumen, sin cuadros de dialogo."""
        self.ui.etiquetaResumen.setText(mensaje)
        self.ui.etiquetaResumen.setProperty("aviso", True)
        repulir(self.ui.etiquetaResumen)
        QTimer.singleShot(3000, self, self._quitar_aviso)

    def _quitar_aviso(self) -> None:
        self.ui.etiquetaResumen.setProperty("aviso", False)
        repulir(self.ui.etiquetaResumen)
        self._actualizar_resumen()


class DialogoDevolucion(QDialog):
    """Confirma la devolucion con los datos del prestamo a la vista.

    Es corto a proposito: una pregunta, tres datos y dos botones. La fecha de
    devolucion la pone la base al confirmar.
    """

    def __init__(self, padre: QWidget | None, prestamo: Prestamo) -> None:
        super().__init__(padre)
        self.setWindowTitle("Registrar devolución")
        self.setMinimumWidth(500)

        columna = QVBoxLayout(self)
        columna.setContentsMargins(30, 26, 30, 26)
        columna.setSpacing(16)

        titulo = QLabel("Registrar devolución")
        titulo.setProperty("rol", "tituloDialogo")
        self.pregunta = QLabel(f"¿{prestamo.nombre_alumno} devolvió «{prestamo.titulo_libro}»?")
        self.pregunta.setProperty("rol", "textoDialogo")
        self.pregunta.setWordWrap(True)
        columna.addWidget(titulo)
        columna.addWidget(self.pregunta)

        datos = QGridLayout()
        datos.setHorizontalSpacing(16)
        datos.setVerticalSpacing(8)
        filas = (
            ("Prestado", fecha_corta(prestamo.fecha_prestamo) if prestamo.fecha_prestamo else "—"),
            ("Vencía", fecha_corta(prestamo.fecha_limite) if prestamo.fecha_limite else "—"),
            ("Situación", prestamo.resumen),
        )
        for fila, (rotulo, valor) in enumerate(filas):
            dato = QLabel(rotulo)
            dato.setProperty("rol", "dato")
            texto = QLabel(valor)
            texto.setProperty("rol", "valor")
            if rotulo == "Situación" and prestamo.esta_vencido:
                texto.setProperty("alerta", True)
            datos.addWidget(dato, fila, 0)
            datos.addWidget(texto, fila, 1)
        datos.setColumnStretch(1, 1)
        columna.addLayout(datos)

        nota = QLabel("La fecha de devolución la pone la base al confirmar, "
                      "y el ejemplar vuelve al estante.")
        nota.setProperty("rol", "notaCampo")
        nota.setWordWrap(True)
        columna.addWidget(nota)

        botones = QHBoxLayout()
        botones.addStretch(1)
        self.boton_no = QPushButton("No")
        self.boton_no.setProperty("secundario", True)
        self.boton_si = QPushButton("Sí, lo devolvió")
        botones.addWidget(self.boton_no)
        botones.addWidget(self.boton_si)
        columna.addLayout(botones)

        self.boton_no.clicked.connect(self.reject)
        self.boton_si.clicked.connect(self.accept)
        self.boton_si.setDefault(True)

