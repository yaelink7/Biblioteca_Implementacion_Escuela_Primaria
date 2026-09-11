"""Compila los disenos de Qt Designer a modulos de Python.

Equivale a lo que NetBeans hacia solo al guardar un .form, con una
diferencia: aqui el codigo generado vive en su propio archivo y nunca
se mezcla con la logica que escribe el equipo.

    python herramientas/compilar_ui.py

Cada src/biblioteca/ui/disenos/<nombre>.ui produce
src/biblioteca/ui/generado/ui_<nombre>.py
"""

import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DISENOS = RAIZ / "src" / "biblioteca" / "ui" / "disenos"
GENERADO = RAIZ / "src" / "biblioteca" / "ui" / "generado"
UIC = RAIZ / ".venv" / "Lib" / "site-packages" / "PySide6" / "uic.exe"


def main() -> int:
    if not UIC.exists():
        print(f"No se encontro el compilador en {UIC}")
        print("Instala las dependencias: pip install -r requirements.txt")
        return 1

    GENERADO.mkdir(parents=True, exist_ok=True)
    (GENERADO / "__init__.py").touch()

    archivos = sorted(DISENOS.glob("*.ui"))
    if not archivos:
        print(f"No hay disenos en {DISENOS}")
        return 0

    for diseno in archivos:
        destino = GENERADO / f"ui_{diseno.stem}.py"
        resultado = subprocess.run(
            [str(UIC), "-g", "python", str(diseno), "-o", str(destino)],
            capture_output=True,
            text=True,
        )
        if resultado.returncode != 0:
            print(f"  ERROR en {diseno.name}: {resultado.stderr.strip()}")
            return 1
        print(f"  {diseno.name} -> {destino.name}")

    print(f"\n{len(archivos)} diseno(s) compilado(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
