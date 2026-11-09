# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'alumnos.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_PantallaAlumnos(object):
    def setupUi(self, PantallaAlumnos):
        if not PantallaAlumnos.objectName():
            PantallaAlumnos.setObjectName(u"PantallaAlumnos")
        PantallaAlumnos.resize(1100, 680)
        self.disposicion = QVBoxLayout(PantallaAlumnos)
        self.disposicion.setSpacing(18)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(0, 0, 0, 0)
        self.encabezado = QHBoxLayout()
        self.encabezado.setSpacing(12)
        self.encabezado.setObjectName(u"encabezado")
        self.textoEncabezado = QVBoxLayout()
        self.textoEncabezado.setSpacing(6)
        self.textoEncabezado.setObjectName(u"textoEncabezado")
        self.etiquetaTitulo = QLabel(PantallaAlumnos)
        self.etiquetaTitulo.setObjectName(u"etiquetaTitulo")

        self.textoEncabezado.addWidget(self.etiquetaTitulo)

        self.etiquetaResumen = QLabel(PantallaAlumnos)
        self.etiquetaResumen.setObjectName(u"etiquetaResumen")

        self.textoEncabezado.addWidget(self.etiquetaResumen)


        self.encabezado.addLayout(self.textoEncabezado)


        self.disposicion.addLayout(self.encabezado)

        self.filaAcciones = QHBoxLayout()
        self.filaAcciones.setSpacing(12)
        self.filaAcciones.setObjectName(u"filaAcciones")
        self.campoBusqueda = QLineEdit(PantallaAlumnos)
        self.campoBusqueda.setObjectName(u"campoBusqueda")
        self.campoBusqueda.setMinimumSize(QSize(340, 44))
        self.campoBusqueda.setClearButtonEnabled(True)

        self.filaAcciones.addWidget(self.campoBusqueda)

        self.botonMaestros = QPushButton(PantallaAlumnos)
        self.botonMaestros.setObjectName(u"botonMaestros")
        self.botonMaestros.setMinimumHeight(44)
        self.botonMaestros.setProperty(u"secundario", True)

        self.filaAcciones.addWidget(self.botonMaestros)

        self.botonNuevo = QPushButton(PantallaAlumnos)
        self.botonNuevo.setObjectName(u"botonNuevo")
        self.botonNuevo.setMinimumHeight(44)

        self.filaAcciones.addWidget(self.botonNuevo)

        self.espacioAcciones = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.filaAcciones.addItem(self.espacioAcciones)


        self.disposicion.addLayout(self.filaAcciones)

        self.cuerpo = QHBoxLayout()
        self.cuerpo.setSpacing(18)
        self.cuerpo.setObjectName(u"cuerpo")
        self.tarjetaTabla = QFrame(PantallaAlumnos)
        self.tarjetaTabla.setObjectName(u"tarjetaTabla")
        self.disposicionTarjeta = QVBoxLayout(self.tarjetaTabla)
        self.disposicionTarjeta.setSpacing(0)
        self.disposicionTarjeta.setObjectName(u"disposicionTarjeta")
        self.disposicionTarjeta.setContentsMargins(1, 4, 1, 8)
        self.tablaAlumnos = QTableWidget(self.tarjetaTabla)
        if (self.tablaAlumnos.columnCount() < 5):
            self.tablaAlumnos.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tablaAlumnos.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tablaAlumnos.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tablaAlumnos.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tablaAlumnos.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tablaAlumnos.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tablaAlumnos.setObjectName(u"tablaAlumnos")
        self.tablaAlumnos.setFrameShape(QFrame.NoFrame)
        self.tablaAlumnos.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablaAlumnos.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tablaAlumnos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaAlumnos.setShowGrid(False)
        self.tablaAlumnos.setWordWrap(False)
        self.tablaAlumnos.setSortingEnabled(True)
        self.tablaAlumnos.horizontalHeader().setHighlightSections(False)
        self.tablaAlumnos.horizontalHeader().setStretchLastSection(True)
        self.tablaAlumnos.verticalHeader().setVisible(False)
        self.tablaAlumnos.verticalHeader().setDefaultSectionSize(46)

        self.disposicionTarjeta.addWidget(self.tablaAlumnos)

        self.etiquetaVacio = QLabel(self.tarjetaTabla)
        self.etiquetaVacio.setObjectName(u"etiquetaVacio")
        self.etiquetaVacio.setWordWrap(True)
        self.etiquetaVacio.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.etiquetaVacio.sizePolicy().hasHeightForWidth())
        self.etiquetaVacio.setSizePolicy(sizePolicy)

        self.disposicionTarjeta.addWidget(self.etiquetaVacio)


        self.cuerpo.addWidget(self.tarjetaTabla)

        self.columnaPanel = QVBoxLayout()
        self.columnaPanel.setSpacing(0)
        self.columnaPanel.setObjectName(u"columnaPanel")
        self.panelAlumno = QFrame(PantallaAlumnos)
        self.panelAlumno.setObjectName(u"panelAlumno")
        self.panelAlumno.setMinimumWidth(300)
        self.panelAlumno.setMaximumWidth(340)
        self.disposicionPanel = QVBoxLayout(self.panelAlumno)
        self.disposicionPanel.setSpacing(18)
        self.disposicionPanel.setObjectName(u"disposicionPanel")
        self.disposicionPanel.setContentsMargins(22, 22, 22, 24)
        self.etiquetaPanel = QLabel(self.panelAlumno)
        self.etiquetaPanel.setObjectName(u"etiquetaPanel")

        self.disposicionPanel.addWidget(self.etiquetaPanel)

        self.etiquetaPanelVacio = QLabel(self.panelAlumno)
        self.etiquetaPanelVacio.setObjectName(u"etiquetaPanelVacio")
        self.etiquetaPanelVacio.setWordWrap(True)

        self.disposicionPanel.addWidget(self.etiquetaPanelVacio)

        self.fichaAlumno = QWidget(self.panelAlumno)
        self.fichaAlumno.setObjectName(u"fichaAlumno")
        self.disposicionFicha = QVBoxLayout(self.fichaAlumno)
        self.disposicionFicha.setSpacing(18)
        self.disposicionFicha.setObjectName(u"disposicionFicha")
        self.disposicionFicha.setContentsMargins(0, 0, 0, 0)
        self.cabezaFicha = QHBoxLayout()
        self.cabezaFicha.setSpacing(12)
        self.cabezaFicha.setObjectName(u"cabezaFicha")
        self.avatar = QLabel(self.fichaAlumno)
        self.avatar.setObjectName(u"avatar")
        self.avatar.setMinimumSize(QSize(44, 44))
        self.avatar.setMaximumSize(QSize(44, 44))
        self.avatar.setAlignment(Qt.AlignCenter)

        self.cabezaFicha.addWidget(self.avatar, 0, Qt.AlignTop)

        self.nombreFicha = QVBoxLayout()
        self.nombreFicha.setSpacing(2)
        self.nombreFicha.setObjectName(u"nombreFicha")
        self.etiquetaNombre = QLabel(self.fichaAlumno)
        self.etiquetaNombre.setObjectName(u"etiquetaNombre")
        self.etiquetaNombre.setWordWrap(True)

        self.nombreFicha.addWidget(self.etiquetaNombre)

        self.etiquetaDetalle = QLabel(self.fichaAlumno)
        self.etiquetaDetalle.setObjectName(u"etiquetaDetalle")
        self.etiquetaDetalle.setWordWrap(True)

        self.nombreFicha.addWidget(self.etiquetaDetalle)


        self.cabezaFicha.addLayout(self.nombreFicha)


        self.disposicionFicha.addLayout(self.cabezaFicha)

        self.cajaSituacion = QFrame(self.fichaAlumno)
        self.cajaSituacion.setObjectName(u"cajaSituacion")
        self.disposicionCaja = QHBoxLayout(self.cajaSituacion)
        self.disposicionCaja.setSpacing(10)
        self.disposicionCaja.setObjectName(u"disposicionCaja")
        self.disposicionCaja.setContentsMargins(14, 12, 14, 12)
        self.iconoCaja = QLabel(self.cajaSituacion)
        self.iconoCaja.setObjectName(u"iconoCaja")
        self.iconoCaja.setMinimumSize(QSize(20, 20))
        self.iconoCaja.setMaximumSize(QSize(20, 20))

        self.disposicionCaja.addWidget(self.iconoCaja, 0, Qt.AlignTop)

        self.textosCaja = QVBoxLayout()
        self.textosCaja.setSpacing(2)
        self.textosCaja.setObjectName(u"textosCaja")
        self.tituloCaja = QLabel(self.cajaSituacion)
        self.tituloCaja.setObjectName(u"tituloCaja")
        self.tituloCaja.setWordWrap(True)

        self.textosCaja.addWidget(self.tituloCaja)

        self.textoCaja = QLabel(self.cajaSituacion)
        self.textoCaja.setObjectName(u"textoCaja")
        self.textoCaja.setWordWrap(True)

        self.textosCaja.addWidget(self.textoCaja)


        self.disposicionCaja.addLayout(self.textosCaja)


        self.disposicionFicha.addWidget(self.cajaSituacion)

        self.datosAlumno = QGridLayout()
        self.datosAlumno.setObjectName(u"datosAlumno")
        self.datosAlumno.setHorizontalSpacing(16)
        self.datosAlumno.setVerticalSpacing(10)
        self.datoCurp = QLabel(self.fichaAlumno)
        self.datoCurp.setObjectName(u"datoCurp")

        self.datosAlumno.addWidget(self.datoCurp, 0, 0, 1, 1, Qt.AlignTop)

        self.valorCurp = QLabel(self.fichaAlumno)
        self.valorCurp.setObjectName(u"valorCurp")
        self.valorCurp.setWordWrap(True)
        self.valorCurp.setProperty(u"mono", True)

        self.datosAlumno.addWidget(self.valorCurp, 0, 1, 1, 1)

        self.datoMaestro = QLabel(self.fichaAlumno)
        self.datoMaestro.setObjectName(u"datoMaestro")

        self.datosAlumno.addWidget(self.datoMaestro, 1, 0, 1, 1, Qt.AlignTop)

        self.valorMaestro = QLabel(self.fichaAlumno)
        self.valorMaestro.setObjectName(u"valorMaestro")
        self.valorMaestro.setWordWrap(True)

        self.datosAlumno.addWidget(self.valorMaestro, 1, 1, 1, 1)

        self.datoTelefono = QLabel(self.fichaAlumno)
        self.datoTelefono.setObjectName(u"datoTelefono")

        self.datosAlumno.addWidget(self.datoTelefono, 2, 0, 1, 1, Qt.AlignTop)

        self.valorTelefono = QLabel(self.fichaAlumno)
        self.valorTelefono.setObjectName(u"valorTelefono")
        self.valorTelefono.setWordWrap(True)
        self.valorTelefono.setProperty(u"mono", True)

        self.datosAlumno.addWidget(self.valorTelefono, 2, 1, 1, 1)

        self.datoDireccion = QLabel(self.fichaAlumno)
        self.datoDireccion.setObjectName(u"datoDireccion")

        self.datosAlumno.addWidget(self.datoDireccion, 3, 0, 1, 1, Qt.AlignTop)

        self.valorDireccion = QLabel(self.fichaAlumno)
        self.valorDireccion.setObjectName(u"valorDireccion")
        self.valorDireccion.setWordWrap(True)

        self.datosAlumno.addWidget(self.valorDireccion, 3, 1, 1, 1)

        self.datosAlumno.setColumnStretch(1, 1)

        self.disposicionFicha.addLayout(self.datosAlumno)


        self.disposicionPanel.addWidget(self.fichaAlumno)

        self.accionesPanel = QVBoxLayout()
        self.accionesPanel.setSpacing(10)
        self.accionesPanel.setObjectName(u"accionesPanel")
        self.botonEditar = QPushButton(self.panelAlumno)
        self.botonEditar.setObjectName(u"botonEditar")
        self.botonEditar.setMinimumHeight(44)
        self.botonEditar.setEnabled(False)

        self.accionesPanel.addWidget(self.botonEditar)

        self.botonHistorial = QPushButton(self.panelAlumno)
        self.botonHistorial.setObjectName(u"botonHistorial")
        self.botonHistorial.setMinimumHeight(44)
        self.botonHistorial.setEnabled(False)
        self.botonHistorial.setProperty(u"secundario", True)

        self.accionesPanel.addWidget(self.botonHistorial)


        self.disposicionPanel.addLayout(self.accionesPanel)


        self.columnaPanel.addWidget(self.panelAlumno)

        self.espacioPanel = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.columnaPanel.addItem(self.espacioPanel)

        self.columnaPanel.setStretch(1, 1)

        self.cuerpo.addLayout(self.columnaPanel)

        self.cuerpo.setStretch(0, 1)

        self.disposicion.addLayout(self.cuerpo)

        self.disposicion.setStretch(2, 1)
        QWidget.setTabOrder(self.campoBusqueda, self.botonMaestros)
        QWidget.setTabOrder(self.botonMaestros, self.botonNuevo)
        QWidget.setTabOrder(self.botonNuevo, self.tablaAlumnos)
        QWidget.setTabOrder(self.tablaAlumnos, self.botonEditar)
        QWidget.setTabOrder(self.botonEditar, self.botonHistorial)

        self.retranslateUi(PantallaAlumnos)

        QMetaObject.connectSlotsByName(PantallaAlumnos)
    # setupUi

    def retranslateUi(self, PantallaAlumnos):
        PantallaAlumnos.setWindowTitle(QCoreApplication.translate("PantallaAlumnos", u"Alumnos", None))
        self.etiquetaTitulo.setText(QCoreApplication.translate("PantallaAlumnos", u"Alumnos", None))
        self.etiquetaTitulo.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"titulo", None))
        self.etiquetaResumen.setText("")
        self.etiquetaResumen.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"resumen", None))
        self.campoBusqueda.setPlaceholderText(QCoreApplication.translate("PantallaAlumnos", u"Nombre, c\u00f3digo, CURP o sal\u00f3n (4B)", None))
        self.campoBusqueda.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"busqueda", None))
        self.botonMaestros.setText(QCoreApplication.translate("PantallaAlumnos", u"Maestros de grupo", None))
        self.botonNuevo.setText(QCoreApplication.translate("PantallaAlumnos", u"Registrar alumno", None))
        self.tarjetaTabla.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"tarjeta", None))
        ___qtablewidgetitem = self.tablaAlumnos.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PantallaAlumnos", u"C\u00f3digo", None))
        ___qtablewidgetitem1 = self.tablaAlumnos.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PantallaAlumnos", u"Alumno", None))
        ___qtablewidgetitem2 = self.tablaAlumnos.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PantallaAlumnos", u"Sal\u00f3n", None))
        ___qtablewidgetitem3 = self.tablaAlumnos.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PantallaAlumnos", u"Contacto del tutor", None))
        ___qtablewidgetitem4 = self.tablaAlumnos.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PantallaAlumnos", u"Situaci\u00f3n", None))
        self.etiquetaVacio.setText(QCoreApplication.translate("PantallaAlumnos", u"No hay alumnos registrados.", None))
        self.etiquetaVacio.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"tablaVacia", None))
        self.panelAlumno.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"panel", None))
        self.etiquetaPanel.setText(QCoreApplication.translate("PantallaAlumnos", u"Alumno seleccionado", None))
        self.etiquetaPanel.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"etiquetaPanel", None))
        self.etiquetaPanelVacio.setText(QCoreApplication.translate("PantallaAlumnos", u"Elige un alumno para ver su ficha, su pr\u00e9stamo y su historial.", None))
        self.etiquetaPanelVacio.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"panelVacio", None))
        self.avatar.setText("")
        self.avatar.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"avatar", None))
        self.etiquetaNombre.setText("")
        self.etiquetaNombre.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"nombrePanel", None))
        self.etiquetaDetalle.setText("")
        self.etiquetaDetalle.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"detallePanel", None))
        self.cajaSituacion.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"caja", None))
        self.iconoCaja.setText("")
        self.tituloCaja.setText("")
        self.tituloCaja.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"tituloCaja", None))
        self.textoCaja.setText("")
        self.textoCaja.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"textoCaja", None))
        self.datoCurp.setText(QCoreApplication.translate("PantallaAlumnos", u"CURP", None))
        self.datoCurp.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"dato", None))
        self.valorCurp.setText("")
        self.valorCurp.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"valor", None))
        self.datoMaestro.setText(QCoreApplication.translate("PantallaAlumnos", u"Maestro", None))
        self.datoMaestro.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"dato", None))
        self.valorMaestro.setText("")
        self.valorMaestro.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"valor", None))
        self.datoTelefono.setText(QCoreApplication.translate("PantallaAlumnos", u"Tel. del tutor", None))
        self.datoTelefono.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"dato", None))
        self.valorTelefono.setText("")
        self.valorTelefono.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"valor", None))
        self.datoDireccion.setText(QCoreApplication.translate("PantallaAlumnos", u"Direcci\u00f3n", None))
        self.datoDireccion.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"dato", None))
        self.valorDireccion.setText("")
        self.valorDireccion.setProperty(u"rol", QCoreApplication.translate("PantallaAlumnos", u"valor", None))
        self.botonEditar.setText(QCoreApplication.translate("PantallaAlumnos", u"Modificar", None))
        self.botonHistorial.setText(QCoreApplication.translate("PantallaAlumnos", u"Ver historial", None))
    # retranslateUi

