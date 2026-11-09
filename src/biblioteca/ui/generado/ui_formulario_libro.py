# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formulario_libro.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDialog,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_FormularioLibro(object):
    def setupUi(self, FormularioLibro):
        if not FormularioLibro.objectName():
            FormularioLibro.setObjectName(u"FormularioLibro")
        FormularioLibro.resize(700, 720)
        self.disposicion = QVBoxLayout(FormularioLibro)
        self.disposicion.setSpacing(16)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(30, 26, 30, 26)
        self.encabezado = QVBoxLayout()
        self.encabezado.setSpacing(4)
        self.encabezado.setObjectName(u"encabezado")
        self.etiquetaEncabezado = QLabel(FormularioLibro)
        self.etiquetaEncabezado.setObjectName(u"etiquetaEncabezado")

        self.encabezado.addWidget(self.etiquetaEncabezado)

        self.etiquetaSubtitulo = QLabel(FormularioLibro)
        self.etiquetaSubtitulo.setObjectName(u"etiquetaSubtitulo")
        self.etiquetaSubtitulo.setWordWrap(True)

        self.encabezado.addWidget(self.etiquetaSubtitulo)


        self.disposicion.addLayout(self.encabezado)

        self.cajaError = QFrame(FormularioLibro)
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

        self.formulario = QGridLayout()
        self.formulario.setObjectName(u"formulario")
        self.formulario.setHorizontalSpacing(18)
        self.formulario.setVerticalSpacing(6)
        self.etiquetaTitulo = QLabel(FormularioLibro)
        self.etiquetaTitulo.setObjectName(u"etiquetaTitulo")

        self.formulario.addWidget(self.etiquetaTitulo, 0, 0, 1, 2)

        self.campoTitulo = QLineEdit(FormularioLibro)
        self.campoTitulo.setObjectName(u"campoTitulo")

        self.formulario.addWidget(self.campoTitulo, 1, 0, 1, 2)

        self.etiquetaAutor = QLabel(FormularioLibro)
        self.etiquetaAutor.setObjectName(u"etiquetaAutor")

        self.formulario.addWidget(self.etiquetaAutor, 2, 0, 1, 1)

        self.etiquetaEditorial = QLabel(FormularioLibro)
        self.etiquetaEditorial.setObjectName(u"etiquetaEditorial")

        self.formulario.addWidget(self.etiquetaEditorial, 2, 1, 1, 1)

        self.campoAutor = QLineEdit(FormularioLibro)
        self.campoAutor.setObjectName(u"campoAutor")

        self.formulario.addWidget(self.campoAutor, 3, 0, 1, 1)

        self.campoEditorial = QLineEdit(FormularioLibro)
        self.campoEditorial.setObjectName(u"campoEditorial")

        self.formulario.addWidget(self.campoEditorial, 3, 1, 1, 1)

        self.etiquetaColeccion = QLabel(FormularioLibro)
        self.etiquetaColeccion.setObjectName(u"etiquetaColeccion")

        self.formulario.addWidget(self.etiquetaColeccion, 4, 0, 1, 1)

        self.etiquetaAsignatura = QLabel(FormularioLibro)
        self.etiquetaAsignatura.setObjectName(u"etiquetaAsignatura")

        self.formulario.addWidget(self.etiquetaAsignatura, 4, 1, 1, 1)

        self.campoColeccion = QComboBox(FormularioLibro)
        self.campoColeccion.setObjectName(u"campoColeccion")

        self.formulario.addWidget(self.campoColeccion, 5, 0, 1, 1)

        self.campoAsignatura = QComboBox(FormularioLibro)
        self.campoAsignatura.setObjectName(u"campoAsignatura")

        self.formulario.addWidget(self.campoAsignatura, 5, 1, 1, 1)

        self.notaColeccion = QLabel(FormularioLibro)
        self.notaColeccion.setObjectName(u"notaColeccion")
        self.notaColeccion.setWordWrap(True)

        self.formulario.addWidget(self.notaColeccion, 6, 0, 1, 1)

        self.etiquetaExistencias = QLabel(FormularioLibro)
        self.etiquetaExistencias.setObjectName(u"etiquetaExistencias")

        self.formulario.addWidget(self.etiquetaExistencias, 7, 0, 1, 1)

        self.etiquetaAno = QLabel(FormularioLibro)
        self.etiquetaAno.setObjectName(u"etiquetaAno")

        self.formulario.addWidget(self.etiquetaAno, 7, 1, 1, 1)

        self.campoExistencias = QSpinBox(FormularioLibro)
        self.campoExistencias.setObjectName(u"campoExistencias")
        self.campoExistencias.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.campoExistencias.setMinimum(0)
        self.campoExistencias.setMaximum(9999)
        self.campoExistencias.setValue(1)

        self.formulario.addWidget(self.campoExistencias, 8, 0, 1, 1)

        self.campoAno = QSpinBox(FormularioLibro)
        self.campoAno.setObjectName(u"campoAno")
        self.campoAno.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.campoAno.setMinimum(1399)
        self.campoAno.setMaximum(2026)
        self.campoAno.setValue(1399)

        self.formulario.addWidget(self.campoAno, 8, 1, 1, 1)

        self.notaExistencias = QLabel(FormularioLibro)
        self.notaExistencias.setObjectName(u"notaExistencias")
        self.notaExistencias.setWordWrap(True)

        self.formulario.addWidget(self.notaExistencias, 9, 0, 1, 1)

        self.etiquetaPaginas = QLabel(FormularioLibro)
        self.etiquetaPaginas.setObjectName(u"etiquetaPaginas")

        self.formulario.addWidget(self.etiquetaPaginas, 10, 0, 1, 1)

        self.campoPaginas = QSpinBox(FormularioLibro)
        self.campoPaginas.setObjectName(u"campoPaginas")
        self.campoPaginas.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.campoPaginas.setMinimum(0)
        self.campoPaginas.setMaximum(99999)
        self.campoPaginas.setValue(0)

        self.formulario.addWidget(self.campoPaginas, 11, 0, 1, 1)

        self.formulario.setColumnStretch(0, 1)
        self.formulario.setColumnStretch(1, 1)

        self.disposicion.addLayout(self.formulario)

        self.etiquetaObligatorios = QLabel(FormularioLibro)
        self.etiquetaObligatorios.setObjectName(u"etiquetaObligatorios")
        self.etiquetaObligatorios.setWordWrap(True)

        self.disposicion.addWidget(self.etiquetaObligatorios)

        self.espacio = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.disposicion.addItem(self.espacio)

        self.filaBotones = QHBoxLayout()
        self.filaBotones.setSpacing(10)
        self.filaBotones.setObjectName(u"filaBotones")
        self.espacioBotones = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.filaBotones.addItem(self.espacioBotones)

        self.botonCancelar = QPushButton(FormularioLibro)
        self.botonCancelar.setObjectName(u"botonCancelar")
        self.botonCancelar.setMinimumHeight(44)
        self.botonCancelar.setProperty(u"secundario", True)

        self.filaBotones.addWidget(self.botonCancelar)

        self.botonGuardar = QPushButton(FormularioLibro)
        self.botonGuardar.setObjectName(u"botonGuardar")
        self.botonGuardar.setMinimumHeight(44)

        self.filaBotones.addWidget(self.botonGuardar)


        self.disposicion.addLayout(self.filaBotones)

        QWidget.setTabOrder(self.campoTitulo, self.campoAutor)
        QWidget.setTabOrder(self.campoAutor, self.campoEditorial)
        QWidget.setTabOrder(self.campoEditorial, self.campoColeccion)
        QWidget.setTabOrder(self.campoColeccion, self.campoAsignatura)
        QWidget.setTabOrder(self.campoAsignatura, self.campoExistencias)
        QWidget.setTabOrder(self.campoExistencias, self.campoAno)
        QWidget.setTabOrder(self.campoAno, self.campoPaginas)
        QWidget.setTabOrder(self.campoPaginas, self.botonGuardar)
        QWidget.setTabOrder(self.botonGuardar, self.botonCancelar)

        self.retranslateUi(FormularioLibro)

        QMetaObject.connectSlotsByName(FormularioLibro)
    # setupUi

    def retranslateUi(self, FormularioLibro):
        FormularioLibro.setWindowTitle(QCoreApplication.translate("FormularioLibro", u"Libro", None))
        self.etiquetaEncabezado.setText(QCoreApplication.translate("FormularioLibro", u"Registrar libro", None))
        self.etiquetaEncabezado.setProperty(u"rol", QCoreApplication.translate("FormularioLibro", u"tituloDialogo", None))
        self.etiquetaSubtitulo.setText("")
        self.etiquetaSubtitulo.setProperty(u"rol", QCoreApplication.translate("FormularioLibro", u"subtituloDialogo", None))
        self.tituloError.setText(QCoreApplication.translate("FormularioLibro", u"Revisa estos datos:", None))
        self.etiquetaError.setText("")
        self.etiquetaTitulo.setText(QCoreApplication.translate("FormularioLibro", u"T\u00edtulo <span style=\"color:#A3261B\">*</span>", None))
        self.etiquetaTitulo.setProperty(u"rol", QCoreApplication.translate("FormularioLibro", u"etiquetaCampo", None))
        self.etiquetaAutor.setText(QCoreApplication.translate("FormularioLibro", u"Autor <span style=\"color:#A3261B\">*</span>", None))
        self.etiquetaAutor.setProperty(u"rol", QCoreApplication.translate("FormularioLibro", u"etiquetaCampo", None))
        self.etiquetaEditorial.setText(QCoreApplication.translate("FormularioLibro", u"Editorial", None))
        self.etiquetaEditorial.setProperty(u"rol", QCoreApplication.translate("FormularioLibro", u"etiquetaCampo", None))
        self.etiquetaColeccion.setText(QCoreApplication.translate("FormularioLibro", u"Colecci\u00f3n", None))
        self.etiquetaColeccion.setProperty(u"rol", QCoreApplication.translate("FormularioLibro", u"etiquetaCampo", None))
        self.etiquetaAsignatura.setText(QCoreApplication.translate("FormularioLibro", u"Asignatura", None))
        self.etiquetaAsignatura.setProperty(u"rol", QCoreApplication.translate("FormularioLibro", u"etiquetaCampo", None))
        self.notaColeccion.setText(QCoreApplication.translate("FormularioLibro", u"Libros del Rinc\u00f3n, con los grados de cada una.", None))
        self.notaColeccion.setProperty(u"rol", QCoreApplication.translate("FormularioLibro", u"notaCampo", None))
        self.etiquetaExistencias.setText(QCoreApplication.translate("FormularioLibro", u"Ejemplares <span style=\"color:#A3261B\">*</span>", None))
        self.etiquetaExistencias.setProperty(u"rol", QCoreApplication.translate("FormularioLibro", u"etiquetaCampo", None))
        self.etiquetaAno.setText(QCoreApplication.translate("FormularioLibro", u"A\u00f1o de publicaci\u00f3n", None))
        self.etiquetaAno.setProperty(u"rol", QCoreApplication.translate("FormularioLibro", u"etiquetaCampo", None))
        self.campoAno.setSpecialValueText(QCoreApplication.translate("FormularioLibro", u"Sin especificar", None))
        self.notaExistencias.setText(QCoreApplication.translate("FormularioLibro", u"Los que est\u00e1n hoy en el estante.", None))
        self.notaExistencias.setProperty(u"rol", QCoreApplication.translate("FormularioLibro", u"notaCampo", None))
        self.etiquetaPaginas.setText(QCoreApplication.translate("FormularioLibro", u"N\u00famero de p\u00e1ginas", None))
        self.etiquetaPaginas.setProperty(u"rol", QCoreApplication.translate("FormularioLibro", u"etiquetaCampo", None))
        self.campoPaginas.setSpecialValueText(QCoreApplication.translate("FormularioLibro", u"Sin especificar", None))
        self.etiquetaObligatorios.setText(QCoreApplication.translate("FormularioLibro", u"<span style=\"color:#A3261B\">*</span> Campos obligatorios", None))
        self.etiquetaObligatorios.setProperty(u"rol", QCoreApplication.translate("FormularioLibro", u"notaCampo", None))
        self.botonCancelar.setText(QCoreApplication.translate("FormularioLibro", u"Cancelar", None))
        self.botonGuardar.setText(QCoreApplication.translate("FormularioLibro", u"Guardar", None))
    # retranslateUi

