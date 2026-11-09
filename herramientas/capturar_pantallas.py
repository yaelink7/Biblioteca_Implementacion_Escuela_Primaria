"""Fotografia las doce pantallas del sistema contra la base real.

Inicia sesion con la cuenta de demostracion y abre cada pantalla con los datos
que la base devuelva en ese momento. Las capturas no son maquetas: son el
sistema corriendo.

Las ventanas se muestran un instante y se cierran solas: hace falta la
plataforma nativa de Windows porque la de modo offscreen no tiene
tipografias y el texto saldria como cajas vacias.
"""

from __future__ import annotations

import sys
from pathlib import Path

# NO se usa QT_QPA_PLATFORM=offscreen: esa plataforma no trae tipografias y
# todo el texto sale como cajas vacias. Con la plataforma nativa de Windows
# las ventanas parpadean un momento, que es el precio de que se lea el texto.

from PySide6.QtCore import Qt  # noqa: E402
from PySide6.QtWidgets import QApplication, QLineEdit, QWidget  # noqa: E402

from biblioteca.core.sesion import iniciar_sesion  # noqa: E402
from biblioteca.repositorios import libros as repo_libros  # noqa: E402
from biblioteca.repositorios import personas as repo_personas  # noqa: E402
from biblioteca.ui.alumnos import PantallaAlumnos  # noqa: E402
from biblioteca.ui.catalogo import PantallaCatalogo  # noqa: E402
from biblioteca.ui.deudores import PantallaDeudores  # noqa: E402
from biblioteca.ui.empleados import PantallaEmpleados  # noqa: E402
from biblioteca.ui.estilo import HOJA_DE_ESTILO  # noqa: E402
from biblioteca.ui.formulario_alumno import FormularioAlumno  # noqa: E402
from biblioteca.ui.formulario_empleado import FormularioEmpleado  # noqa: E402
from biblioteca.ui.formulario_libro import FormularioLibro  # noqa: E402
from biblioteca.ui.historial_alumno import DialogoHistorial  # noqa: E402
from biblioteca.ui.login import DialogoLogin  # noqa: E402
from biblioteca.ui.nuevo_prestamo import DialogoNuevoPrestamo  # noqa: E402
from biblioteca.ui.prestamos import PantallaPrestamos  # noqa: E402
from biblioteca.ui.ventana_principal import VentanaPrincipal  # noqa: E402

# Uso:  .venv/Scripts/python.exe herramientas/capturar_pantallas.py <carpeta>
DESTINO = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("capturas")
CORREO, CONTRASENA = "bibliotecaria@demo.com", "123456"


def despeinar(widget: QWidget) -> None:
    """Quita la seleccion de los campos de texto.

    El campo que recibe el foco al abrirse un formulario queda con todo su
    texto seleccionado, y en la captura sale resaltado en magenta como si
    estuviera mal. No es un error del sistema, pero en el documento lo
    parece.
    """
    for campo in widget.findChildren(QLineEdit):
        campo.deselect()
        campo.setCursorPosition(0)


def retratar(app: QApplication, widget: QWidget, nombre: str,
             ancho: int | None = None, alto: int | None = None) -> None:
    """Muestra el widget, deja que Qt lo dibuje y lo guarda."""
    if ancho and alto:
        widget.resize(ancho, alto)
    widget.show()
    app.processEvents()
    # Despues de mostrar, no antes: el foco se reparte al mostrar la ventana,
    # y es el foco el que selecciona el texto del campo.
    despeinar(widget)
    app.processEvents()
    widget.grab().save(str(DESTINO / f"{nombre}.png"))
    widget.hide()
    print(f"  {nombre}.png")


def main() -> int:
    DESTINO.mkdir(parents=True, exist_ok=True)

    app = QApplication(sys.argv[:1])
    app.setApplicationName("Biblioteca Escolar Adalberto Tejeda")
    app.setStyleSheet(HOJA_DE_ESTILO)

    # 1. El login, antes de entrar: es lo primero que ve el usuario.
    print("Capturando:")
    login = DialogoLogin()
    login.ui.campoCorreo.setText(CORREO)
    login.ui.campoContrasena.setText("••••••")
    login.ui.botonEntrar.setFocus()
    retratar(app, login, "01_login")

    # 2. Sesion real contra Supabase. De aqui en adelante, lo que se ve son
    #    los datos que las politicas RLS dejan ver a esta cuenta.
    sesion = iniciar_sesion(CORREO, CONTRASENA)
    print(f"  (sesion iniciada: {sesion.saludo})")

    # 3. La ventana completa, con sus cinco pestanas.
    ventana = VentanaPrincipal(sesion)
    retratar(app, ventana, "02_ventana_principal", 1000, 640)

    # 4. Cada pestana por separado, para poder describirla aparte.
    pestanas = [
        ("03_catalogo", PantallaCatalogo),
        ("04_prestamos", PantallaPrestamos),
        ("05_alumnos", PantallaAlumnos),
        ("06_deudores", PantallaDeudores),
        ("07_empleados", PantallaEmpleados),
    ]
    for nombre, clase in pestanas:
        retratar(app, clase(), nombre, 980, 560)

    # 5. El dialogo de prestamo, con alumno y libro ya elegidos: asi se ve el
    #    resumen y el aviso del plazo, que es lo que explica la pantalla.
    nuevo = DialogoNuevoPrestamo()
    if nuevo.ui.listaAlumnos.count():
        nuevo.ui.listaAlumnos.setCurrentRow(0)
    for fila in range(nuevo.ui.listaLibros.count()):
        marcas = nuevo.ui.listaLibros.item(fila).flags()
        if marcas & Qt.ItemFlag.ItemIsEnabled:   # los agotados no se eligen
            nuevo.ui.listaLibros.setCurrentRow(fila)
            break
    retratar(app, nuevo, "08_nuevo_prestamo", 760, 520)

    # 6. Formulario de libro, en modo modificacion y con un libro de verdad.
    acervo = repo_libros.listar()
    retratar(app, FormularioLibro(libro=acervo[0] if acervo else None),
             "09_formulario_libro")

    # 7. Formulario de alumno, con un alumno del padron.
    padron = repo_personas.listar_alumnos()
    retratar(app, FormularioAlumno(alumno=padron[0] if padron else None),
             "10_formulario_alumno")

    # 8. Formulario de empleado. El combo de perfil de acceso se ve habilitado
    #    porque la cuenta de demostracion es administradora.
    plantilla = repo_personas.listar_empleados()
    retratar(app, FormularioEmpleado(empleado=plantilla[0] if plantilla else None),
             "11_formulario_empleado")

    # 9. Historial de un alumno que tenga movimientos.
    if padron:
        con_historial = padron[0]
        for alumno in padron:
            from biblioteca.repositorios import prestamos as repo_prestamos
            if repo_prestamos.historial_de(alumno.id):
                con_historial = alumno
                break
        retratar(app, DialogoHistorial(None, con_historial),
                 "12_historial_alumno", 720, 480)

    print(f"\nListo. {len(list(DESTINO.glob('*.png')))} capturas en {DESTINO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
