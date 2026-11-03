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

from PySide6.QtCore import QByteArray, QRectF, Qt
from PySide6.QtGui import QFontDatabase, QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

RECURSOS = Path(__file__).resolve().parent / "recursos"

FAMILIA = "Manrope"
FAMILIA_MONO = "IBM Plex Mono"


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
