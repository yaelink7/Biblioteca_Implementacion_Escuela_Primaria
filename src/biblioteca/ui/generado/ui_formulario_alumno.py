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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_FormularioAlumno(object):
    def setupUi(self, FormularioAlumno):
        if not FormularioAlumno.objectName():
            FormularioAlumno.setObjectName(u"FormularioAlumno")
        FormularioAlumno.resize(700, 780)
        self.disposicion = QVBoxLayout(FormularioAlumno)
        self.disposicion.setSpacing(16)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(30, 26, 30, 26)
        self.encabezado = QVBoxLayout()
        self.encabezado.setSpacing(4)
        self.encabezado.setObjectName(u"encabezado")
        self.etiquetaEncabezado = QLabel(FormularioAlumno)
        self.etiquetaEncabezado.setObjectName(u"etiquetaEncabezado")

        self.encabezado.addWidget(self.etiquetaEncabezado)

        self.etiquetaSubtitulo = QLabel(FormularioAlumno)
        self.etiquetaSubtitulo.setObjectName(u"etiquetaSubtitulo")
        self.etiquetaSubtitulo.setWordWrap(True)

        self.encabezado.addWidget(self.etiquetaSubtitulo)


        self.disposicion.addLayout(self.encabezado)

        self.cajaError = QFrame(FormularioAlumno)
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
        self.etiquetaCodigo = QLabel(FormularioAlumno)
        self.etiquetaCodigo.setObjectName(u"etiquetaCodigo")

        self.formulario.addWidget(self.etiquetaCodigo, 0, 0, 1, 1)

        self.etiquetaCurp = QLabel(FormularioAlumno)
        self.etiquetaCurp.setObjectName(u"etiquetaCurp")

        self.formulario.addWidget(self.etiquetaCurp, 0, 1, 1, 1)

        self.campoCodigo = QLineEdit(FormularioAlumno)
        self.campoCodigo.setObjectName(u"campoCodigo")

        self.formulario.addWidget(self.campoCodigo, 1, 0, 1, 1)

        self.campoCurp = QLineEdit(FormularioAlumno)
        self.campoCurp.setObjectName(u"campoCurp")
        self.campoCurp.setMaxLength(18)

        self.formulario.addWidget(self.campoCurp, 1, 1, 1, 1)

        self.notaCurp = QLabel(FormularioAlumno)
        self.notaCurp.setObjectName(u"notaCurp")
        self.notaCurp.setWordWrap(True)

        self.formulario.addWidget(self.notaCurp, 2, 1, 1, 1)

        self.etiquetaNombre = QLabel(FormularioAlumno)
        self.etiquetaNombre.setObjectName(u"etiquetaNombre")

        self.formulario.addWidget(self.etiquetaNombre, 3, 0, 1, 1)

        self.etiquetaApellido = QLabel(FormularioAlumno)
        self.etiquetaApellido.setObjectName(u"etiquetaApellido")

        self.formulario.addWidget(self.etiquetaApellido, 3, 1, 1, 1)

        self.campoNombre = QLineEdit(FormularioAlumno)
        self.campoNombre.setObjectName(u"campoNombre")

        self.formulario.addWidget(self.campoNombre, 4, 0, 1, 1)

        self.campoApellido = QLineEdit(FormularioAlumno)
        self.campoApellido.setObjectName(u"campoApellido")

        self.formulario.addWidget(self.campoApellido, 4, 1, 1, 1)

        self.etiquetaGrado = QLabel(FormularioAlumno)
        self.etiquetaGrado.setObjectName(u"etiquetaGrado")

        self.formulario.addWidget(self.etiquetaGrado, 5, 0, 1, 1)

        self.etiquetaGrupo = QLabel(FormularioAlumno)
        self.etiquetaGrupo.setObjectName(u"etiquetaGrupo")

        self.formulario.addWidget(self.etiquetaGrupo, 5, 1, 1, 1)

        self.campoGrado = QComboBox(FormularioAlumno)
        self.campoGrado.setObjectName(u"campoGrado")

        self.formulario.addWidget(self.campoGrado, 6, 0, 1, 1)

        self.campoGrupo = QComboBox(FormularioAlumno)
        self.campoGrupo.setObjectName(u"campoGrupo")

        self.formulario.addWidget(self.campoGrupo, 6, 1, 1, 1)

        self.etiquetaMaestro = QLabel(FormularioAlumno)
        self.etiquetaMaestro.setObjectName(u"etiquetaMaestro")

        self.formulario.addWidget(self.etiquetaMaestro, 7, 0, 1, 2)

        self.valorMaestro = QLabel(FormularioAlumno)
        self.valorMaestro.setObjectName(u"valorMaestro")
        self.valorMaestro.setWordWrap(True)

        self.formulario.addWidget(self.valorMaestro, 8, 0, 1, 2)

        self.separadorTutor = QLabel(FormularioAlumno)
        self.separadorTutor.setObjectName(u"separadorTutor")

        self.formulario.addWidget(self.separadorTutor, 9, 0, 1, 2)

        self.etiquetaTelefono = QLabel(FormularioAlumno)
        self.etiquetaTelefono.setObjectName(u"etiquetaTelefono")

        self.formulario.addWidget(self.etiquetaTelefono, 10, 0, 1, 1)

        self.etiquetaColonia = QLabel(FormularioAlumno)
        self.etiquetaColonia.setObjectName(u"etiquetaColonia")

        self.formulario.addWidget(self.etiquetaColonia, 10, 1, 1, 1)

        self.campoTelefono = QLineEdit(FormularioAlumno)
        self.campoTelefono.setObjectName(u"campoTelefono")

        self.formulario.addWidget(self.campoTelefono, 11, 0, 1, 1)

        self.campoColonia = QLineEdit(FormularioAlumno)
        self.campoColonia.setObjectName(u"campoColonia")

        self.formulario.addWidget(self.campoColonia, 11, 1, 1, 1)

        self.etiquetaCalle = QLabel(FormularioAlumno)
        self.etiquetaCalle.setObjectName(u"etiquetaCalle")

        self.formulario.addWidget(self.etiquetaCalle, 12, 0, 1, 2)

        self.campoCalle = QLineEdit(FormularioAlumno)
        self.campoCalle.setObjectName(u"campoCalle")

        self.formulario.addWidget(self.campoCalle, 13, 0, 1, 2)

        self.formulario.setColumnStretch(0, 1)
        self.formulario.setColumnStretch(1, 1)

        self.disposicion.addLayout(self.formulario)

        self.etiquetaAviso = QLabel(FormularioAlumno)
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

        self.botonCancelar = QPushButton(FormularioAlumno)
        self.botonCancelar.setObjectName(u"botonCancelar")
        self.botonCancelar.setMinimumHeight(44)
        self.botonCancelar.setProperty(u"secundario", True)

        self.filaBotones.addWidget(self.botonCancelar)

        self.botonGuardar = QPushButton(FormularioAlumno)
        self.botonGuardar.setObjectName(u"botonGuardar")
        self.botonGuardar.setMinimumHeight(44)

        self.filaBotones.addWidget(self.botonGuardar)


        self.disposicion.addLayout(self.filaBotones)

        QWidget.setTabOrder(self.campoCodigo, self.campoCurp)
        QWidget.setTabOrder(self.campoCurp, self.campoNombre)
        QWidget.setTabOrder(self.campoNombre, self.campoApellido)
        QWidget.setTabOrder(self.campoApellido, self.campoGrado)
        QWidget.setTabOrder(self.campoGrado, self.campoGrupo)
        QWidget.setTabOrder(self.campoGrupo, self.campoTelefono)
        QWidget.setTabOrder(self.campoTelefono, self.campoColonia)
        QWidget.setTabOrder(self.campoColonia, self.campoCalle)
        QWidget.setTabOrder(self.campoCalle, self.botonGuardar)
        QWidget.setTabOrder(self.botonGuardar, self.botonCancelar)

        self.retranslateUi(FormularioAlumno)

        QMetaObject.connectSlotsByName(FormularioAlumno)
    # setupUi

    def retranslateUi(self, FormularioAlumno):
        FormularioAlumno.setWindowTitle(QCoreApplication.translate("FormularioAlumno", u"Alumno", None))
        self.etiquetaEncabezado.setText(QCoreApplication.translate("FormularioAlumno", u"Registrar alumno", None))
        self.etiquetaEncabezado.setProperty(u"rol", QCoreApplication.translate("FormularioAlumno", u"tituloDialogo", None))
        self.etiquetaSubtitulo.setText("")
        self.etiquetaSubtitulo.setProperty(u"rol", QCoreApplication.translate("FormularioAlumno", u"subtituloDialogo", None))
        self.tituloError.setText(QCoreApplication.translate("FormularioAlumno", u"Revisa estos datos:", None))
        self.etiquetaError.setText("")
        self.etiquetaCodigo.setText(QCoreApplication.translate("FormularioAlumno", u"C\u00f3digo <span style=\"color:#A3261B\">*</span>", None))
        self.etiquetaCodigo.setProperty(u"rol", QCoreApplication.translate("FormularioAlumno", u"etiquetaCampo", None))
        self.etiquetaCurp.setText(QCoreApplication.translate("FormularioAlumno", u"CURP", None))
        self.etiquetaCurp.setProperty(u"rol", QCoreApplication.translate("FormularioAlumno", u"etiquetaCampo", None))
        self.campoCodigo.setPlaceholderText(QCoreApplication.translate("FormularioAlumno", u"A-0401", None))
        self.campoCurp.setPlaceholderText(QCoreApplication.translate("FormularioAlumno", u"CURV200412MVZRMLA4", None))
        self.notaCurp.setText(QCoreApplication.translate("FormularioAlumno", u"18 caracteres; se revisa el formato oficial.", None))
        self.notaCurp.setProperty(u"rol", QCoreApplication.translate("FormularioAlumno", u"notaCampo", None))
        self.etiquetaNombre.setText(QCoreApplication.translate("FormularioAlumno", u"Nombre <span style=\"color:#A3261B\">*</span>", None))
        self.etiquetaNombre.setProperty(u"rol", QCoreApplication.translate("FormularioAlumno", u"etiquetaCampo", None))
        self.etiquetaApellido.setText(QCoreApplication.translate("FormularioAlumno", u"Apellidos <span style=\"color:#A3261B\">*</span>", None))
        self.etiquetaApellido.setProperty(u"rol", QCoreApplication.translate("FormularioAlumno", u"etiquetaCampo", None))
        self.etiquetaGrado.setText(QCoreApplication.translate("FormularioAlumno", u"Grado", None))
        self.etiquetaGrado.setProperty(u"rol", QCoreApplication.translate("FormularioAlumno", u"etiquetaCampo", None))
        self.etiquetaGrupo.setText(QCoreApplication.translate("FormularioAlumno", u"Grupo", None))
        self.etiquetaGrupo.setProperty(u"rol", QCoreApplication.translate("FormularioAlumno", u"etiquetaCampo", None))
        self.etiquetaMaestro.setText(QCoreApplication.translate("FormularioAlumno", u"Maestro de grupo", None))
        self.etiquetaMaestro.setProperty(u"rol", QCoreApplication.translate("FormularioAlumno", u"etiquetaCampo", None))
        self.valorMaestro.setText(QCoreApplication.translate("FormularioAlumno", u"Se muestra al elegir grado y grupo.", None))
        self.valorMaestro.setProperty(u"rol", QCoreApplication.translate("FormularioAlumno", u"datoFijo", None))
        self.separadorTutor.setText(QCoreApplication.translate("FormularioAlumno", u"Datos del tutor", None))
        self.separadorTutor.setProperty(u"rol", QCoreApplication.translate("FormularioAlumno", u"separador", None))
        self.etiquetaTelefono.setText(QCoreApplication.translate("FormularioAlumno", u"Tel\u00e9fono del tutor <span style=\"color:#A3261B\">*</span>", None))
        self.etiquetaTelefono.setProperty(u"rol", QCoreApplication.translate("FormularioAlumno", u"etiquetaCampo", None))
        self.etiquetaColonia.setText(QCoreApplication.translate("FormularioAlumno", u"Colonia", None))
        self.etiquetaColonia.setProperty(u"rol", QCoreApplication.translate("FormularioAlumno", u"etiquetaCampo", None))
        self.campoTelefono.setPlaceholderText(QCoreApplication.translate("FormularioAlumno", u"229 555 0100", None))
        self.etiquetaCalle.setText(QCoreApplication.translate("FormularioAlumno", u"Calle y n\u00famero", None))
        self.etiquetaCalle.setProperty(u"rol", QCoreApplication.translate("FormularioAlumno", u"etiquetaCampo", None))
        self.etiquetaAviso.setText(QCoreApplication.translate("FormularioAlumno", u"<span style=\"color:#A3261B\">*</span> Campos obligatorios. El tel\u00e9fono del tutor sirve para avisarle si hay un pr\u00e9stamo vencido.", None))
        self.etiquetaAviso.setProperty(u"rol", QCoreApplication.translate("FormularioAlumno", u"notaCampo", None))
        self.botonCancelar.setText(QCoreApplication.translate("FormularioAlumno", u"Cancelar", None))
        self.botonGuardar.setText(QCoreApplication.translate("FormularioAlumno", u"Guardar", None))
    # retranslateUi

