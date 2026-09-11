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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_PantallaCatalogo(object):
    def setupUi(self, PantallaCatalogo):
        if not PantallaCatalogo.objectName():
            PantallaCatalogo.setObjectName(u"PantallaCatalogo")
        PantallaCatalogo.resize(900, 560)
        self.disposicion = QVBoxLayout(PantallaCatalogo)
        self.disposicion.setSpacing(14)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(20, 20, 20, 20)
        self.filaBusqueda = QHBoxLayout()
        self.filaBusqueda.setSpacing(10)
        self.filaBusqueda.setObjectName(u"filaBusqueda")
        self.campoBusqueda = QLineEdit(PantallaCatalogo)
        self.campoBusqueda.setObjectName(u"campoBusqueda")
        self.campoBusqueda.setMinimumHeight(36)
        self.campoBusqueda.setClearButtonEnabled(True)

        self.filaBusqueda.addWidget(self.campoBusqueda)

        self.casillaVerBajas = QCheckBox(PantallaCatalogo)
        self.casillaVerBajas.setObjectName(u"casillaVerBajas")

        self.filaBusqueda.addWidget(self.casillaVerBajas)


        self.disposicion.addLayout(self.filaBusqueda)

        self.tablaLibros = QTableWidget(PantallaCatalogo)
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
        self.tablaLibros.setAlternatingRowColors(True)
        self.tablaLibros.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablaLibros.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tablaLibros.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaLibros.setSortingEnabled(True)
        self.tablaLibros.horizontalHeader().setStretchLastSection(True)
        self.tablaLibros.verticalHeader().setVisible(False)

        self.disposicion.addWidget(self.tablaLibros)

        self.filaAcciones = QHBoxLayout()
        self.filaAcciones.setSpacing(10)
        self.filaAcciones.setObjectName(u"filaAcciones")
        self.etiquetaResumen = QLabel(PantallaCatalogo)
        self.etiquetaResumen.setObjectName(u"etiquetaResumen")

        self.filaAcciones.addWidget(self.etiquetaResumen)

        self.espacioAcciones = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.filaAcciones.addItem(self.espacioAcciones)

        self.botonNuevo = QPushButton(PantallaCatalogo)
        self.botonNuevo.setObjectName(u"botonNuevo")
        self.botonNuevo.setMinimumHeight(34)

        self.filaAcciones.addWidget(self.botonNuevo)

        self.botonEditar = QPushButton(PantallaCatalogo)
        self.botonEditar.setObjectName(u"botonEditar")
        self.botonEditar.setMinimumHeight(34)
        self.botonEditar.setEnabled(False)

        self.filaAcciones.addWidget(self.botonEditar)

        self.botonBaja = QPushButton(PantallaCatalogo)
        self.botonBaja.setObjectName(u"botonBaja")
        self.botonBaja.setMinimumHeight(34)
        self.botonBaja.setEnabled(False)

        self.filaAcciones.addWidget(self.botonBaja)


        self.disposicion.addLayout(self.filaAcciones)


        self.retranslateUi(PantallaCatalogo)

        QMetaObject.connectSlotsByName(PantallaCatalogo)
    # setupUi

    def retranslateUi(self, PantallaCatalogo):
        PantallaCatalogo.setWindowTitle(QCoreApplication.translate("PantallaCatalogo", u"Cat\u00e1logo", None))
        self.campoBusqueda.setPlaceholderText(QCoreApplication.translate("PantallaCatalogo", u"Buscar por t\u00edtulo, autor o tipo\u2026", None))
        self.casillaVerBajas.setText(QCoreApplication.translate("PantallaCatalogo", u"Ver dados de baja", None))
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
        self.etiquetaResumen.setText("")
        self.botonNuevo.setText(QCoreApplication.translate("PantallaCatalogo", u"Registrar libro", None))
        self.botonEditar.setText(QCoreApplication.translate("PantallaCatalogo", u"Modificar", None))
        self.botonBaja.setText(QCoreApplication.translate("PantallaCatalogo", u"Dar de baja", None))
    # retranslateUi

