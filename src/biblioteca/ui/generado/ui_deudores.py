# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'deudores.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_PantallaDeudores(object):
    def setupUi(self, PantallaDeudores):
        if not PantallaDeudores.objectName():
            PantallaDeudores.setObjectName(u"PantallaDeudores")
        PantallaDeudores.resize(900, 560)
        self.disposicion = QVBoxLayout(PantallaDeudores)
        self.disposicion.setSpacing(14)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(20, 20, 20, 20)
        self.marcoTotales = QFrame(PantallaDeudores)
        self.marcoTotales.setObjectName(u"marcoTotales")
        self.marcoTotales.setFrameShape(QFrame.StyledPanel)
        self.disposicionTotales = QHBoxLayout(self.marcoTotales)
        self.disposicionTotales.setSpacing(28)
        self.disposicionTotales.setObjectName(u"disposicionTotales")
        self.disposicionTotales.setContentsMargins(18, 14, 18, 14)
        self.etiquetaTotal = QLabel(self.marcoTotales)
        self.etiquetaTotal.setObjectName(u"etiquetaTotal")

        self.disposicionTotales.addWidget(self.etiquetaTotal)

        self.etiquetaMasAtrasado = QLabel(self.marcoTotales)
        self.etiquetaMasAtrasado.setObjectName(u"etiquetaMasAtrasado")

        self.disposicionTotales.addWidget(self.etiquetaMasAtrasado)

        self.espacioTotales = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.disposicionTotales.addItem(self.espacioTotales)

        self.etiquetaGenerado = QLabel(self.marcoTotales)
        self.etiquetaGenerado.setObjectName(u"etiquetaGenerado")

        self.disposicionTotales.addWidget(self.etiquetaGenerado)


        self.disposicion.addWidget(self.marcoTotales)

        self.filaFiltro = QHBoxLayout()
        self.filaFiltro.setSpacing(10)
        self.filaFiltro.setObjectName(u"filaFiltro")
        self.etiquetaSalon = QLabel(PantallaDeudores)
        self.etiquetaSalon.setObjectName(u"etiquetaSalon")

        self.filaFiltro.addWidget(self.etiquetaSalon)

        self.campoSalon = QComboBox(PantallaDeudores)
        self.campoSalon.setObjectName(u"campoSalon")
        self.campoSalon.setMinimumHeight(32)
        self.campoSalon.setMinimumWidth(160)

        self.filaFiltro.addWidget(self.campoSalon)

        self.espacioFiltro = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.filaFiltro.addItem(self.espacioFiltro)

        self.botonActualizar = QPushButton(PantallaDeudores)
        self.botonActualizar.setObjectName(u"botonActualizar")
        self.botonActualizar.setMinimumHeight(34)

        self.filaFiltro.addWidget(self.botonActualizar)


        self.disposicion.addLayout(self.filaFiltro)

        self.tablaDeudores = QTableWidget(PantallaDeudores)
        if (self.tablaDeudores.columnCount() < 6):
            self.tablaDeudores.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tablaDeudores.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tablaDeudores.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tablaDeudores.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tablaDeudores.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tablaDeudores.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tablaDeudores.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.tablaDeudores.setObjectName(u"tablaDeudores")
        self.tablaDeudores.setAlternatingRowColors(True)
        self.tablaDeudores.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablaDeudores.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaDeudores.setSortingEnabled(True)
        self.tablaDeudores.horizontalHeader().setStretchLastSection(True)
        self.tablaDeudores.verticalHeader().setVisible(False)

        self.disposicion.addWidget(self.tablaDeudores)

        self.etiquetaNota = QLabel(PantallaDeudores)
        self.etiquetaNota.setObjectName(u"etiquetaNota")
        self.etiquetaNota.setWordWrap(True)

        self.disposicion.addWidget(self.etiquetaNota)


        self.retranslateUi(PantallaDeudores)

        QMetaObject.connectSlotsByName(PantallaDeudores)
    # setupUi

    def retranslateUi(self, PantallaDeudores):
        PantallaDeudores.setWindowTitle(QCoreApplication.translate("PantallaDeudores", u"Deudores", None))
        self.etiquetaTotal.setText(QCoreApplication.translate("PantallaDeudores", u"\u2014", None))
        self.etiquetaMasAtrasado.setText("")
        self.etiquetaGenerado.setText("")
        self.etiquetaSalon.setText(QCoreApplication.translate("PantallaDeudores", u"Filtrar por sal\u00f3n", None))
        self.botonActualizar.setText(QCoreApplication.translate("PantallaDeudores", u"Actualizar", None))
        ___qtablewidgetitem = self.tablaDeudores.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PantallaDeudores", u"Alumno", None))
        ___qtablewidgetitem1 = self.tablaDeudores.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PantallaDeudores", u"Sal\u00f3n", None))
        ___qtablewidgetitem2 = self.tablaDeudores.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PantallaDeudores", u"Libro", None))
        ___qtablewidgetitem3 = self.tablaDeudores.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PantallaDeudores", u"Debi\u00f3 entregar", None))
        ___qtablewidgetitem4 = self.tablaDeudores.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PantallaDeudores", u"Retraso", None))
        ___qtablewidgetitem5 = self.tablaDeudores.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("PantallaDeudores", u"Contacto del tutor", None))
        self.etiquetaNota.setText(QCoreApplication.translate("PantallaDeudores", u"El reporte se genera del estado actual de los pr\u00e9stamos. No requiere revisar registros a mano.", None))
    # retranslateUi

