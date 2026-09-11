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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_PantallaAlumnos(object):
    def setupUi(self, PantallaAlumnos):
        if not PantallaAlumnos.objectName():
            PantallaAlumnos.setObjectName(u"PantallaAlumnos")
        PantallaAlumnos.resize(900, 560)
        self.disposicion = QVBoxLayout(PantallaAlumnos)
        self.disposicion.setSpacing(14)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(20, 20, 20, 20)
        self.campoBusqueda = QLineEdit(PantallaAlumnos)
        self.campoBusqueda.setObjectName(u"campoBusqueda")
        self.campoBusqueda.setMinimumHeight(36)
        self.campoBusqueda.setClearButtonEnabled(True)

        self.disposicion.addWidget(self.campoBusqueda)

        self.tablaAlumnos = QTableWidget(PantallaAlumnos)
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
        self.tablaAlumnos.setAlternatingRowColors(True)
        self.tablaAlumnos.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablaAlumnos.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tablaAlumnos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaAlumnos.setSortingEnabled(True)
        self.tablaAlumnos.horizontalHeader().setStretchLastSection(True)
        self.tablaAlumnos.verticalHeader().setVisible(False)

        self.disposicion.addWidget(self.tablaAlumnos)

        self.filaAcciones = QHBoxLayout()
        self.filaAcciones.setSpacing(10)
        self.filaAcciones.setObjectName(u"filaAcciones")
        self.etiquetaResumen = QLabel(PantallaAlumnos)
        self.etiquetaResumen.setObjectName(u"etiquetaResumen")

        self.filaAcciones.addWidget(self.etiquetaResumen)

        self.espacioAcciones = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.filaAcciones.addItem(self.espacioAcciones)

        self.botonNuevo = QPushButton(PantallaAlumnos)
        self.botonNuevo.setObjectName(u"botonNuevo")
        self.botonNuevo.setMinimumHeight(34)

        self.filaAcciones.addWidget(self.botonNuevo)

        self.botonEditar = QPushButton(PantallaAlumnos)
        self.botonEditar.setObjectName(u"botonEditar")
        self.botonEditar.setMinimumHeight(34)
        self.botonEditar.setEnabled(False)

        self.filaAcciones.addWidget(self.botonEditar)

        self.botonHistorial = QPushButton(PantallaAlumnos)
        self.botonHistorial.setObjectName(u"botonHistorial")
        self.botonHistorial.setMinimumHeight(34)
        self.botonHistorial.setEnabled(False)

        self.filaAcciones.addWidget(self.botonHistorial)


        self.disposicion.addLayout(self.filaAcciones)


        self.retranslateUi(PantallaAlumnos)

        QMetaObject.connectSlotsByName(PantallaAlumnos)
    # setupUi

    def retranslateUi(self, PantallaAlumnos):
        PantallaAlumnos.setWindowTitle(QCoreApplication.translate("PantallaAlumnos", u"Alumnos", None))
        self.campoBusqueda.setPlaceholderText(QCoreApplication.translate("PantallaAlumnos", u"Buscar por nombre, c\u00f3digo o sal\u00f3n (4B)\u2026", None))
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
        self.etiquetaResumen.setText("")
        self.botonNuevo.setText(QCoreApplication.translate("PantallaAlumnos", u"Registrar alumno", None))
        self.botonEditar.setText(QCoreApplication.translate("PantallaAlumnos", u"Modificar", None))
        self.botonHistorial.setText(QCoreApplication.translate("PantallaAlumnos", u"Ver historial", None))
    # retranslateUi

