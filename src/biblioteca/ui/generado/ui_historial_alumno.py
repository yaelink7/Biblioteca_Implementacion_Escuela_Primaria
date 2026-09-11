# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'historial_alumno.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDialog, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_DialogoHistorial(object):
    def setupUi(self, DialogoHistorial):
        if not DialogoHistorial.objectName():
            DialogoHistorial.setObjectName(u"DialogoHistorial")
        DialogoHistorial.resize(680, 440)
        self.disposicion = QVBoxLayout(DialogoHistorial)
        self.disposicion.setSpacing(12)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(20, 20, 20, 20)
        self.etiquetaAlumno = QLabel(DialogoHistorial)
        self.etiquetaAlumno.setObjectName(u"etiquetaAlumno")

        self.disposicion.addWidget(self.etiquetaAlumno)

        self.etiquetaResumen = QLabel(DialogoHistorial)
        self.etiquetaResumen.setObjectName(u"etiquetaResumen")

        self.disposicion.addWidget(self.etiquetaResumen)

        self.tablaHistorial = QTableWidget(DialogoHistorial)
        if (self.tablaHistorial.columnCount() < 5):
            self.tablaHistorial.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tablaHistorial.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tablaHistorial.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tablaHistorial.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tablaHistorial.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tablaHistorial.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tablaHistorial.setObjectName(u"tablaHistorial")
        self.tablaHistorial.setAlternatingRowColors(True)
        self.tablaHistorial.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablaHistorial.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaHistorial.setSortingEnabled(True)
        self.tablaHistorial.horizontalHeader().setStretchLastSection(True)
        self.tablaHistorial.verticalHeader().setVisible(False)

        self.disposicion.addWidget(self.tablaHistorial)

        self.etiquetaNota = QLabel(DialogoHistorial)
        self.etiquetaNota.setObjectName(u"etiquetaNota")
        self.etiquetaNota.setWordWrap(True)

        self.disposicion.addWidget(self.etiquetaNota)

        self.filaBotones = QHBoxLayout()
        self.filaBotones.setObjectName(u"filaBotones")
        self.espacioBotones = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.filaBotones.addItem(self.espacioBotones)

        self.botonCerrar = QPushButton(DialogoHistorial)
        self.botonCerrar.setObjectName(u"botonCerrar")
        self.botonCerrar.setMinimumHeight(34)

        self.filaBotones.addWidget(self.botonCerrar)


        self.disposicion.addLayout(self.filaBotones)


        self.retranslateUi(DialogoHistorial)

        self.botonCerrar.setDefault(True)


        QMetaObject.connectSlotsByName(DialogoHistorial)
    # setupUi

    def retranslateUi(self, DialogoHistorial):
        DialogoHistorial.setWindowTitle(QCoreApplication.translate("DialogoHistorial", u"Historial de pr\u00e9stamos", None))
        self.etiquetaAlumno.setText("")
        self.etiquetaResumen.setText("")
        ___qtablewidgetitem = self.tablaHistorial.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("DialogoHistorial", u"Libro", None))
        ___qtablewidgetitem1 = self.tablaHistorial.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("DialogoHistorial", u"Prestado", None))
        ___qtablewidgetitem2 = self.tablaHistorial.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("DialogoHistorial", u"Venc\u00eda", None))
        ___qtablewidgetitem3 = self.tablaHistorial.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("DialogoHistorial", u"Devuelto", None))
        ___qtablewidgetitem4 = self.tablaHistorial.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("DialogoHistorial", u"Situaci\u00f3n", None))
        self.etiquetaNota.setText(QCoreApplication.translate("DialogoHistorial", u"El historial se conserva aunque el libro se d\u00e9 de baja del acervo.", None))
        self.botonCerrar.setText(QCoreApplication.translate("DialogoHistorial", u"Cerrar", None))
    # retranslateUi

