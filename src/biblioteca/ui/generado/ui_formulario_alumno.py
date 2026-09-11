# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'formulario_alumno.ui'
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
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_FormularioAlumno(object):
    def setupUi(self, FormularioAlumno):
        if not FormularioAlumno.objectName():
            FormularioAlumno.setObjectName(u"FormularioAlumno")
        FormularioAlumno.resize(500, 560)
        self.disposicion = QVBoxLayout(FormularioAlumno)
        self.disposicion.setSpacing(12)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(24, 24, 24, 24)
        self.formulario = QFormLayout()
        self.formulario.setObjectName(u"formulario")
        self.formulario.setHorizontalSpacing(14)
        self.formulario.setVerticalSpacing(10)
        self.etiquetaCodigo = QLabel(FormularioAlumno)
        self.etiquetaCodigo.setObjectName(u"etiquetaCodigo")

        self.formulario.setWidget(0, QFormLayout.ItemRole.LabelRole, self.etiquetaCodigo)

        self.campoCodigo = QLineEdit(FormularioAlumno)
        self.campoCodigo.setObjectName(u"campoCodigo")
        self.campoCodigo.setMinimumHeight(32)

        self.formulario.setWidget(0, QFormLayout.ItemRole.FieldRole, self.campoCodigo)

        self.etiquetaNombre = QLabel(FormularioAlumno)
        self.etiquetaNombre.setObjectName(u"etiquetaNombre")

        self.formulario.setWidget(1, QFormLayout.ItemRole.LabelRole, self.etiquetaNombre)

        self.campoNombre = QLineEdit(FormularioAlumno)
        self.campoNombre.setObjectName(u"campoNombre")
        self.campoNombre.setMinimumHeight(32)

        self.formulario.setWidget(1, QFormLayout.ItemRole.FieldRole, self.campoNombre)

        self.etiquetaApellido = QLabel(FormularioAlumno)
        self.etiquetaApellido.setObjectName(u"etiquetaApellido")

        self.formulario.setWidget(2, QFormLayout.ItemRole.LabelRole, self.etiquetaApellido)

        self.campoApellido = QLineEdit(FormularioAlumno)
        self.campoApellido.setObjectName(u"campoApellido")
        self.campoApellido.setMinimumHeight(32)

        self.formulario.setWidget(2, QFormLayout.ItemRole.FieldRole, self.campoApellido)

        self.etiquetaGrado = QLabel(FormularioAlumno)
        self.etiquetaGrado.setObjectName(u"etiquetaGrado")

        self.formulario.setWidget(3, QFormLayout.ItemRole.LabelRole, self.etiquetaGrado)

        self.campoGrado = QSpinBox(FormularioAlumno)
        self.campoGrado.setObjectName(u"campoGrado")
        self.campoGrado.setMinimum(0)
        self.campoGrado.setMaximum(6)
        self.campoGrado.setValue(0)
        self.campoGrado.setMinimumHeight(32)

        self.formulario.setWidget(3, QFormLayout.ItemRole.FieldRole, self.campoGrado)

        self.etiquetaGrupo = QLabel(FormularioAlumno)
        self.etiquetaGrupo.setObjectName(u"etiquetaGrupo")

        self.formulario.setWidget(4, QFormLayout.ItemRole.LabelRole, self.etiquetaGrupo)

        self.campoGrupo = QComboBox(FormularioAlumno)
        self.campoGrupo.addItem("")
        self.campoGrupo.addItem("")
        self.campoGrupo.addItem("")
        self.campoGrupo.addItem("")
        self.campoGrupo.addItem("")
        self.campoGrupo.setObjectName(u"campoGrupo")
        self.campoGrupo.setEditable(True)
        self.campoGrupo.setMinimumHeight(32)

        self.formulario.setWidget(4, QFormLayout.ItemRole.FieldRole, self.campoGrupo)

        self.etiquetaCorreo = QLabel(FormularioAlumno)
        self.etiquetaCorreo.setObjectName(u"etiquetaCorreo")

        self.formulario.setWidget(5, QFormLayout.ItemRole.LabelRole, self.etiquetaCorreo)

        self.campoCorreo = QLineEdit(FormularioAlumno)
        self.campoCorreo.setObjectName(u"campoCorreo")
        self.campoCorreo.setMinimumHeight(32)

        self.formulario.setWidget(5, QFormLayout.ItemRole.FieldRole, self.campoCorreo)

        self.etiquetaTelefono = QLabel(FormularioAlumno)
        self.etiquetaTelefono.setObjectName(u"etiquetaTelefono")

        self.formulario.setWidget(6, QFormLayout.ItemRole.LabelRole, self.etiquetaTelefono)

        self.campoTelefono = QLineEdit(FormularioAlumno)
        self.campoTelefono.setObjectName(u"campoTelefono")
        self.campoTelefono.setMinimumHeight(32)

        self.formulario.setWidget(6, QFormLayout.ItemRole.FieldRole, self.campoTelefono)

        self.etiquetaCalle = QLabel(FormularioAlumno)
        self.etiquetaCalle.setObjectName(u"etiquetaCalle")

        self.formulario.setWidget(7, QFormLayout.ItemRole.LabelRole, self.etiquetaCalle)

        self.campoCalle = QLineEdit(FormularioAlumno)
        self.campoCalle.setObjectName(u"campoCalle")
        self.campoCalle.setMinimumHeight(32)

        self.formulario.setWidget(7, QFormLayout.ItemRole.FieldRole, self.campoCalle)

        self.etiquetaColonia = QLabel(FormularioAlumno)
        self.etiquetaColonia.setObjectName(u"etiquetaColonia")

        self.formulario.setWidget(8, QFormLayout.ItemRole.LabelRole, self.etiquetaColonia)

        self.campoColonia = QLineEdit(FormularioAlumno)
        self.campoColonia.setObjectName(u"campoColonia")
        self.campoColonia.setMinimumHeight(32)

        self.formulario.setWidget(8, QFormLayout.ItemRole.FieldRole, self.campoColonia)


        self.disposicion.addLayout(self.formulario)

        self.etiquetaAviso = QLabel(FormularioAlumno)
        self.etiquetaAviso.setObjectName(u"etiquetaAviso")
        self.etiquetaAviso.setWordWrap(True)

        self.disposicion.addWidget(self.etiquetaAviso)

        self.etiquetaError = QLabel(FormularioAlumno)
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

        self.botonCancelar = QPushButton(FormularioAlumno)
        self.botonCancelar.setObjectName(u"botonCancelar")
        self.botonCancelar.setMinimumHeight(34)

        self.filaBotones.addWidget(self.botonCancelar)

        self.botonGuardar = QPushButton(FormularioAlumno)
        self.botonGuardar.setObjectName(u"botonGuardar")
        self.botonGuardar.setMinimumHeight(34)

        self.filaBotones.addWidget(self.botonGuardar)


        self.disposicion.addLayout(self.filaBotones)


        self.retranslateUi(FormularioAlumno)

        self.botonGuardar.setDefault(True)


        QMetaObject.connectSlotsByName(FormularioAlumno)
    # setupUi

    def retranslateUi(self, FormularioAlumno):
        FormularioAlumno.setWindowTitle(QCoreApplication.translate("FormularioAlumno", u"Alumno", None))
        self.etiquetaCodigo.setText(QCoreApplication.translate("FormularioAlumno", u"C\u00f3digo *", None))
        self.campoCodigo.setPlaceholderText(QCoreApplication.translate("FormularioAlumno", u"A-0401", None))
        self.etiquetaNombre.setText(QCoreApplication.translate("FormularioAlumno", u"Nombre *", None))
        self.etiquetaApellido.setText(QCoreApplication.translate("FormularioAlumno", u"Apellidos *", None))
        self.etiquetaGrado.setText(QCoreApplication.translate("FormularioAlumno", u"Grado", None))
        self.campoGrado.setSpecialValueText(QCoreApplication.translate("FormularioAlumno", u"Sin asignar", None))
        self.etiquetaGrupo.setText(QCoreApplication.translate("FormularioAlumno", u"Grupo", None))
        self.campoGrupo.setItemText(0, "")
        self.campoGrupo.setItemText(1, QCoreApplication.translate("FormularioAlumno", u"A", None))
        self.campoGrupo.setItemText(2, QCoreApplication.translate("FormularioAlumno", u"B", None))
        self.campoGrupo.setItemText(3, QCoreApplication.translate("FormularioAlumno", u"C", None))
        self.campoGrupo.setItemText(4, QCoreApplication.translate("FormularioAlumno", u"D", None))

        self.etiquetaCorreo.setText(QCoreApplication.translate("FormularioAlumno", u"Correo del tutor", None))
        self.campoCorreo.setPlaceholderText(QCoreApplication.translate("FormularioAlumno", u"tutor@ejemplo.com", None))
        self.etiquetaTelefono.setText(QCoreApplication.translate("FormularioAlumno", u"Tel\u00e9fono", None))
        self.etiquetaCalle.setText(QCoreApplication.translate("FormularioAlumno", u"Calle y n\u00famero", None))
        self.etiquetaColonia.setText(QCoreApplication.translate("FormularioAlumno", u"Colonia", None))
        self.etiquetaAviso.setText(QCoreApplication.translate("FormularioAlumno", u"* Campos obligatorios. Los datos del tutor sirven para avisar de pr\u00e9stamos vencidos.", None))
        self.etiquetaError.setText("")
        self.botonCancelar.setText(QCoreApplication.translate("FormularioAlumno", u"Cancelar", None))
        self.botonGuardar.setText(QCoreApplication.translate("FormularioAlumno", u"Guardar", None))
    # retranslateUi

