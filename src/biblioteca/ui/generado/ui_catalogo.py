# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'catalogo.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_PantallaCatalogo(object):
    def setupUi(self, PantallaCatalogo):
        if not PantallaCatalogo.objectName():
            PantallaCatalogo.setObjectName(u"PantallaCatalogo")
        PantallaCatalogo.resize(1100, 680)
        self.disposicion = QVBoxLayout(PantallaCatalogo)
        self.disposicion.setSpacing(18)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(0, 0, 0, 0)
        self.encabezado = QHBoxLayout()
        self.encabezado.setSpacing(12)
        self.encabezado.setObjectName(u"encabezado")
        self.textoEncabezado = QVBoxLayout()
        self.textoEncabezado.setSpacing(6)
        self.textoEncabezado.setObjectName(u"textoEncabezado")
        self.etiquetaTitulo = QLabel(PantallaCatalogo)
        self.etiquetaTitulo.setObjectName(u"etiquetaTitulo")

        self.textoEncabezado.addWidget(self.etiquetaTitulo)

        self.etiquetaResumen = QLabel(PantallaCatalogo)
        self.etiquetaResumen.setObjectName(u"etiquetaResumen")

        self.textoEncabezado.addWidget(self.etiquetaResumen)


        self.encabezado.addLayout(self.textoEncabezado)

        self.espacioEncabezado = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.encabezado.addItem(self.espacioEncabezado)

        self.campoBusqueda = QLineEdit(PantallaCatalogo)
        self.campoBusqueda.setObjectName(u"campoBusqueda")
        self.campoBusqueda.setMinimumSize(QSize(300, 44))
        self.campoBusqueda.setClearButtonEnabled(True)

        self.encabezado.addWidget(self.campoBusqueda, 0, Qt.AlignBottom)

        self.botonNuevo = QPushButton(PantallaCatalogo)
        self.botonNuevo.setObjectName(u"botonNuevo")
        self.botonNuevo.setMinimumHeight(44)

        self.encabezado.addWidget(self.botonNuevo, 0, Qt.AlignBottom)


        self.disposicion.addLayout(self.encabezado)

        self.cuerpo = QHBoxLayout()
        self.cuerpo.setSpacing(18)
        self.cuerpo.setObjectName(u"cuerpo")
        self.tarjetaTabla = QFrame(PantallaCatalogo)
        self.tarjetaTabla.setObjectName(u"tarjetaTabla")
        self.disposicionTarjeta = QVBoxLayout(self.tarjetaTabla)
        self.disposicionTarjeta.setSpacing(0)
        self.disposicionTarjeta.setObjectName(u"disposicionTarjeta")
        self.disposicionTarjeta.setContentsMargins(1, 0, 1, 8)
        self.barraTabla = QFrame(self.tarjetaTabla)
        self.barraTabla.setObjectName(u"barraTabla")
        self.barraTabla.setMinimumHeight(48)
        self.disposicionBarra = QHBoxLayout(self.barraTabla)
        self.disposicionBarra.setObjectName(u"disposicionBarra")
        self.disposicionBarra.setContentsMargins(16, 0, 16, 0)
        self.casillaVerBajas = QCheckBox(self.barraTabla)
        self.casillaVerBajas.setObjectName(u"casillaVerBajas")

        self.disposicionBarra.addWidget(self.casillaVerBajas)

        self.espacioBarra = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.disposicionBarra.addItem(self.espacioBarra)

        self.etiquetaPista = QLabel(self.barraTabla)
        self.etiquetaPista.setObjectName(u"etiquetaPista")

        self.disposicionBarra.addWidget(self.etiquetaPista)


        self.disposicionTarjeta.addWidget(self.barraTabla)

        self.tablaLibros = QTableWidget(self.tarjetaTabla)
        if (self.tablaLibros.columnCount() < 5):
            self.tablaLibros.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tablaLibros.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tablaLibros.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tablaLibros.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tablaLibros.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tablaLibros.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tablaLibros.setObjectName(u"tablaLibros")
        self.tablaLibros.setFrameShape(QFrame.NoFrame)
        self.tablaLibros.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablaLibros.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tablaLibros.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaLibros.setShowGrid(False)
        self.tablaLibros.setWordWrap(False)
        self.tablaLibros.setSortingEnabled(True)
        self.tablaLibros.horizontalHeader().setHighlightSections(False)
        self.tablaLibros.horizontalHeader().setStretchLastSection(True)
        self.tablaLibros.verticalHeader().setVisible(False)
        self.tablaLibros.verticalHeader().setDefaultSectionSize(46)

        self.disposicionTarjeta.addWidget(self.tablaLibros)


        self.cuerpo.addWidget(self.tarjetaTabla)

        self.panelLibro = QFrame(PantallaCatalogo)
        self.panelLibro.setObjectName(u"panelLibro")
        self.panelLibro.setMinimumWidth(300)
        self.panelLibro.setMaximumWidth(340)
        self.disposicionPanel = QVBoxLayout(self.panelLibro)
        self.disposicionPanel.setSpacing(18)
        self.disposicionPanel.setObjectName(u"disposicionPanel")
        self.disposicionPanel.setContentsMargins(22, 22, 22, 24)
        self.etiquetaPanel = QLabel(self.panelLibro)
        self.etiquetaPanel.setObjectName(u"etiquetaPanel")

        self.disposicionPanel.addWidget(self.etiquetaPanel)

        self.etiquetaPanelVacio = QLabel(self.panelLibro)
        self.etiquetaPanelVacio.setObjectName(u"etiquetaPanelVacio")
        self.etiquetaPanelVacio.setWordWrap(True)

        self.disposicionPanel.addWidget(self.etiquetaPanelVacio)

        self.fichaLibro = QWidget(self.panelLibro)
        self.fichaLibro.setObjectName(u"fichaLibro")
        self.disposicionFicha = QVBoxLayout(self.fichaLibro)
        self.disposicionFicha.setSpacing(18)
        self.disposicionFicha.setObjectName(u"disposicionFicha")
        self.disposicionFicha.setContentsMargins(0, 0, 0, 0)
        self.cabezaFicha = QHBoxLayout()
        self.cabezaFicha.setSpacing(12)
        self.cabezaFicha.setObjectName(u"cabezaFicha")
        self.portada = QLabel(self.fichaLibro)
        self.portada.setObjectName(u"portada")
        self.portada.setMinimumSize(QSize(52, 70))
        self.portada.setMaximumSize(QSize(52, 70))
        self.portada.setAlignment(Qt.AlignCenter)

        self.cabezaFicha.addWidget(self.portada)

        self.nombreFicha = QVBoxLayout()
        self.nombreFicha.setSpacing(2)
        self.nombreFicha.setObjectName(u"nombreFicha")
        self.etiquetaLibroTitulo = QLabel(self.fichaLibro)
        self.etiquetaLibroTitulo.setObjectName(u"etiquetaLibroTitulo")
        self.etiquetaLibroTitulo.setWordWrap(True)

        self.nombreFicha.addWidget(self.etiquetaLibroTitulo)

        self.etiquetaLibroAutor = QLabel(self.fichaLibro)
        self.etiquetaLibroAutor.setObjectName(u"etiquetaLibroAutor")
        self.etiquetaLibroAutor.setWordWrap(True)

        self.nombreFicha.addWidget(self.etiquetaLibroAutor)


        self.cabezaFicha.addLayout(self.nombreFicha)


        self.disposicionFicha.addLayout(self.cabezaFicha)

        self.cajaBaja = QFrame(self.fichaLibro)
        self.cajaBaja.setObjectName(u"cajaBaja")
        self.disposicionBaja = QVBoxLayout(self.cajaBaja)
        self.disposicionBaja.setObjectName(u"disposicionBaja")
        self.disposicionBaja.setContentsMargins(14, 12, 14, 12)
        self.etiquetaBaja = QLabel(self.cajaBaja)
        self.etiquetaBaja.setObjectName(u"etiquetaBaja")
        self.etiquetaBaja.setWordWrap(True)

        self.disposicionBaja.addWidget(self.etiquetaBaja)


        self.disposicionFicha.addWidget(self.cajaBaja)

        self.datosLibro = QGridLayout()
        self.datosLibro.setObjectName(u"datosLibro")
        self.datosLibro.setHorizontalSpacing(16)
        self.datosLibro.setVerticalSpacing(10)
        self.datoTipo = QLabel(self.fichaLibro)
        self.datoTipo.setObjectName(u"datoTipo")

        self.datosLibro.addWidget(self.datoTipo, 0, 0, 1, 1)

        self.valorTipo = QLabel(self.fichaLibro)
        self.valorTipo.setObjectName(u"valorTipo")
        self.valorTipo.setWordWrap(True)

        self.datosLibro.addWidget(self.valorTipo, 0, 1, 1, 1)

        self.datoEditorial = QLabel(self.fichaLibro)
        self.datoEditorial.setObjectName(u"datoEditorial")

        self.datosLibro.addWidget(self.datoEditorial, 1, 0, 1, 1)

        self.valorEditorial = QLabel(self.fichaLibro)
        self.valorEditorial.setObjectName(u"valorEditorial")
        self.valorEditorial.setWordWrap(True)

        self.datosLibro.addWidget(self.valorEditorial, 1, 1, 1, 1)

        self.datoAno = QLabel(self.fichaLibro)
        self.datoAno.setObjectName(u"datoAno")

        self.datosLibro.addWidget(self.datoAno, 2, 0, 1, 1)

        self.valorAno = QLabel(self.fichaLibro)
        self.valorAno.setObjectName(u"valorAno")
        self.valorAno.setProperty(u"mono", True)

        self.datosLibro.addWidget(self.valorAno, 2, 1, 1, 1)

        self.datoPaginas = QLabel(self.fichaLibro)
        self.datoPaginas.setObjectName(u"datoPaginas")

        self.datosLibro.addWidget(self.datoPaginas, 3, 0, 1, 1)

        self.valorPaginas = QLabel(self.fichaLibro)
        self.valorPaginas.setObjectName(u"valorPaginas")
        self.valorPaginas.setProperty(u"mono", True)

        self.datosLibro.addWidget(self.valorPaginas, 3, 1, 1, 1)

        self.datoDisponibles = QLabel(self.fichaLibro)
        self.datoDisponibles.setObjectName(u"datoDisponibles")

        self.datosLibro.addWidget(self.datoDisponibles, 4, 0, 1, 1)

        self.valorDisponibles = QLabel(self.fichaLibro)
        self.valorDisponibles.setObjectName(u"valorDisponibles")
        self.valorDisponibles.setProperty(u"mono", True)

        self.datosLibro.addWidget(self.valorDisponibles, 4, 1, 1, 1)

        self.datosLibro.setColumnStretch(1, 1)

        self.disposicionFicha.addLayout(self.datosLibro)


        self.disposicionPanel.addWidget(self.fichaLibro)

        self.accionesPanel = QVBoxLayout()
        self.accionesPanel.setSpacing(10)
        self.accionesPanel.setObjectName(u"accionesPanel")
        self.botonEditar = QPushButton(self.panelLibro)
        self.botonEditar.setObjectName(u"botonEditar")
        self.botonEditar.setMinimumHeight(44)
        self.botonEditar.setEnabled(False)

        self.accionesPanel.addWidget(self.botonEditar)

        self.botonBaja = QPushButton(self.panelLibro)
        self.botonBaja.setObjectName(u"botonBaja")
        self.botonBaja.setMinimumHeight(44)
        self.botonBaja.setEnabled(False)
        self.botonBaja.setProperty(u"peligro", True)

        self.accionesPanel.addWidget(self.botonBaja)


        self.disposicionPanel.addLayout(self.accionesPanel)


        self.cuerpo.addWidget(self.panelLibro, 0, Qt.AlignTop)

        self.cuerpo.setStretch(0, 1)

        self.disposicion.addLayout(self.cuerpo)

        self.disposicion.setStretch(1, 1)
        QWidget.setTabOrder(self.campoBusqueda, self.botonNuevo)
        QWidget.setTabOrder(self.botonNuevo, self.casillaVerBajas)
        QWidget.setTabOrder(self.casillaVerBajas, self.tablaLibros)
        QWidget.setTabOrder(self.tablaLibros, self.botonEditar)
        QWidget.setTabOrder(self.botonEditar, self.botonBaja)

        self.retranslateUi(PantallaCatalogo)

        QMetaObject.connectSlotsByName(PantallaCatalogo)
    # setupUi

    def retranslateUi(self, PantallaCatalogo):
        PantallaCatalogo.setWindowTitle(QCoreApplication.translate("PantallaCatalogo", u"Cat\u00e1logo", None))
        self.etiquetaTitulo.setText(QCoreApplication.translate("PantallaCatalogo", u"Cat\u00e1logo", None))
        self.etiquetaTitulo.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"titulo", None))
        self.etiquetaResumen.setText("")
        self.etiquetaResumen.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"resumen", None))
        self.campoBusqueda.setPlaceholderText(QCoreApplication.translate("PantallaCatalogo", u"T\u00edtulo, autor o tipo", None))
        self.campoBusqueda.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"busqueda", None))
        self.botonNuevo.setText(QCoreApplication.translate("PantallaCatalogo", u"Registrar libro", None))
        self.tarjetaTabla.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"tarjeta", None))
        self.barraTabla.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"barraTabla", None))
        self.casillaVerBajas.setText(QCoreApplication.translate("PantallaCatalogo", u"Ver dados de baja", None))
        self.etiquetaPista.setText(QCoreApplication.translate("PantallaCatalogo", u"Doble clic para modificar", None))
        self.etiquetaPista.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"pista", None))
        ___qtablewidgetitem = self.tablaLibros.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PantallaCatalogo", u"T\u00edtulo", None))
        ___qtablewidgetitem1 = self.tablaLibros.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PantallaCatalogo", u"Autor", None))
        ___qtablewidgetitem2 = self.tablaLibros.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PantallaCatalogo", u"Tipo", None))
        ___qtablewidgetitem3 = self.tablaLibros.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PantallaCatalogo", u"A\u00f1o", None))
        ___qtablewidgetitem4 = self.tablaLibros.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PantallaCatalogo", u"Estado", None))
        self.panelLibro.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"panel", None))
        self.etiquetaPanel.setText(QCoreApplication.translate("PantallaCatalogo", u"Libro seleccionado", None))
        self.etiquetaPanel.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"etiquetaPanel", None))
        self.etiquetaPanelVacio.setText(QCoreApplication.translate("PantallaCatalogo", u"Elige un libro de la tabla para ver su ficha.", None))
        self.etiquetaPanelVacio.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"panelVacio", None))
        self.portada.setText("")
        self.etiquetaLibroTitulo.setText("")
        self.etiquetaLibroTitulo.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"nombrePanel", None))
        self.etiquetaLibroAutor.setText("")
        self.etiquetaLibroAutor.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"detallePanel", None))
        self.cajaBaja.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"cajaGris", None))
        self.etiquetaBaja.setText("")
        self.etiquetaBaja.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"textoCaja", None))
        self.datoTipo.setText(QCoreApplication.translate("PantallaCatalogo", u"Tipo o g\u00e9nero", None))
        self.datoTipo.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"dato", None))
        self.valorTipo.setText("")
        self.valorTipo.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"valor", None))
        self.datoEditorial.setText(QCoreApplication.translate("PantallaCatalogo", u"Editorial", None))
        self.datoEditorial.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"dato", None))
        self.valorEditorial.setText("")
        self.valorEditorial.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"valor", None))
        self.datoAno.setText(QCoreApplication.translate("PantallaCatalogo", u"A\u00f1o", None))
        self.datoAno.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"dato", None))
        self.valorAno.setText("")
        self.valorAno.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"valor", None))
        self.datoPaginas.setText(QCoreApplication.translate("PantallaCatalogo", u"P\u00e1ginas", None))
        self.datoPaginas.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"dato", None))
        self.valorPaginas.setText("")
        self.valorPaginas.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"valor", None))
        self.datoDisponibles.setText(QCoreApplication.translate("PantallaCatalogo", u"Disponibles", None))
        self.datoDisponibles.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"dato", None))
        self.valorDisponibles.setText("")
        self.valorDisponibles.setProperty(u"rol", QCoreApplication.translate("PantallaCatalogo", u"valor", None))
        self.botonEditar.setText(QCoreApplication.translate("PantallaCatalogo", u"Modificar", None))
        self.botonBaja.setText(QCoreApplication.translate("PantallaCatalogo", u"Dar de baja", None))
    # retranslateUi

