"""Interfaz · «Entrar rápido» de la copia de pruebas.

Es la sección del prototipo mostaza. Solo aparece cuando el .env de la copia
de pruebas trae PRUEBAS_CORREO y PRUEBAS_CONTRASENA, y nunca contra la base de
la escuela. El clic se manda a la ventana, como lo hace el ratón, para que
Qt busque qué hay debajo del puntero: las letras de la tarjeta no pueden
quedarse con él.
"""

from __future__ import annotations

import pytest
from PySide6.QtCore import QPoint, Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QFrame, QLabel

from biblioteca.core import config
from biblioteca.core.sesion import ErrorDeAcceso
from biblioteca.ui import login as ui_login
from biblioteca.ui.login import DialogoLogin, _iniciales

CORREO = "maria.rodriguez@biblioteca.test"
COPIA_DE_PRUEBAS = "https://urorpysxbzgzebrdrrtb.supabase.co"


@pytest.fixture
def con_cuenta_de_pruebas(monkeypatch):
    monkeypatch.setattr(config, "ACCESO_DE_PRUEBAS", True)
    monkeypatch.setattr(config, "PRUEBAS_CORREO", CORREO)
    monkeypatch.setattr(config, "PRUEBAS_CONTRASENA", "clave-de-prueba")


def abrir(dialogo: DialogoLogin) -> DialogoLogin:
    dialogo.resize(980, 720)
    dialogo.show()
    QTest.qWaitForWindowExposed(dialogo)
    return dialogo


def clic_en_el_centro(dialogo: DialogoLogin) -> None:
    boton = dialogo.botonEntradaRapida
    centro = boton.mapTo(dialogo, boton.rect().center())
    QTest.mouseClick(dialogo.windowHandle(), Qt.MouseButton.LeftButton,
                     Qt.KeyboardModifier.NoModifier, centro)


# ===========================================================================
# Cuándo aparece
# ===========================================================================

def test_nunca_aparece_contra_la_base_de_la_escuela():
    escuela = f"https://{config.PROYECTO_DE_LA_ESCUELA}.supabase.co"
    assert not config.acceso_de_pruebas_permitido(escuela, CORREO, "x")


@pytest.mark.parametrize("correo, contrasena", [("", "x"), (CORREO, ""), ("", "")])
def test_sin_correo_y_contrasena_no_aparece(correo, contrasena):
    assert not config.acceso_de_pruebas_permitido(COPIA_DE_PRUEBAS, correo, contrasena)


def test_con_los_dos_en_la_copia_de_pruebas_aparece():
    assert config.acceso_de_pruebas_permitido(COPIA_DE_PRUEBAS, CORREO, "x")


def test_sin_la_cuenta_de_pruebas_la_ficha_queda_como_siempre(app, monkeypatch):
    monkeypatch.setattr(config, "ACCESO_DE_PRUEBAS", False)
    dialogo = DialogoLogin()

    assert dialogo.botonEntradaRapida is None
    assert dialogo.findChild(QFrame, "entradaRapida") is None


# ===========================================================================
# Qué muestra y dónde
# ===========================================================================

def test_la_seccion_va_entre_entrar_y_la_perforacion(app, con_cuenta_de_pruebas):
    dialogo = DialogoLogin()
    cuerpo = dialogo.ui.cuerpoFicha
    seccion = dialogo.findChild(QFrame, "entradaRapida")

    assert (cuerpo.indexOf(dialogo.ui.botonEntrar)
            < cuerpo.indexOf(seccion)
            < cuerpo.indexOf(dialogo.ui.perforacion))


def test_la_tarjeta_dice_con_que_cuenta_entra_y_nunca_la_contrasena(
    app, con_cuenta_de_pruebas
):
    dialogo = DialogoLogin()
    textos = [e.text() for e in dialogo.findChild(QFrame, "entradaRapida")
              .findChildren(QLabel)]

    assert "Entrar rápido" in textos
    assert "· solo en la copia de pruebas" in textos
    assert {"MR", "Cuenta de pruebas", CORREO} <= set(textos)
    assert not any("clave-de-prueba" in t for t in textos)


