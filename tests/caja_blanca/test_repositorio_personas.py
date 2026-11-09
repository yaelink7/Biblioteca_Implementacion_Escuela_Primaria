"""Caja blanca · repositorio del padrón y de la plantilla.

Equivale a `UsuarioDao` y `EmpleadoDao` del sistema Java (casos TC-18 y TC-11
a TC-13 de la matriz), con una diferencia de fondo: allá cada alta era una
escritura a un archivo, y aquí los datos de una persona viven en **dos
tablas** —`perfiles` más `usuarios` o `empleados`—.

Eso es lo que estas pruebas vigilan. El Corolario 3 del archivo de contexto
dice que esas dos tablas nunca se escriben con dos llamadas separadas desde
Python, porque si la segunda falla queda un registro a medias. Ya pasó dos
veces: en el alta (PR #53) y en la modificación (PR #55). La garantía está en
que se llama a una función de Postgres, que las agrupa en una transacción.

Una prueba de caja negra no puede ver esa diferencia: desde fuera, guardar
bien y guardar a medias se parecen hasta que algo falla. Por eso estas
pruebas comprueban **qué se llamó**, no solo qué devolvió.
"""

from __future__ import annotations

import pytest

from biblioteca.modelos.persona import Alumno, Empleado, Perfil, Rol
from biblioteca.repositorios import personas
from biblioteca.repositorios.personas import ErrorDePersona
from tests.conftest import ClienteFalso, ConsultaFalsa, RespuestaFalsa


class ConsultaEnSecuencia(ConsultaFalsa):
    """Una respuesta distinta en cada `execute()`, en el orden en que se piden.

    `buscar_alumnos` hace dos consultas —nombre y código en `perfiles`, CURP
    en `usuarios`— y el doble común les contesta lo mismo a las dos, así que
    no deja ver qué pasa cuando un alumno aparece solo por su CURP.
    """

    def __init__(self, *respuestas):
        super().__init__()
        self.pendientes = list(respuestas)

    def execute(self):
        self.llamadas.append(("execute", (), {}))
        return RespuestaFalsa(self.pendientes.pop(0))


def instalar_en_secuencia(monkeypatch, *respuestas) -> ClienteFalso:
    cliente = ClienteFalso(ConsultaEnSecuencia(*respuestas))
    monkeypatch.setattr(personas, "obtener_cliente", lambda: cliente)
    return cliente

# Fabricas y no constantes: `_aplanar` saca la tabla anidada con `fila.pop()`,
# de modo que consume el diccionario que recibe. Una fila compartida entre dos
# pruebas llega sin el anidado a la segunda. En produccion no importa —cada
# fila viene recien deserializada de la respuesta— pero aqui si, y conviene
# que quede visible: la funcion no es inocua con su argumento.

def fila_alumno(**cambios) -> dict:
    fila = {
        "id": "a-1", "codigo": "A-001", "nombre": "Ana", "apellido": "Martínez",
        "rol": "alumno", "activo": True, "telefono": "2281234567",
        "usuarios": {"grado": 4, "grupo": "B"},
    }
    fila.update(cambios)
    return fila


def fila_empleado(**cambios) -> dict:
    fila = {
        "id": "e-1", "codigo": "EMP-001", "nombre": "María",
        "apellido": "Hernández", "rol": "administrador", "activo": True,
        "correo": "bibliotecaria@demo.com",
        "empleados": {"tipo_empleado": "Bibliotecaria",
                      "fecha_ingreso": "2026-01-15"},
    }
    fila.update(cambios)
    return fila


# ===========================================================================
# listar_alumnos()
# ===========================================================================

def test_listar_alumnos_filtra_por_rol_y_por_activo(monkeypatch, cliente_falso):
    cliente = cliente_falso(monkeypatch, personas, respuesta=[fila_alumno()])

    resultado = personas.listar_alumnos()

    assert len(resultado) == 1
    assert resultado[0].salon == "4B", "no se aplanó la tabla anidada"
    filtros = cliente.consulta.argumentos_de("eq")
    assert ("rol", "alumno") in filtros
    assert ("activo", True) in filtros


def test_listar_alumnos_pide_la_tabla_anidada(monkeypatch, cliente_falso):
    """Grado, grupo y CURP viven en `usuarios`: sin el anidado no llegan."""
    cliente = cliente_falso(monkeypatch, personas, respuesta=[])

    personas.listar_alumnos()

    seleccion = cliente.consulta.argumentos_de("select")[0][0]
    assert "usuarios(grado, grupo, curp)" in seleccion


