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
        PantallaDeudores.resize(1100, 680)
        self.disposicion = QVBoxLayout(PantallaDeudores)
        self.disposicion.setSpacing(18)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(0, 0, 0, 0)
        self.encabezado = QHBoxLayout()
        self.encabezado.setSpacing(12)
        self.encabezado.setObjectName(u"encabezado")
        self.textoEncabezado = QVBoxLayout()
        self.textoEncabezado.setSpacing(6)
        self.textoEncabezado.setObjectName(u"textoEncabezado")
        self.etiquetaTitulo = QLabel(PantallaDeudores)
        self.etiquetaTitulo.setObjectName(u"etiquetaTitulo")

        self.textoEncabezado.addWidget(self.etiquetaTitulo)

        self.etiquetaGenerado = QLabel(PantallaDeudores)
        self.etiquetaGenerado.setObjectName(u"etiquetaGenerado")

        self.textoEncabezado.addWidget(self.etiquetaGenerado)


        self.encabezado.addLayout(self.textoEncabezado)

        self.espacioEncabezado = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.encabezado.addItem(self.espacioEncabezado)

        self.etiquetaSalon = QLabel(PantallaDeudores)
        self.etiquetaSalon.setObjectName(u"etiquetaSalon")
        self.etiquetaSalon.setMinimumHeight(44)

        self.encabezado.addWidget(self.etiquetaSalon, 0, Qt.AlignBottom)

        self.campoSalon = QComboBox(PantallaDeudores)
        self.campoSalon.setObjectName(u"campoSalon")
        self.campoSalon.setMinimumSize(QSize(150, 44))

        self.encabezado.addWidget(self.campoSalon, 0, Qt.AlignBottom)

        self.botonActualizar = QPushButton(PantallaDeudores)
        self.botonActualizar.setObjectName(u"botonActualizar")
        self.botonActualizar.setMinimumHeight(44)
        self.botonActualizar.setProperty(u"secundario", True)

        self.encabezado.addWidget(self.botonActualizar, 0, Qt.AlignBottom)


        self.disposicion.addLayout(self.encabezado)

        self.hojaReporte = QFrame(PantallaDeudores)
        self.hojaReporte.setObjectName(u"hojaReporte")
        self.disposicionHoja = QVBoxLayout(self.hojaReporte)
        self.disposicionHoja.setSpacing(0)
        self.disposicionHoja.setObjectName(u"disposicionHoja")
        self.disposicionHoja.setContentsMargins(0, 0, 0, 0)
        self.franjaHoja = QFrame(self.hojaReporte)
        self.franjaHoja.setObjectName(u"franjaHoja")
        self.franjaHoja.setMinimumHeight(6)
        self.franjaHoja.setMaximumHeight(6)

        self.disposicionHoja.addWidget(self.franjaHoja)

        self.cabezaHoja = QHBoxLayout()
        self.cabezaHoja.setSpacing(12)
        self.cabezaHoja.setObjectName(u"cabezaHoja")
        self.cabezaHoja.setContentsMargins(26, 22, 26, 14)
        self.iconoTotal = QLabel(self.hojaReporte)
        self.iconoTotal.setObjectName(u"iconoTotal")
        self.iconoTotal.setMinimumSize(QSize(28, 28))
        self.iconoTotal.setMaximumSize(QSize(28, 28))

        self.cabezaHoja.addWidget(self.iconoTotal, 0, Qt.AlignVCenter)

        self.etiquetaTotal = QLabel(self.hojaReporte)
        self.etiquetaTotal.setObjectName(u"etiquetaTotal")

        self.cabezaHoja.addWidget(self.etiquetaTotal, 0, Qt.AlignBottom)

        self.etiquetaTotalTexto = QLabel(self.hojaReporte)
        self.etiquetaTotalTexto.setObjectName(u"etiquetaTotalTexto")

        self.cabezaHoja.addWidget(self.etiquetaTotalTexto, 0, Qt.AlignBottom)

        self.espacioCabeza = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.cabezaHoja.addItem(self.espacioCabeza)

        self.etiquetaMasAtrasado = QLabel(self.hojaReporte)
        self.etiquetaMasAtrasado.setObjectName(u"etiquetaMasAtrasado")

        self.cabezaHoja.addWidget(self.etiquetaMasAtrasado, 0, Qt.AlignBottom)


        self.disposicionHoja.addLayout(self.cabezaHoja)

        self.marcoRaya = QVBoxLayout()
        self.marcoRaya.setObjectName(u"marcoRaya")
        self.marcoRaya.setContentsMargins(26, 0, 26, 4)
        self.dobleRaya = QFrame(self.hojaReporte)
        self.dobleRaya.setObjectName(u"dobleRaya")
        self.dobleRaya.setMinimumHeight(5)
        self.dobleRaya.setMaximumHeight(5)

        self.marcoRaya.addWidget(self.dobleRaya)


        self.disposicionHoja.addLayout(self.marcoRaya)

        self.marcoTablaHoja = QVBoxLayout()
        self.marcoTablaHoja.setObjectName(u"marcoTablaHoja")
        self.marcoTablaHoja.setContentsMargins(12, 0, 12, 0)
        self.tablaDeudores = QTableWidget(self.hojaReporte)
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
        self.tablaDeudores.setFrameShape(QFrame.NoFrame)
        self.tablaDeudores.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablaDeudores.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tablaDeudores.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaDeudores.setShowGrid(False)
        self.tablaDeudores.setWordWrap(False)
        self.tablaDeudores.setSortingEnabled(True)
        self.tablaDeudores.horizontalHeader().setHighlightSections(False)
        self.tablaDeudores.horizontalHeader().setStretchLastSection(True)
        self.tablaDeudores.verticalHeader().setVisible(False)
        self.tablaDeudores.verticalHeader().setDefaultSectionSize(46)

        self.marcoTablaHoja.addWidget(self.tablaDeudores)


        self.disposicionHoja.addLayout(self.marcoTablaHoja)

        self.pieHoja = QFrame(self.hojaReporte)
        self.pieHoja.setObjectName(u"pieHoja")
        self.disposicionPie = QHBoxLayout(self.pieHoja)
        self.disposicionPie.setSpacing(12)
        self.disposicionPie.setObjectName(u"disposicionPie")
        self.disposicionPie.setContentsMargins(26, 14, 26, 18)
        self.etiquetaNota = QLabel(self.pieHoja)
        self.etiquetaNota.setObjectName(u"etiquetaNota")
        self.etiquetaNota.setWordWrap(True)

        self.disposicionPie.addWidget(self.etiquetaNota)

        self.etiquetaCriterio = QLabel(self.pieHoja)
        self.etiquetaCriterio.setObjectName(u"etiquetaCriterio")

        self.disposicionPie.addWidget(self.etiquetaCriterio)

        self.disposicionPie.setStretch(0, 1)

        self.disposicionHoja.addWidget(self.pieHoja)


        self.disposicion.addWidget(self.hojaReporte)

        self.espacioFinal = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.disposicion.addItem(self.espacioFinal)

        self.disposicion.setStretch(2, 1)
        QWidget.setTabOrder(self.campoSalon, self.botonActualizar)
        QWidget.setTabOrder(self.botonActualizar, self.tablaDeudores)

        self.retranslateUi(PantallaDeudores)

        QMetaObject.connectSlotsByName(PantallaDeudores)
    # setupUi

    def retranslateUi(self, PantallaDeudores):
        PantallaDeudores.setWindowTitle(QCoreApplication.translate("PantallaDeudores", u"Deudores", None))
        self.etiquetaTitulo.setText(QCoreApplication.translate("PantallaDeudores", u"Deudores", None))
        self.etiquetaTitulo.setProperty(u"rol", QCoreApplication.translate("PantallaDeudores", u"titulo", None))
        self.etiquetaGenerado.setText("")
        self.etiquetaGenerado.setProperty(u"rol", QCoreApplication.translate("PantallaDeudores", u"resumen", None))
        self.etiquetaSalon.setText(QCoreApplication.translate("PantallaDeudores", u"Filtrar por sal\u00f3n", None))
        self.etiquetaSalon.setProperty(u"rol", QCoreApplication.translate("PantallaDeudores", u"etiquetaLinea", None))
        self.botonActualizar.setText(QCoreApplication.translate("PantallaDeudores", u"Actualizar", None))
        self.hojaReporte.setProperty(u"rol", QCoreApplication.translate("PantallaDeudores", u"hoja", None))
        self.iconoTotal.setText("")
        self.etiquetaTotal.setText(QCoreApplication.translate("PantallaDeudores", u"\u2014", None))
        self.etiquetaTotal.setProperty(u"rol", QCoreApplication.translate("PantallaDeudores", u"cifra", None))
        self.etiquetaTotalTexto.setText("")
        self.etiquetaTotalTexto.setProperty(u"rol", QCoreApplication.translate("PantallaDeudores", u"cifraTexto", None))
        self.etiquetaMasAtrasado.setText("")
        self.etiquetaMasAtrasado.setProperty(u"rol", QCoreApplication.translate("PantallaDeudores", u"peor", None))
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
        self.pieHoja.setProperty(u"rol", QCoreApplication.translate("PantallaDeudores", u"pieHoja", None))
        self.etiquetaNota.setText(QCoreApplication.translate("PantallaDeudores", u"El reporte se genera del estado actual de los pr\u00e9stamos. No requiere revisar registros a mano.", None))
        self.etiquetaNota.setProperty(u"rol", QCoreApplication.translate("PantallaDeudores", u"notaHoja", None))
        self.etiquetaCriterio.setText("")
        self.etiquetaCriterio.setProperty(u"rol", QCoreApplication.translate("PantallaDeudores", u"pista", None))
    # retranslateUi

