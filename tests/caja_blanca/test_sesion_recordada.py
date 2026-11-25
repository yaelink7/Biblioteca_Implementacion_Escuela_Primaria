"""Caja blanca · acceso rápido de la copia de pruebas.

Con `RECORDAR_SESION=1` en el `.env` de la copia de pruebas, el programa
guarda el permiso de renovación que da Supabase al entrar y lo usa para
reanudar la sesión al abrirse. Nunca guarda la contraseña.

Las dos trampas que estas pruebas cuidan:

- `sign_out()` revoca ese permiso en Supabase, así que cerrar la ventana no
  puede llamarlo: la próxima apertura volvería a pedir la contraseña;
- Supabase cambia el permiso en cada renovación, así que el archivo tiene
  que seguir al último, o la próxima apertura llevaría uno ya usado.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from supabase_auth.errors import AuthApiError

from biblioteca.core import config
from biblioteca.core import sesion as modulo_sesion
from biblioteca.core.sesion import (
    cerrar_sesion,
    hay_sesion,
    iniciar_sesion,
    restaurar_sesion_recordada,
)

from tests.conftest import UsuarioFalso

FILA_PERFIL = {
    "id": "e-1", "auth_id": "auth-1", "codigo": "EMP-001", "nombre": "María Elena",
    "apellido": "Rodríguez Lara", "rol": "administrador", "activo": True,
    "correo": "maria.rodriguez@biblioteca.test",
}


class AuthRecordable:
    """Doble de `cliente.auth` con renovación y aviso de cambios."""

    def __init__(self, usuario=UsuarioFalso(), permiso_nuevo="permiso-2",
                 error_al_renovar: Exception | None = None):
        self.usuario = usuario
        self.permiso_nuevo = permiso_nuevo
        self.error_al_renovar = error_al_renovar
        self.renovaciones: list[str] = []
        self.escuchas: list = []
        self.salidas = 0

    def sign_in_with_password(self, credenciales):
        return SimpleNamespace(
            user=self.usuario, session=SimpleNamespace(refresh_token="permiso-1"))

    def refresh_session(self, permiso):
        self.renovaciones.append(permiso)
        if self.error_al_renovar:
            raise self.error_al_renovar
        return SimpleNamespace(
            user=self.usuario,
            session=SimpleNamespace(refresh_token=self.permiso_nuevo))

    def on_auth_state_change(self, aviso):
        self.escuchas.append(aviso)

    def sign_out(self):
        self.salidas += 1


@pytest.fixture(autouse=True)
def estado_limpio(monkeypatch, tmp_path):
    """Cada prueba empieza sin sesión, sin escucha y con su propio archivo."""
    monkeypatch.setattr(modulo_sesion, "_sesion_actual", None)
    monkeypatch.setattr(modulo_sesion, "_escucha_activa", False)
    monkeypatch.setattr(config, "ARCHIVO_DE_SESION", tmp_path / ".sesion_recordada")
    monkeypatch.setattr(config, "RECORDAR_SESION", True)
    yield
    modulo_sesion._sesion_actual = None


def instalar(monkeypatch, cliente_falso, auth=None, filas=(FILA_PERFIL,)):
    auth = auth or AuthRecordable()
    cliente_falso(monkeypatch, modulo_sesion, respuesta=list(filas), auth=auth)
    return auth


# ===========================================================================
# La bandera
# ===========================================================================

def test_la_bandera_nunca_se_activa_contra_la_base_de_la_escuela():
    escuela = f"https://{config.PROYECTO_DE_LA_ESCUELA}.supabase.co"
    assert not config.recordar_sesion_permitido(escuela, "1")


def test_la_bandera_se_activa_en_la_copia_de_pruebas():
    assert config.recordar_sesion_permitido("https://urorpysxbzgzebrdrrtb.supabase.co", "1")


@pytest.mark.parametrize("bandera", [None, "", "0", "si"])
def test_sin_la_bandera_exacta_no_se_recuerda(bandera):
    assert not config.recordar_sesion_permitido("https://otra.supabase.co", bandera)


def test_sin_la_bandera_no_se_guarda_ni_se_reanuda(monkeypatch, cliente_falso):
    monkeypatch.setattr(config, "RECORDAR_SESION", False)
    auth = instalar(monkeypatch, cliente_falso)

    iniciar_sesion("maria.rodriguez@biblioteca.test", "x")

    assert not config.ARCHIVO_DE_SESION.exists()
    assert restaurar_sesion_recordada() is None
    assert auth.renovaciones == []


# ===========================================================================
# Entrar y reanudar
# ===========================================================================

def test_al_entrar_se_guarda_el_permiso_y_no_la_contrasena(monkeypatch, cliente_falso):
    instalar(monkeypatch, cliente_falso)

    iniciar_sesion("maria.rodriguez@biblioteca.test", "contrasena-secreta")

    guardado = config.ARCHIVO_DE_SESION.read_text(encoding="utf-8")
    assert guardado == "permiso-1"
    assert "contrasena-secreta" not in guardado


def test_al_abrir_se_reanuda_la_sesion_guardada(monkeypatch, cliente_falso):
    auth = instalar(monkeypatch, cliente_falso)
    config.ARCHIVO_DE_SESION.write_text("permiso-1", encoding="utf-8")

    sesion = restaurar_sesion_recordada()

    assert sesion is not None
    assert sesion.perfil.nombre_completo == "María Elena Rodríguez Lara"
    assert auth.renovaciones == ["permiso-1"]
    assert hay_sesion()


def test_al_reanudar_se_guarda_el_permiso_nuevo(monkeypatch, cliente_falso):
    """Supabase cambia el permiso al renovar; el viejo ya no sirve."""
    instalar(monkeypatch, cliente_falso)
    config.ARCHIVO_DE_SESION.write_text("permiso-1", encoding="utf-8")

    restaurar_sesion_recordada()

    assert config.ARCHIVO_DE_SESION.read_text(encoding="utf-8") == "permiso-2"


def test_cada_renovacion_posterior_reescribe_el_archivo(monkeypatch, cliente_falso):
    auth = instalar(monkeypatch, cliente_falso)
    iniciar_sesion("maria.rodriguez@biblioteca.test", "x")
    assert len(auth.escuchas) == 1

    auth.escuchas[0]("TOKEN_REFRESHED", SimpleNamespace(refresh_token="permiso-9"))
    auth.escuchas[0]("SIGNED_OUT", None)

    assert config.ARCHIVO_DE_SESION.read_text(encoding="utf-8") == "permiso-9"


def test_la_escucha_se_registra_una_sola_vez(monkeypatch, cliente_falso):
    auth = instalar(monkeypatch, cliente_falso)

    iniciar_sesion("maria.rodriguez@biblioteca.test", "x")
    restaurar_sesion_recordada()

    assert len(auth.escuchas) == 1


def test_sin_archivo_guardado_se_pide_entrar(monkeypatch, cliente_falso):
    auth = instalar(monkeypatch, cliente_falso)

    assert restaurar_sesion_recordada() is None
    assert auth.renovaciones == []


def test_un_archivo_vacio_cuenta_como_sin_sesion(monkeypatch, cliente_falso):
    auth = instalar(monkeypatch, cliente_falso)
    config.ARCHIVO_DE_SESION.write_text("  \n", encoding="utf-8")

    assert restaurar_sesion_recordada() is None
    assert auth.renovaciones == []


# ===========================================================================
# Cuando el permiso guardado ya no sirve
# ===========================================================================

def test_un_permiso_vencido_se_olvida(monkeypatch, cliente_falso):
    vencido = AuthApiError("Invalid Refresh Token", 400, "refresh_token_not_found")
    instalar(monkeypatch, cliente_falso, auth=AuthRecordable(error_al_renovar=vencido))
    config.ARCHIVO_DE_SESION.write_text("permiso-viejo", encoding="utf-8")

    assert restaurar_sesion_recordada() is None
    assert not config.ARCHIVO_DE_SESION.exists()


def test_sin_internet_el_permiso_se_conserva_para_la_proxima(monkeypatch, cliente_falso):
    """Sin red no se sabe si el permiso sirve: borrarlo obligaría a teclear."""
    instalar(monkeypatch, cliente_falso,
             auth=AuthRecordable(error_al_renovar=ConnectionError("sin red")))
    config.ARCHIVO_DE_SESION.write_text("permiso-1", encoding="utf-8")

    assert restaurar_sesion_recordada() is None
    assert config.ARCHIVO_DE_SESION.read_text(encoding="utf-8") == "permiso-1"


def test_una_renovacion_sin_usuario_se_olvida(monkeypatch, cliente_falso):
    instalar(monkeypatch, cliente_falso, auth=AuthRecordable(usuario=None))
    config.ARCHIVO_DE_SESION.write_text("permiso-1", encoding="utf-8")

    assert restaurar_sesion_recordada() is None
    assert not config.ARCHIVO_DE_SESION.exists()


def test_una_cuenta_sin_perfil_no_deja_sesion_ni_archivo(monkeypatch, cliente_falso):
    instalar(monkeypatch, cliente_falso, filas=())
    config.ARCHIVO_DE_SESION.write_text("permiso-1", encoding="utf-8")

    assert restaurar_sesion_recordada() is None
    assert not hay_sesion()
    assert not config.ARCHIVO_DE_SESION.exists()


# ===========================================================================
# Cerrar la ventana frente a «Cerrar sesión»
# ===========================================================================

def test_cerrar_la_ventana_no_revoca_la_sesion_guardada(monkeypatch, cliente_falso):
    auth = instalar(monkeypatch, cliente_falso)
    iniciar_sesion("maria.rodriguez@biblioteca.test", "x")

    cerrar_sesion(olvidar=False)

    assert auth.salidas == 0
    assert config.ARCHIVO_DE_SESION.exists()
    assert not hay_sesion()


def test_cerrar_sesion_la_olvida_y_la_revoca(monkeypatch, cliente_falso):
    auth = instalar(monkeypatch, cliente_falso)
    iniciar_sesion("maria.rodriguez@biblioteca.test", "x")

    cerrar_sesion()

    assert auth.salidas == 1
    assert not config.ARCHIVO_DE_SESION.exists()


def test_sin_la_bandera_cerrar_la_ventana_cierra_como_siempre(monkeypatch, cliente_falso):
    """En la copia de la escuela nada cambia: la ventana cierra la sesión."""
    monkeypatch.setattr(config, "RECORDAR_SESION", False)
    auth = instalar(monkeypatch, cliente_falso)

    cerrar_sesion(olvidar=False)

    assert auth.salidas == 1
