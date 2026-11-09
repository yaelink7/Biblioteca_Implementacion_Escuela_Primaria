"""Arma el ejecutable de Windows: la biblioteca se abre sin VS Code.

Equivale al «Clean and Build» que en NetBeans dejaba el .jar, con dos
diferencias: el resultado no necesita que la computadora tenga Python, y
queda un acceso directo «Biblioteca Escolar» en el escritorio.

    python herramientas/empaquetar.py
    python herramientas/empaquetar.py --destino E:/   (para llevarlo a otra computadora)

Por omision deja la aplicacion en %LOCALAPPDATA%/Programs/Biblioteca Escolar/
con el .env del proyecto junto al ejecutable: ahi lo busca core/config.py una
vez empaquetado, porque tres carpetas arriba de config.py queda la del .exe.

El ejecutable es una foto del proyecto en el momento de armarlo: despues de
cada cambio al codigo hay que volver a correr este guion, con la aplicacion
cerrada.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RECURSOS = RAIZ / "src" / "biblioteca" / "ui" / "recursos"
NOMBRE = "Biblioteca Escolar"

# Los colores del diseno «Lapiz», los mismos de ui/estilo.py
GRAFITO = "#26282C"
MOSTAZA = "#E0A526"
TEXTO = "#1E2023"


def dibujar_icono(destino: Path) -> Path:
    """El icono del ejecutable: el libro del menu en su pastilla mostaza."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtCore import QByteArray, QRectF, Qt
    from PySide6.QtGui import QColor, QGuiApplication, QImage, QPainter
    from PySide6.QtSvg import QSvgRenderer

    app = QGuiApplication.instance() or QGuiApplication([])  # noqa: F841 (Qt la necesita viva)
    lado = 256
    imagen = QImage(lado, lado, QImage.Format.Format_ARGB32)
    imagen.fill(Qt.GlobalColor.transparent)

    pintor = QPainter(imagen)
    pintor.setRenderHint(QPainter.RenderHint.Antialiasing)
    pintor.setPen(Qt.PenStyle.NoPen)
    pintor.setBrush(QColor(GRAFITO))
    pintor.drawRoundedRect(QRectF(0, 0, lado, lado), 56, 56)
    pintor.setBrush(QColor(MOSTAZA))
    pintor.drawRoundedRect(QRectF(36, 68, 184, 120), 60, 60)
    trazo = (RECURSOS / "iconos" / "catalogo.svg").read_text(encoding="utf-8")
    trazo = trazo.replace("currentColor", TEXTO)
    QSvgRenderer(QByteArray(trazo.encode("utf-8"))).render(pintor, QRectF(86, 86, 84, 84))
    pintor.end()

    if not imagen.save(str(destino), "ICO"):
        raise SystemExit(f"No se pudo escribir el icono en {destino}")
    return destino


def empaquetar(destino: Path, trabajo: Path) -> Path:
    """Corre PyInstaller y devuelve la carpeta de la aplicacion."""
    icono = dibujar_icono(trabajo / "biblioteca.ico")
    orden = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm", "--clean", "--windowed",
        "--name", NOMBRE,
        "--icon", str(icono),
        "--paths", str(RAIZ / "src"),
        # Las letras y los iconos del diseno, donde ui/apariencia.py los busca
        "--add-data", f"{RECURSOS}{os.pathsep}biblioteca/ui/recursos",
        "--distpath", str(destino),
        "--workpath", str(trabajo / "build"),
        "--specpath", str(trabajo),
        str(RAIZ / "main.py"),
    ]
    subprocess.run(orden, check=True)
    return destino / NOMBRE


def copiar_configuracion(carpeta: Path) -> None:
    """El .env va junto al ejecutable. Su llave publishable no es secreta."""
    origen = RAIZ / ".env"
    if not origen.exists():
        raise SystemExit("Falta el .env del proyecto: pide la llave al Scrum Master.")
    shutil.copyfile(origen, carpeta / ".env")


def _para_powershell(ruta: Path) -> str:
    return str(ruta).replace("'", "''")


def acceso_directo(ejecutable: Path) -> str:
    """Crea o actualiza «Biblioteca Escolar» en el escritorio de quien lo corre."""
    orden = (
        "$escritorio = [Environment]::GetFolderPath('Desktop');"
        f"$ruta = Join-Path $escritorio '{NOMBRE}.lnk';"
        "$acceso = (New-Object -ComObject WScript.Shell).CreateShortcut($ruta);"
        f"$acceso.TargetPath = '{_para_powershell(ejecutable)}';"
        f"$acceso.WorkingDirectory = '{_para_powershell(ejecutable.parent)}';"
        f"$acceso.IconLocation = '{_para_powershell(ejecutable)},0';"
        "$acceso.Description = 'Biblioteca de la Escuela Primaria Adalberto Tejeda';"
        "$acceso.Save();"
        "Write-Output $ruta"
    )
    resultado = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", orden],
        capture_output=True, text=True, check=True,
    )
    return resultado.stdout.strip()


def main() -> int:
    argumentos = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    argumentos.add_argument(
        "--destino", type=Path,
        default=Path(os.environ.get("LOCALAPPDATA", RAIZ)) / "Programs",
        help="carpeta donde queda la aplicacion (por omision, la de programas del usuario)",
    )
    argumentos.add_argument(
        "--sin-acceso-directo", action="store_true",
        help="no tocar el escritorio; util al armar para otra computadora",
    )
    opciones = argumentos.parse_args()

    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("Falta PyInstaller. Instala las dependencias:")
        print("    .venv/Scripts/python.exe -m pip install -r requirements.txt")
        return 1

    with tempfile.TemporaryDirectory(prefix="biblioteca-empaquetado-") as temporal:
        carpeta = empaquetar(opciones.destino.resolve(), Path(temporal))
    copiar_configuracion(carpeta)
    ejecutable = carpeta / f"{NOMBRE}.exe"
    print(f"\nListo: {ejecutable}")

    if not opciones.sin_acceso_directo:
        print(f"Acceso directo: {acceso_directo(ejecutable)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
