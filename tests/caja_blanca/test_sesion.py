"""Caja blanca · inicio y cierre de sesión.

El sistema Java **no tenía esto**: abría directo en el menú principal sin
validar quién entraba, y las credenciales de la base estaban escritas dentro
de `ConexionBD.java`, en un repositorio público. No hay casos TC que heredar
porque no había nada que probar.

`iniciar_sesion` tiene cuatro salidas, y hasta ahora ninguna estaba
recorrida: el módulo entero estaba al 0 %. Dos de ellas son las que la
auditoría señaló:

- sin internet, el login decía «correo o contraseña incorrectos», así que la
  bibliotecaria tecleaba su contraseña cinco veces y terminaba cambiándola;
- una cuenta de Auth sin perfil en la tabla `perfiles` dejaba la sesión medio
  abierta.

El estado de la sesión es una variable de módulo, así que cada prueba la
limpia al entrar y al salir: si una dejara sesión abierta, la siguiente
pasaría por el motivo equivocado.
"""

from __future__ import annotations

import pytest

from biblioteca.core import sesion as modulo_sesion
from biblioteca.core.sesion import (
    ErrorDeAcceso,
    Sesion,
    cerrar_sesion,
    exigir_personal,
    hay_sesion,
    iniciar_sesion,
    sesion_actual,
)
from biblioteca.modelos.persona import Perfil, Rol

from tests.conftest import AuthFalsa, UsuarioFalso

FILA_PERFIL = {
    "id": "e-1", "auth_id": "auth-1", "codigo": "EMP-001", "nombre": "María",
    "apellido": "Hernández", "rol": "administrador", "activo": True,
    "correo": "bibliotecaria@demo.com",
}


@pytest.fixture(autouse=True)
def sin_sesion_previa():
    """Aísla la variable de módulo: ninguna prueba hereda la sesión de otra."""
    modulo_sesion._sesion_actual = None
    yield
    modulo_sesion._sesion_actual = None


def entrar(monkeypatch, cliente_falso, *, usuario=UsuarioFalso(),
           error=None, filas=(FILA_PERFIL,), error_al_salir=None):
    """Arma el cliente con el desenlace que la prueba necesita."""
    return cliente_falso(
        monkeypatch, modulo_sesion, respuesta=list(filas),
        auth=AuthFalsa(usuario=usuario, error=error,
                       error_al_salir=error_al_salir),
    )


# ===========================================================================
# iniciar_sesion() · camino feliz
# ===========================================================================

def test_el_camino_feliz_carga_el_perfil(monkeypatch, cliente_falso):
    entrar(monkeypatch, cliente_falso)

    sesion = iniciar_sesion("bibliotecaria@demo.com", "123456")

    assert sesion.perfil.nombre_completo == "María Hernández"
    assert sesion.perfil.rol is Rol.ADMINISTRADOR
    assert hay_sesion()


def test_el_perfil_se_busca_por_el_identificador_de_auth(
    monkeypatch, cliente_falso
):
    """Es la unión entre Supabase Auth y la tabla `perfiles`."""
    cliente = entrar(monkeypatch, cliente_falso)

    iniciar_sesion("bibliotecaria@demo.com", "123456")

    assert cliente.tablas == ["perfiles"]
    assert ("auth_id", "auth-1") in cliente.consulta.argumentos_de("eq")


def test_las_credenciales_se_envian_tal_como_se_capturaron(
    monkeypatch, cliente_falso
):
    cliente = entrar(monkeypatch, cliente_falso)

    iniciar_sesion("bibliotecaria@demo.com", "123456")

    assert cliente.auth.entradas == [
        {"email": "bibliotecaria@demo.com", "password": "123456"}]


def test_la_sesion_queda_disponible_para_el_resto_del_programa(
    monkeypatch, cliente_falso
):
    entrar(monkeypatch, cliente_falso)

    devuelta = iniciar_sesion("bibliotecaria@demo.com", "123456")

    assert sesion_actual() is devuelta


