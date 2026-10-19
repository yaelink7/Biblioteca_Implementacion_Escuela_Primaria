"""Andamiaje comun de la suite.

Resuelve lo que impedia probar media aplicacion: `core/config.py` lee las
variables de entorno **al importarse** y revienta si faltan, y los
repositorios lo arrastran. Eso dejaba sin probar hasta sus funciones puras en
cualquier maquina sin `.env`, que es el obstaculo que `QA-02` registraba.

Aqui se ponen valores de prueba antes de que nada importe el paquete. Son
falsos a proposito: ninguna prueba de esta suite toca la red. Si alguna lo
intentara, el `create_client` fallaria y se notaria.
"""

from __future__ import annotations

import os

# Antes de cualquier import de biblioteca: config.py los lee al cargarse.
os.environ.setdefault("SUPABASE_URL", "https://pruebas.supabase.co")
os.environ.setdefault("SUPABASE_KEY", "sb_publishable_solo_para_pruebas")

from datetime import date  # noqa: E402

import pytest  # noqa: E402

from biblioteca.modelos.libro import Libro  # noqa: E402
from biblioteca.modelos.persona import Alumno, Empleado, Perfil, Rol  # noqa: E402
from biblioteca.modelos.prestamo import EstadoPrestamo, Prestamo  # noqa: E402


# ---------------------------------------------------------------- fabricas
# Cada fabrica devuelve el caso valido minimo. Una prueba cambia solo el
# campo que le interesa, de modo que el fallo senala ese campo y no el ruido
# de los otros ocho.

@pytest.fixture
def libro_valido() -> Libro:
    """Un libro que pasa todas las reglas: el camino feliz del grupo A."""
    return Libro(
        id=1,
        titulo="El principito",
        autor="Antoine de Saint-Exupéry",
        tipo_libro="Infantil",
        editorial="Salamandra",
        existencias=3,
        ano_publicacion=1943,
        num_paginas=96,
    )


@pytest.fixture
def alumno_valido() -> Alumno:
    """Alumno con los datos minimos que la biblioteca necesita."""
    return Alumno(
        id="a-1",
        codigo="A-001",
        nombre="Ana Sofía",
        apellido="Martínez",
        grado=4,
        grupo="B",
        telefono="2281234567",
    )


@pytest.fixture
def empleado_valido() -> Empleado:
    """Empleado con correo, que es con lo que inicia sesion."""
    return Empleado(
        id="e-1",
        codigo="EMP-001",
        nombre="María",
        apellido="Hernández",
        correo="bibliotecaria@demo.com",
        tipo_empleado="Bibliotecaria",
        fecha_ingreso=date(2026, 1, 15),
        rol=Rol.ADMINISTRADOR,
    )


@pytest.fixture
def prestamo_activo() -> Prestamo:
    """Prestamo abierto con tres dias por delante, segun la base."""
    return Prestamo(
        id=1,
        libro_id=1,
        usuario_id="a-1",
        fecha_prestamo=date(2026, 9, 15),
        fecha_limite=date(2026, 9, 22),
        estado=EstadoPrestamo.ACTIVO,
        dias_restantes=3,
        titulo_libro="El principito",
    )


@pytest.fixture
def perfil_valido() -> Perfil:
    return Perfil(
        id="p-1",
        codigo="P-001",
        nombre="Juan",
        apellido="Pérez",
        telefono="2281112222",
    )


# -------------------------------------------------------- dobles de la base
class RespuestaFalsa:
    """Lo que devuelve `.execute()` de supabase-py: un objeto con `.data`."""

    def __init__(self, data):
        self.data = data


class ConsultaFalsa:
    """Doble del constructor de consultas de supabase-py.

    Encadena como el real —`.select().eq().order().execute()`— y guarda lo que
    se le pidio, para poder comprobar **que** consulta se armo sin tocar la red.
    """

    def __init__(self, respuesta=None, error: Exception | None = None):
        self.respuesta = respuesta if respuesta is not None else []
        self.error = error
        self.llamadas: list[tuple] = []

    def _anota(self, nombre, *args, **kwargs):
        self.llamadas.append((nombre, args, kwargs))
        return self

    def __getattr__(self, nombre):
        # Cualquier metodo de encadenado se anota y devuelve la misma consulta.
        def encadenar(*args, **kwargs):
            return self._anota(nombre, *args, **kwargs)
        return encadenar

    def execute(self):
        self.llamadas.append(("execute", (), {}))
        if self.error:
            raise self.error
        return RespuestaFalsa(self.respuesta)

    # --- ayudas para las aserciones ---
    def nombres(self) -> list[str]:
        return [n for n, _, _ in self.llamadas]

    def argumentos_de(self, nombre: str) -> list[tuple]:
        return [a for n, a, _ in self.llamadas if n == nombre]