def test_listar_alumnos_trae_la_curp_al_modelo(monkeypatch, cliente_falso):
    fila = fila_alumno(usuarios={"grado": 4, "grupo": "B",
                                 "curp": "CURV200412MVZRMLA4"})
    cliente_falso(monkeypatch, personas, respuesta=[fila])

    assert personas.listar_alumnos()[0].curp == "CURV200412MVZRMLA4"


# ===========================================================================
# _aplanar() · las tres formas en que PostgREST devuelve el anidado
# ===========================================================================

class TestAplanar:
    """PostgREST devuelve el anidado como objeto, como lista o como nulo.

    Las tres aparecen según la relación y la consulta, y el código tiene una
    rama para cada una. Ninguna estaba probada.
    """

    def test_como_objeto(self):
        fila = {"codigo": "A-1", "usuarios": {"grado": 3, "grupo": "A"}}

        assert personas._aplanar(fila, "usuarios") == {
            "codigo": "A-1", "grado": 3, "grupo": "A"}

    def test_como_lista_de_un_elemento(self):
        fila = {"codigo": "A-1", "usuarios": [{"grado": 3, "grupo": "A"}]}

        assert personas._aplanar(fila, "usuarios")["grado"] == 3

    def test_como_lista_vacia(self):
        fila = {"codigo": "A-1", "usuarios": []}

        assert personas._aplanar(fila, "usuarios") == {"codigo": "A-1"}

    def test_como_nulo(self):
        """Un perfil sin ficha de alumno: la relación es opcional."""
        fila = {"codigo": "A-1", "usuarios": None}

        assert personas._aplanar(fila, "usuarios") == {"codigo": "A-1"}

    def test_cuando_la_clave_no_viene(self):
        assert personas._aplanar({"codigo": "A-1"}, "usuarios") == {"codigo": "A-1"}

    def test_el_anidado_se_saca_de_la_fila(self):
        """Si se quedara, `desde_fila` recibiría una clave que no es columna."""
        fila = {"codigo": "A-1", "usuarios": {"grado": 3}}

        assert "usuarios" not in personas._aplanar(fila, "usuarios")

    def test_la_fila_que_se_recibe_queda_consumida(self):
        """Lo saca con `pop`, así que modifica el diccionario del que llama.

        En la aplicación da igual: cada fila viene recién deserializada de la
        respuesta y se usa una sola vez. Queda anotado porque no es evidente
        al leer la llamada, y porque hizo fallar una prueba de este mismo
        archivo que reutilizaba una fila entre dos casos.
        """
        fila = {"codigo": "A-1", "usuarios": {"grado": 3}}

        personas._aplanar(fila, "usuarios")

        assert "usuarios" not in fila, (
            "si esto cambia, la función se volvió inocua y la nota de arriba "
            "sobra"
        )


# ===========================================================================
# buscar_alumnos()
# ===========================================================================

@pytest.mark.parametrize("texto", ["", "  "])
def test_buscar_alumnos_sin_texto_cae_en_listar(monkeypatch, cliente_falso, texto):
    cliente = cliente_falso(monkeypatch, personas, respuesta=[fila_alumno()])

    personas.buscar_alumnos(texto)

    assert "or_" not in cliente.consulta.nombres()


def test_buscar_alumnos_interroga_nombre_apellido_y_codigo(
    monkeypatch, cliente_falso
):
    cliente = cliente_falso(monkeypatch, personas, respuesta=[])

    personas.buscar_alumnos("ana")

    filtro = cliente.consulta.argumentos_de("or_")[0][0]
    assert filtro.count("ilike") == 3


def test_buscar_un_apellido_con_coma_no_parte_el_filtro(monkeypatch, cliente_falso):
    """«García, Ana» es como se captura un apellido en un cuaderno."""
    cliente = cliente_falso(monkeypatch, personas, respuesta=[])

    personas.buscar_alumnos("García, Ana")

    assert cliente.consulta.argumentos_de("or_")[0][0].count("ilike") == 3


# ===========================================================================
# buscar_alumnos() · la CURP, en una segunda consulta (USU-07)
# ===========================================================================

