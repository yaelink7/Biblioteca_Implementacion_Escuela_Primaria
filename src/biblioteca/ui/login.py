"""Pantalla de inicio de sesion (REQ-USU-02).

El sistema Java abria directo en el menu principal. Aqui esta pantalla es
obligatoria: sin sesion las politicas RLS de Supabase no devuelven ni un
libro, asi que no hay forma de saltarsela.

En el diseno «Lapiz» es una ficha de biblioteca sobre el grafito punteado:
la franja mostaza, los rotulos a maquina y la perforacion de abajo.
"""

from __future__ import annotations

import re

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPen
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from biblioteca.core import config
from biblioteca.core.errores import causa as causa_del_error
from biblioteca.core.sesion import (
    ErrorDeAcceso,
    Sesion,
    iniciar_sesion,
    restaurar_sesion_recordada,
)
from biblioteca.ui.apariencia import FAMILIA_MONO, icono, logo_escuela, marca_escuela
from biblioteca.ui.estilo import (
    APAGADO,
    BORDE,
    BORDE_CONTROL,
    COLOR_ERROR,
    GRAFITO,
    GRAFITO_CLARO,
    GRIS,
    MOSTAZA,
    MOSTAZA_TEXTO,
    SOBRE_FILA,
    SUPERFICIE,
    TENUE,
    TEXTO,
    rotular,
)
from biblioteca.ui.generado.ui_login import Ui_DialogoLogin

# Distancia entre los puntos del fondo, como la reticula del prototipo
PASO_DE_PUNTOS = 24

# La seccion «Entrar rapido» del prototipo mostaza, solo en la copia de
# pruebas. Los selectores van por nombre de objeto: la hoja se queda en esta
# seccion y no le gana a nada de la ficha.
HOJA_ENTRADA_RAPIDA = f"""
QFrame#entradaRapida {{ background: transparent; border: none; }}
QLabel#tituloEntradaRapida {{ font-family: "{FAMILIA_MONO}"; font-size: 12px; color: {GRIS}; }}
QLabel#aclaracionEntradaRapida {{ font-family: "{FAMILIA_MONO}"; font-size: 12px; color: {TENUE}; }}
QPushButton#botonEntradaRapida {{
    background: {SUPERFICIE}; border: 1px solid {BORDE_CONTROL}; border-radius: 8px;
    padding: 0; min-height: 58px;
}}
QPushButton#botonEntradaRapida:hover {{ background: #FCF7EA; border-color: {MOSTAZA}; }}
QPushButton#botonEntradaRapida:focus {{ border: 2px solid {MOSTAZA_TEXTO}; }}
QPushButton#botonEntradaRapida:disabled {{ background: {SOBRE_FILA}; border-color: {BORDE}; }}
QLabel#avatarEntradaRapida {{
    background: {GRAFITO}; color: #FFFFFF; border-radius: 18px; font-size: 12px; font-weight: 700;
}}
QLabel#avatarEntradaRapida:disabled {{ background: {APAGADO}; }}
QLabel#nombreEntradaRapida {{ background: transparent; font-size: 14px; font-weight: 700; color: {TEXTO}; }}
QLabel#correoEntradaRapida {{ background: transparent; font-size: 13px; color: {TENUE}; }}
QLabel#nombreEntradaRapida:disabled, QLabel#correoEntradaRapida:disabled {{ color: {APAGADO}; }}
QLabel#flechaEntradaRapida {{ background: transparent; }}
"""


class _SeccionPunteada(QFrame):
    """La raya punteada de arriba de la seccion, dibujada a mano.

    Con Windows al 125 %, el `border-top: 1px dashed` de la hoja de estilo
    queda fuera del recorte y sale #F9F8F4 sobre el #FBFAF6 de la ficha: no se
    ve. Una pluma de un punto dentro del control si se ve.
    """

    def paintEvent(self, evento) -> None:  # noqa: N802 (lo nombra Qt)
        super().paintEvent(evento)
        pintor = QPainter(self)
        pluma = QPen(QColor(BORDE_CONTROL))
        pluma.setWidth(1)
        pluma.setDashPattern([3.0, 3.0])
        pintor.setPen(pluma)
        pintor.drawLine(QPointF(0, 0.5), QPointF(self.width(), 0.5))
        pintor.end()


