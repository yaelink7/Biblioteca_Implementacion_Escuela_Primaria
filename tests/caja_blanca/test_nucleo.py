"""Caja blanca · las ramas que quedaban sin recorrer en el núcleo.

Las pruebas de este archivo no salen de una regla del negocio: salen de leer
el código y buscar qué camino no había pasado nadie. Es la diferencia que el
informe de métricas del sistema Java señalaba —74 % de instrucciones contra
24 % de ramas— y que resumía así: las pruebas recorren el código, pero no lo
interrogan.

Cada clase de aquí cierra una rama concreta, y el comentario dice cuál.
"""

from __future__ import annotations

import pytest

from biblioteca.core import config
from biblioteca.core.errores import explicar, mensaje
from biblioteca.modelos.persona import Perfil
from biblioteca.modelos.prestamo import Prestamo, _salon
from biblioteca.servicios.validador_libro import Resultado


class ErrorDeCatalogo(Exception):
    """Homónima de la del repositorio: se reconoce por el nombre de la clase."""


# ===========================================================================
# errores.py · un error propio que envuelve algo irreconocible
# ===========================================================================

class TestErrorPropioConCausaDesconocida:
    """La rama que faltaba: el envoltorio se desenvuelve y tampoco se entiende.

    `explicar` intenta primero la causa original, porque es la que trae la
    señal. Si la causa tampoco se reconoce, debe quedarse con el texto del
    envoltorio: es el único mensaje escrito por nosotros que hay disponible.
    """

    def test_se_conserva_el_texto_del_envoltorio(self):
        envoltorio = ErrorDeCatalogo("No se pudo guardar el libro.")
        envoltorio.__cause__ = Exception("algo que nadie clasificó")

        explicacion = explicar(envoltorio)

        assert explicacion.tipo == "propio"
        assert explicacion.causa == "No se pudo guardar el libro."

    def test_y_aun_asi_dice_qué_hacer(self):
        """RNF-USA-03: ningún mensaje se queda en «falló» y nada más."""
        envoltorio = ErrorDeCatalogo("No se pudo guardar el libro.")
        envoltorio.__cause__ = Exception("algo que nadie clasificó")

        assert explicar(envoltorio).que_hacer

    def test_una_causa_reconocible_gana_sobre_el_envoltorio(self):
        """La otra mitad de la rama, para que la comparación quede completa."""
        envoltorio = ErrorDeCatalogo("No se pudo guardar el libro.")
        envoltorio.__cause__ = Exception('No hay ejemplares disponibles de "Momo".')

        assert explicar(envoltorio).tipo == "regla"

    def test_sin_causa_se_comporta_igual_que_con_una_desconocida(self):
        assert explicar(ErrorDeCatalogo("x")).tipo == "propio"

    def test_el_envoltorio_vacio_no_deja_el_dialogo_en_blanco(self):
        envoltorio = ErrorDeCatalogo()
        envoltorio.__cause__ = TypeError("otra cosa")

        assert mensaje(envoltorio).strip()


# ===========================================================================
# validador_libro.py · Resultado como valor de verdad
# ===========================================================================

class TestResultadoComoCondicion:
    """`__bool__` permite escribir `if not revision:` en las pantallas.

    Nadie lo usaba así en las pruebas, de modo que la línea existía sin que
    nada la ejerciera.
    """

    def test_un_resultado_sin_errores_es_verdadero(self):
        assert bool(Resultado()) is True
        assert Resultado()

    def test_un_resultado_con_errores_es_falso(self):
        assert bool(Resultado(errores=["algo"])) is False
        assert not Resultado(errores=["algo"])

    def test_sirve_dentro_de_un_if(self):
        if Resultado(errores=["algo"]):
            pytest.fail("un resultado con errores se evaluó como verdadero")


# ===========================================================================
# persona.py · auth_id en la fila
# ===========================================================================

class TestAuthIdEnLaFila:
    """Las dos ramas de `a_fila()`, que decide si incluir la columna.

    Un alumno tiene ficha sin cuenta —`auth_id` nulo— y un empleado la tiene
    siempre, porque inicia sesión. Mandar la columna en nulo no es lo mismo
    que no mandarla: la primera forma sobrescribiría un vínculo existente.
    """

    def test_con_cuenta_la_columna_viaja(self):
        perfil = Perfil(codigo="E-1", nombre="María", apellido="Hernández",
                        auth_id="auth-1")

        assert perfil.a_fila()["auth_id"] == "auth-1"

    def test_sin_cuenta_la_columna_no_viaja(self):
        perfil = Perfil(codigo="A-1", nombre="Ana", apellido="Martínez")

        assert "auth_id" not in perfil.a_fila()

    def test_el_id_sigue_la_misma_regla(self):
        con_id = Perfil(codigo="A-1", nombre="Ana", apellido="M", id="p-1")
        sin_id = Perfil(codigo="A-1", nombre="Ana", apellido="M")

        assert con_id.a_fila()["id"] == "p-1"
        assert "id" not in sin_id.a_fila()