class TestBuscarPorCurp:
    """La CURP también encuentra al alumno, como en el prototipo.

    Vive en `usuarios`, y PostgREST no la puede mezclar en el mismo `.or_()`
    con las columnas de `perfiles`: va en una segunda consulta, y quien ya
    apareció por su nombre no se repite.
    """

    def _por_curp(self, **cambios):
        perfil = {"id": "a-2", "codigo": "A-002", "nombre": "Luis",
                  "apellido": "Bravo", "rol": "alumno", "activo": True}
        perfil.update(cambios)
        return {"grado": 2, "grupo": "A", "curp": "BALU180303HVZRSSA1",
                "perfiles": perfil}

    def test_la_curp_se_busca_en_usuarios(self, monkeypatch):
        cliente = instalar_en_secuencia(monkeypatch, [], [])

        personas.buscar_alumnos("vzr")

        assert cliente.tablas == ["perfiles", "usuarios"]
        assert ("curp", "%vzr%") in cliente.consulta.argumentos_de("ilike")

    def test_quien_aparece_solo_por_su_curp_llega_completo(self, monkeypatch):
        instalar_en_secuencia(monkeypatch, [], [self._por_curp()])

        resultado = personas.buscar_alumnos("BALU18")

        assert [a.codigo for a in resultado] == ["A-002"]
        assert resultado[0].curp == "BALU180303HVZRSSA1"
        assert resultado[0].salon == "2A"

    def test_quien_ya_aparecio_por_su_nombre_no_se_repite(self, monkeypatch):
        por_nombre = fila_alumno(id="a-2", codigo="A-002", nombre="Luis",
                                 apellido="Bravo")
        instalar_en_secuencia(monkeypatch, [por_nombre], [self._por_curp()])

        assert [a.id for a in personas.buscar_alumnos("Luis")] == ["a-2"]

    def test_los_que_llegan_por_curp_se_ordenan_con_los_demas(self, monkeypatch):
        """La base ordenó la primera consulta; la mezcla se ordena aquí."""
        por_nombre = fila_alumno(id="a-1", apellido="Martínez")
        instalar_en_secuencia(monkeypatch, [por_nombre], [self._por_curp()])

        apellidos = [a.apellido for a in personas.buscar_alumnos("a")]

        assert apellidos == ["Bravo", "Martínez"]

    def test_sin_alumnos_nuevos_queda_el_orden_de_la_base(self, monkeypatch):
        """No se reordena si la CURP no agregó a nadie: el orden ya es el de
        la consulta, y reordenar en Python podría contradecirla."""
        filas = [fila_alumno(id="a-9", apellido="Zúñiga"),
                 fila_alumno(id="a-1", apellido="Bravo")]
        instalar_en_secuencia(monkeypatch, filas, [])

        apellidos = [a.apellido for a in personas.buscar_alumnos("a")]

        assert apellidos == ["Zúñiga", "Bravo"]

    def test_un_alumno_dado_de_baja_no_aparece_por_su_curp(self, monkeypatch):
        """El mismo filtro que la búsqueda por salón: sin él, la CURP
        mostraría a quien su nombre ya no muestra."""
        instalar_en_secuencia(monkeypatch, [], [self._por_curp(activo=False)])

        assert personas.buscar_alumnos("BALU") == []


# ===========================================================================
# listar_maestros() y guardar_maestros() · el maestro de cada salón (USU-09)
# ===========================================================================

