# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
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
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_DialogoLogin(object):
    def setupUi(self, DialogoLogin):
        if not DialogoLogin.objectName():
            DialogoLogin.setObjectName(u"DialogoLogin")
        DialogoLogin.resize(980, 720)
        self.disposicion = QVBoxLayout(DialogoLogin)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(24, 24, 24, 24)
        self.espacioSuperior = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.disposicion.addItem(self.espacioSuperior)

        self.centro = QHBoxLayout()
        self.centro.setObjectName(u"centro")
        self.espacioIzquierdo = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.centro.addItem(self.espacioIzquierdo)

        self.ficha = QFrame(DialogoLogin)
        self.ficha.setObjectName(u"ficha")
        self.ficha.setMinimumWidth(440)
        self.ficha.setMaximumWidth(500)
        self.disposicionFicha = QVBoxLayout(self.ficha)
        self.disposicionFicha.setSpacing(0)
        self.disposicionFicha.setObjectName(u"disposicionFicha")
        self.disposicionFicha.setContentsMargins(0, 0, 0, 0)
        self.franjaFicha = QFrame(self.ficha)
        self.franjaFicha.setObjectName(u"franjaFicha")
        self.franjaFicha.setMinimumHeight(8)
        self.franjaFicha.setMaximumHeight(8)

        self.disposicionFicha.addWidget(self.franjaFicha)

        self.cuerpoFicha = QVBoxLayout()
        self.cuerpoFicha.setSpacing(10)
        self.cuerpoFicha.setObjectName(u"cuerpoFicha")
        self.cuerpoFicha.setContentsMargins(38, 30, 38, 18)
        self.etiquetaRotulo = QLabel(self.ficha)
        self.etiquetaRotulo.setObjectName(u"etiquetaRotulo")

        self.cuerpoFicha.addWidget(self.etiquetaRotulo)

        self.espacioRotulo = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.cuerpoFicha.addItem(self.espacioRotulo)

        self.marca = QHBoxLayout()
        self.marca.setSpacing(14)
        self.marca.setObjectName(u"marca")
        self.logoFicha = QLabel(self.ficha)
        self.logoFicha.setObjectName(u"logoFicha")
        self.logoFicha.setMinimumSize(QSize(120, 68))
        self.logoFicha.setMaximumSize(QSize(120, 68))
        self.logoFicha.setAlignment(Qt.AlignCenter)

        self.marca.addWidget(self.logoFicha)

        self.nombreEscuela = QVBoxLayout()
        self.nombreEscuela.setSpacing(2)
        self.nombreEscuela.setObjectName(u"nombreEscuela")
        self.etiquetaTitulo = QLabel(self.ficha)
        self.etiquetaTitulo.setObjectName(u"etiquetaTitulo")

        self.nombreEscuela.addWidget(self.etiquetaTitulo)

        self.etiquetaEscuela = QLabel(self.ficha)
        self.etiquetaEscuela.setObjectName(u"etiquetaEscuela")

        self.nombreEscuela.addWidget(self.etiquetaEscuela)


        self.marca.addLayout(self.nombreEscuela)


        self.cuerpoFicha.addLayout(self.marca)

        self.espacioMarca = QSpacerItem(20, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.cuerpoFicha.addItem(self.espacioMarca)

        self.rayaFicha = QFrame(self.ficha)
        self.rayaFicha.setObjectName(u"rayaFicha")
        self.rayaFicha.setMinimumHeight(4)
        self.rayaFicha.setMaximumHeight(4)

        self.cuerpoFicha.addWidget(self.rayaFicha)

        self.espacioRaya = QSpacerItem(20, 12, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.cuerpoFicha.addItem(self.espacioRaya)

        self.etiquetaCorreo = QLabel(self.ficha)
        self.etiquetaCorreo.setObjectName(u"etiquetaCorreo")

        self.cuerpoFicha.addWidget(self.etiquetaCorreo)

        self.campoCorreo = QLineEdit(self.ficha)
        self.campoCorreo.setObjectName(u"campoCorreo")

        self.cuerpoFicha.addWidget(self.campoCorreo)

        self.espacioCorreo = QSpacerItem(20, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.cuerpoFicha.addItem(self.espacioCorreo)

        self.etiquetaContrasena = QLabel(self.ficha)
        self.etiquetaContrasena.setObjectName(u"etiquetaContrasena")

        self.cuerpoFicha.addWidget(self.etiquetaContrasena)

        self.campoContrasena = QLineEdit(self.ficha)
        self.campoContrasena.setObjectName(u"campoContrasena")
        self.campoContrasena.setEchoMode(QLineEdit.Password)

        self.cuerpoFicha.addWidget(self.campoContrasena)

        self.etiquetaError = QLabel(self.ficha)
        self.etiquetaError.setObjectName(u"etiquetaError")
        self.etiquetaError.setWordWrap(True)
        self.etiquetaError.setMinimumHeight(34)

        self.cuerpoFicha.addWidget(self.etiquetaError)

        self.botonEntrar = QPushButton(self.ficha)
        self.botonEntrar.setObjectName(u"botonEntrar")

        self.cuerpoFicha.addWidget(self.botonEntrar)

        self.espacioBoton = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.cuerpoFicha.addItem(self.espacioBoton)

        self.perforacion = QLabel(self.ficha)
        self.perforacion.setObjectName(u"perforacion")
        self.perforacion.setMinimumSize(QSize(18, 18))
        self.perforacion.setMaximumSize(QSize(18, 18))

        self.cuerpoFicha.addWidget(self.perforacion, 0, Qt.AlignHCenter)


        self.disposicionFicha.addLayout(self.cuerpoFicha)


        self.centro.addWidget(self.ficha)

        self.espacioDerecho = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.centro.addItem(self.espacioDerecho)


        self.disposicion.addLayout(self.centro)

        self.espacioInferior = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.disposicion.addItem(self.espacioInferior)

        QWidget.setTabOrder(self.campoCorreo, self.campoContrasena)
        QWidget.setTabOrder(self.campoContrasena, self.botonEntrar)

        self.retranslateUi(DialogoLogin)

        self.botonEntrar.setDefault(True)


        QMetaObject.connectSlotsByName(DialogoLogin)
    # setupUi

    def retranslateUi(self, DialogoLogin):
        DialogoLogin.setWindowTitle(QCoreApplication.translate("DialogoLogin", u"Iniciar sesi\u00f3n", None))
        self.etiquetaRotulo.setText(QCoreApplication.translate("DialogoLogin", u"Iniciar sesi\u00f3n", None))
        self.etiquetaRotulo.setProperty(u"rol", QCoreApplication.translate("DialogoLogin", u"rotuloFicha", None))
        self.logoFicha.setText("")
        self.etiquetaTitulo.setText(QCoreApplication.translate("DialogoLogin", u"Biblioteca Escolar", None))
        self.etiquetaTitulo.setProperty(u"rol", QCoreApplication.translate("DialogoLogin", u"tituloFicha", None))
        self.etiquetaEscuela.setText(QCoreApplication.translate("DialogoLogin", u"Escuela Primaria Adalberto Tejeda", None))
        self.etiquetaEscuela.setProperty(u"rol", QCoreApplication.translate("DialogoLogin", u"escuelaFicha", None))
        self.etiquetaCorreo.setText(QCoreApplication.translate("DialogoLogin", u"Correo electr\u00f3nico", None))
        self.etiquetaCorreo.setProperty(u"rol", QCoreApplication.translate("DialogoLogin", u"rotuloCampo", None))
        self.campoCorreo.setPlaceholderText(QCoreApplication.translate("DialogoLogin", u"usuario@ejemplo.com", None))
        self.campoCorreo.setProperty(u"rol", QCoreApplication.translate("DialogoLogin", u"campoFicha", None))
        self.etiquetaContrasena.setText(QCoreApplication.translate("DialogoLogin", u"Contrase\u00f1a", None))
        self.etiquetaContrasena.setProperty(u"rol", QCoreApplication.translate("DialogoLogin", u"rotuloCampo", None))
        self.campoContrasena.setProperty(u"rol", QCoreApplication.translate("DialogoLogin", u"campoFicha", None))
        self.etiquetaError.setText("")
        self.botonEntrar.setText(QCoreApplication.translate("DialogoLogin", u"Entrar", None))
        self.perforacion.setText("")
    # retranslateUi

