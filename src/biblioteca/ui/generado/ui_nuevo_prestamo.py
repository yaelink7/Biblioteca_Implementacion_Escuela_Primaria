# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nuevo_prestamo.ui'
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
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_DialogoNuevoPrestamo(object):
    def setupUi(self, DialogoNuevoPrestamo):
        if not DialogoNuevoPrestamo.objectName():
            DialogoNuevoPrestamo.setObjectName(u"DialogoNuevoPrestamo")
        DialogoNuevoPrestamo.resize(880, 680)
        self.disposicion = QVBoxLayout(DialogoNuevoPrestamo)
        self.disposicion.setSpacing(16)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(30, 26, 30, 26)
        self.encabezado = QVBoxLayout()
        self.encabezado.setSpacing(4)
        self.encabezado.setObjectName(u"encabezado")
        self.etiquetaEncabezado = QLabel(DialogoNuevoPrestamo)
        self.etiquetaEncabezado.setObjectName(u"etiquetaEncabezado")

        self.encabezado.addWidget(self.etiquetaEncabezado)

        self.etiquetaSubtitulo = QLabel(DialogoNuevoPrestamo)
        self.etiquetaSubtitulo.setObjectName(u"etiquetaSubtitulo")
        self.etiquetaSubtitulo.setWordWrap(True)

        self.encabezado.addWidget(self.etiquetaSubtitulo)


        self.disposicion.addLayout(self.encabezado)

        self.filaColumnas = QHBoxLayout()
        self.filaColumnas.setSpacing(18)
        self.filaColumnas.setObjectName(u"filaColumnas")
        self.columnaAlumno = QVBoxLayout()
        self.columnaAlumno.setSpacing(10)
        self.columnaAlumno.setObjectName(u"columnaAlumno")
        self.etiquetaAlumno = QLabel(DialogoNuevoPrestamo)
        self.etiquetaAlumno.setObjectName(u"etiquetaAlumno")

        self.columnaAlumno.addWidget(self.etiquetaAlumno)

        self.campoBuscarAlumno = QLineEdit(DialogoNuevoPrestamo)
        self.campoBuscarAlumno.setObjectName(u"campoBuscarAlumno")
        self.campoBuscarAlumno.setMinimumSize(QSize(200, 44))
        self.campoBuscarAlumno.setClearButtonEnabled(True)

        self.columnaAlumno.addWidget(self.campoBuscarAlumno)

        self.listaAlumnos = QListWidget(DialogoNuevoPrestamo)
        self.listaAlumnos.setObjectName(u"listaAlumnos")
        self.listaAlumnos.setMinimumHeight(300)
        self.listaAlumnos.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listaAlumnos.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.columnaAlumno.addWidget(self.listaAlumnos)


        self.filaColumnas.addLayout(self.columnaAlumno)

        self.columnaLibro = QVBoxLayout()
        self.columnaLibro.setSpacing(10)
        self.columnaLibro.setObjectName(u"columnaLibro")
        self.etiquetaLibro = QLabel(DialogoNuevoPrestamo)
        self.etiquetaLibro.setObjectName(u"etiquetaLibro")

        self.columnaLibro.addWidget(self.etiquetaLibro)

        self.campoBuscarLibro = QLineEdit(DialogoNuevoPrestamo)
        self.campoBuscarLibro.setObjectName(u"campoBuscarLibro")
        self.campoBuscarLibro.setMinimumSize(QSize(200, 44))
        self.campoBuscarLibro.setClearButtonEnabled(True)

        self.columnaLibro.addWidget(self.campoBuscarLibro)

        self.listaLibros = QListWidget(DialogoNuevoPrestamo)
        self.listaLibros.setObjectName(u"listaLibros")
        self.listaLibros.setMinimumHeight(300)
        self.listaLibros.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listaLibros.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.columnaLibro.addWidget(self.listaLibros)


        self.filaColumnas.addLayout(self.columnaLibro)


        self.disposicion.addLayout(self.filaColumnas)

        self.cierre = QVBoxLayout()
        self.cierre.setSpacing(4)
        self.cierre.setObjectName(u"cierre")
        self.etiquetaResumen = QLabel(DialogoNuevoPrestamo)
        self.etiquetaResumen.setObjectName(u"etiquetaResumen")
        self.etiquetaResumen.setWordWrap(True)

        self.cierre.addWidget(self.etiquetaResumen)

        self.etiquetaPlazo = QLabel(DialogoNuevoPrestamo)
        self.etiquetaPlazo.setObjectName(u"etiquetaPlazo")
        self.etiquetaPlazo.setWordWrap(True)

        self.cierre.addWidget(self.etiquetaPlazo)


        self.disposicion.addLayout(self.cierre)

        self.cajaError = QFrame(DialogoNuevoPrestamo)
        self.cajaError.setObjectName(u"cajaError")
        self.disposicionError = QHBoxLayout(self.cajaError)
        self.disposicionError.setSpacing(10)
        self.disposicionError.setObjectName(u"disposicionError")
        self.disposicionError.setContentsMargins(14, 12, 14, 12)
        self.iconoError = QLabel(self.cajaError)
        self.iconoError.setObjectName(u"iconoError")
        self.iconoError.setMinimumSize(QSize(20, 20))
        self.iconoError.setMaximumSize(QSize(20, 20))

        self.disposicionError.addWidget(self.iconoError, 0, Qt.AlignTop)

        self.etiquetaError = QLabel(self.cajaError)
        self.etiquetaError.setObjectName(u"etiquetaError")
        self.etiquetaError.setWordWrap(True)

        self.disposicionError.addWidget(self.etiquetaError)


        self.disposicion.addWidget(self.cajaError)

        self.filaBotones = QHBoxLayout()
        self.filaBotones.setSpacing(10)
        self.filaBotones.setObjectName(u"filaBotones")
        self.espacioBotones = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.filaBotones.addItem(self.espacioBotones)

        self.botonCancelar = QPushButton(DialogoNuevoPrestamo)
        self.botonCancelar.setObjectName(u"botonCancelar")
        self.botonCancelar.setMinimumHeight(44)
        self.botonCancelar.setProperty(u"secundario", True)

        self.filaBotones.addWidget(self.botonCancelar)

        self.botonPrestar = QPushButton(DialogoNuevoPrestamo)
        self.botonPrestar.setObjectName(u"botonPrestar")
        self.botonPrestar.setMinimumHeight(44)
        self.botonPrestar.setEnabled(False)

        self.filaBotones.addWidget(self.botonPrestar)


        self.disposicion.addLayout(self.filaBotones)

        self.disposicion.setStretch(1, 1)
        QWidget.setTabOrder(self.campoBuscarAlumno, self.listaAlumnos)
        QWidget.setTabOrder(self.listaAlumnos, self.campoBuscarLibro)
        QWidget.setTabOrder(self.campoBuscarLibro, self.listaLibros)
        QWidget.setTabOrder(self.listaLibros, self.botonPrestar)
        QWidget.setTabOrder(self.botonPrestar, self.botonCancelar)

        self.retranslateUi(DialogoNuevoPrestamo)

        QMetaObject.connectSlotsByName(DialogoNuevoPrestamo)
    # setupUi

    def retranslateUi(self, DialogoNuevoPrestamo):
        DialogoNuevoPrestamo.setWindowTitle(QCoreApplication.translate("DialogoNuevoPrestamo", u"Registrar pr\u00e9stamo", None))
        self.etiquetaEncabezado.setText(QCoreApplication.translate("DialogoNuevoPrestamo", u"Registrar pr\u00e9stamo", None))
        self.etiquetaEncabezado.setProperty(u"rol", QCoreApplication.translate("DialogoNuevoPrestamo", u"tituloDialogo", None))
        self.etiquetaSubtitulo.setText(QCoreApplication.translate("DialogoNuevoPrestamo", u"Dos b\u00fasquedas y un bot\u00f3n. El plazo y el inventario los calcula la base.", None))
        self.etiquetaSubtitulo.setProperty(u"rol", QCoreApplication.translate("DialogoNuevoPrestamo", u"subtituloDialogo", None))
        self.etiquetaAlumno.setText(QCoreApplication.translate("DialogoNuevoPrestamo", u"1. \u00bfQui\u00e9n se lo lleva?", None))
        self.etiquetaAlumno.setProperty(u"rol", QCoreApplication.translate("DialogoNuevoPrestamo", u"paso", None))
        self.campoBuscarAlumno.setPlaceholderText(QCoreApplication.translate("DialogoNuevoPrestamo", u"Nombre, c\u00f3digo o sal\u00f3n (4B)", None))
        self.campoBuscarAlumno.setProperty(u"rol", QCoreApplication.translate("DialogoNuevoPrestamo", u"busqueda", None))
        self.listaAlumnos.setProperty(u"rol", QCoreApplication.translate("DialogoNuevoPrestamo", u"opciones", None))
        self.etiquetaLibro.setText(QCoreApplication.translate("DialogoNuevoPrestamo", u"2. \u00bfQu\u00e9 libro?", None))
        self.etiquetaLibro.setProperty(u"rol", QCoreApplication.translate("DialogoNuevoPrestamo", u"paso", None))
        self.campoBuscarLibro.setPlaceholderText(QCoreApplication.translate("DialogoNuevoPrestamo", u"T\u00edtulo o autor", None))
        self.campoBuscarLibro.setProperty(u"rol", QCoreApplication.translate("DialogoNuevoPrestamo", u"busqueda", None))
        self.listaLibros.setProperty(u"rol", QCoreApplication.translate("DialogoNuevoPrestamo", u"opciones", None))
        self.etiquetaResumen.setText(QCoreApplication.translate("DialogoNuevoPrestamo", u"Elige un alumno y un libro.", None))
        self.etiquetaResumen.setProperty(u"rol", QCoreApplication.translate("DialogoNuevoPrestamo", u"resumenPrestamo", None))
        self.etiquetaPlazo.setText("")
        self.etiquetaPlazo.setProperty(u"rol", QCoreApplication.translate("DialogoNuevoPrestamo", u"notaCampo", None))
        self.iconoError.setText("")
        self.etiquetaError.setText("")
        self.botonCancelar.setText(QCoreApplication.translate("DialogoNuevoPrestamo", u"Cancelar", None))
        self.botonPrestar.setText(QCoreApplication.translate("DialogoNuevoPrestamo", u"Prestar", None))
    # retranslateUi

