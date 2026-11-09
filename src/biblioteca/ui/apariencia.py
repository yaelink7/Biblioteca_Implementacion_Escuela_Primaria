"""Tipografias e iconos del diseno «Lapiz» (propuesta D, mostaza sobre grafito).

Las letras y los iconos viajan dentro del paquete: la aplicacion se ve igual
en la computadora de la biblioteca aunque no tenga Manrope instalada, y no
necesita internet para dibujarse.

Licencias: Manrope e IBM Plex Mono son OFL (recursos/fuentes); los iconos son
de Lucide, ISC (recursos/iconos). Los trazos son los mismos del prototipo.
"""

from __future__ import annotations

import tempfile
from functools import cache
from pathlib import Path

from PySide6.QtCore import QByteArray, QRect, QRectF, Qt
from PySide6.QtGui import QFontDatabase, QIcon, QPainter, QPainterPath, QPixmap
from PySide6.QtSvg import QSvgRenderer

RECURSOS = Path(__file__).resolve().parent / "recursos"

FAMILIA = "Manrope"
FAMILIA_MONO = "IBM Plex Mono"

# El logo de la escuela, provisional: lo entrego Yael el 8 de noviembre. Para
# cambiarlo basta con sustituir este archivo.
LOGO = RECURSOS / "logo" / "escuela.jpg"
# El arbol del logo, sin letras encima: es la marca donde el letrero entero
# no se alcanzaria a leer, como la columna de iconos (x, y, lado, en pixeles
# de la imagen original).
RECORTE_ARBOL = (6, 12, 446)


@cache
def cargar_tipografias() -> frozenset[str]:
    """Registra las tipografias del paquete y devuelve las familias que cargo.

    Se registran una sola vez por proceso: Qt duplicaria las familias si se
    llamara de nuevo, por ejemplo al volver a iniciar sesion.
    """
    familias: set[str] = set()
    for archivo in sorted((RECURSOS / "fuentes").glob("*.ttf")):
        ident = QFontDatabase.addApplicationFont(str(archivo))
        familias.update(QFontDatabase.applicationFontFamilies(ident))
    return frozenset(familias)


def _svg(nombre: str, color: str) -> bytes:
    """El SVG de Lucide con el trazo en el color pedido."""
    texto = (RECURSOS / "iconos" / f"{nombre}.svg").read_text(encoding="utf-8")
    return texto.replace("currentColor", color).encode("utf-8")


@cache
def icono(nombre: str, color: str, tamano: int = 18, aire: int = 0) -> QIcon:
    """Un icono en el color pedido, nitido tambien en pantallas de alta densidad.

    `aire` deja espacio transparente a la derecha del dibujo: Qt separa el
    icono del texto de un boton solo cuatro pixeles, y el prototipo ocho.
    """
    dibujo = QSvgRenderer(QByteArray(_svg(nombre, color)))
    resultado = QIcon()
    for escala in (1, 2):
        lado = tamano * escala
        imagen = QPixmap((tamano + aire) * escala, lado)
        imagen.fill(Qt.GlobalColor.transparent)
        pintor = QPainter(imagen)
        dibujo.render(pintor, QRectF(0, 0, lado, lado))
        pintor.end()
        imagen.setDevicePixelRatio(escala)
        resultado.addPixmap(imagen)
    return resultado


def _redondeada(imagen: QPixmap, ancho: int, alto: int, radio: float) -> QPixmap:
    """La imagen ajustada al tamano pedido, con las esquinas redondeadas.

    La hoja de estilo de Qt redondea el borde de una etiqueta pero no recorta
    la imagen que lleva dentro: el recorte se hace aqui, al dibujarla. Se
    dibuja al doble para que se vea nitida en pantallas de alta densidad.
    """
    escala = 2
    resultado = QPixmap(ancho * escala, alto * escala)
    resultado.fill(Qt.GlobalColor.transparent)
    pintor = QPainter(resultado)
    pintor.setRenderHint(QPainter.RenderHint.Antialiasing)
    pintor.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    contorno = QPainterPath()
    contorno.addRoundedRect(QRectF(resultado.rect()), radio * escala, radio * escala)
    pintor.setClipPath(contorno)
    pintor.drawPixmap(resultado.rect(), imagen)
    pintor.end()
    resultado.setDevicePixelRatio(escala)
    return resultado


@cache
def logo_escuela(ancho: int, alto: int, radio: float = 8) -> QPixmap:
    """El logo completo de la escuela, para donde cabe el letrero."""
    return _redondeada(QPixmap(str(LOGO)), ancho, alto, radio)


@cache
def marca_escuela(lado: int, radio: float = 12) -> QPixmap:
    """El arbol del logo, cuadrado: la marca de la columna de iconos."""
    x, y, recorte = RECORTE_ARBOL
    arbol = QPixmap(str(LOGO)).copy(QRect(x, y, recorte, recorte))
    return _redondeada(arbol, lado, lado, radio)


def ruta_para_hoja(nombre: str, color: str) -> str:
    """Copia coloreada de un icono, para citarla en la hoja de estilo con url().

    La hoja de estilo de Qt no sabe tenir un SVG, asi que cada color que pide
    se escribe en la carpeta temporal del sistema.
    """
    carpeta = Path(tempfile.gettempdir()) / "biblioteca-iconos"
    carpeta.mkdir(exist_ok=True)
    destino = carpeta / f"{nombre}-{color.lstrip('#').lower()}.svg"
    destino.write_bytes(_svg(nombre, color))
    return destino.as_posix()