class TestMaestrosDeGrupo:
    """Se asigna una vez por salón y lo heredan sus alumnos.

    Al empezar otro ciclo escolar se corrige aquí, sin tocar la ficha de
    ningún niño. Un nombre vacío quita la asignación.
    """

    def _llamadas(self, cliente, nombre):
        return [(a, k) for n, a, k in cliente.consulta.llamadas if n == nombre]

    def test_listar_devuelve_el_maestro_de_cada_salon(self, monkeypatch, cliente_falso):
        cliente = cliente_falso(monkeypatch, personas, respuesta=[
            {"grado": 4, "grupo": "B", "maestro": "Mtro. Felipe Navarro"},
            {"grado": 1, "grupo": "A", "maestro": "Mtra. Laura Méndez"},
        ])

        maestros = personas.listar_maestros()

        assert maestros == {(4, "B"): "Mtro. Felipe Navarro",
                            (1, "A"): "Mtra. Laura Méndez"}
        assert cliente.tablas == ["maestros_de_grupo"]

    def test_sin_maestros_devuelve_un_diccionario_vacio(self, monkeypatch, cliente_falso):
        cliente_falso(monkeypatch, personas, respuesta=[])

        assert personas.listar_maestros() == {}

    def test_asignar_es_un_upsert_por_salon(self, monkeypatch, cliente_falso):
        """`on_conflict` por grado y grupo: guardar dos veces no duplica."""
        cliente = cliente_falso(monkeypatch, personas)

        personas.guardar_maestros({(4, "B"): "  Mtro. Felipe Navarro  "})

        [(argumentos, opciones)] = self._llamadas(cliente, "upsert")
        assert argumentos[0] == [{"grado": 4, "grupo": "B",
                                  "maestro": "Mtro. Felipe Navarro"}]
        assert opciones == {"on_conflict": "grado,grupo"}
        assert not self._llamadas(cliente, "delete")

    @pytest.mark.parametrize("vacio", ["", "   ", None])
    def test_un_nombre_vacio_quita_al_maestro_del_salon(
        self, monkeypatch, cliente_falso, vacio
    ):
        """La base rechaza un maestro en blanco: vacío significa quitarlo."""
        cliente = cliente_falso(monkeypatch, personas)

        personas.guardar_maestros({(6, "B"): vacio})

        assert not self._llamadas(cliente, "upsert")
        assert len(self._llamadas(cliente, "delete")) == 1
        filtros = cliente.consulta.argumentos_de("eq")
        assert ("grado", 6) in filtros
        assert ("grupo", "B") in filtros

    def test_asignar_y_quitar_en_una_sola_llamada(self, monkeypatch, cliente_falso):
        """Un upsert con todos los nombres, y un borrado por cada salón vacío."""
        cliente = cliente_falso(monkeypatch, personas)

        personas.guardar_maestros({(4, "B"): "Mtro. Felipe Navarro",
                                   (5, "A"): "Mtra. Irma Castillo",
                                   (6, "B"): ""})

        [(argumentos, _)] = self._llamadas(cliente, "upsert")
        assert len(argumentos[0]) == 2
        assert len(self._llamadas(cliente, "delete")) == 1
        assert cliente.tablas == ["maestros_de_grupo"] * 2

    def test_sin_cambios_no_toca_la_base(self, monkeypatch, cliente_falso):
        cliente = cliente_falso(monkeypatch, personas)

        personas.guardar_maestros({})

        assert cliente.tablas == []

    def test_el_rechazo_de_la_base_llega_traducido(self, monkeypatch, cliente_falso):
        cliente_falso(monkeypatch, personas, error=Exception(
            'new row for relation "maestros_de_grupo" violates check '
            'constraint "maestros_de_grupo_grado_check"'))

        with pytest.raises(ErrorDePersona, match="grado no existe"):
            personas.guardar_maestros({(7, "A"): "Alguien"})


# ===========================================================================
# buscar_alumnos_o_salon() · la bifurcación que decide el tipo de búsqueda
# ===========================================================================

class TestBuscarPorSalonOPorNombre:
    """El bibliotecario no elige el criterio: se deduce de lo que escribe.

    Lo pide `RNF-USA-01` —préstamo en menos de treinta segundos—, y es una
    expresión regular la que decide. Hay que recorrer sus dos salidas y los
    bordes de cada una.
    """

    @pytest.mark.parametrize("texto,grado,grupo", [
        ("4B", 4, "B"),
        ("4b", 4, "B"),      # se normaliza a mayúscula
        ("4 B", 4, "B"),     # con espacio en medio
        ("1A", 1, "A"),      # primer grado
        ("6F", 6, "F"),      # último grado
        ("  3C  ", 3, "C"),  # con espacios alrededor
    ])
    def test_lo_que_parece_salon_va_por_la_tabla_usuarios(
        self, monkeypatch, cliente_falso, texto, grado, grupo
    ):
        cliente = cliente_falso(monkeypatch, personas, respuesta=[])

        personas.buscar_alumnos_o_salon(texto)

        assert cliente.tablas == ["usuarios"]
        filtros = cliente.consulta.argumentos_de("eq")
        assert ("grado", grado) in filtros
        assert ("grupo", grupo) in filtros

    @pytest.mark.parametrize("texto", [
        "Ana",      # un nombre
        "A-001",    # un código
        "7B",       # grado que no existe en una primaria
        "0A",       # tampoco
        "44B",      # dos dígitos
        "4BB",      # dos letras
        "4",        # solo el grado
        "B",        # solo el grupo
    ])
    def test_lo_demas_va_por_la_busqueda_de_nombre(
        self, monkeypatch, cliente_falso, texto
    ):
        cliente = cliente_falso(monkeypatch, personas, respuesta=[])

        personas.buscar_alumnos_o_salon(texto)

        # Nombre y código se buscan en `perfiles`; la CURP, en `usuarios`.
        # Lo que no cambia: nunca se filtra por grado y grupo como un salón.
        assert cliente.tablas == ["perfiles", "usuarios"]
        filtrados = {columna for columna, _ in cliente.consulta.argumentos_de("eq")}
        assert not filtrados & {"grado", "grupo"}


