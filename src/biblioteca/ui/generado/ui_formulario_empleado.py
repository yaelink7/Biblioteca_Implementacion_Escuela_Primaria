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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_FormularioEmpleado(object):
    def setupUi(self, FormularioEmpleado):
        if not FormularioEmpleado.objectName():
            FormularioEmpleado.setObjectName(u"FormularioEmpleado")
        FormularioEmpleado.resize(480, 500)
        self.disposicion = QVBoxLayout(FormularioEmpleado)
        self.disposicion.setSpacing(12)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(24, 24, 24, 24)
        self.formulario = QFormLayout()
        self.formulario.setObjectName(u"formulario")
        self.formulario.setHorizontalSpacing(14)
        self.formulario.setVerticalSpacing(10)
        self.etiquetaCodigo = QLabel(FormularioEmpleado)
        self.etiquetaCodigo.setObjectName(u"etiquetaCodigo")

        self.formulario.setWidget(0, QFormLayout.ItemRole.LabelRole, self.etiquetaCodigo)

        self.campoCodigo = QLineEdit(FormularioEmpleado)
        self.campoCodigo.setObjectName(u"campoCodigo")
        self.campoCodigo.setMinimumHeight(32)

        self.formulario.setWidget(0, QFormLayout.ItemRole.FieldRole, self.campoCodigo)

        self.etiquetaNombre = QLabel(FormularioEmpleado)
        self.etiquetaNombre.setObjectName(u"etiquetaNombre")

        self.formulario.setWidget(1, QFormLayout.ItemRole.LabelRole, self.etiquetaNombre)

        self.campoNombre = QLineEdit(FormularioEmpleado)
        self.campoNombre.setObjectName(u"campoNombre")
        self.campoNombre.setMinimumHeight(32)

        self.formulario.setWidget(1, QFormLayout.ItemRole.FieldRole, self.campoNombre)

        self.etiquetaApellido = QLabel(FormularioEmpleado)
        self.etiquetaApellido.setObjectName(u"etiquetaApellido")

        self.formulario.setWidget(2, QFormLayout.ItemRole.LabelRole, self.etiquetaApellido)

        self.campoApellido = QLineEdit(FormularioEmpleado)
        self.campoApellido.setObjectName(u"campoApellido")
        self.campoApellido.setMinimumHeight(32)

        self.formulario.setWidget(2, QFormLayout.ItemRole.FieldRole, self.campoApellido)

        self.etiquetaPuesto = QLabel(FormularioEmpleado)
        self.etiquetaPuesto.setObjectName(u"etiquetaPuesto")

        self.formulario.setWidget(3, QFormLayout.ItemRole.LabelRole, self.etiquetaPuesto)

        self.campoPuesto = QComboBox(FormularioEmpleado)
        self.campoPuesto.addItem("")
        self.campoPuesto.addItem("")
        self.campoPuesto.addItem("")
        self.campoPuesto.addItem("")
        self.campoPuesto.setObjectName(u"campoPuesto")
        self.campoPuesto.setEditable(True)
        self.campoPuesto.setMinimumHeight(32)

        self.formulario.setWidget(3, QFormLayout.ItemRole.FieldRole, self.campoPuesto)

        self.etiquetaRol = QLabel(FormularioEmpleado)
        self.etiquetaRol.setObjectName(u"etiquetaRol")

        self.formulario.setWidget(4, QFormLayout.ItemRole.LabelRole, self.etiquetaRol)

        self.campoRol = QComboBox(FormularioEmpleado)
        self.campoRol.addItem("")
        self.campoRol.addItem("")
        self.campoRol.setObjectName(u"campoRol")
        self.campoRol.setMinimumHeight(32)

        self.formulario.setWidget(4, QFormLayout.ItemRole.FieldRole, self.campoRol)

        self.etiquetaCorreo = QLabel(FormularioEmpleado)
        self.etiquetaCorreo.setObjectName(u"etiquetaCorreo")

        self.formulario.setWidget(5, QFormLayout.ItemRole.LabelRole, self.etiquetaCorreo)

        self.campoCorreo = QLineEdit(FormularioEmpleado)
        self.campoCorreo.setObjectName(u"campoCorreo")
        self.campoCorreo.setMinimumHeight(32)

        self.formulario.setWidget(5, QFormLayout.ItemRole.FieldRole, self.campoCorreo)

        self.etiquetaTelefono = QLabel(FormularioEmpleado)
        self.etiquetaTelefono.setObjectName(u"etiquetaTelefono")

        self.formulario.setWidget(6, QFormLayout.ItemRole.LabelRole, self.etiquetaTelefono)

        self.campoTelefono = QLineEdit(FormularioEmpleado)
        self.campoTelefono.setObjectName(u"campoTelefono")
        self.campoTelefono.setMinimumHeight(32)

        self.formulario.setWidget(6, QFormLayout.ItemRole.FieldRole, self.campoTelefono)

        self.etiquetaCalle = QLabel(FormularioEmpleado)
        self.etiquetaCalle.setObjectName(u"etiquetaCalle")

        self.formulario.setWidget(7, QFormLayout.ItemRole.LabelRole, self.etiquetaCalle)

        self.campoCalle = QLineEdit(FormularioEmpleado)
        self.campoCalle.setObjectName(u"campoCalle")
        self.campoCalle.setMinimumHeight(32)

        self.formulario.setWidget(7, QFormLayout.ItemRole.FieldRole, self.campoCalle)

        self.etiquetaColonia = QLabel(FormularioEmpleado)
        self.etiquetaColonia.setObjectName(u"etiquetaColonia")

        self.formulario.setWidget(8, QFormLayout.ItemRole.LabelRole, self.etiquetaColonia)

        self.campoColonia = QLineEdit(FormularioEmpleado)
        self.campoColonia.setObjectName(u"campoColonia")
        self.campoColonia.setMinimumHeight(32)

        self.formulario.setWidget(8, QFormLayout.ItemRole.FieldRole, self.campoColonia)


        self.disposicion.addLayout(self.formulario)

        self.etiquetaAviso = QLabel(FormularioEmpleado)
        self.etiquetaAviso.setObjectName(u"etiquetaAviso")
        self.etiquetaAviso.setWordWrap(True)

        self.disposicion.addWidget(self.etiquetaAviso)

        self.etiquetaError = QLabel(FormularioEmpleado)
        self.etiquetaError.setObjectName(u"etiquetaError")
        self.etiquetaError.setWordWrap(True)
        self.etiquetaError.setMinimumHeight(40)
        self.etiquetaError.setAlignment(Qt.AlignTop)

        self.disposicion.addWidget(self.etiquetaError)

        self.espacio = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.disposicion.addItem(self.espacio)

        self.filaBotones = QHBoxLayout()
        self.filaBotones.setObjectName(u"filaBotones")
        self.espacioBotones = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.filaBotones.addItem(self.espacioBotones)

        self.botonCancelar = QPushButton(FormularioEmpleado)
        self.botonCancelar.setObjectName(u"botonCancelar")
        self.botonCancelar.setMinimumHeight(34)

        self.filaBotones.addWidget(self.botonCancelar)

        self.botonGuardar = QPushButton(FormularioEmpleado)
        self.botonGuardar.setObjectName(u"botonGuardar")
        self.botonGuardar.setMinimumHeight(34)

        self.filaBotones.addWidget(self.botonGuardar)


        self.disposicion.addLayout(self.filaBotones)


        self.retranslateUi(FormularioEmpleado)

        self.botonGuardar.setDefault(True)


        QMetaObject.connectSlotsByName(FormularioEmpleado)
    # setupUi

    def retranslateUi(self, FormularioEmpleado):
        FormularioEmpleado.setWindowTitle(QCoreApplication.translate("FormularioEmpleado", u"Empleado", None))
        self.etiquetaCodigo.setText(QCoreApplication.translate("FormularioEmpleado", u"C\u00f3digo *", None))
        self.campoCodigo.setPlaceholderText(QCoreApplication.translate("FormularioEmpleado", u"EMP-002", None))
        self.etiquetaNombre.setText(QCoreApplication.translate("FormularioEmpleado", u"Nombre *", None))
        self.etiquetaApellido.setText(QCoreApplication.translate("FormularioEmpleado", u"Apellidos *", None))
        self.etiquetaPuesto.setText(QCoreApplication.translate("FormularioEmpleado", u"Puesto *", None))
        self.campoPuesto.setItemText(0, QCoreApplication.translate("FormularioEmpleado", u"Bibliotecaria", None))
        self.campoPuesto.setItemText(1, QCoreApplication.translate("FormularioEmpleado", u"Auxiliar", None))
        self.campoPuesto.setItemText(2, QCoreApplication.translate("FormularioEmpleado", u"Docente encargado", None))
        self.campoPuesto.setItemText(3, QCoreApplication.translate("FormularioEmpleado", u"Direcci\u00f3n", None))

        self.etiquetaRol.setText(QCoreApplication.translate("FormularioEmpleado", u"Perfil en el sistema *", None))
        self.campoRol.setItemText(0, QCoreApplication.translate("FormularioEmpleado", u"Bibliotecario", None))
        self.campoRol.setItemText(1, QCoreApplication.translate("FormularioEmpleado", u"Administrador", None))

        self.etiquetaCorreo.setText(QCoreApplication.translate("FormularioEmpleado", u"Correo *", None))
        self.campoCorreo.setPlaceholderText(QCoreApplication.translate("FormularioEmpleado", u"empleado@ejemplo.com", None))
        self.etiquetaTelefono.setText(QCoreApplication.translate("FormularioEmpleado", u"Tel\u00e9fono", None))
        self.etiquetaCalle.setText(QCoreApplication.translate("FormularioEmpleado", u"Calle y n\u00famero", None))
        self.etiquetaColonia.setText(QCoreApplication.translate("FormularioEmpleado", u"Colonia", None))
        self.etiquetaAviso.setText(QCoreApplication.translate("FormularioEmpleado", u"* Campos obligatorios. El correo es con lo que el empleado inicia sesi\u00f3n.", None))
        self.etiquetaError.setText("")
        self.botonCancelar.setText(QCoreApplication.translate("FormularioEmpleado", u"Cancelar", None))
        self.botonGuardar.setText(QCoreApplication.translate("FormularioEmpleado", u"Guardar", None))
    # retranslateUi

