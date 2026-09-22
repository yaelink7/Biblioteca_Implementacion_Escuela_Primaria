"""Comprueba que cada mensaje que levanta Postgres llegue traducido.

Nace de un defecto que la auditoria encontro: los patrones del traductor se
escribieron contra mensajes **supuestos**, no contra los que los disparadores
emiten de verdad. Tres de las reglas mas usadas no coincidian, de modo que el
bibliotecario leia el volcado crudo del error en lugar de «no quedan
ejemplares disponibles».

Las pruebas anteriores no lo detectaban porque solo ejercitaban una de las
ocho reglas del diccionario: `coverage` reportaba 100 % de lineas y de ramas
con siete reglas sin interrogar. Aqui se prueba cada una por separado.

**Los textos de MENSAJES_REALES estan copiados literalmente de los `raise
exception` de `database/migraciones/`.** Si un disparador cambia su texto y
nadie actualiza el traductor, la prueba correspondiente falla. Esa es toda su
razon de ser.
"""

import pytest

from biblioteca.core.errores import causa, explicar, mensaje


class ErrorDePrestamo(Exception):
    """Homonima de la del repositorio: se reconoce por el nombre de la clase."""


# Texto que levanta la base  ->  fragmento que el bibliotecario debe leer
MENSAJES_REALES = [
    # 03_prestamos_y_reglas.sql
    ('No hay ejemplares disponibles de "El principito".', "ejemplares"),
    ('El libro "Momo" esta dado de baja del acervo.', "dado de baja"),
    ('No se puede dar de baja "Momo": tiene 2 prestamo(s) sin devolver.',
     "ejemplares prestados"),
    # 02_catalogo_y_bitacora.sql
    ("El ano de publicacion (3000) no puede ser futuro.", "futuro"),
    ("El ano de publicacion (1200) no es valido.", "no es válido"),
    # 06_altas_de_personas_transaccionales.sql
    ("Un empleado no puede tener perfil de alumno.", "perfil de alumno"),
    # 07_actualizar_alumno_y_vista_prestamos.sql
    ("No se encontró el alumno indicado.", "padrón"),
    # 09_permisos_de_bibliotecario_y_proteccion_de_rol.sql
    ("No puedes cambiar tu propio perfil de acceso. Pídelo a un administrador.",
     "tu propio perfil"),
    ("Solo un administrador puede cambiar el perfil de acceso.",
     "administrador"),
    # Restricciones e indices
    ('duplicate key value violates unique constraint "prestamo_unico_activo_por_usuario"',
     "préstamo activo"),
    ('duplicate key value violates unique constraint "perfiles_codigo_key"',
     "ese código"),
    ('new row for relation "libros" violates check constraint "baja_con_motivo"',
     "motivo de la baja"),
    ('violates check constraint "devolucion_coherente"', "fecha de devolución"),
]


@pytest.mark.parametrize("texto,fragmento", MENSAJES_REALES)
def test_cada_mensaje_de_la_base_se_traduce(texto, fragmento):
    explicacion = explicar(Exception(texto))

    assert explicacion.tipo == "regla", (
        f"«{texto[:45]}…» no se reconocio como regla de la base; "
        f"el bibliotecario leeria: {explicacion.causa}"
    )
    assert fragmento.lower() in explicacion.causa.lower()
    assert explicacion.que_hacer, "una regla sin «qué hacer» incumple RNF-USA-03"


@pytest.mark.parametrize("texto,_", MENSAJES_REALES)
def test_ningun_mensaje_de_la_base_llega_crudo(texto, _):
    """El sintoma que se quiere evitar: Postgres hablandole al bibliotecario."""
    assert "La base de datos rechazó la operación" not in mensaje(Exception(texto))


# --------------------------------------------------------------------------
# El «401» que mandaba a reiniciar sesion
# --------------------------------------------------------------------------

@pytest.mark.parametrize("texto", [
    "duplicate key ... DETAIL: Key (id)=(1401) already exists",
    "El libro 401 no existe",
    'insert or update violates foreign key constraint, libro_id = 2401',
])
def test_un_401_dentro_de_un_numero_no_es_sesion_vencida(texto):
    """`401` como subcadena aparecia en cualquier identificador o cantidad."""
    assert explicar(Exception(texto)).tipo != "sesion"


def test_una_sesion_vencida_de_verdad_si_se_reconoce():
    explicacion = explicar(Exception("JWT expired"))

    assert explicacion.tipo == "sesion"
    assert "entrar" in explicacion.que_hacer.lower()


def test_las_credenciales_malas_no_se_confunden_con_la_sesion():
    """REQ-USU-02: no debe revelar cual de los dos campos fallo."""
    explicacion = explicar(Exception("Invalid login credentials"))

    assert explicacion.tipo == "credenciales"
    assert "correo o contraseña" in explicacion.causa.lower()


# --------------------------------------------------------------------------
# Los errores propios envuelven al de la base
# --------------------------------------------------------------------------

def test_un_error_propio_se_explica_por_su_causa_original():
    """Los repositorios envuelven; el traductor desenvuelve."""
    envoltorio = ErrorDePrestamo("no se pudo prestar")
    envoltorio.__cause__ = Exception('No hay ejemplares disponibles de "Momo".')

    explicacion = explicar(envoltorio)

    assert explicacion.tipo == "regla"
    assert "ejemplares" in explicacion.causa


def test_un_error_propio_sin_causa_conserva_su_texto_y_dice_que_hacer():
    explicacion = explicar(ErrorDePrestamo("No se encontró ese préstamo."))

    assert explicacion.causa == "No se encontró ese préstamo."
    assert explicacion.que_hacer, "sin «qué hacer» se incumple RNF-USA-03"


def test_un_error_propio_sin_texto_no_deja_el_mensaje_vacio():
    assert causa(ErrorDePrestamo()).strip()


# --------------------------------------------------------------------------
# Que la red siga distinguiendose de lo demas
# --------------------------------------------------------------------------

@pytest.mark.parametrize("error", [
    ConnectionError("Connection refused"),
    OSError("[Errno 11001] getaddrinfo failed"),
    Exception("httpx.ConnectTimeout: timed out"),
])
def test_los_fallos_de_red_se_reconocen(error):
    assert explicar(error).es_de_red


def test_un_defecto_de_programacion_no_se_atribuye_a_la_conexion():
    explicacion = explicar(TypeError("'NoneType' object is not subscriptable"))

    assert explicacion.tipo == "defecto"
    assert not explicacion.es_de_red


def test_las_cinco_familias_se_distinguen_entre_si():
    tipos = {
        explicar(ConnectionError("Connection refused")).tipo,
        explicar(Exception("42501: row-level security")).tipo,
        explicar(Exception("JWT expired")).tipo,
        explicar(Exception('No hay ejemplares disponibles de "x".')).tipo,
        explicar(TypeError("x")).tipo,
    }
    assert len(tipos) == 5