def _iniciales(correo: str) -> str:
    """«maria.rodriguez@…» da «MR», como el avatar de la columna de iconos."""
    partes = [p for p in re.split(r"[._+-]", correo.split("@")[0]) if p]
    return "".join(p[0] for p in partes[:2]).upper() or "?"


class DialogoLogin(QDialog):
    """Pide las credenciales y deja lista la sesion del bibliotecario."""

    def __init__(self, padre: QWidget | None = None) -> None:
        super().__init__(padre)
        self.ui = Ui_DialogoLogin()
        self.ui.setupUi(self)

        self.sesion: Sesion | None = None

        self._preparar_aspecto()
        self.ui.etiquetaError.setStyleSheet(f"color: {COLOR_ERROR};")

        # Solo en la copia de pruebas, y nunca contra la base de la escuela
        self.botonEntradaRapida: QPushButton | None = (
            self._agregar_entrada_rapida() if config.ACCESO_DE_PRUEBAS else None
        )

        self.ui.botonEntrar.clicked.connect(self._entrar)
        self.ui.campoCorreo.returnPressed.connect(self._entrar)
        self.ui.campoContrasena.returnPressed.connect(self._entrar)

        self.ui.campoCorreo.setFocus()

    def _preparar_aspecto(self) -> None:
        ui = self.ui
        for etiqueta in (ui.etiquetaRotulo, ui.etiquetaCorreo, ui.etiquetaContrasena):
            rotular(etiqueta)
        posicion = QLineEdit.ActionPosition.LeadingPosition
        ui.campoCorreo.addAction(icono("correo", TENUE), posicion)
        ui.campoContrasena.addAction(icono("candado", TENUE), posicion)
        # El logo de la escuela, provisional, junto al nombre de la biblioteca
        ui.logoFicha.setPixmap(logo_escuela(120, 68))
        ui.logoFicha.setAccessibleName("Escuela Primaria Adalberto Tejeda")
        self.setWindowIcon(QIcon(marca_escuela(64)))
        # La flecha va despues de la palabra, como en el prototipo
        ui.botonEntrar.setIcon(icono("flecha", TEXTO))
        ui.botonEntrar.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        sombra = QGraphicsDropShadowEffect(ui.ficha)
        sombra.setBlurRadius(60)
        sombra.setOffset(0, 24)
        sombra.setColor(QColor(0, 0, 0, 170))
        ui.ficha.setGraphicsEffect(sombra)

    def _agregar_entrada_rapida(self) -> QPushButton:
        """La seccion «Entrar rapido» del prototipo, entre Entrar y la perforacion.

        Entra con el correo y la contrasena que quien usa la copia de pruebas
        escribio en su .env. Despues, la sesion recordada hace que el programa
        ya no pregunte al abrirse.
        """
        seccion = _SeccionPunteada(self.ui.ficha)
        seccion.setObjectName("entradaRapida")
        disposicion = QVBoxLayout(seccion)
        disposicion.setContentsMargins(0, 18, 0, 0)
        disposicion.setSpacing(10)

        rotulo = QHBoxLayout()
        rotulo.setSpacing(6)
        titulo = QLabel("Entrar rápido")
        titulo.setObjectName("tituloEntradaRapida")
        rotular(titulo)
        # En el prototipo la aclaracion no va en mayusculas
        aclaracion = QLabel("· solo en la copia de pruebas")
        aclaracion.setObjectName("aclaracionEntradaRapida")
        rotulo.addWidget(titulo)
        rotulo.addWidget(aclaracion)
        rotulo.addStretch()
        disposicion.addLayout(rotulo)

        boton = QPushButton(seccion)
        boton.setObjectName("botonEntradaRapida")
        boton.setCursor(Qt.CursorShape.PointingHandCursor)
        boton.setAccessibleName(f"Entrar rápido con {config.PRUEBAS_CORREO}")
        interior = QHBoxLayout(boton)
        interior.setContentsMargins(12, 8, 12, 8)
        interior.setSpacing(10)

        avatar = QLabel(_iniciales(config.PRUEBAS_CORREO))
        avatar.setObjectName("avatarEntradaRapida")
        avatar.setFixedSize(36, 36)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        textos = QVBoxLayout()
        textos.setSpacing(1)
        nombre = QLabel("Cuenta de pruebas")
        nombre.setObjectName("nombreEntradaRapida")
        correo = QLabel(config.PRUEBAS_CORREO)
        correo.setObjectName("correoEntradaRapida")
        textos.addWidget(nombre)
        textos.addWidget(correo)
        flecha = QLabel()
        flecha.setObjectName("flechaEntradaRapida")
        flecha.setPixmap(icono("flecha", TEXTO).pixmap(16, 16))

        # El clic es del boton entero, no de sus letras
        for hijo in (avatar, nombre, correo, flecha):
            hijo.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        interior.addWidget(avatar)
        interior.addLayout(textos, 1)
        interior.addWidget(flecha)
        disposicion.addWidget(boton)

        seccion.setStyleSheet(HOJA_ENTRADA_RAPIDA)
        self.ui.cuerpoFicha.insertWidget(
            self.ui.cuerpoFicha.indexOf(self.ui.perforacion), seccion
        )
        boton.clicked.connect(self._entrar_rapido)
        return boton

    def _entrar_rapido(self) -> None:
        """Llena la ficha con la cuenta de pruebas y entra como siempre."""
        self.ui.campoCorreo.setText(config.PRUEBAS_CORREO)
        self.ui.campoContrasena.setText(config.PRUEBAS_CONTRASENA)
        self._entrar()

    def paintEvent(self, evento) -> None:  # noqa: N802 (lo nombra Qt)
        """El grafito con su reticula de puntos, detras de la ficha."""
        pintor = QPainter(self)
        pintor.fillRect(self.rect(), QColor(GRAFITO))
        pintor.setRenderHint(QPainter.RenderHint.Antialiasing)
        pintor.setPen(Qt.PenStyle.NoPen)
        pintor.setBrush(QColor(GRAFITO_CLARO))
        mitad = PASO_DE_PUNTOS / 2
        for x in range(0, self.width(), PASO_DE_PUNTOS):
            for y in range(0, self.height(), PASO_DE_PUNTOS):
                pintor.drawEllipse(QPointF(x + mitad, y + mitad), 1.2, 1.2)
        pintor.end()

    def _entrar(self) -> None:
        correo = self.ui.campoCorreo.text().strip()
        contrasena = self.ui.campoContrasena.text()

        if not correo or not contrasena:
            self._mostrar_error("Escribe tu correo y tu contraseña.")
            return

        self._ocupado(True)
        try:
            self.sesion = iniciar_sesion(correo, contrasena)
        except ErrorDeAcceso as error:
            self._mostrar_error(str(error))
            self.ui.campoContrasena.clear()
            self.ui.campoContrasena.setFocus()
            return
        except Exception as error:
            # Un correo mal escrito, una sesion caida y un servidor apagado
            # no son el mismo problema: decir cual es evita que la persona
            # revise el cable cuando lo que falla es otra cosa.
            self._mostrar_error(causa_del_error(error))
            return
        finally:
            self._ocupado(False)

        self.accept()

    def _mostrar_error(self, mensaje: str) -> None:
        self.ui.etiquetaError.setText(mensaje)

    def _ocupado(self, ocupado: bool) -> None:
        """Evita dobles clics mientras se valida contra el servidor."""
        self.ui.botonEntrar.setEnabled(not ocupado)
        if self.botonEntradaRapida is not None:
            self.botonEntradaRapida.setEnabled(not ocupado)
        self.ui.botonEntrar.setText("Verificando…" if ocupado else "Entrar")
        if ocupado:
            self.ui.etiquetaError.clear()
        QApplication.processEvents()


def pedir_sesion(padre: QWidget | None = None) -> Sesion | None:
    """Muestra el dialogo y devuelve la sesion, o None si se cancelo.

    En la copia de pruebas, primero intenta reanudar la sesion guardada.
    """
    recordada = restaurar_sesion_recordada()
    if recordada is not None:
        return recordada
    dialogo = DialogoLogin(padre)
    if dialogo.exec() == QDialog.DialogCode.Accepted:
        return dialogo.sesion
    return None
