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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_PantallaPrestamos(object):
    def setupUi(self, PantallaPrestamos):
        if not PantallaPrestamos.objectName():
            PantallaPrestamos.setObjectName(u"PantallaPrestamos")
        PantallaPrestamos.resize(900, 560)
        self.disposicion = QVBoxLayout(PantallaPrestamos)
        self.disposicion.setSpacing(14)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(20, 20, 20, 20)
        self.filaFiltro = QHBoxLayout()
        self.filaFiltro.setSpacing(10)
        self.filaFiltro.setObjectName(u"filaFiltro")
        self.campoFiltro = QLineEdit(PantallaPrestamos)
        self.campoFiltro.setObjectName(u"campoFiltro")
        self.campoFiltro.setMinimumHeight(36)
        self.campoFiltro.setClearButtonEnabled(True)

        self.filaFiltro.addWidget(self.campoFiltro)

        self.casillaSoloVencidos = QCheckBox(PantallaPrestamos)
        self.casillaSoloVencidos.setObjectName(u"casillaSoloVencidos")

        self.filaFiltro.addWidget(self.casillaSoloVencidos)


        self.disposicion.addLayout(self.filaFiltro)

        self.tablaPrestamos = QTableWidget(PantallaPrestamos)
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
        self.tablaPrestamos.setAlternatingRowColors(True)
        self.tablaPrestamos.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablaPrestamos.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tablaPrestamos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaPrestamos.setSortingEnabled(True)
        self.tablaPrestamos.horizontalHeader().setStretchLastSection(True)
        self.tablaPrestamos.verticalHeader().setVisible(False)

        self.disposicion.addWidget(self.tablaPrestamos)

        self.filaAcciones = QHBoxLayout()
        self.filaAcciones.setSpacing(10)
        self.filaAcciones.setObjectName(u"filaAcciones")
        self.etiquetaResumen = QLabel(PantallaPrestamos)
        self.etiquetaResumen.setObjectName(u"etiquetaResumen")

        self.filaAcciones.addWidget(self.etiquetaResumen)

        self.espacioAcciones = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.filaAcciones.addItem(self.espacioAcciones)

        self.botonNuevo = QPushButton(PantallaPrestamos)
        self.botonNuevo.setObjectName(u"botonNuevo")
        self.botonNuevo.setMinimumHeight(34)

        self.filaAcciones.addWidget(self.botonNuevo)

        self.botonDevolver = QPushButton(PantallaPrestamos)
        self.botonDevolver.setObjectName(u"botonDevolver")
        self.botonDevolver.setMinimumHeight(34)
        self.botonDevolver.setEnabled(False)

        self.filaAcciones.addWidget(self.botonDevolver)


        self.disposicion.addLayout(self.filaAcciones)


        self.retranslateUi(PantallaPrestamos)

        QMetaObject.connectSlotsByName(PantallaPrestamos)
    # setupUi

    def retranslateUi(self, PantallaPrestamos):
        PantallaPrestamos.setWindowTitle(QCoreApplication.translate("PantallaPrestamos", u"Pr\u00e9stamos", None))
        self.campoFiltro.setPlaceholderText(QCoreApplication.translate("PantallaPrestamos", u"Filtrar por alumno o libro\u2026", None))
        self.casillaSoloVencidos.setText(QCoreApplication.translate("PantallaPrestamos", u"Solo vencidos", None))
        ___qtablewidgetitem = self.tablaPrestamos.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PantallaPrestamos", u"Alumno", None))
        ___qtablewidgetitem1 = self.tablaPrestamos.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PantallaPrestamos", u"Libro", None))
        ___qtablewidgetitem2 = self.tablaPrestamos.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PantallaPrestamos", u"Prestado", None))
        ___qtablewidgetitem3 = self.tablaPrestamos.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PantallaPrestamos", u"Vence", None))
        ___qtablewidgetitem4 = self.tablaPrestamos.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PantallaPrestamos", u"Situaci\u00f3n", None))
        self.etiquetaResumen.setText("")
        self.botonNuevo.setText(QCoreApplication.translate("PantallaPrestamos", u"Registrar pr\u00e9stamo", None))
        self.botonDevolver.setText(QCoreApplication.translate("PantallaPrestamos", u"Registrar devoluci\u00f3n", None))
    # retranslateUi

