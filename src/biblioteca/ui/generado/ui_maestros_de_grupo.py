# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'maestros_de_grupo.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_DialogoMaestros(object):
    def setupUi(self, DialogoMaestros):
        if not DialogoMaestros.objectName():
            DialogoMaestros.setObjectName(u"DialogoMaestros")
        DialogoMaestros.resize(640, 620)
        self.disposicion = QVBoxLayout(DialogoMaestros)
        self.disposicion.setSpacing(16)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(30, 26, 30, 26)
        self.encabezado = QVBoxLayout()
        self.encabezado.setSpacing(4)
        self.encabezado.setObjectName(u"encabezado")
        self.etiquetaEncabezado = QLabel(DialogoMaestros)
        self.etiquetaEncabezado.setObjectName(u"etiquetaEncabezado")

        self.encabezado.addWidget(self.etiquetaEncabezado)


        self.disposicion.addLayout(self.encabezado)

        self.etiquetaExplicacion = QLabel(DialogoMaestros)
        self.etiquetaExplicacion.setObjectName(u"etiquetaExplicacion")
        self.etiquetaExplicacion.setWordWrap(True)

        self.disposicion.addWidget(self.etiquetaExplicacion)

        self.cajaError = QFrame(DialogoMaestros)
        self.cajaError.setObjectName(u"cajaError")
        self.disposicionError = QVBoxLayout(self.cajaError)
        self.disposicionError.setSpacing(4)
        self.disposicionError.setObjectName(u"disposicionError")
        self.disposicionError.setContentsMargins(16, 12, 16, 12)
        self.tituloError = QLabel(self.cajaError)
        self.tituloError.setObjectName(u"tituloError")

        self.disposicionError.addWidget(self.tituloError)

        self.etiquetaError = QLabel(self.cajaError)
        self.etiquetaError.setObjectName(u"etiquetaError")
        self.etiquetaError.setWordWrap(True)

        self.disposicionError.addWidget(self.etiquetaError)


        self.disposicion.addWidget(self.cajaError)

        self.marcoTabla = QFrame(DialogoMaestros)
        self.marcoTabla.setObjectName(u"marcoTabla")
        self.disposicionMarco = QVBoxLayout(self.marcoTabla)
        self.disposicionMarco.setSpacing(0)
        self.disposicionMarco.setObjectName(u"disposicionMarco")
        self.disposicionMarco.setContentsMargins(1, 1, 1, 1)
        self.tablaMaestros = QTableWidget(self.marcoTabla)
        if (self.tablaMaestros.columnCount() < 3):
            self.tablaMaestros.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.tablaMaestros.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tablaMaestros.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tablaMaestros.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.tablaMaestros.setObjectName(u"tablaMaestros")
        self.tablaMaestros.setFrameShape(QFrame.NoFrame)
        self.tablaMaestros.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablaMaestros.setSelectionMode(QAbstractItemView.NoSelection)
        self.tablaMaestros.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaMaestros.setShowGrid(False)
        self.tablaMaestros.setWordWrap(False)
        self.tablaMaestros.setSortingEnabled(False)
        self.tablaMaestros.setFocusPolicy(Qt.NoFocus)
        self.tablaMaestros.horizontalHeader().setHighlightSections(False)
        self.tablaMaestros.horizontalHeader().setStretchLastSection(False)
        self.tablaMaestros.verticalHeader().setVisible(False)
        self.tablaMaestros.verticalHeader().setDefaultSectionSize(56)

        self.disposicionMarco.addWidget(self.tablaMaestros)


        self.disposicion.addWidget(self.marcoTabla)

        self.filaBotones = QHBoxLayout()
        self.filaBotones.setSpacing(10)
        self.filaBotones.setObjectName(u"filaBotones")
        self.espacioBotones = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.filaBotones.addItem(self.espacioBotones)

        self.botonCancelar = QPushButton(DialogoMaestros)
        self.botonCancelar.setObjectName(u"botonCancelar")
        self.botonCancelar.setMinimumHeight(44)
        self.botonCancelar.setProperty(u"secundario", True)

        self.filaBotones.addWidget(self.botonCancelar)

        self.botonGuardar = QPushButton(DialogoMaestros)
        self.botonGuardar.setObjectName(u"botonGuardar")
        self.botonGuardar.setMinimumHeight(44)

        self.filaBotones.addWidget(self.botonGuardar)


        self.disposicion.addLayout(self.filaBotones)

        self.disposicion.setStretch(3, 1)
        QWidget.setTabOrder(self.tablaMaestros, self.botonGuardar)
        QWidget.setTabOrder(self.botonGuardar, self.botonCancelar)

        self.retranslateUi(DialogoMaestros)

        QMetaObject.connectSlotsByName(DialogoMaestros)
    # setupUi

    def retranslateUi(self, DialogoMaestros):
        DialogoMaestros.setWindowTitle(QCoreApplication.translate("DialogoMaestros", u"Maestros de grupo", None))
        self.etiquetaEncabezado.setText(QCoreApplication.translate("DialogoMaestros", u"Maestros de grupo", None))
        self.etiquetaEncabezado.setProperty(u"rol", QCoreApplication.translate("DialogoMaestros", u"tituloDialogo", None))
        self.etiquetaExplicacion.setText(QCoreApplication.translate("DialogoMaestros", u"El maestro se asigna una vez por sal\u00f3n y todos sus alumnos lo heredan. Al empezar otro ciclo escolar se corrige aqu\u00ed.", None))
        self.etiquetaExplicacion.setProperty(u"rol", QCoreApplication.translate("DialogoMaestros", u"textoDialogo", None))
        self.tituloError.setText(QCoreApplication.translate("DialogoMaestros", u"No se pudo guardar:", None))
        self.etiquetaError.setText("")
        self.marcoTabla.setProperty(u"rol", QCoreApplication.translate("DialogoMaestros", u"marcoTabla", None))
        ___qtablewidgetitem = self.tablaMaestros.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("DialogoMaestros", u"Sal\u00f3n", None))
        ___qtablewidgetitem1 = self.tablaMaestros.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("DialogoMaestros", u"Maestro de grupo", None))
        ___qtablewidgetitem2 = self.tablaMaestros.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("DialogoMaestros", u"Alumnos", None))
        self.tablaMaestros.setProperty(u"rol", QCoreApplication.translate("DialogoMaestros", u"tablaDialogo", None))
        self.botonCancelar.setText(QCoreApplication.translate("DialogoMaestros", u"Cancelar", None))
        self.botonGuardar.setText(QCoreApplication.translate("DialogoMaestros", u"Guardar", None))
    # retranslateUi