@pytest.mark.parametrize("correo, iniciales", [
    ("maria.rodriguez@biblioteca.test", "MR"),
    ("auxiliar@demo.com", "A"),
    ("ana_luisa-perez@x.mx", "AL"),
    ("@sin-nombre", "?"),
])
def test_las_iniciales_salen_del_correo(correo, iniciales):
    assert _iniciales(correo) == iniciales


def test_la_ficha_cabe_en_la_ventana_con_la_seccion_y_con_un_error(
    app, con_cuenta_de_pruebas
):
    """La sección alarga la ficha: no puede empujar la perforación fuera."""
    dialogo = abrir(DialogoLogin())
    seccion = dialogo.findChild(QFrame, "entradaRapida")

    for estado in ("normal", "con error"):
        if estado == "con error":
            dialogo.ui.etiquetaError.setText("Correo o contraseña incorrectos.")
            QTest.qWait(0)
        ficha = dialogo.ui.ficha.geometry()
        assert dialogo.rect().contains(ficha), estado
        abajo_de_entrar = dialogo.ui.botonEntrar.geometry().bottom()
        assert seccion.geometry().top() > abajo_de_entrar, estado
        assert dialogo.ui.perforacion.geometry().top() > seccion.geometry().bottom(), estado
        assert dialogo.botonEntradaRapida.height() >= 58, estado
    dialogo.close()


# ===========================================================================
# El clic
# ===========================================================================

def test_un_clic_en_el_centro_entra_con_la_cuenta_del_env(
    app, con_cuenta_de_pruebas, monkeypatch, sesion_de_administradora
):
    llamadas = []

    def espiar(correo, contrasena):
        # Mientras se verifica, ningún botón admite un segundo clic
        llamadas.append((correo, contrasena,
                         dialogo.ui.botonEntrar.isEnabled(),
                         dialogo.botonEntradaRapida.isEnabled()))
        return sesion_de_administradora

    monkeypatch.setattr(ui_login, "iniciar_sesion", espiar)
    dialogo = abrir(DialogoLogin())

    clic_en_el_centro(dialogo)

    assert llamadas == [(CORREO, "clave-de-prueba", False, False)]
    assert dialogo.sesion is sesion_de_administradora
    assert dialogo.result() == dialogo.DialogCode.Accepted


def test_si_la_cuenta_no_entra_se_explica_y_se_puede_reintentar(
    app, con_cuenta_de_pruebas, monkeypatch
):
    def rechazar(correo, contrasena):
        raise ErrorDeAcceso("Correo o contraseña incorrectos.")

    monkeypatch.setattr(ui_login, "iniciar_sesion", rechazar)
    dialogo = abrir(DialogoLogin())

    clic_en_el_centro(dialogo)

    assert dialogo.ui.etiquetaError.text() == "Correo o contraseña incorrectos."
    assert dialogo.ui.campoContrasena.text() == ""
    assert dialogo.botonEntradaRapida.isEnabled()
    assert dialogo.result() != dialogo.DialogCode.Accepted
    dialogo.close()


def test_el_centro_del_boton_es_del_boton(app, con_cuenta_de_pruebas):
    """Lo que Qt encuentra bajo el puntero, sin contar las letras de adentro."""
    dialogo = abrir(DialogoLogin())
    boton = dialogo.botonEntradaRapida

    for punto in (boton.rect().center(), QPoint(20, boton.height() // 2),
                  QPoint(boton.width() - 20, boton.height() // 2)):
        debajo = dialogo.childAt(boton.mapTo(dialogo, punto))
        assert debajo is boton or (
            debajo is not None
            and debajo.testAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            and boton.isAncestorOf(debajo)
        ), punto
    dialogo.close()
