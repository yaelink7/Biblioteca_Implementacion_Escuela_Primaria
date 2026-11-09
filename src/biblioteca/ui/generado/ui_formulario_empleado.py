# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formulario_empleado.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_FormularioEmpleado(object):
    def setupUi(self, FormularioEmpleado):
        if not FormularioEmpleado.objectName():
            FormularioEmpleado.setObjectName(u"FormularioEmpleado")
        FormularioEmpleado.resize(700, 700)
        self.disposicion = QVBoxLayout(FormularioEmpleado)
        self.disposicion.setSpacing(16)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(30, 26, 30, 26)
        self.encabezado = QVBoxLayout()
        self.encabezado.setSpacing(4)
        self.encabezado.setObjectName(u"encabezado")
        self.etiquetaEncabezado = QLabel(FormularioEmpleado)
        self.etiquetaEncabezado.setObjectName(u"etiquetaEncabezado")

        self.encabezado.addWidget(self.etiquetaEncabezado)

        self.etiquetaSubtitulo = QLabel(FormularioEmpleado)
        self.etiquetaSubtitulo.setObjectName(u"etiquetaSubtitulo")
        self.etiquetaSubtitulo.setWordWrap(True)

        self.encabezado.addWidget(self.etiquetaSubtitulo)


        self.disposicion.addLayout(self.encabezado)

        self.cajaError = QFrame(FormularioEmpleado)
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
        self.etiquetaCodigo = QLabel(FormularioEmpleado)
        self.etiquetaCodigo.setObjectName(u"etiquetaCodigo")

        self.formulario.addWidget(self.etiquetaCodigo, 0, 0, 1, 1)

        self.etiquetaPuesto = QLabel(FormularioEmpleado)
        self.etiquetaPuesto.setObjectName(u"etiquetaPuesto")

        self.formulario.addWidget(self.etiquetaPuesto, 0, 1, 1, 1)

        self.campoCodigo = QLineEdit(FormularioEmpleado)
        self.campoCodigo.setObjectName(u"campoCodigo")

        self.formulario.addWidget(self.campoCodigo, 1, 0, 1, 1)

        self.campoPuesto = QComboBox(FormularioEmpleado)
        self.campoPuesto.setObjectName(u"campoPuesto")

        self.formulario.addWidget(self.campoPuesto, 1, 1, 1, 1)

        self.etiquetaNombre = QLabel(FormularioEmpleado)
        self.etiquetaNombre.setObjectName(u"etiquetaNombre")

        self.formulario.addWidget(self.etiquetaNombre, 2, 0, 1, 1)

        self.etiquetaApellido = QLabel(FormularioEmpleado)
        self.etiquetaApellido.setObjectName(u"etiquetaApellido")

        self.formulario.addWidget(self.etiquetaApellido, 2, 1, 1, 1)

        self.campoNombre = QLineEdit(FormularioEmpleado)
        self.campoNombre.setObjectName(u"campoNombre")

        self.formulario.addWidget(self.campoNombre, 3, 0, 1, 1)

        self.campoApellido = QLineEdit(FormularioEmpleado)
        self.campoApellido.setObjectName(u"campoApellido")

        self.formulario.addWidget(self.campoApellido, 3, 1, 1, 1)

        self.etiquetaRol = QLabel(FormularioEmpleado)
        self.etiquetaRol.setObjectName(u"etiquetaRol")

        self.formulario.addWidget(self.etiquetaRol, 4, 0, 1, 1)

        self.etiquetaCorreo = QLabel(FormularioEmpleado)
        self.etiquetaCorreo.setObjectName(u"etiquetaCorreo")

        self.formulario.addWidget(self.etiquetaCorreo, 4, 1, 1, 1)

        self.campoRol = QComboBox(FormularioEmpleado)
        self.campoRol.addItem("")
        self.campoRol.addItem("")
        self.campoRol.setObjectName(u"campoRol")

        self.formulario.addWidget(self.campoRol, 5, 0, 1, 1)

        self.campoCorreo = QLineEdit(FormularioEmpleado)
        self.campoCorreo.setObjectName(u"campoCorreo")

        self.formulario.addWidget(self.campoCorreo, 5, 1, 1, 1)

        self.notaRol = QLabel(FormularioEmpleado)
        self.notaRol.setObjectName(u"notaRol")
        self.notaRol.setWordWrap(True)

        self.formulario.addWidget(self.notaRol, 6, 0, 1, 1)

        self.notaCorreo = QLabel(FormularioEmpleado)
        self.notaCorreo.setObjectName(u"notaCorreo")
        self.notaCorreo.setWordWrap(True)

        self.formulario.addWidget(self.notaCorreo, 6, 1, 1, 1)

        self.etiquetaTelefono = QLabel(FormularioEmpleado)
        self.etiquetaTelefono.setObjectName(u"etiquetaTelefono")

        self.formulario.addWidget(self.etiquetaTelefono, 7, 0, 1, 1)

        self.etiquetaColonia = QLabel(FormularioEmpleado)
        self.etiquetaColonia.setObjectName(u"etiquetaColonia")

        self.formulario.addWidget(self.etiquetaColonia, 7, 1, 1, 1)

        self.campoTelefono = QLineEdit(FormularioEmpleado)
        self.campoTelefono.setObjectName(u"campoTelefono")

        self.formulario.addWidget(self.campoTelefono, 8, 0, 1, 1)

        self.campoColonia = QLineEdit(FormularioEmpleado)
        self.campoColonia.setObjectName(u"campoColonia")

        self.formulario.addWidget(self.campoColonia, 8, 1, 1, 1)

        self.etiquetaCalle = QLabel(FormularioEmpleado)
        self.etiquetaCalle.setObjectName(u"etiquetaCalle")

        self.formulario.addWidget(self.etiquetaCalle, 9, 0, 1, 2)

        self.campoCalle = QLineEdit(FormularioEmpleado)
        self.campoCalle.setObjectName(u"campoCalle")

        self.formulario.addWidget(self.campoCalle, 10, 0, 1, 2)

        self.formulario.setColumnStretch(0, 1)
        self.formulario.setColumnStretch(1, 1)

        self.disposicion.addLayout(self.formulario)

        self.etiquetaAviso = QLabel(FormularioEmpleado)
        self.etiquetaAviso.setObjectName(u"etiquetaAviso")
        self.etiquetaAviso.setWordWrap(True)

        self.disposicion.addWidget(self.etiquetaAviso)

        self.espacio = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.disposicion.addItem(self.espacio)

        self.filaBotones = QHBoxLayout()
        self.filaBotones.setSpacing(10)
        self.filaBotones.setObjectName(u"filaBotones")
        self.espacioBotones = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.filaBotones.addItem(self.espacioBotones)

        self.botonCancelar = QPushButton(FormularioEmpleado)
        self.botonCancelar.setObjectName(u"botonCancelar")
        self.botonCancelar.setMinimumHeight(44)
        self.botonCancelar.setProperty(u"secundario", True)

        self.filaBotones.addWidget(self.botonCancelar)

        self.botonGuardar = QPushButton(FormularioEmpleado)
        self.botonGuardar.setObjectName(u"botonGuardar")
        self.botonGuardar.setMinimumHeight(44)

        self.filaBotones.addWidget(self.botonGuardar)


        self.disposicion.addLayout(self.filaBotones)

        QWidget.setTabOrder(self.campoCodigo, self.campoPuesto)
        QWidget.setTabOrder(self.campoPuesto, self.campoNombre)
        QWidget.setTabOrder(self.campoNombre, self.campoApellido)
        QWidget.setTabOrder(self.campoApellido, self.campoRol)
        QWidget.setTabOrder(self.campoRol, self.campoCorreo)
        QWidget.setTabOrder(self.campoCorreo, self.campoTelefono)
        QWidget.setTabOrder(self.campoTelefono, self.campoColonia)
        QWidget.setTabOrder(self.campoColonia, self.campoCalle)
        QWidget.setTabOrder(self.campoCalle, self.botonGuardar)
        QWidget.setTabOrder(self.botonGuardar, self.botonCancelar)

        self.retranslateUi(FormularioEmpleado)

        QMetaObject.connectSlotsByName(FormularioEmpleado)
    # setupUi

    def retranslateUi(self, FormularioEmpleado):
        FormularioEmpleado.setWindowTitle(QCoreApplication.translate("FormularioEmpleado", u"Empleado", None))
        self.etiquetaEncabezado.setText(QCoreApplication.translate("FormularioEmpleado", u"Registrar empleado", None))
        self.etiquetaEncabezado.setProperty(u"rol", QCoreApplication.translate("FormularioEmpleado", u"tituloDialogo", None))
        self.etiquetaSubtitulo.setText("")
        self.etiquetaSubtitulo.setProperty(u"rol", QCoreApplication.translate("FormularioEmpleado", u"subtituloDialogo", None))
        self.tituloError.setText(QCoreApplication.translate("FormularioEmpleado", u"Revisa estos datos:", None))
        self.etiquetaError.setText("")
        self.etiquetaCodigo.setText(QCoreApplication.translate("FormularioEmpleado", u"C\u00f3digo <span style=\"color:#A3261B\">*</span>", None))
        self.etiquetaCodigo.setProperty(u"rol", QCoreApplication.translate("FormularioEmpleado", u"etiquetaCampo", None))
        self.etiquetaPuesto.setText(QCoreApplication.translate("FormularioEmpleado", u"Puesto <span style=\"color:#A3261B\">*</span>", None))
        self.etiquetaPuesto.setProperty(u"rol", QCoreApplication.translate("FormularioEmpleado", u"etiquetaCampo", None))
        self.campoCodigo.setPlaceholderText(QCoreApplication.translate("FormularioEmpleado", u"EMP-004", None))
        self.etiquetaNombre.setText(QCoreApplication.translate("FormularioEmpleado", u"Nombre <span style=\"color:#A3261B\">*</span>", None))
        self.etiquetaNombre.setProperty(u"rol", QCoreApplication.translate("FormularioEmpleado", u"etiquetaCampo", None))
        self.etiquetaApellido.setText(QCoreApplication.translate("FormularioEmpleado", u"Apellidos <span style=\"color:#A3261B\">*</span>", None))
        self.etiquetaApellido.setProperty(u"rol", QCoreApplication.translate("FormularioEmpleado", u"etiquetaCampo", None))
        self.etiquetaRol.setText(QCoreApplication.translate("FormularioEmpleado", u"Perfil en el sistema <span style=\"color:#A3261B\">*</span>", None))
        self.etiquetaRol.setProperty(u"rol", QCoreApplication.translate("FormularioEmpleado", u"etiquetaCampo", None))
        self.etiquetaCorreo.setText(QCoreApplication.translate("FormularioEmpleado", u"Correo <span style=\"color:#A3261B\">*</span>", None))
        self.etiquetaCorreo.setProperty(u"rol", QCoreApplication.translate("FormularioEmpleado", u"etiquetaCampo", None))
        self.campoRol.setItemText(0, QCoreApplication.translate("FormularioEmpleado", u"Bibliotecario", None))
        self.campoRol.setItemText(1, QCoreApplication.translate("FormularioEmpleado", u"Administrador", None))

        self.campoCorreo.setPlaceholderText(QCoreApplication.translate("FormularioEmpleado", u"empleado@ejemplo.com", None))
        self.notaRol.setText("")
        self.notaRol.setProperty(u"rol", QCoreApplication.translate("FormularioEmpleado", u"notaCampo", None))
        self.notaCorreo.setText(QCoreApplication.translate("FormularioEmpleado", u"Es con lo que inicia sesi\u00f3n.", None))
        self.notaCorreo.setProperty(u"rol", QCoreApplication.translate("FormularioEmpleado", u"notaCampo", None))
        self.etiquetaTelefono.setText(QCoreApplication.translate("FormularioEmpleado", u"Tel\u00e9fono", None))
        self.etiquetaTelefono.setProperty(u"rol", QCoreApplication.translate("FormularioEmpleado", u"etiquetaCampo", None))
        self.etiquetaColonia.setText(QCoreApplication.translate("FormularioEmpleado", u"Colonia", None))
        self.etiquetaColonia.setProperty(u"rol", QCoreApplication.translate("FormularioEmpleado", u"etiquetaCampo", None))
        self.etiquetaCalle.setText(QCoreApplication.translate("FormularioEmpleado", u"Calle y n\u00famero", None))
        self.etiquetaCalle.setProperty(u"rol", QCoreApplication.translate("FormularioEmpleado", u"etiquetaCampo", None))
        self.etiquetaAviso.setText(QCoreApplication.translate("FormularioEmpleado", u"<span style=\"color:#A3261B\">*</span> Campos obligatorios. El correo es con lo que el empleado inicia sesi\u00f3n.", None))
        self.etiquetaAviso.setProperty(u"rol", QCoreApplication.translate("FormularioEmpleado", u"notaCampo", None))
        self.botonCancelar.setText(QCoreApplication.translate("FormularioEmpleado", u"Cancelar", None))
        self.botonGuardar.setText(QCoreApplication.translate("FormularioEmpleado", u"Guardar", None))
    # retranslateUi

