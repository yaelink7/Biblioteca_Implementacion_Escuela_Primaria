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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFormLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_FormularioLibro(object):
    def setupUi(self, FormularioLibro):
        if not FormularioLibro.objectName():
            FormularioLibro.setObjectName(u"FormularioLibro")
        FormularioLibro.resize(480, 520)
        self.disposicion = QVBoxLayout(FormularioLibro)
        self.disposicion.setSpacing(12)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(24, 24, 24, 24)
        self.formulario = QFormLayout()
        self.formulario.setObjectName(u"formulario")
        self.formulario.setHorizontalSpacing(14)
        self.formulario.setVerticalSpacing(10)
        self.etiquetaTitulo = QLabel(FormularioLibro)
        self.etiquetaTitulo.setObjectName(u"etiquetaTitulo")

        self.formulario.setWidget(0, QFormLayout.ItemRole.LabelRole, self.etiquetaTitulo)

        self.campoTitulo = QLineEdit(FormularioLibro)
        self.campoTitulo.setObjectName(u"campoTitulo")
        self.campoTitulo.setMinimumHeight(32)

        self.formulario.setWidget(0, QFormLayout.ItemRole.FieldRole, self.campoTitulo)

        self.etiquetaAutor = QLabel(FormularioLibro)
        self.etiquetaAutor.setObjectName(u"etiquetaAutor")

        self.formulario.setWidget(1, QFormLayout.ItemRole.LabelRole, self.etiquetaAutor)

        self.campoAutor = QLineEdit(FormularioLibro)
        self.campoAutor.setObjectName(u"campoAutor")
        self.campoAutor.setMinimumHeight(32)

        self.formulario.setWidget(1, QFormLayout.ItemRole.FieldRole, self.campoAutor)

        self.etiquetaTipo = QLabel(FormularioLibro)
        self.etiquetaTipo.setObjectName(u"etiquetaTipo")

        self.formulario.setWidget(2, QFormLayout.ItemRole.LabelRole, self.etiquetaTipo)

        self.campoTipo = QComboBox(FormularioLibro)
        self.campoTipo.addItem("")
        self.campoTipo.addItem("")
        self.campoTipo.addItem("")
        self.campoTipo.addItem("")
        self.campoTipo.addItem("")
        self.campoTipo.addItem("")
        self.campoTipo.addItem("")
        self.campoTipo.addItem("")
        self.campoTipo.setObjectName(u"campoTipo")
        self.campoTipo.setEditable(True)
        self.campoTipo.setMinimumHeight(32)

        self.formulario.setWidget(2, QFormLayout.ItemRole.FieldRole, self.campoTipo)

        self.etiquetaEditorial = QLabel(FormularioLibro)
        self.etiquetaEditorial.setObjectName(u"etiquetaEditorial")

        self.formulario.setWidget(3, QFormLayout.ItemRole.LabelRole, self.etiquetaEditorial)

        self.campoEditorial = QLineEdit(FormularioLibro)
        self.campoEditorial.setObjectName(u"campoEditorial")
        self.campoEditorial.setMinimumHeight(32)

        self.formulario.setWidget(3, QFormLayout.ItemRole.FieldRole, self.campoEditorial)

        self.etiquetaExistencias = QLabel(FormularioLibro)
        self.etiquetaExistencias.setObjectName(u"etiquetaExistencias")

        self.formulario.setWidget(4, QFormLayout.ItemRole.LabelRole, self.etiquetaExistencias)

        self.campoExistencias = QSpinBox(FormularioLibro)
        self.campoExistencias.setObjectName(u"campoExistencias")
        self.campoExistencias.setMinimum(0)
        self.campoExistencias.setMaximum(9999)
        self.campoExistencias.setValue(1)
        self.campoExistencias.setMinimumHeight(32)

        self.formulario.setWidget(4, QFormLayout.ItemRole.FieldRole, self.campoExistencias)

        self.etiquetaAno = QLabel(FormularioLibro)
        self.etiquetaAno.setObjectName(u"etiquetaAno")

        self.formulario.setWidget(5, QFormLayout.ItemRole.LabelRole, self.etiquetaAno)

        self.campoAno = QSpinBox(FormularioLibro)
        self.campoAno.setObjectName(u"campoAno")
        self.campoAno.setMinimum(1399)
        self.campoAno.setMaximum(2026)
        self.campoAno.setValue(1399)
        self.campoAno.setMinimumHeight(32)

        self.formulario.setWidget(5, QFormLayout.ItemRole.FieldRole, self.campoAno)

        self.etiquetaPaginas = QLabel(FormularioLibro)
        self.etiquetaPaginas.setObjectName(u"etiquetaPaginas")

        self.formulario.setWidget(6, QFormLayout.ItemRole.LabelRole, self.etiquetaPaginas)

        self.campoPaginas = QSpinBox(FormularioLibro)
        self.campoPaginas.setObjectName(u"campoPaginas")
        self.campoPaginas.setMinimum(0)
        self.campoPaginas.setMaximum(99999)
        self.campoPaginas.setValue(0)
        self.campoPaginas.setMinimumHeight(32)

        self.formulario.setWidget(6, QFormLayout.ItemRole.FieldRole, self.campoPaginas)


        self.disposicion.addLayout(self.formulario)

        self.etiquetaObligatorios = QLabel(FormularioLibro)
        self.etiquetaObligatorios.setObjectName(u"etiquetaObligatorios")

        self.disposicion.addWidget(self.etiquetaObligatorios)

        self.etiquetaError = QLabel(FormularioLibro)
        self.etiquetaError.setObjectName(u"etiquetaError")
        self.etiquetaError.setWordWrap(True)
        self.etiquetaError.setMinimumHeight(44)
        self.etiquetaError.setAlignment(Qt.AlignTop)

        self.disposicion.addWidget(self.etiquetaError)

        self.espacio = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.disposicion.addItem(self.espacio)

        self.filaBotones = QHBoxLayout()
        self.filaBotones.setObjectName(u"filaBotones")
        self.espacioBotones = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.filaBotones.addItem(self.espacioBotones)

        self.botonCancelar = QPushButton(FormularioLibro)
        self.botonCancelar.setObjectName(u"botonCancelar")
        self.botonCancelar.setMinimumHeight(34)

        self.filaBotones.addWidget(self.botonCancelar)

        self.botonGuardar = QPushButton(FormularioLibro)
        self.botonGuardar.setObjectName(u"botonGuardar")
        self.botonGuardar.setMinimumHeight(34)

        self.filaBotones.addWidget(self.botonGuardar)


        self.disposicion.addLayout(self.filaBotones)


        self.retranslateUi(FormularioLibro)

        self.botonGuardar.setDefault(True)


        QMetaObject.connectSlotsByName(FormularioLibro)
    # setupUi

    def retranslateUi(self, FormularioLibro):
        FormularioLibro.setWindowTitle(QCoreApplication.translate("FormularioLibro", u"Libro", None))
        self.etiquetaTitulo.setText(QCoreApplication.translate("FormularioLibro", u"T\u00edtulo *", None))
        self.etiquetaAutor.setText(QCoreApplication.translate("FormularioLibro", u"Autor *", None))
        self.etiquetaTipo.setText(QCoreApplication.translate("FormularioLibro", u"Tipo o g\u00e9nero", None))
        self.campoTipo.setItemText(0, QCoreApplication.translate("FormularioLibro", u"Infantil", None))
        self.campoTipo.setItemText(1, QCoreApplication.translate("FormularioLibro", u"Juvenil", None))
        self.campoTipo.setItemText(2, QCoreApplication.translate("FormularioLibro", u"Cuento", None))
        self.campoTipo.setItemText(3, QCoreApplication.translate("FormularioLibro", u"Novela", None))
        self.campoTipo.setItemText(4, QCoreApplication.translate("FormularioLibro", u"Poes\u00eda", None))
        self.campoTipo.setItemText(5, QCoreApplication.translate("FormularioLibro", u"Aventura", None))
        self.campoTipo.setItemText(6, QCoreApplication.translate("FormularioLibro", u"Fantas\u00eda", None))
        self.campoTipo.setItemText(7, QCoreApplication.translate("FormularioLibro", u"Consulta", None))

        self.etiquetaEditorial.setText(QCoreApplication.translate("FormularioLibro", u"Editorial", None))
        self.etiquetaExistencias.setText(QCoreApplication.translate("FormularioLibro", u"Ejemplares *", None))
        self.etiquetaAno.setText(QCoreApplication.translate("FormularioLibro", u"A\u00f1o de publicaci\u00f3n", None))
        self.campoAno.setSpecialValueText(QCoreApplication.translate("FormularioLibro", u"Sin especificar", None))
        self.etiquetaPaginas.setText(QCoreApplication.translate("FormularioLibro", u"N\u00famero de p\u00e1ginas", None))
        self.campoPaginas.setSpecialValueText(QCoreApplication.translate("FormularioLibro", u"Sin especificar", None))
        self.etiquetaObligatorios.setText(QCoreApplication.translate("FormularioLibro", u"* Campos obligatorios", None))
        self.etiquetaError.setText("")
        self.botonCancelar.setText(QCoreApplication.translate("FormularioLibro", u"Cancelar", None))
        self.botonGuardar.setText(QCoreApplication.translate("FormularioLibro", u"Guardar", None))
    # retranslateUi