# ===========================================================================
# alumnos_del_salon() · el filtro que se hace en Python, y por qué
# ===========================================================================

class TestAlumnosDelSalon:
    """El filtro de `activo` y `rol` se aplica aquí y no en la consulta.

    El `.eq()` de PostgREST sobre una tabla anidada recorta el anidado, no la
    fila padre, así que hay que filtrar después. Es el defecto que la
    auditoría encontró: teclear «4B» mostraba alumnos dados de baja que
    teclear su nombre no mostraba.
    """

    def _fila(self, **cambios):
        perfil = {"id": "a-1", "codigo": "A-001", "nombre": "Ana",
                  "apellido": "Martínez", "rol": "alumno", "activo": True}
        perfil.update(cambios)
        return {"grado": 4, "grupo": "B", "perfiles": perfil}

    def test_un_alumno_activo_aparece(self, monkeypatch, cliente_falso):
        cliente_falso(monkeypatch, personas, respuesta=[self._fila()])

        assert len(personas.alumnos_del_salon(4, "B")) == 1

    def test_un_alumno_dado_de_baja_no_aparece(self, monkeypatch, cliente_falso):
        cliente_falso(monkeypatch, personas, respuesta=[self._fila(activo=False)])

        assert personas.alumnos_del_salon(4, "B") == []

    def test_quien_no_es_alumno_no_aparece(self, monkeypatch, cliente_falso):
        """Un empleado con grado y grupo sería un dato raro, pero no imposible."""
        cliente_falso(monkeypatch, personas,
                      respuesta=[self._fila(rol="bibliotecario")])

        assert personas.alumnos_del_salon(4, "B") == []

    def test_una_fila_sin_perfil_no_revienta(self, monkeypatch, cliente_falso):
        """Pasa si RLS esconde el perfil pero deja ver la ficha."""
        cliente_falso(monkeypatch, personas,
                      respuesta=[{"grado": 4, "grupo": "B", "perfiles": None}])

        assert personas.alumnos_del_salon(4, "B") == []

    def test_se_ordenan_por_apellido(self, monkeypatch, cliente_falso):
        """La consulta no lleva `order`: el orden se pone aquí."""
        cliente_falso(monkeypatch, personas, respuesta=[
            self._fila(apellido="Zúñiga", codigo="A-9"),
            self._fila(apellido="Álvarez", codigo="A-1"),
            self._fila(apellido="Martínez", codigo="A-5"),
        ])

        apellidos = [a.apellido for a in personas.alumnos_del_salon(4, "B")]

        assert apellidos == sorted(apellidos)

    def test_el_grado_y_el_grupo_llegan_al_modelo(self, monkeypatch, cliente_falso):
        cliente_falso(monkeypatch, personas, respuesta=[self._fila()])

        assert personas.alumnos_del_salon(4, "B")[0].salon == "4B"


# ===========================================================================
# dar_de_alta_alumno() · la transacción del Corolario 3
# ===========================================================================

def test_el_alta_de_alumno_va_por_la_funcion_de_la_base(
    monkeypatch, cliente_falso, alumno_valido
):
    """Dos tablas, una llamada. Si fueran dos, quedaría un perfil huérfano."""
    cliente = cliente_falso(monkeypatch, personas, respuesta="a-nuevo")

    personas.dar_de_alta_alumno(alumno_valido)

    assert cliente.tablas == [], "se escribió una tabla directamente"
    assert [n for n, _ in cliente.rpc_llamadas] == ["registrar_alumno"]


def test_el_alta_de_alumno_manda_los_datos_de_las_dos_tablas(
    monkeypatch, cliente_falso, alumno_valido
):
    cliente = cliente_falso(monkeypatch, personas, respuesta="a-nuevo")

    personas.dar_de_alta_alumno(alumno_valido)

    _, parametros = cliente.rpc_llamadas[0]
    assert parametros["p_codigo"] == "A-001"       # va a perfiles
    assert parametros["p_grado"] == 4              # va a usuarios
    assert parametros["p_grupo"] == "B"


