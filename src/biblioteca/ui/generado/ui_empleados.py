# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'empleados.ui'
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
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_PantallaEmpleados(object):
    def setupUi(self, PantallaEmpleados):
        if not PantallaEmpleados.objectName():
            PantallaEmpleados.setObjectName(u"PantallaEmpleados")
        PantallaEmpleados.resize(900, 560)
        self.disposicion = QVBoxLayout(PantallaEmpleados)
        self.disposicion.setSpacing(14)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(20, 20, 20, 20)
        self.etiquetaAviso = QLabel(PantallaEmpleados)
        self.etiquetaAviso.setObjectName(u"etiquetaAviso")
        self.etiquetaAviso.setWordWrap(True)

        self.disposicion.addWidget(self.etiquetaAviso)

        self.tablaEmpleados = QTableWidget(PantallaEmpleados)
        if (self.tablaEmpleados.columnCount() < 5):
            self.tablaEmpleados.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tablaEmpleados.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tablaEmpleados.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tablaEmpleados.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tablaEmpleados.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tablaEmpleados.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tablaEmpleados.setObjectName(u"tablaEmpleados")
        self.tablaEmpleados.setAlternatingRowColors(True)
        self.tablaEmpleados.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablaEmpleados.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tablaEmpleados.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaEmpleados.setSortingEnabled(True)
        self.tablaEmpleados.horizontalHeader().setStretchLastSection(True)
        self.tablaEmpleados.verticalHeader().setVisible(False)

        self.disposicion.addWidget(self.tablaEmpleados)

        self.filaAcciones = QHBoxLayout()
        self.filaAcciones.setSpacing(10)
        self.filaAcciones.setObjectName(u"filaAcciones")
        self.etiquetaResumen = QLabel(PantallaEmpleados)
        self.etiquetaResumen.setObjectName(u"etiquetaResumen")

        self.filaAcciones.addWidget(self.etiquetaResumen)

        self.espacioAcciones = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.filaAcciones.addItem(self.espacioAcciones)

        self.botonNuevo = QPushButton(PantallaEmpleados)
        self.botonNuevo.setObjectName(u"botonNuevo")
        self.botonNuevo.setMinimumHeight(34)

        self.filaAcciones.addWidget(self.botonNuevo)

        self.botonEditar = QPushButton(PantallaEmpleados)
        self.botonEditar.setObjectName(u"botonEditar")
        self.botonEditar.setMinimumHeight(34)
        self.botonEditar.setEnabled(False)

        self.filaAcciones.addWidget(self.botonEditar)


        self.disposicion.addLayout(self.filaAcciones)


        self.retranslateUi(PantallaEmpleados)

        QMetaObject.connectSlotsByName(PantallaEmpleados)
    # setupUi

    def retranslateUi(self, PantallaEmpleados):
        PantallaEmpleados.setWindowTitle(QCoreApplication.translate("PantallaEmpleados", u"Empleados", None))
        self.etiquetaAviso.setText("")
        ___qtablewidgetitem = self.tablaEmpleados.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PantallaEmpleados", u"C\u00f3digo", None))
        ___qtablewidgetitem1 = self.tablaEmpleados.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PantallaEmpleados", u"Nombre", None))
        ___qtablewidgetitem2 = self.tablaEmpleados.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PantallaEmpleados", u"Puesto", None))
        ___qtablewidgetitem3 = self.tablaEmpleados.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PantallaEmpleados", u"Correo", None))
        ___qtablewidgetitem4 = self.tablaEmpleados.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PantallaEmpleados", u"Perfil", None))
        self.etiquetaResumen.setText("")
        self.botonNuevo.setText(QCoreApplication.translate("PantallaEmpleados", u"Registrar empleado", None))
        self.botonEditar.setText(QCoreApplication.translate("PantallaEmpleados", u"Modificar", None))
    # retranslateUi