class UsuarioFalso:
    """Lo que trae `respuesta.user` de Supabase Auth."""

    def __init__(self, id="auth-1"):
        self.id = id


class AuthFalsa:
    """Doble de `cliente.auth`, para las pruebas de sesion.

    `usuario` controla los tres desenlaces del inicio de sesion: un usuario,
    `None` —credenciales rechazadas sin excepcion— o una excepcion.
    """

    def __init__(self, usuario=None, error: Exception | None = None,
                 error_al_salir: Exception | None = None):
        self.usuario = usuario
        self.error = error
        self.error_al_salir = error_al_salir
        self.entradas: list[dict] = []
        self.salidas = 0

    def sign_in_with_password(self, credenciales):
        self.entradas.append(credenciales)
        if self.error:
            raise self.error
        return type("Respuesta", (), {"user": self.usuario})()

    def sign_out(self):
        self.salidas += 1
        if self.error_al_salir:
            raise self.error_al_salir


class ClienteFalso:
    """Doble de `obtener_cliente()`."""

    def __init__(self, consulta: ConsultaFalsa | None = None, auth=None):
        self.consulta = consulta or ConsultaFalsa()
        self.auth = auth or AuthFalsa()
        self.tablas: list[str] = []
        self.rpc_llamadas: list[tuple[str, dict]] = []

    def table(self, nombre):
        self.tablas.append(nombre)
        return self.consulta

    def rpc(self, nombre, parametros=None):
        self.rpc_llamadas.append((nombre, parametros or {}))
        return self.consulta


@pytest.fixture(scope="session", autouse=True)
def nunca_la_red_de_verdad():
    """Red de seguridad: ninguna prueba sale a internet, ni por descuido.

    La hizo falta un caso concreto. `cerrar_sesion()` usa el
    `obtener_cliente` de `core/sesion.py`, y una prueba que cerraba la
    ventana principal lo llamaba sin que nadie lo hubiera sustituido: se
    construia un cliente de verdad contra la URL de pruebas y la llamada se
    quedaba esperando el tiempo de espera de la conexion. El
    `except Exception: pass` de `cerrar_sesion` se tragaba el fallo despues,
    asi que no habia ni mensaje: la suite entera se colgaba sin decir por que.

    Cada modulo hace `from ... import obtener_cliente`, de modo que sustituir
    el nombre en un modulo no alcanza a los otros. Lo que se sustituye aqui es
    `create_client`, que es por donde pasan todos, y se vacia la cache de
    `lru_cache` para que no quede uno construido de antes.

    **Va en ambito de sesion a proposito.** Siendo por prueba se retiraba
    antes de que pytest cerrara la sesion, y ahi Qt todavia procesa los
    eventos pendientes: el `closeEvent` de una ventana que quedo viva llamaba
    a `cerrar_sesion()` con la proteccion ya levantada, y la suite se colgaba
    **despues de la ultima prueba**, con todos los puntos impresos. Sin
    mensaje y sin prueba a la que culpar, que es la peor forma de fallar.
    """
    from biblioteca.core import supabase_cliente

    with pytest.MonkeyPatch.context() as parche:
        supabase_cliente.obtener_cliente.cache_clear()
        parche.setattr(supabase_cliente, "create_client",
                       lambda url, key: ClienteFalso())
        yield
        supabase_cliente.obtener_cliente.cache_clear()


@pytest.fixture
def cliente_falso():
    """Entrega una fabrica para instalar el doble en el modulo que se pruebe."""
    def instalar(monkeypatch, modulo, respuesta=None, error=None, auth=None):
        consulta = ConsultaFalsa(respuesta, error)
        cliente = ClienteFalso(consulta, auth=auth)
        monkeypatch.setattr(modulo, "obtener_cliente", lambda: cliente)
        return cliente
    return instalar