# ===========================================================================
# iniciar_sesion() · las tres salidas de error
# ===========================================================================

def test_sin_conexion_no_se_culpa_a_la_contrasena(monkeypatch, cliente_falso):
    """El defecto que hacía cambiar una contraseña que estaba bien.

    Antes, cualquier excepción salía como credenciales malas.
    """
    entrar(monkeypatch, cliente_falso,
           error=ConnectionError("Connection refused"))

    with pytest.raises(ErrorDeAcceso) as fallo:
        iniciar_sesion("bibliotecaria@demo.com", "123456")

    mensaje = str(fallo.value).lower()
    assert "contraseña" not in mensaje
    assert "conexión" in mensaje or "internet" in mensaje
    assert not hay_sesion()


def test_las_credenciales_malas_no_dicen_cual_de_los_dos_fallo(
    monkeypatch, cliente_falso
):
    """REQ-USU-02. Decir «ese correo no existe» enumera cuentas."""
    entrar(monkeypatch, cliente_falso,
           error=Exception("Invalid login credentials"))

    with pytest.raises(ErrorDeAcceso) as fallo:
        iniciar_sesion("quien.sea@demo.com", "equivocada")

    mensaje = str(fallo.value).lower()
    assert "correo o contraseña" in mensaje
    assert "no existe" not in mensaje


def test_una_respuesta_sin_usuario_tambien_se_rechaza(monkeypatch, cliente_falso):
    """Rama aparte: Auth puede responder sin excepción y sin usuario."""
    entrar(monkeypatch, cliente_falso, usuario=None)

    with pytest.raises(ErrorDeAcceso, match="Correo o contraseña"):
        iniciar_sesion("bibliotecaria@demo.com", "123456")

    assert not hay_sesion()


def test_una_cuenta_sin_perfil_no_deja_entrar(monkeypatch, cliente_falso):
    """Pasa si alguien crea el usuario en Auth y olvida registrar el perfil.

    Sin perfil no hay rol, y sin rol las políticas RLS no devuelven ni una
    fila: la aplicación abriría vacía sin explicar por qué.
    """
    entrar(monkeypatch, cliente_falso, filas=())

    with pytest.raises(ErrorDeAcceso, match="no tiene un perfil asignado"):
        iniciar_sesion("bibliotecaria@demo.com", "123456")


def test_una_cuenta_sin_perfil_deja_la_sesion_cerrada(monkeypatch, cliente_falso):
    """Media sesión abierta es peor que ninguna: el token quedaría vivo."""
    cliente = entrar(monkeypatch, cliente_falso, filas=())

    with pytest.raises(ErrorDeAcceso):
        iniciar_sesion("bibliotecaria@demo.com", "123456")

    assert not hay_sesion()
    assert cliente.auth.salidas == 1, "no se cerró la sesión de Auth"


def test_la_sesion_anterior_sobrevive_a_un_intento_fallido(
    monkeypatch, cliente_falso
):
    """Un fallo de red no debe expulsar a quien ya estaba dentro.

    `_sesion_actual` solo se reasigna en la última línea del camino feliz.
    """
    entrar(monkeypatch, cliente_falso)
    iniciar_sesion("bibliotecaria@demo.com", "123456")

    entrar(monkeypatch, cliente_falso, error=ConnectionError("sin red"))
    with pytest.raises(ErrorDeAcceso):
        iniciar_sesion("otra@demo.com", "x")

    assert hay_sesion(), "un intento fallido tiró la sesión en curso"


# ===========================================================================
# cerrar_sesion()
# ===========================================================================

def test_cerrar_sesion_limpia_el_estado(monkeypatch, cliente_falso):
    cliente = entrar(monkeypatch, cliente_falso)
    iniciar_sesion("bibliotecaria@demo.com", "123456")

    cerrar_sesion()

    assert not hay_sesion()
    assert cliente.auth.salidas == 1


