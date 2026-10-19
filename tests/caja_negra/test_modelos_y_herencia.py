"""Caja negra · entidades del dominio y su conversión a fila.

Reúne los **grupos A.3 y A.4** de la matriz del sistema Java —casos TC-08 a
TC-13— y lo que allá era el grupo A.5.

| Matriz Java | Qué probaba | Equivalente aquí |
|---|---|---|
| TC-08, TC-09 | Los dos constructores de `Publicacion`, con y sin id | `id = None` mientras la base no lo asigne |
| TC-10 | `getPublicacion()` y `getAnoPublicacion()` devolvían el mismo atributo (**D-03**) | Un solo campo `ano_publicacion` |
| TC-11, TC-12 | `toStringUsuario()` de `Usuario` y de `Empleado` | `a_fila()` y `datos_propios()` |
| TC-13 | `Persona` sin identificador | `Perfil` con `id = None` |
| TC-14, TC-18 | Ida y vuelta por el archivo CSV | Ida y vuelta por el diccionario de la fila |

La ida y vuelta cambió de medio —antes un archivo, ahora una fila de
Postgres— pero la pregunta es la misma: lo que sale debe poder volver a
entrar sin perder nada por el camino.
"""

from __future__ import annotations

from datetime import date

import pytest

from biblioteca.modelos.libro import Libro
from biblioteca.modelos.persona import Alumno, Empleado, Perfil, Rol


# ===========================================================================
# TC-08, TC-09 · el identificador lo asigna la base
# ===========================================================================

def test_tc08_un_libro_recuperado_de_la_base_conserva_su_id():
    libro = Libro.desde_fila({
        "id": 10, "titulo": "Título", "autor": "Autor",
        "ano_publicacion": 2020, "existencias": 4,
    })

    assert libro.id == 10
    assert libro.existencias == 4


def test_tc09_un_libro_nuevo_nace_sin_id():
    """El Java usaba 0 como «todavía sin id»; aquí es `None`.

    Importa porque 0 es un id válido en una tabla y `None` no: la ambigüedad
    desaparece.
    """
    nuevo = Libro(titulo="Título", autor="Autor", ano_publicacion=2020, existencias=4)

    assert nuevo.id is None
    assert "id" not in nuevo.a_fila(), "el alta no debe mandar un id inventado"


def test_tc10_el_ano_de_publicacion_se_expone_una_sola_vez():
    """D-03: el original tenía dos getters del mismo atributo.

    Si alguien volviera a agregar un alias, esta prueba lo nota.
    """
    atributos = {a for a in dir(Libro) if "ublicacion" in a or "ano" in a}

    assert atributos == {"ano_publicacion"}


# ===========================================================================
# TC-13 · herencia de los datos personales
# ===========================================================================

def test_tc13_un_perfil_nuevo_nace_sin_identificador():
    perfil = Perfil(codigo="P-001", nombre="Juan", apellido="Pérez")

    assert perfil.id is None
    assert perfil.auth_id is None
    assert "id" not in perfil.a_fila()


def test_un_alumno_sin_cuenta_es_un_caso_valido(alumno_valido):
    """`auth_id` admite nulo a propósito: el niño tiene ficha, no cuenta.

    Es la diferencia con el sistema Java, donde toda persona era una cuenta.
    """
    alumno_valido.auth_id = None

    assert "auth_id" not in alumno_valido.a_fila()


@pytest.mark.parametrize("clase", [Alumno, Empleado])
def test_alumno_y_empleado_heredan_los_campos_del_perfil(clase):
    persona = clase(codigo="X-1", nombre="Ana", apellido="López")

    assert persona.nombre_completo == "Ana López"
    assert hasattr(persona, "telefono")
    assert isinstance(persona, Perfil)


def test_un_alumno_siempre_queda_con_perfil_de_alumno():
    """Aunque la fila diga otra cosa: es lo que cierra la escalada por el modelo."""
    alumno = Alumno(codigo="A-1", nombre="Ana", apellido="López",
                    rol=Rol.ADMINISTRADOR)

    assert alumno.rol is Rol.ALUMNO


def test_el_personal_se_distingue_del_alumno_por_el_perfil():
    assert Rol.ADMINISTRADOR.es_personal
    assert Rol.BIBLIOTECARIO.es_personal
    assert not Rol.ALUMNO.es_personal


# ===========================================================================
# TC-11, TC-12 · cada clase escribe lo suyo
# ===========================================================================

def test_tc11_el_alumno_aporta_grado_y_grupo(alumno_valido):
    assert alumno_valido.datos_propios() == {"grado": 4, "grupo": "B"}


def test_tc12_el_empleado_aporta_puesto_y_fecha_de_ingreso(empleado_valido):
    propios = empleado_valido.datos_propios()

    assert propios["tipo_empleado"] == "Bibliotecaria"
    assert propios["fecha_ingreso"] == "2026-01-15"


def test_un_empleado_sin_fecha_de_ingreso_no_manda_la_columna_en_nulo():
    """La columna es `not null`: mandarla vacía sería un rechazo seguro."""
    empleado = Empleado(codigo="E-1", nombre="Ana", apellido="López")

    assert "fecha_ingreso" not in empleado.datos_propios()


def test_los_datos_propios_no_repiten_los_del_perfil(alumno_valido, empleado_valido):
    """Son dos tablas: lo común va en `perfiles` y lo propio en la otra.

    Si un campo apareciera en las dos, una de las dos copias quedaría vieja.
    """
    comunes = set(alumno_valido.a_fila())

    assert comunes.isdisjoint(alumno_valido.datos_propios())
    assert comunes.isdisjoint(empleado_valido.datos_propios())