# ===========================================================================
# prestamo.py · de dónde sale el salón
# ===========================================================================

class TestSalonDelPrestamo:
    """Tres ramas, porque las vistas no devuelven todas lo mismo.

    `v_prestamos` trae el salón ya armado; `v_deudores` trae grado y grupo por
    separado. La función cubre las dos, y el caso en que no llega ninguno.
    """

    def test_si_la_vista_ya_lo_trae_armado_se_usa_tal_cual(self):
        assert _salon({"salon": "4B"}) == "4B"

    def test_si_vienen_grado_y_grupo_se_arma(self):
        assert _salon({"grado": 4, "grupo": "B"}) == "4B"

    def test_el_armado_no_se_hace_a_medias(self):
        assert _salon({"grado": 4}) is None
        assert _salon({"grupo": "B"}) is None

    def test_sin_datos_queda_en_nulo(self):
        assert _salon({}) is None

    def test_el_salon_armado_tiene_prioridad(self):
        """Si llegaran los dos, manda el de la vista: es el que ella calculó."""
        assert _salon({"salon": "5C", "grado": 4, "grupo": "B"}) == "5C"

    def test_llega_hasta_el_modelo(self):
        fila = {"libro_id": 1, "usuario_id": "a-1", "grado": 3, "grupo": "A"}

        assert Prestamo.desde_fila(fila).salon == "3A"

    def test_el_titulo_admite_los_dos_nombres_de_columna(self):
        """`v_prestamos` lo llama `titulo_libro`; una consulta directa, `titulo`."""
        con_alias = {"libro_id": 1, "usuario_id": "a", "titulo_libro": "Momo"}
        sin_alias = {"libro_id": 1, "usuario_id": "a", "titulo": "Momo"}

        assert Prestamo.desde_fila(con_alias).titulo_libro == "Momo"
        assert Prestamo.desde_fila(sin_alias).titulo_libro == "Momo"


# ===========================================================================
# config.py · la rama que avisa de un .env incompleto
# ===========================================================================

class TestConfiguracionIncompleta:
    """El mensaje que recibe quien clona el repositorio y no tiene `.env`.

    Se prueba la funcion y no el import, porque `config.py` lee el entorno
    **al importarse**: una vez cargado en este proceso ya no vuelve a
    comprobar nada, y volver a importarlo con el entorno vacio no serviria
    tampoco, porque `load_dotenv` encontraria el `.env` real del equipo.

    Es la misma razon por la que esta suite necesita un `conftest.py` que
    ponga las variables antes de cualquier import, y lo que `QA-02` tenia
    anotado como obstaculo para probar los repositorios.
    """

    def test_una_variable_presente_se_devuelve(self, monkeypatch):
        monkeypatch.setenv("UNA_VARIABLE", "un valor")

        assert config._requerido("UNA_VARIABLE") == "un valor"

    def test_una_variable_que_falta_detiene_el_arranque(self, monkeypatch):
        monkeypatch.delenv("UNA_VARIABLE", raising=False)

        with pytest.raises(RuntimeError):
            config._requerido("UNA_VARIABLE")

    def test_una_variable_vacia_cuenta_como_faltante(self, monkeypatch):
        """Un `.env` con `SUPABASE_KEY=` es un `.env` a medio llenar."""
        monkeypatch.setenv("UNA_VARIABLE", "")

        with pytest.raises(RuntimeError):
            config._requerido("UNA_VARIABLE")

    @pytest.mark.parametrize("variable", ["SUPABASE_URL", "SUPABASE_KEY"])
    def test_el_mensaje_dice_cual_falta_y_que_hacer(self, monkeypatch, variable):
        """No basta con fallar: hay que decir que copiar y a quien pedirlo.

        Quien clona el repositorio no tiene forma de adivinar que la llave se
        le pide al Scrum Master.
        """
        monkeypatch.delenv(variable, raising=False)

        with pytest.raises(RuntimeError) as fallo:
            config._requerido(variable)

        aviso = str(fallo.value)
        assert variable in aviso
        assert ".env" in aviso
        assert "Scrum Master" in aviso

    def test_las_dos_reglas_del_negocio_siguen_donde_se_declararon(self):
        """REQ-PRE-01 y REQ-PRE-02, que la base aplica como reglas.

        Aqui solo sirven para redactar los avisos de la interfaz. Si alguien
        los cambia sin una migracion nueva, la pantalla diria una cosa y la
        base haria otra.
        """
        assert config.DIAS_DE_PRESTAMO == 7
        assert config.LIBROS_POR_USUARIO == 1