def test_el_alta_de_alumno_manda_la_curp(monkeypatch, cliente_falso, alumno_valido):
    cliente = cliente_falso(monkeypatch, personas, respuesta="a-nuevo")
    alumno_valido.curp = "CURV200412MVZRMLA4"

    personas.dar_de_alta_alumno(alumno_valido)

    assert cliente.rpc_llamadas[0][1]["p_curp"] == "CURV200412MVZRMLA4"


def test_el_alta_de_alumno_coincide_con_la_firma_de_la_migracion_11(
    monkeypatch, cliente_falso, alumno_valido
):
    """La lista está copiada de `11_datos_que_pidio_la_escuela.sql`.

    `p_curp` es el último parámetro y tiene valor por omisión, así que la
    base aceptaría una llamada sin él: la CURP se perdería en silencio. Por
    eso se comprueba aquí que la aplicación la manda.
    """
    cliente = cliente_falso(monkeypatch, personas, respuesta="a-nuevo")

    personas.dar_de_alta_alumno(alumno_valido)

    assert set(cliente.rpc_llamadas[0][1]) == {
        "p_codigo", "p_nombre", "p_apellido", "p_grado", "p_grupo", "p_correo",
        "p_telefono", "p_calle", "p_colonia", "p_codigo_postal", "p_numero",
        "p_curp",
    }


def test_la_curp_repetida_se_explica(monkeypatch, cliente_falso, alumno_valido):
    """Que no se repita lo decide la base: el validador no ve el padrón."""
    cliente_falso(
        monkeypatch, personas,
        error=Exception('duplicate key value violates unique constraint '
                        '"usuarios_curp_key"'),
    )

    with pytest.raises(ErrorDePersona, match="esa CURP"):
        personas.dar_de_alta_alumno(alumno_valido)


def test_el_alta_de_alumno_devuelve_el_id_que_asigno_la_base(
    monkeypatch, cliente_falso, alumno_valido
):
    cliente_falso(monkeypatch, personas, respuesta="a-nuevo")

    assert personas.dar_de_alta_alumno(alumno_valido).id == "a-nuevo"


def test_el_alta_de_alumno_traduce_el_codigo_repetido(
    monkeypatch, cliente_falso, alumno_valido
):
    cliente_falso(
        monkeypatch, personas,
        error=Exception('duplicate key value violates unique constraint '
                        '"perfiles_codigo_key"'),
    )

    with pytest.raises(ErrorDePersona, match="código"):
        personas.dar_de_alta_alumno(alumno_valido)


# ===========================================================================
# dar_de_alta_empleado()
# ===========================================================================

def test_el_alta_de_empleado_va_por_la_funcion_de_la_base(
    monkeypatch, cliente_falso, empleado_valido
):
    cliente = cliente_falso(monkeypatch, personas, respuesta="e-nuevo")

    personas.dar_de_alta_empleado(empleado_valido)

    assert cliente.tablas == []
    assert [n for n, _ in cliente.rpc_llamadas] == ["registrar_empleado"]


def test_el_alta_de_empleado_manda_el_perfil_de_acceso(
    monkeypatch, cliente_falso, empleado_valido
):
    """Quién puede conceder qué perfil lo decide la base, no esta capa.

    `registrar_empleado` rechaza `administrador` si quien llama no lo es. Si
    el rol se descartara aquí, la regla viviría en el cliente, donde cualquiera
    con la llave publishable podría saltarla.
    """
    cliente = cliente_falso(monkeypatch, personas, respuesta="e-nuevo")

    personas.dar_de_alta_empleado(empleado_valido)

    assert cliente.rpc_llamadas[0][1]["p_rol"] == "administrador"


def test_el_alta_de_empleado_traduce_la_escalada_rechazada(
    monkeypatch, cliente_falso, empleado_valido
):
    cliente_falso(
        monkeypatch, personas,
        error=Exception("Solo un administrador puede cambiar el perfil de acceso."),
    )

    with pytest.raises(ErrorDePersona, match="administrador"):
        personas.dar_de_alta_empleado(empleado_valido)


# ===========================================================================
# actualizar_alumno() · guarda del id y transacción
# ===========================================================================

