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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_DialogoLogin(object):
    def setupUi(self, DialogoLogin):
        if not DialogoLogin.objectName():
            DialogoLogin.setObjectName(u"DialogoLogin")
        DialogoLogin.resize(420, 380)
        self.disposicion = QVBoxLayout(DialogoLogin)
        self.disposicion.setSpacing(12)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(36, 36, 36, 36)
        self.etiquetaTitulo = QLabel(DialogoLogin)
        self.etiquetaTitulo.setObjectName(u"etiquetaTitulo")
        self.etiquetaTitulo.setAlignment(Qt.AlignCenter)

        self.disposicion.addWidget(self.etiquetaTitulo)

        self.etiquetaEscuela = QLabel(DialogoLogin)
        self.etiquetaEscuela.setObjectName(u"etiquetaEscuela")
        self.etiquetaEscuela.setAlignment(Qt.AlignCenter)

        self.disposicion.addWidget(self.etiquetaEscuela)

        self.espacioSuperior = QSpacerItem(20, 24, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.disposicion.addItem(self.espacioSuperior)

        self.etiquetaCorreo = QLabel(DialogoLogin)
        self.etiquetaCorreo.setObjectName(u"etiquetaCorreo")

        self.disposicion.addWidget(self.etiquetaCorreo)

        self.campoCorreo = QLineEdit(DialogoLogin)
        self.campoCorreo.setObjectName(u"campoCorreo")
        self.campoCorreo.setMinimumHeight(34)

        self.disposicion.addWidget(self.campoCorreo)

        self.etiquetaContrasena = QLabel(DialogoLogin)
        self.etiquetaContrasena.setObjectName(u"etiquetaContrasena")

        self.disposicion.addWidget(self.etiquetaContrasena)

        self.campoContrasena = QLineEdit(DialogoLogin)
        self.campoContrasena.setObjectName(u"campoContrasena")
        self.campoContrasena.setEchoMode(QLineEdit.Password)
        self.campoContrasena.setMinimumHeight(34)

        self.disposicion.addWidget(self.campoContrasena)

        self.etiquetaError = QLabel(DialogoLogin)
        self.etiquetaError.setObjectName(u"etiquetaError")
        self.etiquetaError.setWordWrap(True)
        self.etiquetaError.setAlignment(Qt.AlignCenter)
        self.etiquetaError.setMinimumHeight(34)

        self.disposicion.addWidget(self.etiquetaError)

        self.botonEntrar = QPushButton(DialogoLogin)
        self.botonEntrar.setObjectName(u"botonEntrar")
        self.botonEntrar.setMinimumHeight(38)

        self.disposicion.addWidget(self.botonEntrar)

        self.espacioInferior = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.disposicion.addItem(self.espacioInferior)

        QWidget.setTabOrder(self.campoCorreo, self.campoContrasena)
        QWidget.setTabOrder(self.campoContrasena, self.botonEntrar)

        self.retranslateUi(DialogoLogin)

        self.botonEntrar.setDefault(True)


        QMetaObject.connectSlotsByName(DialogoLogin)
    # setupUi

    def retranslateUi(self, DialogoLogin):
        DialogoLogin.setWindowTitle(QCoreApplication.translate("DialogoLogin", u"Iniciar sesi\u00f3n", None))
        self.etiquetaTitulo.setText(QCoreApplication.translate("DialogoLogin", u"Biblioteca Escolar", None))
        self.etiquetaEscuela.setText(QCoreApplication.translate("DialogoLogin", u"Escuela Primaria Adalberto Tejeda", None))
        self.etiquetaCorreo.setText(QCoreApplication.translate("DialogoLogin", u"Correo electr\u00f3nico", None))
        self.campoCorreo.setPlaceholderText(QCoreApplication.translate("DialogoLogin", u"usuario@ejemplo.com", None))
        self.etiquetaContrasena.setText(QCoreApplication.translate("DialogoLogin", u"Contrase\u00f1a", None))
        self.etiquetaError.setText("")
        self.botonEntrar.setText(QCoreApplication.translate("DialogoLogin", u"Entrar", None))
    # retranslateUi

