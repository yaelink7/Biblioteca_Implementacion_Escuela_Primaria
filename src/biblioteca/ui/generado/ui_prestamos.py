# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'prestamos.ui'
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

class Ui_PantallaPrestamos(object):
    def setupUi(self, PantallaPrestamos):
        if not PantallaPrestamos.objectName():
            PantallaPrestamos.setObjectName(u"PantallaPrestamos")
        PantallaPrestamos.resize(1100, 680)
        self.disposicion = QVBoxLayout(PantallaPrestamos)
        self.disposicion.setSpacing(18)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(0, 0, 0, 0)
        self.encabezado = QHBoxLayout()
        self.encabezado.setSpacing(12)
        self.encabezado.setObjectName(u"encabezado")
        self.textoEncabezado = QVBoxLayout()
        self.textoEncabezado.setSpacing(6)
        self.textoEncabezado.setObjectName(u"textoEncabezado")
        self.etiquetaTitulo = QLabel(PantallaPrestamos)
        self.etiquetaTitulo.setObjectName(u"etiquetaTitulo")

        self.textoEncabezado.addWidget(self.etiquetaTitulo)

        self.etiquetaResumen = QLabel(PantallaPrestamos)
        self.etiquetaResumen.setObjectName(u"etiquetaResumen")

        self.textoEncabezado.addWidget(self.etiquetaResumen)


        self.encabezado.addLayout(self.textoEncabezado)

        self.espacioEncabezado = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.encabezado.addItem(self.espacioEncabezado)

        self.campoFiltro = QLineEdit(PantallaPrestamos)
        self.campoFiltro.setObjectName(u"campoFiltro")
        self.campoFiltro.setMinimumSize(QSize(300, 44))
        self.campoFiltro.setClearButtonEnabled(True)

        self.encabezado.addWidget(self.campoFiltro, 0, Qt.AlignBottom)

        self.botonNuevo = QPushButton(PantallaPrestamos)
        self.botonNuevo.setObjectName(u"botonNuevo")
        self.botonNuevo.setMinimumHeight(44)

        self.encabezado.addWidget(self.botonNuevo, 0, Qt.AlignBottom)


        self.disposicion.addLayout(self.encabezado)

        self.cuerpo = QHBoxLayout()
        self.cuerpo.setSpacing(18)
        self.cuerpo.setObjectName(u"cuerpo")
        self.tarjetaTabla = QFrame(PantallaPrestamos)
        self.tarjetaTabla.setObjectName(u"tarjetaTabla")
        self.disposicionTarjeta = QVBoxLayout(self.tarjetaTabla)
        self.disposicionTarjeta.setSpacing(0)
        self.disposicionTarjeta.setObjectName(u"disposicionTarjeta")
        self.disposicionTarjeta.setContentsMargins(1, 0, 1, 8)
        self.barraTabla = QFrame(self.tarjetaTabla)
        self.barraTabla.setObjectName(u"barraTabla")
        self.barraTabla.setMinimumHeight(52)
        self.barraTabla.setMaximumHeight(52)
        self.disposicionBarra = QHBoxLayout(self.barraTabla)
        self.disposicionBarra.setSpacing(2)
        self.disposicionBarra.setObjectName(u"disposicionBarra")
        self.disposicionBarra.setContentsMargins(10, 0, 16, 0)
        self.espacioBarra = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.disposicionBarra.addItem(self.espacioBarra)


        self.disposicionTarjeta.addWidget(self.barraTabla)

        self.tablaPrestamos = QTableWidget(self.tarjetaTabla)
        if (self.tablaPrestamos.columnCount() < 5):
            self.tablaPrestamos.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tablaPrestamos.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tablaPrestamos.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tablaPrestamos.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tablaPrestamos.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tablaPrestamos.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tablaPrestamos.setObjectName(u"tablaPrestamos")
        self.tablaPrestamos.setFrameShape(QFrame.NoFrame)
        self.tablaPrestamos.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablaPrestamos.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tablaPrestamos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaPrestamos.setShowGrid(False)
        self.tablaPrestamos.setWordWrap(False)
        self.tablaPrestamos.setSortingEnabled(True)
        self.tablaPrestamos.horizontalHeader().setHighlightSections(False)
        self.tablaPrestamos.horizontalHeader().setStretchLastSection(True)
        self.tablaPrestamos.verticalHeader().setVisible(False)
        self.tablaPrestamos.verticalHeader().setDefaultSectionSize(46)

        self.disposicionTarjeta.addWidget(self.tablaPrestamos)

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
        self.panelPrestamo = QFrame(PantallaPrestamos)
        self.panelPrestamo.setObjectName(u"panelPrestamo")
        self.panelPrestamo.setMinimumWidth(300)
        self.panelPrestamo.setMaximumWidth(340)
        self.disposicionPanel = QVBoxLayout(self.panelPrestamo)
        self.disposicionPanel.setSpacing(18)
        self.disposicionPanel.setObjectName(u"disposicionPanel")
        self.disposicionPanel.setContentsMargins(22, 22, 22, 24)
        self.etiquetaPanel = QLabel(self.panelPrestamo)
        self.etiquetaPanel.setObjectName(u"etiquetaPanel")

        self.disposicionPanel.addWidget(self.etiquetaPanel)

        self.etiquetaPanelVacio = QLabel(self.panelPrestamo)
        self.etiquetaPanelVacio.setObjectName(u"etiquetaPanelVacio")
        self.etiquetaPanelVacio.setWordWrap(True)

        self.disposicionPanel.addWidget(self.etiquetaPanelVacio)

        self.fichaPrestamo = QWidget(self.panelPrestamo)
        self.fichaPrestamo.setObjectName(u"fichaPrestamo")
        self.disposicionFicha = QVBoxLayout(self.fichaPrestamo)
        self.disposicionFicha.setSpacing(18)
        self.disposicionFicha.setObjectName(u"disposicionFicha")
        self.disposicionFicha.setContentsMargins(0, 0, 0, 0)
        self.cabezaFicha = QHBoxLayout()
        self.cabezaFicha.setSpacing(12)
        self.cabezaFicha.setObjectName(u"cabezaFicha")
        self.avatar = QLabel(self.fichaPrestamo)
        self.avatar.setObjectName(u"avatar")
        self.avatar.setMinimumSize(QSize(44, 44))
        self.avatar.setMaximumSize(QSize(44, 44))
        self.avatar.setAlignment(Qt.AlignCenter)

        self.cabezaFicha.addWidget(self.avatar, 0, Qt.AlignTop)

        self.nombreFicha = QVBoxLayout()
        self.nombreFicha.setSpacing(2)
        self.nombreFicha.setObjectName(u"nombreFicha")
        self.etiquetaNombre = QLabel(self.fichaPrestamo)
        self.etiquetaNombre.setObjectName(u"etiquetaNombre")
        self.etiquetaNombre.setWordWrap(True)

        self.nombreFicha.addWidget(self.etiquetaNombre)

        self.etiquetaDetalle = QLabel(self.fichaPrestamo)
        self.etiquetaDetalle.setObjectName(u"etiquetaDetalle")
        self.etiquetaDetalle.setWordWrap(True)

        self.nombreFicha.addWidget(self.etiquetaDetalle)


        self.cabezaFicha.addLayout(self.nombreFicha)


        self.disposicionFicha.addLayout(self.cabezaFicha)

        self.cajaSituacion = QFrame(self.fichaPrestamo)
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

        self.datosPrestamo = QGridLayout()
        self.datosPrestamo.setObjectName(u"datosPrestamo")
        self.datosPrestamo.setHorizontalSpacing(16)
        self.datosPrestamo.setVerticalSpacing(10)
        self.datoLibro = QLabel(self.fichaPrestamo)
        self.datoLibro.setObjectName(u"datoLibro")

        self.datosPrestamo.addWidget(self.datoLibro, 0, 0, 1, 1, Qt.AlignTop)

        self.valorLibro = QLabel(self.fichaPrestamo)
        self.valorLibro.setObjectName(u"valorLibro")
        self.valorLibro.setWordWrap(True)

        self.datosPrestamo.addWidget(self.valorLibro, 0, 1, 1, 1)

        self.datoAutor = QLabel(self.fichaPrestamo)
        self.datoAutor.setObjectName(u"datoAutor")

        self.datosPrestamo.addWidget(self.datoAutor, 1, 0, 1, 1, Qt.AlignTop)

        self.valorAutor = QLabel(self.fichaPrestamo)
        self.valorAutor.setObjectName(u"valorAutor")
        self.valorAutor.setWordWrap(True)

        self.datosPrestamo.addWidget(self.valorAutor, 1, 1, 1, 1)

        self.datoPrestado = QLabel(self.fichaPrestamo)
        self.datoPrestado.setObjectName(u"datoPrestado")

        self.datosPrestamo.addWidget(self.datoPrestado, 2, 0, 1, 1, Qt.AlignTop)

        self.valorPrestado = QLabel(self.fichaPrestamo)
        self.valorPrestado.setObjectName(u"valorPrestado")
        self.valorPrestado.setWordWrap(True)
        self.valorPrestado.setProperty(u"mono", True)

        self.datosPrestamo.addWidget(self.valorPrestado, 2, 1, 1, 1)

        self.datoVence = QLabel(self.fichaPrestamo)
        self.datoVence.setObjectName(u"datoVence")

        self.datosPrestamo.addWidget(self.datoVence, 3, 0, 1, 1, Qt.AlignTop)

        self.valorVence = QLabel(self.fichaPrestamo)
        self.valorVence.setObjectName(u"valorVence")
        self.valorVence.setWordWrap(True)
        self.valorVence.setProperty(u"mono", True)

        self.datosPrestamo.addWidget(self.valorVence, 3, 1, 1, 1)

        self.datoRegistro = QLabel(self.fichaPrestamo)
        self.datoRegistro.setObjectName(u"datoRegistro")

        self.datosPrestamo.addWidget(self.datoRegistro, 4, 0, 1, 1, Qt.AlignTop)

        self.valorRegistro = QLabel(self.fichaPrestamo)
        self.valorRegistro.setObjectName(u"valorRegistro")
        self.valorRegistro.setWordWrap(True)

        self.datosPrestamo.addWidget(self.valorRegistro, 4, 1, 1, 1)

        self.datoTelefono = QLabel(self.fichaPrestamo)
        self.datoTelefono.setObjectName(u"datoTelefono")

        self.datosPrestamo.addWidget(self.datoTelefono, 5, 0, 1, 1, Qt.AlignTop)

        self.valorTelefono = QLabel(self.fichaPrestamo)
        self.valorTelefono.setObjectName(u"valorTelefono")
        self.valorTelefono.setWordWrap(True)
        self.valorTelefono.setProperty(u"mono", True)

        self.datosPrestamo.addWidget(self.valorTelefono, 5, 1, 1, 1)

        self.datosPrestamo.setColumnStretch(1, 1)

        self.disposicionFicha.addLayout(self.datosPrestamo)


        self.disposicionPanel.addWidget(self.fichaPrestamo)

        self.accionesPanel = QVBoxLayout()
        self.accionesPanel.setSpacing(10)
        self.accionesPanel.setObjectName(u"accionesPanel")
        self.botonDevolver = QPushButton(self.panelPrestamo)
        self.botonDevolver.setObjectName(u"botonDevolver")
        self.botonDevolver.setMinimumHeight(44)
        self.botonDevolver.setEnabled(False)

        self.accionesPanel.addWidget(self.botonDevolver)

        self.botonHistorial = QPushButton(self.panelPrestamo)
        self.botonHistorial.setObjectName(u"botonHistorial")
        self.botonHistorial.setMinimumHeight(44)
        self.botonHistorial.setEnabled(False)
        self.botonHistorial.setProperty(u"secundario", True)

        self.accionesPanel.addWidget(self.botonHistorial)


        self.disposicionPanel.addLayout(self.accionesPanel)


        self.columnaPanel.addWidget(self.panelPrestamo)

        self.espacioPanel = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.columnaPanel.addItem(self.espacioPanel)

        self.columnaPanel.setStretch(1, 1)

        self.cuerpo.addLayout(self.columnaPanel)

        self.cuerpo.setStretch(0, 1)

        self.disposicion.addLayout(self.cuerpo)

        self.disposicion.setStretch(1, 1)
        QWidget.setTabOrder(self.campoFiltro, self.botonNuevo)
        QWidget.setTabOrder(self.botonNuevo, self.tablaPrestamos)
        QWidget.setTabOrder(self.tablaPrestamos, self.botonDevolver)
        QWidget.setTabOrder(self.botonDevolver, self.botonHistorial)

        self.retranslateUi(PantallaPrestamos)

        QMetaObject.connectSlotsByName(PantallaPrestamos)
    # setupUi

    def retranslateUi(self, PantallaPrestamos):
        PantallaPrestamos.setWindowTitle(QCoreApplication.translate("PantallaPrestamos", u"Pr\u00e9stamos", None))
        self.etiquetaTitulo.setText(QCoreApplication.translate("PantallaPrestamos", u"Pr\u00e9stamos", None))
        self.etiquetaTitulo.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"titulo", None))
        self.etiquetaResumen.setText("")
        self.etiquetaResumen.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"resumen", None))
        self.campoFiltro.setPlaceholderText(QCoreApplication.translate("PantallaPrestamos", u"Alumno, libro o sal\u00f3n", None))
        self.campoFiltro.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"busqueda", None))
        self.botonNuevo.setText(QCoreApplication.translate("PantallaPrestamos", u"Nuevo pr\u00e9stamo", None))
        self.tarjetaTabla.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"tarjeta", None))
        self.barraTabla.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"barraTabla", None))
        ___qtablewidgetitem = self.tablaPrestamos.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PantallaPrestamos", u"Alumno", None))
        ___qtablewidgetitem1 = self.tablaPrestamos.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PantallaPrestamos", u"Grupo", None))
        ___qtablewidgetitem2 = self.tablaPrestamos.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PantallaPrestamos", u"Libro", None))
        ___qtablewidgetitem3 = self.tablaPrestamos.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PantallaPrestamos", u"Vence", None))
        ___qtablewidgetitem4 = self.tablaPrestamos.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PantallaPrestamos", u"Situaci\u00f3n", None))
        self.etiquetaVacio.setText(QCoreApplication.translate("PantallaPrestamos", u"No hay pr\u00e9stamos activos.", None))
        self.etiquetaVacio.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"tablaVacia", None))
        self.panelPrestamo.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"panel", None))
        self.etiquetaPanel.setText(QCoreApplication.translate("PantallaPrestamos", u"Pr\u00e9stamo seleccionado", None))
        self.etiquetaPanel.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"etiquetaPanel", None))
        self.etiquetaPanelVacio.setText(QCoreApplication.translate("PantallaPrestamos", u"Elige un pr\u00e9stamo para ver su detalle y registrar la devoluci\u00f3n.", None))
        self.etiquetaPanelVacio.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"panelVacio", None))
        self.avatar.setText("")
        self.avatar.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"avatar", None))
        self.etiquetaNombre.setText("")
        self.etiquetaNombre.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"nombrePanel", None))
        self.etiquetaDetalle.setText("")
        self.etiquetaDetalle.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"detallePanel", None))
        self.cajaSituacion.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"caja", None))
        self.iconoCaja.setText("")
        self.tituloCaja.setText("")
        self.tituloCaja.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"tituloCaja", None))
        self.textoCaja.setText("")
        self.textoCaja.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"textoCaja", None))
        self.datoLibro.setText(QCoreApplication.translate("PantallaPrestamos", u"Libro", None))
        self.datoLibro.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"dato", None))
        self.valorLibro.setText("")
        self.valorLibro.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"valor", None))
        self.datoAutor.setText(QCoreApplication.translate("PantallaPrestamos", u"Autor", None))
        self.datoAutor.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"dato", None))
        self.valorAutor.setText("")
        self.valorAutor.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"valor", None))
        self.datoPrestado.setText(QCoreApplication.translate("PantallaPrestamos", u"Prestado", None))
        self.datoPrestado.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"dato", None))
        self.valorPrestado.setText("")
        self.valorPrestado.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"valor", None))
        self.datoVence.setText(QCoreApplication.translate("PantallaPrestamos", u"Vence", None))
        self.datoVence.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"dato", None))
        self.valorVence.setText("")
        self.valorVence.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"valor", None))
        self.datoRegistro.setText(QCoreApplication.translate("PantallaPrestamos", u"Registr\u00f3", None))
        self.datoRegistro.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"dato", None))
        self.valorRegistro.setText("")
        self.valorRegistro.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"valor", None))
        self.datoTelefono.setText(QCoreApplication.translate("PantallaPrestamos", u"Tel. del tutor", None))
        self.datoTelefono.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"dato", None))
        self.valorTelefono.setText("")
        self.valorTelefono.setProperty(u"rol", QCoreApplication.translate("PantallaPrestamos", u"valor", None))
        self.botonDevolver.setText(QCoreApplication.translate("PantallaPrestamos", u"Registrar devoluci\u00f3n", None))
        self.botonHistorial.setText(QCoreApplication.translate("PantallaPrestamos", u"Ver historial del alumno", None))
    # retranslateUi

