"""Caja negra · alta y modificación de personas.

El sistema Java no tenía estas reglas: capturaba a la persona y la guardaba.
La matriz de casos solo lo tocaba de refilón, en el grupo A.4, para comprobar
que la herencia copiaba los nueve atributos. Por eso aquí no hay números TC
que heredar: los casos salen de `REQ-USU-01` y `REQ-EMP-01`.

Era la pieza menos probada del proyecto —14 % de líneas antes de este
archivo—, y es la que decide qué datos de un menor de edad entran a la base.

Técnica: partición de equivalencia y valores límite sobre cada regla
declarada, más las combinaciones que la operación real produce.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from biblioteca.modelos.persona import Alumno, Empleado, Perfil
from biblioteca.servicios.validador_persona import (
    PATRON_CURP,
    validar_alumno,
    validar_empleado,
    validar_perfil,
)

MIGRACION_11 = (
    Path(__file__).resolve().parents[2]
    / "database" / "migraciones" / "11_datos_que_pidio_la_escuela.sql"
)


# ===========================================================================
# Reglas comunes a toda persona
# ===========================================================================

def test_camino_feliz_del_perfil(perfil_valido):
    assert validar_perfil(perfil_valido).es_valido


@pytest.mark.parametrize("campo,esperado", [
    ("codigo", "código"),
    ("nombre", "nombre"),
    ("apellido", "apellido"),
])
@pytest.mark.parametrize("valor", ["", "   ", "\t"])
def test_los_tres_campos_obligatorios(perfil_valido, campo, esperado, valor):
    setattr(perfil_valido, campo, valor)

    r = validar_perfil(perfil_valido)

    assert not r.es_valido
    assert any(esperado in e.lower() for e in r.errores)


def test_un_perfil_completamente_vacio_reporta_los_tres():
    r = validar_perfil(Perfil(codigo="", nombre="", apellido=""))

    assert len(r.errores) == 3


class TestCorreo:
    """El patrón es deliberadamente laxo: atrapa erratas, no valida dominios."""

    @pytest.mark.parametrize("correo", [
        "bibliotecaria@demo.com",
        "ana.lopez@escuela.edu.mx",
        "a@b.co",
        "nombre+etiqueta@dominio.org",
    ])
    def test_los_correos_corrientes_se_aceptan(self, perfil_valido, correo):
        perfil_valido.correo = correo
        assert validar_perfil(perfil_valido).es_valido

    @pytest.mark.parametrize("correo", [
        "sin-arroba.com",          # falta la arroba
        "sin@punto",               # falta el punto del dominio
        "dos@@arrobas.com",        # arroba repetida
        "con espacio@correo.com",  # espacio en medio
        "@solo-dominio.com",       # falta la parte local
        "falta-dominio@",          # falta el dominio
    ])
    def test_las_erratas_de_captura_se_rechazan(self, perfil_valido, correo):
        perfil_valido.correo = correo

        r = validar_perfil(perfil_valido)

        assert not r.es_valido
        assert any("correo" in e.lower() for e in r.errores)

    def test_sin_correo_el_perfil_sigue_siendo_valido(self, perfil_valido):
        """La escuela pidió quitarlo del alumno: no puede ser obligatorio aquí."""
        perfil_valido.correo = None
        assert validar_perfil(perfil_valido).es_valido

    def test_los_espacios_alrededor_no_invalidan_un_correo_bueno(self, perfil_valido):
        perfil_valido.correo = "  ana@escuela.mx  "
        assert validar_perfil(perfil_valido).es_valido


class TestTelefono:
    """Siete dígitos es el límite: un número local de Veracruz sin lada."""

    @pytest.mark.parametrize("telefono", [
        "2281234567",
        "228 123 4567",
        "(228) 123-4567",
        "+52 228 123 4567",
        "1234567",
    ])
    def test_cualquier_forma_de_capturarlo_se_acepta(self, perfil_valido, telefono):
        """Se cuentan los dígitos, no los caracteres: el formato es libre."""
        perfil_valido.telefono = telefono
        assert validar_perfil(perfil_valido).es_valido

    @pytest.mark.parametrize("telefono", ["123456", "12-34-56", "228", "x"])
    def test_menos_de_siete_digitos_se_rechaza(self, perfil_valido, telefono):
        perfil_valido.telefono = telefono

        r = validar_perfil(perfil_valido)

        assert not r.es_valido
        assert any("teléfono" in e.lower() for e in r.errores)

    def test_siete_digitos_es_el_minimo_que_pasa(self, perfil_valido):
        perfil_valido.telefono = "1234567"
        assert validar_perfil(perfil_valido).es_valido

    def test_seis_digitos_es_el_maximo_que_falla(self, perfil_valido):
        perfil_valido.telefono = "123456"
        assert not validar_perfil(perfil_valido).es_valido

    def test_sin_telefono_el_perfil_base_sigue_siendo_valido(self, perfil_valido):
        perfil_valido.telefono = None
        assert validar_perfil(perfil_valido).es_valido


# ===========================================================================
# Alumno · REQ-USU-01
# ===========================================================================

def test_camino_feliz_del_alumno(alumno_valido):
    assert validar_alumno(alumno_valido).es_valido


class TestGrado:
    """Una primaria tiene seis grados, y ese es todo el rango."""

    @pytest.mark.parametrize("grado", [1, 2, 3, 4, 5, 6])
    def test_los_seis_grados_se_aceptan(self, alumno_valido, grado):
        alumno_valido.grado = grado
        assert validar_alumno(alumno_valido).es_valido

    @pytest.mark.parametrize("grado", [0, 7, -1, 12, 99])
    def test_fuera_del_rango_se_rechaza(self, alumno_valido, grado):
        alumno_valido.grado = grado

        r = validar_alumno(alumno_valido)

        assert not r.es_valido
        assert any("grado" in e.lower() for e in r.errores)

    def test_sin_grado_ni_grupo_se_acepta(self, alumno_valido):
        """Un niño de nuevo ingreso puede entrar al padrón sin salón asignado."""
        alumno_valido.grado = None
        alumno_valido.grupo = None

        assert validar_alumno(alumno_valido).es_valido


class TestGrupo:
    @pytest.mark.parametrize("grupo", ["A", "B", "z", "C"])
    def test_una_sola_letra_se_acepta(self, alumno_valido, grupo):
        alumno_valido.grupo = grupo
        assert validar_alumno(alumno_valido).es_valido

    @pytest.mark.parametrize("grupo", ["AB", "1", "4B", "-", "ñ"])
    def test_cualquier_otra_cosa_se_rechaza(self, alumno_valido, grupo):
        alumno_valido.grupo = grupo

        r = validar_alumno(alumno_valido)

        assert not r.es_valido
        assert any("grupo" in e.lower() for e in r.errores)

    def test_los_espacios_alrededor_no_estorban(self, alumno_valido):
        alumno_valido.grupo = " B "
        assert validar_alumno(alumno_valido).es_valido


class TestGradoYGrupoVanJuntos:
    """La regla que la bibliotecaria encuentra en la práctica.

    Con grado pero sin grupo la búsqueda «por salón» de la Factibilidad
    Operativa no encuentra al alumno, así que media llave no se admite. Es lo
    que hace que elegir el grado y guardar sin tocar el grupo **no cierre el
    formulario**: aparece este mensaje, y es fácil pasarlo por alto.
    """

    def test_los_dos_puestos_se_acepta(self, alumno_valido):
        assert validar_alumno(alumno_valido).es_valido

    def test_ninguno_de_los_dos_se_acepta(self, alumno_valido):
        alumno_valido.grado, alumno_valido.grupo = None, None
        assert validar_alumno(alumno_valido).es_valido

    def test_grado_sin_grupo_se_rechaza(self, alumno_valido):
        alumno_valido.grupo = None

        r = validar_alumno(alumno_valido)

        assert not r.es_valido
        assert any("juntos" in e.lower() for e in r.errores)

    def test_grupo_sin_grado_se_rechaza(self, alumno_valido):
        alumno_valido.grado = None

        r = validar_alumno(alumno_valido)

        assert not r.es_valido
        assert any("juntos" in e.lower() for e in r.errores)

    def test_un_grupo_en_blanco_cuenta_como_no_puesto(self, alumno_valido):
        """Y entonces el grado queda solo, que es lo que se rechaza."""
        alumno_valido.grupo = ""

        assert not validar_alumno(alumno_valido).es_valido


class TestContactoDelTutor:
    """USU-08: el único contacto que cuenta es el teléfono del tutor.

    La escuela confirmó en la reunión que el correo no funciona con las
    familias, así que sin teléfono no hay forma de avisar de un préstamo
    vencido. Hasta la migración 11 bastaba con cualquiera de los dos.
    """

    def test_con_telefono_basta(self, alumno_valido):
        alumno_valido.correo = None
        assert validar_alumno(alumno_valido).es_valido

    def test_el_correo_ya_no_basta(self, alumno_valido):
        alumno_valido.telefono = None
        alumno_valido.correo = "tutor@escuela.mx"

        r = validar_alumno(alumno_valido)

        assert not r.es_valido
        assert any("teléfono del tutor" in e for e in r.errores)

    def test_sin_telefono_se_rechaza(self, alumno_valido):
        alumno_valido.telefono = None
        alumno_valido.correo = None

        r = validar_alumno(alumno_valido)

        assert not r.es_valido
        assert any("teléfono del tutor" in e for e in r.errores)

    def test_un_telefono_corto_falla_por_incompleto_y_no_por_faltante(
        self, alumno_valido
    ):
        """Está incompleto, y al estar incompleto no deja de contar como dado.

        La regla de obligatorio mira si el campo trae algo, no si es
        utilizable. Queda anotado: el aviso de teléfono incompleto es el que
        informa de verdad.
        """
        alumno_valido.correo = None
        alumno_valido.telefono = "228"

        r = validar_alumno(alumno_valido)

        assert not r.es_valido
        assert any("incompleto" in e.lower() for e in r.errores)
        assert not any("registra el teléfono" in e.lower() for e in r.errores)


class TestCurp:
    """USU-07: opcional, pero si se escribe tiene que ser una CURP de verdad.

    Que no se repita no lo puede saber el validador, que no ve el padrón: lo
    decide la base con `usuarios_curp_key` (ver test_repositorio_personas).
    """

    VALIDA = "CURV200412MVZRMLA4"   # el ejemplo del prototipo y del mensaje

    def test_sin_curp_pasa(self, alumno_valido):
        alumno_valido.curp = None
        assert validar_alumno(alumno_valido).es_valido

    def test_una_curp_valida_pasa(self, alumno_valido):
        alumno_valido.curp = self.VALIDA
        assert validar_alumno(alumno_valido).es_valido

    @pytest.mark.parametrize("curp", [
        "CURV200412MVZRMLA",     # 17 caracteres
        "CURV200412MVZRMLA45",   # 19
        "curv200412mvzrmla4",    # minúsculas: la base guarda mayúsculas
        "CURV201312MVZRMLA4",    # mes 13
        "CURV200432MVZRMLA4",    # día 32
        "CURV200412XVZRMLA4",    # sexo que no es H ni M
        "CURV200412MXXRMLA4",    # entidad que no existe
        "CURV200412MVZAMLA4",    # vocal donde va una consonante interna
        "C4RV200412MVZRMLA4",    # número donde va la vocal del apellido
    ])
    def test_otro_formato_se_rechaza_y_dice_cual_es(self, alumno_valido, curp):
        alumno_valido.curp = curp

        r = validar_alumno(alumno_valido)

        assert not r.es_valido
        assert any("formato oficial" in e and self.VALIDA in e for e in r.errores)

    def test_es_la_misma_regla_que_la_de_la_base(self):
        """La expresión se copió de `usuarios_curp_formato`. Si una cambia y la
        otra no, el validador deja pasar lo que la base rechaza, o al revés."""
        sql = MIGRACION_11.read_text(encoding="utf-8")
        cuerpo = re.search(
            r"usuarios_curp_formato check \(curp ~ \((.*?)\)\);", sql, re.S
        ).group(1)
        # Postgres une las cadenas contiguas: '...' '...' es una sola.
        de_la_base = "".join(re.findall(r"'([^']*)'", cuerpo))

        assert PATRON_CURP.pattern == de_la_base


def test_el_alumno_arrastra_las_reglas_del_perfil(alumno_valido):
    """Herencia: las reglas comunes no se reescriben, se heredan."""
    alumno_valido.nombre = ""
    alumno_valido.correo = "mal"

    r = validar_alumno(alumno_valido)

    assert any("nombre" in e.lower() for e in r.errores)
    assert any("correo" in e.lower() for e in r.errores)


def test_un_alumno_sin_nada_capturado_reporta_todo_de_una_vez():
    """Seis errores en una sola pasada, no uno por intento de guardar.

    El grado 9 produce dos: esta fuera de rango y, ademas, deja al grupo sin
    pareja.
    """
    r = validar_alumno(Alumno(codigo="", nombre="", apellido="", grado=9))

    assert len(r.errores) == 6
    assert r.mensaje.count("•") == 6


# ===========================================================================
# Empleado · REQ-EMP-01
# ===========================================================================

def test_camino_feliz_del_empleado(empleado_valido):
    assert validar_empleado(empleado_valido).es_valido


@pytest.mark.parametrize("tipo", ["", "   ", None])
def test_el_puesto_del_empleado_es_obligatorio(empleado_valido, tipo):
    empleado_valido.tipo_empleado = tipo

    r = validar_empleado(empleado_valido)

    assert not r.es_valido
    assert any("tipo de empleado" in e.lower() for e in r.errores)


def test_el_correo_del_empleado_si_es_obligatorio(empleado_valido):
    """A diferencia del alumno: Supabase Auth inicia sesión con el correo.

    Es la razón por la que la escuela pudo pedir quitarlo del niño pero no
    del personal.
    """
    empleado_valido.correo = None

    r = validar_empleado(empleado_valido)

    assert not r.es_valido
    assert any("inicia sesión" in e.lower() for e in r.errores)


def test_un_correo_mal_escrito_en_el_personal_se_rechaza(empleado_valido):
    empleado_valido.correo = "bibliotecaria.demo.com"

    assert not validar_empleado(empleado_valido).es_valido


def test_un_empleado_sin_nada_capturado_reporta_todo_de_una_vez():
    r = validar_empleado(Empleado(codigo="", nombre="", apellido="",
                                  tipo_empleado=""))

    assert len(r.errores) == 5


def test_el_empleado_no_arrastra_las_reglas_del_alumno(empleado_valido):
    """Grado y grupo no le aplican: no son campos suyos."""
    assert validar_empleado(empleado_valido).es_valido
    assert not hasattr(empleado_valido, "grado")