def test_cerrar_sesion_funciona_sin_haberla_iniciado():
    """Lo llama la ventana al cerrarse, haya sesión o no."""
    cerrar_sesion()

    assert not hay_sesion()


def test_un_fallo_al_cerrar_no_impide_salir(monkeypatch, cliente_falso):
    """La rama del `except Exception: pass`, y la razón de que exista.

    Si la aplicación se cierra sin internet, `sign_out` falla. Levantar ahí
    dejaría a la bibliotecaria con una ventana que no se cierra, y el estado
    local ya quedó limpio de todos modos.
    """
    entrar(monkeypatch, cliente_falso,
           error_al_salir=ConnectionError("sin red"))
    iniciar_sesion("bibliotecaria@demo.com", "123456")

    cerrar_sesion()   # no debe levantar

    assert not hay_sesion()


def test_el_estado_se_limpia_antes_de_avisar_a_la_base(monkeypatch, cliente_falso):
    """El orden importa: primero lo local, después la red.

    Al revés, un fallo de red dejaría la sesión local abierta.
    """
    entrar(monkeypatch, cliente_falso,
           error_al_salir=ConnectionError("sin red"))
    iniciar_sesion("bibliotecaria@demo.com", "123456")

    cerrar_sesion()

    assert modulo_sesion._sesion_actual is None


# ===========================================================================
# sesion_actual() y hay_sesion()
# ===========================================================================

def test_sin_sesion_pedirla_es_un_error():
    with pytest.raises(ErrorDeAcceso, match="No hay una sesión iniciada"):
        sesion_actual()


def test_hay_sesion_distingue_los_dos_estados(monkeypatch, cliente_falso):
    assert hay_sesion() is False

    entrar(monkeypatch, cliente_falso)
    iniciar_sesion("bibliotecaria@demo.com", "123456")

    assert hay_sesion() is True


# ===========================================================================
# exigir_personal() · las dos ramas y el caso sin sesión
# ===========================================================================

def _abrir(rol: Rol) -> None:
    modulo_sesion._sesion_actual = Sesion(
        perfil=Perfil(id="p-1", codigo="P-1", nombre="Ana", apellido="López",
                      rol=rol)
    )


@pytest.mark.parametrize("rol", [Rol.ADMINISTRADOR, Rol.BIBLIOTECARIO])
def test_el_personal_pasa(rol):
    _abrir(rol)

    assert exigir_personal().perfil.rol is rol


def test_un_alumno_no_pasa():
    """Es la única defensa del cliente; la de verdad son las políticas RLS."""
    _abrir(Rol.ALUMNO)

    with pytest.raises(ErrorDeAcceso, match="personal de la biblioteca"):
        exigir_personal()


def test_sin_sesion_tampoco_pasa():
    with pytest.raises(ErrorDeAcceso, match="No hay una sesión iniciada"):
        exigir_personal()


# ===========================================================================
# Sesion · lo que se muestra en la barra de la ventana
# ===========================================================================

class TestSaludo:
    @pytest.mark.parametrize("rol,esperado", [
        (Rol.ADMINISTRADOR, "Ana López · Administrador"),
        (Rol.BIBLIOTECARIO, "Ana López · Bibliotecario"),
        (Rol.ALUMNO, "Ana López · Alumno"),
    ])
    def test_nombre_y_perfil(self, rol, esperado):
        sesion = Sesion(perfil=Perfil(codigo="P-1", nombre="Ana",
                                      apellido="López", rol=rol))

        assert sesion.saludo == esperado

    def test_el_personal_se_distingue_del_alumno(self):
        assert Sesion(perfil=Perfil(codigo="P-1", nombre="A", apellido="B",
                                    rol=Rol.BIBLIOTECARIO)).es_personal
        assert not Sesion(perfil=Perfil(codigo="P-1", nombre="A", apellido="B",
                                        rol=Rol.ALUMNO)).es_personal