# ===========================================================================
# TC-14, TC-18 · ida y vuelta sin pérdida
# ===========================================================================

def test_tc14_un_libro_sobrevive_la_ida_y_vuelta(libro_valido):
    """Lo que el Java hacía contra un archivo CSV, aquí contra la fila."""
    regresado = Libro.desde_fila(libro_valido.a_fila())

    assert regresado == libro_valido


def test_tc18_un_alumno_sobrevive_la_ida_y_vuelta(alumno_valido):
    fila = alumno_valido.a_fila() | alumno_valido.datos_propios()

    regresado = Alumno.desde_fila(fila)

    assert regresado.nombre_completo == "Ana Sofía Martínez"
    assert regresado.telefono == "2281234567"
    assert regresado.salon == "4B"


def test_un_empleado_sobrevive_la_ida_y_vuelta(empleado_valido):
    fila = empleado_valido.a_fila() | empleado_valido.datos_propios()

    regresado = Empleado.desde_fila(fila)

    assert regresado == empleado_valido


class TestLoQueLlegaDeLaBase:
    """Las filas reales traen lo que traen: faltan claves y sobran otras."""

    def test_una_fila_sin_los_campos_opcionales_no_rompe(self):
        libro = Libro.desde_fila({"titulo": "Momo", "autor": "Ende"})

        assert libro.existencias == 0
        assert libro.activo is True
        assert libro.num_paginas is None

    def test_una_fila_sin_titulo_falla_de_inmediato(self):
        """Es columna `not null`: si falta, el error está arriba y debe verse."""
        with pytest.raises(KeyError):
            Libro.desde_fila({"autor": "Ende"})

    def test_la_marca_de_tiempo_de_la_baja_se_recorta_a_fecha(self):
        libro = Libro.desde_fila({
            "titulo": "Momo", "autor": "Ende",
            "dado_baja_en": "2026-09-22T18:45:03.221+00:00",
        })

        assert libro.dado_baja_en == date(2026, 9, 22)

    def test_sin_fecha_de_baja_queda_en_nulo(self):
        libro = Libro.desde_fila({"titulo": "Momo", "autor": "Ende",
                                  "dado_baja_en": None})

        assert libro.dado_baja_en is None

    def test_el_perfil_se_separa_de_los_datos_propios(self):
        """Las consultas traen las dos tablas en un solo diccionario."""
        alumno = Alumno.desde_fila({
            "id": "a-9", "codigo": "A-009", "nombre": "Luis",
            "apellido": "Ramírez", "rol": "alumno", "grado": 2, "grupo": "A",
        })

        assert alumno.grado == 2 and alumno.grupo == "A"
        assert alumno.codigo == "A-009"

    def test_el_puesto_tiene_valor_por_omision_si_la_fila_no_lo_trae(self):
        empleado = Empleado.desde_fila({
            "codigo": "E-9", "nombre": "Luis", "apellido": "Ramírez",
            "rol": "bibliotecario",
        })

        assert empleado.tipo_empleado == "Bibliotecario"
        assert empleado.rol is Rol.BIBLIOTECARIO


# ===========================================================================
# Campos derivados que se muestran en pantalla
# ===========================================================================

class TestSalon:
    """Lo que se escribe en la columna «Salón» del padrón."""

    def test_grado_y_grupo_se_juntan(self, alumno_valido):
        assert alumno_valido.salon == "4B"

    @pytest.mark.parametrize("grado,grupo", [
        (None, "B"), (4, None), (None, None), (4, ""),
    ])
    def test_si_falta_uno_de_los_dos_se_muestra_un_guion(self, grado, grupo):
        alumno = Alumno(codigo="A-1", nombre="Ana", apellido="López",
                        grado=grado, grupo=grupo)

        assert alumno.salon == "-"


class TestDireccion:
    """Los campos sueltos que venían del Java se arman en una línea."""

    def test_con_los_tres_campos(self):
        perfil = Perfil(codigo="P-1", nombre="A", apellido="B",
                        calle="Xalapeños Ilustres", numero=12, colonia="Centro")

        assert perfil.direccion == "Xalapeños Ilustres, 12, Centro"

    def test_los_campos_vacios_no_dejan_comas_sueltas(self):
        perfil = Perfil(codigo="P-1", nombre="A", apellido="B",
                        calle="Xalapeños Ilustres", colonia="Centro")

        assert perfil.direccion == "Xalapeños Ilustres, Centro"

    def test_sin_direccion_queda_vacia(self, perfil_valido):
        assert perfil_valido.direccion == ""


def test_el_codigo_postal_conserva_el_cero_a_la_izquierda():
    """Por esto es texto y no entero.

    El sistema Java lo guardaba numérico y «04600» se volvía 4600.
    """
    perfil = Perfil(codigo="P-1", nombre="A", apellido="B", codigo_postal="04600")

    assert perfil.a_fila()["codigo_postal"] == "04600"


def test_el_telefono_conserva_la_forma_en_que_se_capturo():
    """Mismo motivo: un teléfono no es una cantidad con la que se opere."""
    perfil = Perfil(codigo="P-1", nombre="A", apellido="B", telefono="228 123 4567")

    assert perfil.a_fila()["telefono"] == "228 123 4567"
