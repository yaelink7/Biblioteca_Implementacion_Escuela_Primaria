"""Andamiaje de las pruebas de interfaz.

Equivale a `VentanaTestUtils` del paquete `GUIBiblia` del sistema Java, que
resolvía dos problemas: construir cada ventana dentro del hilo de la interfaz
y recorrer el árbol de componentes para encontrarlos. Aquí hacen falta los
dos mismos, más uno nuevo: las pantallas consultan la base al construirse, y
eso hay que interceptarlo.

**Qt se arranca en modo `offscreen`**, así que las pruebas corren sin abrir
ninguna ventana y funcionan igual en una máquina sin pantalla. Es lo que
permite ejecutarlas en el mismo `pytest` que las demás.
"""

from __future__ import annotations

import os

# Antes de importar PySide6: sin esto, Qt intenta abrir ventanas de verdad.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from datetime import date  # noqa: E402

import pytest  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from biblioteca.modelos.libro import Libro  # noqa: E402
from biblioteca.modelos.persona import Alumno, Empleado, Perfil, Rol  # noqa: E402
from biblioteca.modelos.prestamo import EstadoPrestamo, Prestamo  # noqa: E402
from biblioteca.repositorios.prestamos import Deudor  # noqa: E402


@pytest.fixture(scope="session")
def app() -> QApplication:
    """Una sola QApplication para toda la sesión: Qt no admite dos."""
    aplicacion = QApplication.instance() or QApplication([])
    yield aplicacion
    aplicacion.processEvents()


@pytest.fixture(autouse=True)
def procesar_eventos(app):
    """Deja la cola de Qt limpia entre pruebas.

    Varias pantallas usan un `QTimer` para no consultar en cada tecla. Si una
    prueba dejara un disparo pendiente, saltaría durante la siguiente.
    """
    yield
    app.processEvents()


# ------------------------------------------------------- datos de ejemplo
# Suficientes filas para que las tablas tengan algo que mostrar, y con los
# casos que cambian la apariencia: un libro de baja, un prestamo vencido.

@pytest.fixture
def libros_de_ejemplo() -> list[Libro]:
    return [
        Libro(id=1, titulo="El principito", autor="Saint-Exupéry",
              tipo_libro="Infantil", editorial="Salamandra", existencias=3,
              ano_publicacion=1943, num_paginas=96),
        Libro(id=2, titulo="Momo", autor="Michael Ende", tipo_libro="Infantil",
              editorial="Alfaguara", existencias=0, ano_publicacion=1973,
              num_paginas=272),
        Libro(id=3, titulo="Cuentos de la selva", autor="Horacio Quiroga",
              existencias=1, activo=False, motivo_baja="Extraviado",
              dado_baja_en=date(2026, 9, 1)),
    ]


@pytest.fixture
def alumnos_de_ejemplo() -> list[Alumno]:
    return [
        Alumno(id="a-1", codigo="A-001", nombre="Ana Sofía",
               apellido="Martínez", grado=4, grupo="B", telefono="2281234567"),
        Alumno(id="a-2", codigo="A-002", nombre="Luis", apellido="Ramírez",
               grado=2, grupo="A", telefono="2287654321"),
    ]


@pytest.fixture
def empleados_de_ejemplo() -> list[Empleado]:
    return [
        Empleado(id="e-1", codigo="EMP-001", nombre="María",
                 apellido="Hernández", correo="bibliotecaria@demo.com",
                 tipo_empleado="Bibliotecaria", rol=Rol.ADMINISTRADOR,
                 fecha_ingreso=date(2026, 1, 15)),
        Empleado(id="e-2", codigo="EMP-002", nombre="José", apellido="Luna",
                 correo="auxiliar@demo.com", tipo_empleado="Auxiliar",
                 rol=Rol.BIBLIOTECARIO, fecha_ingreso=date(2026, 2, 1)),
    ]


@pytest.fixture
def prestamos_de_ejemplo() -> list[Prestamo]:
    """Uno en plazo y uno vencido: el vencido pinta la fila de otro color."""
    return [
        Prestamo(id=1, libro_id=1, usuario_id="a-1",
                 fecha_prestamo=date(2026, 9, 15), fecha_limite=date(2026, 9, 22),
                 estado=EstadoPrestamo.ACTIVO, dias_restantes=3,
                 titulo_libro="El principito", nombre_alumno="Ana Sofía Martínez",
                 salon="4B"),
        Prestamo(id=2, libro_id=2, usuario_id="a-2",
                 fecha_prestamo=date(2026, 9, 1), fecha_limite=date(2026, 9, 8),
                 estado=EstadoPrestamo.VENCIDO, dias_restantes=-11,
                 titulo_libro="Momo", nombre_alumno="Luis Ramírez", salon="2A"),
    ]


@pytest.fixture
def deudores_de_ejemplo() -> list[Deudor]:
    return [
        Deudor(prestamo_id=2, codigo="A-002", alumno="Luis Ramírez", grado=2,
               grupo="A", correo=None, telefono="2287654321", libro="Momo",
               fecha_prestamo=date(2026, 9, 1), fecha_limite=date(2026, 9, 8),
               dias_de_retraso=11),
    ]


@pytest.fixture
def sesion_de_administradora() -> object:
    from biblioteca.core.sesion import Sesion

    return Sesion(perfil=Perfil(
        id="e-1", codigo="EMP-001", nombre="María", apellido="Hernández",
        rol=Rol.ADMINISTRADOR, correo="bibliotecaria@demo.com",
    ))


@pytest.fixture
def sesion_de_bibliotecario() -> object:
    from biblioteca.core.sesion import Sesion

    return Sesion(perfil=Perfil(
        id="e-2", codigo="EMP-002", nombre="José", apellido="Luna",
        rol=Rol.BIBLIOTECARIO, correo="auxiliar@demo.com",
    ))


@pytest.fixture
def con_sesion(sesion_de_administradora, monkeypatch):
    """Abre una sesion de administradora en la variable del modulo.

    `PantallaEmpleados` y `FormularioEmpleado` consultan el rol al
    construirse, para decidir si el combo de perfil de acceso se deja tocar.
    Sin sesion no se pueden ni crear, y eso es correcto: son las dos
    pantallas que deciden permisos.
    """
    from biblioteca.core import sesion as modulo_sesion

    monkeypatch.setattr(modulo_sesion, "_sesion_actual",
                        sesion_de_administradora)
    return sesion_de_administradora


# --------------------------------------------------- la base, interceptada
# Las pantallas consultan al construirse, asi que no hay forma de crearlas
# sin responderles. Estas funciones sustituyen al repositorio por una
# respuesta fija, y anotan si se llamo.

@pytest.fixture
def sin_base(monkeypatch):
    """Sustituye funciones de repositorio por respuestas fijas.

    `sin_base(modulo, listar=[...], buscar=[...])` deja cada nombre
    devolviendo lo que se le indique. Lo que no se nombre se queda como está,
    de modo que una llamada no prevista falla por intentar salir a la red en
    lugar de pasar inadvertida.
    """
    llamadas: dict[str, list] = {}

    def instalar(modulo, **respuestas):
        for nombre, respuesta in respuestas.items():
            registro = llamadas.setdefault(f"{modulo.__name__}.{nombre}", [])

            def responder(*args, _r=respuesta, _reg=registro, **kwargs):
                _reg.append((args, kwargs))
                if isinstance(_r, Exception):
                    raise _r
                return _r

            monkeypatch.setattr(modulo, nombre, responder)
        return llamadas

    instalar.llamadas = llamadas
    return instalar
