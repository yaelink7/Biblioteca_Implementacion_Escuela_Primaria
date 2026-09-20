"""Comprueba que cada fallo se explique por lo que es, y no siempre por internet.

Nace de una inconsistencia entre el documento y el codigo: el Avance declara
en RNF-USA-03 que los mensajes de error deben indicar la causa y que hacer,
mientras que seis pantallas respondian «Revisa tu conexion a internet» ante
cualquier excepcion. Un permiso faltante, una sesion vencida, una regla de la
base y un defecto de programacion se veian identicos, de modo que ni el
bibliotecario ni el equipo podian saber que estaba pasando en realidad.

Estas pruebas no tocan la base ni la interfaz: le entregan excepciones al
clasificador y revisan como las explica.
"""

import pytest

from biblioteca.core.errores import Explicacion, causa, explicar, mensaje


class ErrorDePrestamo(Exception):
    """Homonima de la del repositorio: se reconoce por el nombre de la clase."""


# --------------------------------------------------------------------------
# Lo que motivo el cambio: no culpar a internet de todo
# --------------------------------------------------------------------------

def test_un_defecto_de_programacion_no_se_atribuye_a_la_conexion():
    """El caso que hacia inutil el mensaje anterior."""
    explicacion = explicar(TypeError("'NoneType' object is not subscriptable"))

    assert not explicacion.es_de_red
    assert "no es un problema de tu conexión" in str(explicacion).lower()
    assert "TypeError" in explicacion.detalle


def test_un_fallo_desconocido_admite_que_no_sabe_la_causa():
    """Inventar una causa es peor que decir que se desconoce."""
    explicacion = explicar(Exception("algo raro paso"))

    assert not explicacion.es_de_red
    assert explicacion.detalle           # siempre queda algo que reportar
    assert explicacion.que_hacer


@pytest.mark.parametrize("error", [
    ConnectionError("Connection refused"),
    OSError("[Errno 11001] getaddrinfo failed"),
    Exception("httpx.ConnectTimeout: timed out"),
])
def test_los_fallos_de_red_si_mencionan_la_conexion(error):
    assert explicar(error).es_de_red


# --------------------------------------------------------------------------
# Cada causa se distingue de las demas
# --------------------------------------------------------------------------

def test_un_permiso_faltante_dice_que_es_de_permisos():
    explicacion = explicar(Exception('42501: new row violates row-level security'))

    assert "permiso" in explicacion.causa.lower()
    assert not explicacion.es_de_red


def test_una_sesion_vencida_pide_volver_a_entrar():
    explicacion = explicar(Exception("JWT expired"))

    assert "sesión" in explicacion.causa.lower()
    assert "entrar" in explicacion.que_hacer.lower()


def test_el_limite_de_un_libro_se_explica_como_regla_y_no_como_falla():
    explicacion = explicar(
        Exception('duplicate key value violates unique constraint "prestamo_unico_activo"')
    )

    assert "préstamo activo" in explicacion.causa
    assert "un libro por alumno" in explicacion.que_hacer
    assert not explicacion.es_de_red


def test_las_cuatro_causas_se_distinguen_entre_si():
    """Si dos fallos distintos dieran el mismo texto, volveriamos al problema."""
    causas = {
        causa(ConnectionError("Connection refused")),
        causa(Exception("42501: row-level security")),
        causa(Exception("JWT expired")),
        causa(TypeError("x")),
    }
    assert len(causas) == 4


# --------------------------------------------------------------------------
# RNF-USA-03: causa y que hacer, siempre
# --------------------------------------------------------------------------

@pytest.mark.parametrize("error", [
    ConnectionError("Connection refused"),
    Exception("42501: row-level security"),
    Exception("JWT expired"),
    TypeError("x"),
    Exception("cualquier otra cosa"),
])
def test_todo_mensaje_dice_la_causa_y_que_hacer(error):
    explicacion = explicar(error)

    assert explicacion.causa.strip()
    assert explicacion.que_hacer.strip()
    assert explicacion.causa in mensaje(error)
    assert explicacion.que_hacer in mensaje(error)


def test_el_detalle_tecnico_acompana_al_mensaje():
    """El equipo necesita el tipo y el texto originales para diagnosticar."""
    texto = mensaje(KeyError("usuario_id"))

    assert "KeyError" in texto
    assert "usuario_id" in texto


# --------------------------------------------------------------------------
# Los errores propios ya vienen escritos para el bibliotecario
# --------------------------------------------------------------------------

def test_un_error_propio_se_muestra_tal_cual():
    propio = ErrorDePrestamo("Este alumno ya tiene un préstamo activo.")

    assert causa(propio) == "Este alumno ya tiene un préstamo activo."
    assert "Detalle técnico" not in mensaje(propio)


def test_un_error_propio_sin_texto_no_deja_el_mensaje_vacio():
    assert causa(ErrorDePrestamo()).strip()


# --------------------------------------------------------------------------
# Forma del resultado
# --------------------------------------------------------------------------

def test_la_explicacion_es_inmutable():
    """Nadie debe poder reescribir la causa despues de clasificarla."""
    explicacion = explicar(TypeError("x"))

    with pytest.raises(Exception):
        explicacion.causa = "otra cosa"


def test_el_mensaje_separa_sus_partes_en_parrafos():
    assert "\n\n" in mensaje(ConnectionError("Connection refused"))


def test_sin_detalle_no_queda_un_parrafo_vacio_al_final():
    texto = str(Explicacion("Causa.", "Qué hacer."))

    assert texto == "Causa.\n\nQué hacer."