def test_actualizar_un_alumno_sin_id_se_rechaza(
    monkeypatch, cliente_falso, alumno_valido
):
    cliente = cliente_falso(monkeypatch, personas)
    alumno_valido.id = None

    with pytest.raises(ErrorDePersona, match="identificador"):
        personas.actualizar_alumno(alumno_valido)

    assert cliente.rpc_llamadas == []


def test_actualizar_un_alumno_va_por_la_funcion_de_la_base(
    monkeypatch, cliente_falso, alumno_valido
):
    """La modificación a medias del PR #55, cerrada.

    Escribir `perfiles` y `usuarios` por separado dejaba los datos personales
    nuevos junto al grado y grupo viejos cuando la segunda fallaba.
    """
    cliente = cliente_falso(monkeypatch, personas)

    personas.actualizar_alumno(alumno_valido)

    assert cliente.tablas == []
    assert cliente.rpc_llamadas[0][0] == "actualizar_alumno"
    assert cliente.rpc_llamadas[0][1]["p_id"] == "a-1"


def test_actualizar_un_alumno_coincide_con_la_firma_de_la_migracion_11(
    monkeypatch, cliente_falso, alumno_valido
):
    """Como en el alta: sin `p_curp`, cambiar la CURP no guardaría nada."""
    cliente = cliente_falso(monkeypatch, personas)
    alumno_valido.curp = "CURV200412MVZRMLA4"

    personas.actualizar_alumno(alumno_valido)

    parametros = cliente.rpc_llamadas[0][1]
    assert set(parametros) == {
        "p_id", "p_nombre", "p_apellido", "p_grado", "p_grupo", "p_correo",
        "p_telefono", "p_calle", "p_colonia", "p_codigo_postal", "p_numero",
        "p_curp",
    }
    assert parametros["p_curp"] == "CURV200412MVZRMLA4"


def test_actualizar_un_alumno_traduce_el_no_encontrado(
    monkeypatch, cliente_falso, alumno_valido
):
    cliente_falso(monkeypatch, personas,
                  error=Exception("No se encontró el alumno indicado."))

    with pytest.raises(ErrorDePersona, match="padrón"):
        personas.actualizar_alumno(alumno_valido)


# ===========================================================================
# actualizar() · el perfil, con sus tres ramas
# ===========================================================================

def test_actualizar_un_perfil_sin_id_se_rechaza(monkeypatch, cliente_falso):
    cliente = cliente_falso(monkeypatch, personas)

    with pytest.raises(ErrorDePersona, match="identificador"):
        personas.actualizar(Perfil(codigo="P-1", nombre="A", apellido="B"))

    assert cliente.tablas == []


def test_actualizar_un_perfil_envia_el_rol(monkeypatch, cliente_falso, perfil_valido):
    """La línea cuya ausencia era la escalada de privilegios.

    Descartar el rol aquí ocultaba el rechazo del disparador `proteger_rol`:
    el formulario confirmaba y el perfil de acceso seguía siendo el anterior.
    """
    cliente = cliente_falso(monkeypatch, personas, respuesta=[{
        "id": "p-1", "codigo": "P-001", "nombre": "Juan", "apellido": "Pérez",
        "rol": "bibliotecario",
    }])
    perfil_valido.rol = Rol.BIBLIOTECARIO

    personas.actualizar(perfil_valido)

    assert cliente.consulta.argumentos_de("update")[0][0]["rol"] == "bibliotecario"


def test_actualizar_un_perfil_sin_respuesta_avisa(
    monkeypatch, cliente_falso, perfil_valido
):
    """Un id que ya no existe, o una fila invisible por RLS."""
    cliente_falso(monkeypatch, personas, respuesta=[])

    with pytest.raises(ErrorDePersona, match="Actualiza la pantalla"):
        personas.actualizar(perfil_valido)


def test_actualizar_un_perfil_traduce_el_rechazo_del_disparador(
    monkeypatch, cliente_falso, perfil_valido
):
    cliente_falso(
        monkeypatch, personas,
        error=Exception("No puedes cambiar tu propio perfil de acceso. "
                        "Pídelo a un administrador."),
    )

    with pytest.raises(ErrorDePersona, match="tu propio perfil"):
        personas.actualizar(perfil_valido)


# ===========================================================================
# actualizar_empleado() · lo que la migración 10 vino a arreglar
# ===========================================================================

def test_actualizar_un_empleado_sin_id_se_rechaza(
    monkeypatch, cliente_falso, empleado_valido
):
    cliente = cliente_falso(monkeypatch, personas)
    empleado_valido.id = None

    with pytest.raises(ErrorDePersona, match="identificador"):
        personas.actualizar_empleado(empleado_valido)

    assert cliente.rpc_llamadas == []


