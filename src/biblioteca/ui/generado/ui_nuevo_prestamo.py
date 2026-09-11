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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_DialogoNuevoPrestamo(object):
    def setupUi(self, DialogoNuevoPrestamo):
        if not DialogoNuevoPrestamo.objectName():
            DialogoNuevoPrestamo.setObjectName(u"DialogoNuevoPrestamo")
        DialogoNuevoPrestamo.resize(760, 500)
        self.disposicion = QVBoxLayout(DialogoNuevoPrestamo)
        self.disposicion.setSpacing(12)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(20, 20, 20, 20)
        self.filaColumnas = QHBoxLayout()
        self.filaColumnas.setSpacing(18)
        self.filaColumnas.setObjectName(u"filaColumnas")
        self.columnaAlumno = QVBoxLayout()
        self.columnaAlumno.setSpacing(8)
        self.columnaAlumno.setObjectName(u"columnaAlumno")
        self.etiquetaAlumno = QLabel(DialogoNuevoPrestamo)
        self.etiquetaAlumno.setObjectName(u"etiquetaAlumno")

        self.columnaAlumno.addWidget(self.etiquetaAlumno)

        self.campoBuscarAlumno = QLineEdit(DialogoNuevoPrestamo)
        self.campoBuscarAlumno.setObjectName(u"campoBuscarAlumno")
        self.campoBuscarAlumno.setMinimumHeight(34)
        self.campoBuscarAlumno.setClearButtonEnabled(True)

        self.columnaAlumno.addWidget(self.campoBuscarAlumno)

        self.listaAlumnos = QListWidget(DialogoNuevoPrestamo)
        self.listaAlumnos.setObjectName(u"listaAlumnos")

        self.columnaAlumno.addWidget(self.listaAlumnos)


        self.filaColumnas.addLayout(self.columnaAlumno)

        self.columnaLibro = QVBoxLayout()
        self.columnaLibro.setSpacing(8)
        self.columnaLibro.setObjectName(u"columnaLibro")
        self.etiquetaLibro = QLabel(DialogoNuevoPrestamo)
        self.etiquetaLibro.setObjectName(u"etiquetaLibro")

        self.columnaLibro.addWidget(self.etiquetaLibro)

        self.campoBuscarLibro = QLineEdit(DialogoNuevoPrestamo)
        self.campoBuscarLibro.setObjectName(u"campoBuscarLibro")
        self.campoBuscarLibro.setMinimumHeight(34)
        self.campoBuscarLibro.setClearButtonEnabled(True)

        self.columnaLibro.addWidget(self.campoBuscarLibro)

        self.listaLibros = QListWidget(DialogoNuevoPrestamo)
        self.listaLibros.setObjectName(u"listaLibros")

        self.columnaLibro.addWidget(self.listaLibros)


        self.filaColumnas.addLayout(self.columnaLibro)


        self.disposicion.addLayout(self.filaColumnas)

        self.marcoResumen = QFrame(DialogoNuevoPrestamo)
        self.marcoResumen.setObjectName(u"marcoResumen")
        self.marcoResumen.setFrameShape(QFrame.StyledPanel)
        self.disposicionResumen = QVBoxLayout(self.marcoResumen)
        self.disposicionResumen.setSpacing(4)
        self.disposicionResumen.setObjectName(u"disposicionResumen")
        self.disposicionResumen.setContentsMargins(14, 12, 14, 12)
        self.etiquetaResumen = QLabel(self.marcoResumen)
        self.etiquetaResumen.setObjectName(u"etiquetaResumen")
        self.etiquetaResumen.setWordWrap(True)

        self.disposicionResumen.addWidget(self.etiquetaResumen)

        self.etiquetaPlazo = QLabel(self.marcoResumen)
        self.etiquetaPlazo.setObjectName(u"etiquetaPlazo")

        self.disposicionResumen.addWidget(self.etiquetaPlazo)


        self.disposicion.addWidget(self.marcoResumen)

        self.etiquetaError = QLabel(DialogoNuevoPrestamo)
        self.etiquetaError.setObjectName(u"etiquetaError")
        self.etiquetaError.setWordWrap(True)
        self.etiquetaError.setMinimumHeight(34)

        self.disposicion.addWidget(self.etiquetaError)

        self.filaBotones = QHBoxLayout()
        self.filaBotones.setObjectName(u"filaBotones")
        self.espacioBotones = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.filaBotones.addItem(self.espacioBotones)

        self.botonCancelar = QPushButton(DialogoNuevoPrestamo)
        self.botonCancelar.setObjectName(u"botonCancelar")
        self.botonCancelar.setMinimumHeight(34)

        self.filaBotones.addWidget(self.botonCancelar)

        self.botonPrestar = QPushButton(DialogoNuevoPrestamo)
        self.botonPrestar.setObjectName(u"botonPrestar")
        self.botonPrestar.setMinimumHeight(34)
        self.botonPrestar.setEnabled(False)

        self.filaBotones.addWidget(self.botonPrestar)


        self.disposicion.addLayout(self.filaBotones)


        self.retranslateUi(DialogoNuevoPrestamo)

        self.botonPrestar.setDefault(True)


        QMetaObject.connectSlotsByName(DialogoNuevoPrestamo)
    # setupUi

    def retranslateUi(self, DialogoNuevoPrestamo):
        DialogoNuevoPrestamo.setWindowTitle(QCoreApplication.translate("DialogoNuevoPrestamo", u"Registrar pr\u00e9stamo", None))
        self.etiquetaAlumno.setText(QCoreApplication.translate("DialogoNuevoPrestamo", u"1. \u00bfQui\u00e9n se lo lleva?", None))
        self.campoBuscarAlumno.setPlaceholderText(QCoreApplication.translate("DialogoNuevoPrestamo", u"Nombre, c\u00f3digo o sal\u00f3n (4B)", None))
        self.etiquetaLibro.setText(QCoreApplication.translate("DialogoNuevoPrestamo", u"2. \u00bfQu\u00e9 libro?", None))
        self.campoBuscarLibro.setPlaceholderText(QCoreApplication.translate("DialogoNuevoPrestamo", u"T\u00edtulo o autor", None))
        self.etiquetaResumen.setText(QCoreApplication.translate("DialogoNuevoPrestamo", u"Elige un alumno y un libro.", None))
        self.etiquetaPlazo.setText("")
        self.etiquetaError.setText("")
        self.botonCancelar.setText(QCoreApplication.translate("DialogoNuevoPrestamo", u"Cancelar", None))
        self.botonPrestar.setText(QCoreApplication.translate("DialogoNuevoPrestamo", u"Prestar", None))
    # retranslateUi

