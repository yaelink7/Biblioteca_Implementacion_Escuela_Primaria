# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'empleados.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_PantallaEmpleados(object):
    def setupUi(self, PantallaEmpleados):
        if not PantallaEmpleados.objectName():
            PantallaEmpleados.setObjectName(u"PantallaEmpleados")
        PantallaEmpleados.resize(1100, 680)
        self.disposicion = QVBoxLayout(PantallaEmpleados)
        self.disposicion.setSpacing(18)
        self.disposicion.setObjectName(u"disposicion")
        self.disposicion.setContentsMargins(0, 0, 0, 0)
        self.encabezado = QHBoxLayout()
        self.encabezado.setSpacing(12)
        self.encabezado.setObjectName(u"encabezado")
        self.textoEncabezado = QVBoxLayout()
        self.textoEncabezado.setSpacing(6)
        self.textoEncabezado.setObjectName(u"textoEncabezado")
        self.etiquetaTitulo = QLabel(PantallaEmpleados)
        self.etiquetaTitulo.setObjectName(u"etiquetaTitulo")

        self.textoEncabezado.addWidget(self.etiquetaTitulo)

        self.etiquetaResumen = QLabel(PantallaEmpleados)
        self.etiquetaResumen.setObjectName(u"etiquetaResumen")

        self.textoEncabezado.addWidget(self.etiquetaResumen)


        self.encabezado.addLayout(self.textoEncabezado)

        self.espacioEncabezado = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.encabezado.addItem(self.espacioEncabezado)

        self.botonNuevo = QPushButton(PantallaEmpleados)
        self.botonNuevo.setObjectName(u"botonNuevo")
        self.botonNuevo.setMinimumHeight(44)

        self.encabezado.addWidget(self.botonNuevo, 0, Qt.AlignBottom)


        self.disposicion.addLayout(self.encabezado)

        self.avisoPermisos = QFrame(PantallaEmpleados)
        self.avisoPermisos.setObjectName(u"avisoPermisos")
        self.disposicionAviso = QHBoxLayout(self.avisoPermisos)
        self.disposicionAviso.setSpacing(10)
        self.disposicionAviso.setObjectName(u"disposicionAviso")
        self.disposicionAviso.setContentsMargins(18, 12, 18, 12)
        self.iconoAviso = QLabel(self.avisoPermisos)
        self.iconoAviso.setObjectName(u"iconoAviso")
        self.iconoAviso.setMinimumSize(QSize(20, 20))
        self.iconoAviso.setMaximumSize(QSize(20, 20))

        self.disposicionAviso.addWidget(self.iconoAviso, 0, Qt.AlignVCenter)

        self.etiquetaAviso = QLabel(self.avisoPermisos)
        self.etiquetaAviso.setObjectName(u"etiquetaAviso")
        self.etiquetaAviso.setWordWrap(True)

        self.disposicionAviso.addWidget(self.etiquetaAviso)


        self.disposicion.addWidget(self.avisoPermisos)

        self.cuerpo = QHBoxLayout()
        self.cuerpo.setSpacing(18)
        self.cuerpo.setObjectName(u"cuerpo")
        self.tarjetaTabla = QFrame(PantallaEmpleados)
        self.tarjetaTabla.setObjectName(u"tarjetaTabla")
        self.disposicionTarjeta = QVBoxLayout(self.tarjetaTabla)
        self.disposicionTarjeta.setSpacing(0)
        self.disposicionTarjeta.setObjectName(u"disposicionTarjeta")
        self.disposicionTarjeta.setContentsMargins(1, 4, 1, 8)
        self.tablaEmpleados = QTableWidget(self.tarjetaTabla)
        if (self.tablaEmpleados.columnCount() < 5):
            self.tablaEmpleados.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tablaEmpleados.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tablaEmpleados.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tablaEmpleados.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tablaEmpleados.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tablaEmpleados.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tablaEmpleados.setObjectName(u"tablaEmpleados")
        self.tablaEmpleados.setFrameShape(QFrame.NoFrame)
        self.tablaEmpleados.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tablaEmpleados.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tablaEmpleados.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tablaEmpleados.setShowGrid(False)
        self.tablaEmpleados.setWordWrap(False)
        self.tablaEmpleados.setSortingEnabled(True)
        self.tablaEmpleados.horizontalHeader().setHighlightSections(False)
        self.tablaEmpleados.horizontalHeader().setStretchLastSection(True)
        self.tablaEmpleados.verticalHeader().setVisible(False)
        self.tablaEmpleados.verticalHeader().setDefaultSectionSize(46)

        self.disposicionTarjeta.addWidget(self.tablaEmpleados)

        self.etiquetaVacio = QLabel(self.tarjetaTabla)
        self.etiquetaVacio.setObjectName(u"etiquetaVacio")
        self.etiquetaVacio.setWordWrap(True)
        self.etiquetaVacio.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.etiquetaVacio.sizePolicy().hasHeightForWidth())
        self.etiquetaVacio.setSizePolicy(sizePolicy)

        self.disposicionTarjeta.addWidget(self.etiquetaVacio)


        self.cuerpo.addWidget(self.tarjetaTabla)

        self.columnaPanel = QVBoxLayout()
        self.columnaPanel.setSpacing(0)
        self.columnaPanel.setObjectName(u"columnaPanel")
        self.panelEmpleado = QFrame(PantallaEmpleados)
        self.panelEmpleado.setObjectName(u"panelEmpleado")
        self.panelEmpleado.setMinimumWidth(300)
        self.panelEmpleado.setMaximumWidth(340)
        self.disposicionPanel = QVBoxLayout(self.panelEmpleado)
        self.disposicionPanel.setSpacing(18)
        self.disposicionPanel.setObjectName(u"disposicionPanel")
        self.disposicionPanel.setContentsMargins(22, 22, 22, 24)
        self.etiquetaPanel = QLabel(self.panelEmpleado)
        self.etiquetaPanel.setObjectName(u"etiquetaPanel")

        self.disposicionPanel.addWidget(self.etiquetaPanel)

        self.etiquetaPanelVacio = QLabel(self.panelEmpleado)
        self.etiquetaPanelVacio.setObjectName(u"etiquetaPanelVacio")
        self.etiquetaPanelVacio.setWordWrap(True)

        self.disposicionPanel.addWidget(self.etiquetaPanelVacio)

        self.fichaEmpleado = QWidget(self.panelEmpleado)
        self.fichaEmpleado.setObjectName(u"fichaEmpleado")
        self.disposicionFicha = QVBoxLayout(self.fichaEmpleado)
        self.disposicionFicha.setSpacing(18)
        self.disposicionFicha.setObjectName(u"disposicionFicha")
        self.disposicionFicha.setContentsMargins(0, 0, 0, 0)
        self.cabezaFicha = QHBoxLayout()
        self.cabezaFicha.setSpacing(12)
        self.cabezaFicha.setObjectName(u"cabezaFicha")
        self.avatar = QLabel(self.fichaEmpleado)
        self.avatar.setObjectName(u"avatar")
        self.avatar.setMinimumSize(QSize(44, 44))
        self.avatar.setMaximumSize(QSize(44, 44))
        self.avatar.setAlignment(Qt.AlignCenter)

        self.cabezaFicha.addWidget(self.avatar, 0, Qt.AlignTop)

        self.nombreFicha = QVBoxLayout()
        self.nombreFicha.setSpacing(2)
        self.nombreFicha.setObjectName(u"nombreFicha")
        self.etiquetaNombre = QLabel(self.fichaEmpleado)
        self.etiquetaNombre.setObjectName(u"etiquetaNombre")
        self.etiquetaNombre.setWordWrap(True)

        self.nombreFicha.addWidget(self.etiquetaNombre)

        self.etiquetaDetalle = QLabel(self.fichaEmpleado)
        self.etiquetaDetalle.setObjectName(u"etiquetaDetalle")
        self.etiquetaDetalle.setWordWrap(True)

        self.nombreFicha.addWidget(self.etiquetaDetalle)


        self.cabezaFicha.addLayout(self.nombreFicha)


        self.disposicionFicha.addLayout(self.cabezaFicha)

        self.datosEmpleado = QGridLayout()
        self.datosEmpleado.setObjectName(u"datosEmpleado")
        self.datosEmpleado.setHorizontalSpacing(16)
        self.datosEmpleado.setVerticalSpacing(10)
        self.datoCorreo = QLabel(self.fichaEmpleado)
        self.datoCorreo.setObjectName(u"datoCorreo")

        self.datosEmpleado.addWidget(self.datoCorreo, 0, 0, 1, 1, Qt.AlignTop)

        self.valorCorreo = QLabel(self.fichaEmpleado)
        self.valorCorreo.setObjectName(u"valorCorreo")
        self.valorCorreo.setWordWrap(True)
        self.valorCorreo.setProperty(u"mono", True)

        self.datosEmpleado.addWidget(self.valorCorreo, 0, 1, 1, 1)

        self.datoPerfil = QLabel(self.fichaEmpleado)
        self.datoPerfil.setObjectName(u"datoPerfil")

        self.datosEmpleado.addWidget(self.datoPerfil, 1, 0, 1, 1, Qt.AlignTop)

        self.valorPerfil = QLabel(self.fichaEmpleado)
        self.valorPerfil.setObjectName(u"valorPerfil")
        self.valorPerfil.setWordWrap(True)

        self.datosEmpleado.addWidget(self.valorPerfil, 1, 1, 1, 1)

        self.datoTelefono = QLabel(self.fichaEmpleado)
        self.datoTelefono.setObjectName(u"datoTelefono")

        self.datosEmpleado.addWidget(self.datoTelefono, 2, 0, 1, 1, Qt.AlignTop)

        self.valorTelefono = QLabel(self.fichaEmpleado)
        self.valorTelefono.setObjectName(u"valorTelefono")
        self.valorTelefono.setWordWrap(True)
        self.valorTelefono.setProperty(u"mono", True)

        self.datosEmpleado.addWidget(self.valorTelefono, 2, 1, 1, 1)

        self.datoDireccion = QLabel(self.fichaEmpleado)
        self.datoDireccion.setObjectName(u"datoDireccion")

        self.datosEmpleado.addWidget(self.datoDireccion, 3, 0, 1, 1, Qt.AlignTop)

        self.valorDireccion = QLabel(self.fichaEmpleado)
        self.valorDireccion.setObjectName(u"valorDireccion")
        self.valorDireccion.setWordWrap(True)

        self.datosEmpleado.addWidget(self.valorDireccion, 3, 1, 1, 1)

        self.datoIngreso = QLabel(self.fichaEmpleado)
        self.datoIngreso.setObjectName(u"datoIngreso")

        self.datosEmpleado.addWidget(self.datoIngreso, 4, 0, 1, 1, Qt.AlignTop)

        self.valorIngreso = QLabel(self.fichaEmpleado)
        self.valorIngreso.setObjectName(u"valorIngreso")
        self.valorIngreso.setWordWrap(True)
        self.valorIngreso.setProperty(u"mono", True)

        self.datosEmpleado.addWidget(self.valorIngreso, 4, 1, 1, 1)

        self.datosEmpleado.setColumnStretch(1, 1)

        self.disposicionFicha.addLayout(self.datosEmpleado)


        self.disposicionPanel.addWidget(self.fichaEmpleado)

        self.accionesPanel = QVBoxLayout()
        self.accionesPanel.setSpacing(10)
        self.accionesPanel.setObjectName(u"accionesPanel")
        self.botonEditar = QPushButton(self.panelEmpleado)
        self.botonEditar.setObjectName(u"botonEditar")
        self.botonEditar.setMinimumHeight(44)
        self.botonEditar.setEnabled(False)

        self.accionesPanel.addWidget(self.botonEditar)


        self.disposicionPanel.addLayout(self.accionesPanel)


        self.columnaPanel.addWidget(self.panelEmpleado)

        self.espacioPanel = QSpacerItem(40, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.columnaPanel.addItem(self.espacioPanel)

        self.columnaPanel.setStretch(1, 1)

        self.cuerpo.addLayout(self.columnaPanel)

        self.cuerpo.setStretch(0, 1)

        self.disposicion.addLayout(self.cuerpo)

        self.disposicion.setStretch(2, 1)
        QWidget.setTabOrder(self.botonNuevo, self.tablaEmpleados)
        QWidget.setTabOrder(self.tablaEmpleados, self.botonEditar)

        self.retranslateUi(PantallaEmpleados)

        QMetaObject.connectSlotsByName(PantallaEmpleados)
    # setupUi

    def retranslateUi(self, PantallaEmpleados):
        PantallaEmpleados.setWindowTitle(QCoreApplication.translate("PantallaEmpleados", u"Empleados", None))
        self.etiquetaTitulo.setText(QCoreApplication.translate("PantallaEmpleados", u"Empleados", None))
        self.etiquetaTitulo.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"titulo", None))
        self.etiquetaResumen.setText("")
        self.etiquetaResumen.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"resumen", None))
        self.botonNuevo.setText(QCoreApplication.translate("PantallaEmpleados", u"Registrar empleado", None))
        self.avisoPermisos.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"aviso", None))
        self.iconoAviso.setText("")
        self.etiquetaAviso.setText("")
        self.etiquetaAviso.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"textoAviso", None))
        self.tarjetaTabla.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"tarjeta", None))
        ___qtablewidgetitem = self.tablaEmpleados.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("PantallaEmpleados", u"C\u00f3digo", None))
        ___qtablewidgetitem1 = self.tablaEmpleados.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("PantallaEmpleados", u"Nombre", None))
        ___qtablewidgetitem2 = self.tablaEmpleados.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("PantallaEmpleados", u"Puesto", None))
        ___qtablewidgetitem3 = self.tablaEmpleados.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("PantallaEmpleados", u"Correo", None))
        ___qtablewidgetitem4 = self.tablaEmpleados.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("PantallaEmpleados", u"Perfil", None))
        self.etiquetaVacio.setText(QCoreApplication.translate("PantallaEmpleados", u"No hay personal registrado.", None))
        self.etiquetaVacio.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"tablaVacia", None))
        self.panelEmpleado.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"panel", None))
        self.etiquetaPanel.setText(QCoreApplication.translate("PantallaEmpleados", u"Persona seleccionada", None))
        self.etiquetaPanel.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"etiquetaPanel", None))
        self.etiquetaPanelVacio.setText(QCoreApplication.translate("PantallaEmpleados", u"Elige a alguien de la plantilla para ver sus datos.", None))
        self.etiquetaPanelVacio.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"panelVacio", None))
        self.avatar.setText("")
        self.avatar.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"avatar", None))
        self.etiquetaNombre.setText("")
        self.etiquetaNombre.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"nombrePanel", None))
        self.etiquetaDetalle.setText("")
        self.etiquetaDetalle.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"detallePanel", None))
        self.datoCorreo.setText(QCoreApplication.translate("PantallaEmpleados", u"Correo", None))
        self.datoCorreo.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"dato", None))
        self.valorCorreo.setText("")
        self.valorCorreo.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"valor", None))
        self.datoPerfil.setText(QCoreApplication.translate("PantallaEmpleados", u"Perfil", None))
        self.datoPerfil.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"dato", None))
        self.valorPerfil.setText("")
        self.valorPerfil.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"valor", None))
        self.datoTelefono.setText(QCoreApplication.translate("PantallaEmpleados", u"Tel\u00e9fono", None))
        self.datoTelefono.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"dato", None))
        self.valorTelefono.setText("")
        self.valorTelefono.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"valor", None))
        self.datoDireccion.setText(QCoreApplication.translate("PantallaEmpleados", u"Direcci\u00f3n", None))
        self.datoDireccion.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"dato", None))
        self.valorDireccion.setText("")
        self.valorDireccion.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"valor", None))
        self.datoIngreso.setText(QCoreApplication.translate("PantallaEmpleados", u"Ingres\u00f3", None))
        self.datoIngreso.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"dato", None))
        self.valorIngreso.setText("")
        self.valorIngreso.setProperty(u"rol", QCoreApplication.translate("PantallaEmpleados", u"valor", None))
        self.botonEditar.setText(QCoreApplication.translate("PantallaEmpleados", u"Modificar", None))
    # retranslateUi