def test_el_puesto_del_empleado_si_se_envia(
    monkeypatch, cliente_falso, empleado_valido
):
    """El defecto que la auditoría encontró y la migración 10 cerró.

    `tipo_empleado` vive en la tabla `empleados` y la ruta anterior pasaba por
    `actualizar()`, que solo escribe `perfiles`: cambiar el puesto de un
    empleado **no guardaba nada** y el formulario confirmaba igual.
    """
    cliente = cliente_falso(monkeypatch, personas)
    empleado_valido.tipo_empleado = "Auxiliar"

    personas.actualizar_empleado(empleado_valido)

    assert cliente.rpc_llamadas[0][0] == "actualizar_empleado"
    assert cliente.rpc_llamadas[0][1]["p_tipo_empleado"] == "Auxiliar"


def test_los_parametros_coinciden_con_la_firma_de_la_migracion(
    monkeypatch, cliente_falso, empleado_valido
):
    """Si la función de la base cambia de firma, esto falla antes que la app.

    La lista está copiada de `database/migraciones/10_correcciones_de_la_
    auditoria.sql`. `actualizar_empleado` se declaró **sin valores por
    omisión**, así que mandar un parámetro de menos no es un dato faltante:
    es un error de «función no encontrada».
    """
    cliente = cliente_falso(monkeypatch, personas)

    personas.actualizar_empleado(empleado_valido)

    assert set(cliente.rpc_llamadas[0][1]) == {
        "p_id", "p_nombre", "p_apellido", "p_tipo_empleado", "p_rol",
        "p_correo", "p_telefono", "p_calle", "p_colonia",
    }


def test_actualizar_un_empleado_traduce_el_error_de_la_base(
    monkeypatch, cliente_falso, empleado_valido
):
    cliente_falso(monkeypatch, personas,
                  error=Exception("Un empleado no puede tener perfil de alumno."))

    with pytest.raises(ErrorDePersona, match="perfil de alumno"):
        personas.actualizar_empleado(empleado_valido)


# ===========================================================================
# listar_empleados()
# ===========================================================================

def test_listar_empleados_excluye_a_los_alumnos(monkeypatch, cliente_falso):
    """`neq` y no `eq`: el personal son dos perfiles distintos."""
    cliente = cliente_falso(monkeypatch, personas, respuesta=[fila_empleado()])

    resultado = personas.listar_empleados()

    assert resultado[0].tipo_empleado == "Bibliotecaria"
    assert ("rol", "alumno") in cliente.consulta.argumentos_de("neq")


def test_listar_empleados_aplana_la_ficha(monkeypatch, cliente_falso):
    cliente_falso(monkeypatch, personas, respuesta=[fila_empleado()])

    empleado = personas.listar_empleados()[0]

    assert empleado.fecha_ingreso is not None
    assert empleado.rol is Rol.ADMINISTRADOR


def test_sin_empleados_devuelve_una_lista_vacia(monkeypatch, cliente_falso):
    cliente_falso(monkeypatch, personas, respuesta=[])

    assert personas.listar_empleados() == []


# ===========================================================================
# Los tipos del padrón se respetan
# ===========================================================================

def test_un_alumno_se_registra_siempre_con_perfil_de_alumno(
    monkeypatch, cliente_falso
):
    """`registrar_alumno` no recibe rol: no hay forma de pedir otro.

    Es la mitad de la puerta que la migración 10 cerró; la otra mitad la
    cierra `perfiles_alta` en la base.
    """
    cliente = cliente_falso(monkeypatch, personas, respuesta="a-nuevo")

    personas.dar_de_alta_alumno(Alumno(codigo="A-9", nombre="Luis",
                                       apellido="Ramírez", telefono="2281234567"))

    assert "p_rol" not in cliente.rpc_llamadas[0][1]


def test_un_empleado_nuevo_sin_fecha_de_ingreso_no_rompe_el_alta(
    monkeypatch, cliente_falso
):
    cliente_falso(monkeypatch, personas, respuesta="e-nuevo")

    guardado = personas.dar_de_alta_empleado(
        Empleado(codigo="E-9", nombre="Luis", apellido="Ramírez",
                 correo="luis@demo.com", rol=Rol.BIBLIOTECARIO)
    )

    assert guardado.id == "e-nuevo"
