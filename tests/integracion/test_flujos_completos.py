"""Integración · los flujos completos, de la pantalla a la base.

Equivale al paquete **`ConsolaBiblia`** del sistema Java, que era un archivo
—`AltaLibroConsolaTest`, 9 pruebas— y la parte mejor probada del original:
88 % de instrucciones y 65 % de ramas, contra el 14 % de ramas de la capa
gráfica.

Conviene saber por qué. `AltaLibroConsola` **no era parte del sistema**: se
escribió para poder probarlo. La matriz de casos explicaba el problema —la
lógica del alta vivía dentro de un método privado de `GUILibro`, atada a los
componentes Swing y a los `JOptionPane`— y la consola fue el desvío: la misma
lógica reescrita sin ventanas, con el DAO sustituido por un doble. Se probaba
el desvío, no el camino que recorría el usuario.

Aquí no hay desvío. Estas pruebas recorren la cadena entera que se ejecuta en
la escuela —**formulario → validador → repositorio → cliente**— con un doble
solo en el último eslabón, el que saldría a la red. Lo que comprueban no es
cada pieza, que ya se prueba aparte, sino que las piezas estén conectadas:
que lo que se teclea llegue a la consulta, y que lo que la base responde
llegue a la pantalla.

Es la diferencia entre las otras tres carpetas y esta:

| Carpeta | Pregunta que responde |
|---|---|
| `caja_negra/` | ¿la regla es la que se declaró? |
| `caja_blanca/` | ¿se recorre cada rama del código? |
| `interfaz/` | ¿la pantalla muestra lo que recibe? |
| `integracion/` | ¿las piezas están conectadas entre sí? |
"""

from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from biblioteca.core import sesion as modulo_sesion  # noqa: E402
from biblioteca.modelos.persona import Rol  # noqa: E402
from biblioteca.repositorios import libros as repo_libros  # noqa: E402
from biblioteca.repositorios import personas as repo_personas  # noqa: E402
from biblioteca.repositorios import prestamos as repo_prestamos  # noqa: E402
from biblioteca.ui.catalogo import PantallaCatalogo  # noqa: E402
from biblioteca.ui.formulario_alumno import FormularioAlumno  # noqa: E402
from biblioteca.ui.formulario_libro import FormularioLibro  # noqa: E402
from biblioteca.ui.nuevo_prestamo import DialogoNuevoPrestamo  # noqa: E402
from biblioteca.ui.prestamos import PantallaPrestamos  # noqa: E402
from biblioteca.ui.ventana_principal import VentanaPrincipal  # noqa: E402

FILA_LIBRO = {
    "id": 7, "titulo": "El Quijote", "autor": "Cervantes",
    "tipo_libro": "Novela", "editorial": "Planeta", "existencias": 3,
    "ano_publicacion": 1605, "num_paginas": 863, "activo": True,
    "motivo_baja": None, "dado_baja_en": None,
}
FILA_ALUMNO = {
    "id": "a-1", "codigo": "A-001", "nombre": "Ana Sofía",
    "apellido": "Martínez", "rol": "alumno", "activo": True,
    "telefono": "2281234567", "grado": 4, "grupo": "B",
}
FILA_PRESTAMO = {
    "id": 1, "libro_id": 7, "usuario_id": "a-1",
    "fecha_prestamo": "2026-09-15", "fecha_limite": "2026-09-22",
    "estado": "activo", "dias_restantes": 3, "titulo_libro": "El Quijote",
    "nombre_alumno": "Ana Sofía Martínez", "salon": "4B",
}


@pytest.fixture(scope="session")
def app():
    aplicacion = QApplication.instance() or QApplication([])
    yield aplicacion
    aplicacion.processEvents()


@pytest.fixture
def sesion_abierta(app, monkeypatch):
    """Una sesión de administradora, como la que abre el login."""
    from biblioteca.core.sesion import Sesion
    from biblioteca.modelos.persona import Perfil

    sesion = Sesion(perfil=Perfil(
        id="e-1", codigo="EMP-001", nombre="María", apellido="Hernández",
        rol=Rol.ADMINISTRADOR, correo="bibliotecaria@demo.com"))
    monkeypatch.setattr(modulo_sesion, "_sesion_actual", sesion)
    return sesion


@pytest.fixture
def base(monkeypatch, cliente_falso):
    """Instala el mismo doble de cliente en los tres repositorios.

    Es el único eslabón sustituido: todo lo que está por encima —pantalla,
    validador, repositorio— es el código que corre en la escuela.
    """
    def instalar(respuesta=None, error=None):
        clientes = {}
        for modulo in (repo_libros, repo_personas, repo_prestamos):
            clientes[modulo.__name__] = cliente_falso(
                monkeypatch, modulo, respuesta=respuesta, error=error)
        return clientes
    return instalar


# ===========================================================================
# Alta de libro · los nueve casos de AltaLibroConsolaTest, sin la consola
# ===========================================================================

class TestAltaDeLibroDePrincipioAFin:
    """`AltaLibroConsolaTest` probaba estos casos contra una consola aparte.

    Aquí van contra el formulario que la bibliotecaria tiene enfrente, y
    atraviesan el validador y el repositorio hasta la consulta.
    """

    def llenar(self, formulario, titulo="El Quijote", autor="Cervantes",
               existencias=3, ano=1605, paginas=863):
        formulario.ui.campoTitulo.setText(titulo)
        formulario.ui.campoAutor.setText(autor)
        formulario.ui.campoTipo.setCurrentText("Novela")
        formulario.ui.campoEditorial.setText("Planeta")
        formulario.ui.campoExistencias.setValue(existencias)
        formulario.ui.campoAno.setValue(ano)
        formulario.ui.campoPaginas.setValue(paginas)
        return formulario

    def test_el_formulario_pide_los_siete_datos_del_libro(self, app):
        """`mainSolicitaLosSieteDatosDelLibro`, pero sobre la pantalla real."""
        formulario = FormularioLibro()

        for campo in ("campoTitulo", "campoAutor", "campoTipo",
                      "campoEditorial", "campoExistencias", "campoAno",
                      "campoPaginas"):
            assert hasattr(formulario.ui, campo), f"falta {campo}"

    def test_lo_capturado_llega_hasta_la_consulta(self, base, app):
        """La cadena completa: siete campos → validador → insert.

        Es la prueba que el sistema Java no podía hacer: su equivalente
        terminaba en un `LibroDaoFalso`, no en la consulta que se enviaría.
        """
        clientes = base(respuesta=[FILA_LIBRO])
        formulario = self.llenar(FormularioLibro())

        formulario.ui.botonGuardar.click()

        cliente = clientes["biblioteca.repositorios.libros"]
        assert cliente.tablas == ["libros"]
        enviado = cliente.consulta.argumentos_de("insert")[0][0]
        assert enviado["titulo"] == "El Quijote"
        assert enviado["autor"] == "Cervantes"
        assert enviado["existencias"] == 3
        assert enviado["ano_publicacion"] == 1605
        assert enviado["num_paginas"] == 863
        assert "id" not in enviado

    def test_el_alta_valida_se_confirma_y_devuelve_el_libro(self, base, app):
        base(respuesta=[FILA_LIBRO])
        formulario = self.llenar(FormularioLibro())

        formulario.ui.botonGuardar.click()

        assert formulario.guardado is not None
        assert formulario.guardado.id == 7
        assert formulario.result() == formulario.DialogCode.Accepted

    def test_un_campo_vacio_no_llega_a_la_base(self, base, app):
        """`altaConCampoVacioNoLlamaAlDao`.

        El validador corta antes, de modo que no se gasta un viaje a la red
        para que Postgres rechace lo que ya se sabía inválido.
        """
        clientes = base(respuesta=[FILA_LIBRO])
        formulario = self.llenar(FormularioLibro(), titulo="")

        formulario.ui.botonGuardar.click()

        assert clientes["biblioteca.repositorios.libros"].tablas == []
        assert formulario.ui.etiquetaError.text()

    def test_las_existencias_en_cero_ya_no_pasan(self, base, app):
        """`existenciasEnCeroSeAceptanPorElDefectoConocido`, al revés.

        Aquella prueba documentaba D-06: el sistema Java aceptaba el registro.
        Aquí el caso se rechaza, así que la prueba que lo celebraba cambió de
        signo.
        """
        clientes = base(respuesta=[FILA_LIBRO])
        formulario = self.llenar(FormularioLibro(), existencias=0)

        formulario.ui.botonGuardar.click()

        assert clientes["biblioteca.repositorios.libros"].tablas == []
        assert "ejemplar" in formulario.ui.etiquetaError.text().lower()

    def test_el_ano_del_futuro_no_se_puede_ni_teclear(self, app):
        """`mainConAnoDeMasDeCuatroDigitosReportaLibroDelFuturo`, cerrado antes.

        El control topa en el año actual, así que D-08 no llega ni al
        validador.
        """
        from datetime import date

        formulario = FormularioLibro()
        formulario.ui.campoAno.setValue(9999)

        assert formulario.ui.campoAno.value() == date.today().year

    def test_un_libro_sin_ejemplares_no_nace_disponible(self, base, app):
        """`libroNuevoSeMarcaDisponiblePorElDefectoConocido`, también al revés.

        D-09 dejó de ser posible: no hay columna que fijar, la
        disponibilidad se deduce de las existencias.
        """
        base(respuesta=[FILA_LIBRO | {"existencias": 0}])
        formulario = self.llenar(FormularioLibro())

        formulario.ui.botonGuardar.click()

        assert formulario.guardado.disponible is False

    def test_lo_que_rechaza_la_base_llega_a_la_pantalla(self, base, app):
        """El eslabón que el doble del sistema Java no podía ejercitar.

        `LibroDaoFalso` solo guardaba el libro recibido: no tenía forma de
        rechazar nada, así que el camino del error quedaba sin recorrer.
        """
        base(error=Exception("El año de publicacion (3000) no puede ser futuro."))
        formulario = self.llenar(FormularioLibro())

        formulario.ui.botonGuardar.click()

        assert "futuro" in formulario.ui.etiquetaError.text().lower()
        assert formulario.guardado is None


# ===========================================================================
# Préstamo y devolución · el flujo que da sentido al sistema
# ===========================================================================

class TestPrestamoYDevolucion:
    """No tiene equivalente en el sistema Java: allá el préstamo no aplicaba
    ninguna regla, así que no había nada que recorrer."""

    def test_de_las_dos_busquedas_al_insert(self, base, sesion_abierta):
        """Dos búsquedas y un botón, y lo que sale son dos datos.

        El plazo y el movimiento de inventario los resuelven los disparadores:
        es la decisión que permite que la app móvil planeada herede las reglas
        sin reimplementarlas.
        """
        clientes = base(respuesta=[FILA_ALUMNO])
        clientes["biblioteca.repositorios.libros"].consulta.respuesta = [FILA_LIBRO]
        clientes["biblioteca.repositorios.prestamos"].consulta.respuesta = [
            FILA_PRESTAMO]

        dialogo = DialogoNuevoPrestamo()
        dialogo.ui.listaAlumnos.setCurrentRow(0)
        dialogo.ui.listaLibros.setCurrentRow(0)
        dialogo.ui.botonPrestar.click()

        cliente = clientes["biblioteca.repositorios.prestamos"]
        enviado = cliente.consulta.argumentos_de("insert")[0][0]
        assert enviado == {"libro_id": 7, "usuario_id": "a-1",
                           "registrado_por": "e-1"}
        assert dialogo.registrado

    def test_el_limite_de_un_libro_por_alumno_llega_explicado(
        self, base, sesion_abierta
    ):
        """La regla es un índice único parcial, a cuatro capas de la pantalla.

        El recorrido completo: índice → PostgREST → repositorio →
        `core/errores.py` → etiqueta. Antes de la auditoría se rompía en el
        traductor, cuyos patrones no coincidían con el texto real.
        """
        clientes = base(respuesta=[FILA_ALUMNO])
        clientes["biblioteca.repositorios.libros"].consulta.respuesta = [FILA_LIBRO]
        clientes["biblioteca.repositorios.prestamos"].consulta.error = Exception(
            'duplicate key value violates unique constraint '
            '"prestamo_unico_activo_por_usuario"')

        dialogo = DialogoNuevoPrestamo()
        dialogo.ui.listaAlumnos.setCurrentRow(0)
        dialogo.ui.listaLibros.setCurrentRow(0)
        dialogo.ui.botonPrestar.click()

        aviso = dialogo.ui.etiquetaError.text()
        assert "préstamo activo" in aviso
        assert "duplicate key" not in aviso
        assert not dialogo.registrado

    def test_la_falta_de_ejemplares_llega_explicada(self, base, sesion_abierta):
        """El disparador `mover_inventario` la aplica; aquí se lee su mensaje."""
        clientes = base(respuesta=[FILA_ALUMNO])
        clientes["biblioteca.repositorios.libros"].consulta.respuesta = [FILA_LIBRO]
        clientes["biblioteca.repositorios.prestamos"].consulta.error = Exception(
            'No hay ejemplares disponibles de "El Quijote".')

        dialogo = DialogoNuevoPrestamo()
        dialogo.ui.listaAlumnos.setCurrentRow(0)
        dialogo.ui.listaLibros.setCurrentRow(0)
        dialogo.ui.botonPrestar.click()

        assert "ejemplares" in dialogo.ui.etiquetaError.text().lower()

    def test_la_devolucion_solo_cambia_el_estado(self, base, sesion_abierta):
        """La fecha la sella la base, con el mismo reloj que calculó el plazo."""
        clientes = base(respuesta=[FILA_PRESTAMO])
        pantalla = PantallaPrestamos()
        pantalla.ui.tablaPrestamos.selectRow(0)

        cliente = clientes["biblioteca.repositorios.prestamos"]
        cliente.consulta.respuesta = [
            FILA_PRESTAMO | {"estado": "devuelto",
                             "fecha_devolucion": "2026-09-20"}]
        repo_prestamos.devolver(1)

        enviado = cliente.consulta.argumentos_de("update")[-1][0]
        assert enviado == {"estado": "devuelto"}

    def test_el_plazo_que_se_anuncia_es_el_que_la_base_aplica(
        self, base, sesion_abierta
    ):
        """Los dos extremos de la cadena tienen que decir lo mismo.

        El aviso de la pantalla sale de `DIAS_DE_PRESTAMO`; la fecha la
        calcula `calcular_fecha_limite`. Si alguien cambiara uno sin el otro,
        la pantalla mentiría, y es lo que esta prueba vigila.
        """
        from biblioteca.core.config import DIAS_DE_PRESTAMO

        clientes = base(respuesta=[FILA_ALUMNO])
        clientes["biblioteca.repositorios.libros"].consulta.respuesta = [FILA_LIBRO]

        dialogo = DialogoNuevoPrestamo()
        dialogo.ui.listaAlumnos.setCurrentRow(0)
        dialogo.ui.listaLibros.setCurrentRow(0)

        assert f"{DIAS_DE_PRESTAMO} días" in dialogo.ui.etiquetaPlazo.text()
        # Y lo que la base devolvio para ese mismo plazo:
        prestado = FILA_PRESTAMO["fecha_prestamo"]
        limite = FILA_PRESTAMO["fecha_limite"]
        from datetime import date
        assert (date.fromisoformat(limite) - date.fromisoformat(prestado)).days \
            == DIAS_DE_PRESTAMO


# ===========================================================================
# Alta de alumno · dos tablas, una transacción
# ===========================================================================

class TestAltaDeAlumnoDePrincipioAFin:
    def test_del_formulario_a_la_funcion_de_la_base(self, base, app):
        """Corolario 3: una sola llamada escribe las dos tablas.

        Dos llamadas separadas dejaban un perfil huérfano cuando la segunda
        fallaba. Ya pasó dos veces, en el alta y en la modificación.
        """
        clientes = base(respuesta="a-nuevo")
        formulario = FormularioAlumno()
        formulario.ui.campoCodigo.setText("A-009")
        formulario.ui.campoNombre.setText("Luis")
        formulario.ui.campoApellido.setText("Ramírez")
        formulario.ui.campoTelefono.setText("2281234567")
        formulario.ui.campoGrado.setValue(2)
        formulario.ui.campoGrupo.setCurrentText("A")

        formulario.ui.botonGuardar.click()

        cliente = clientes["biblioteca.repositorios.personas"]
        assert cliente.tablas == [], "se escribió una tabla por separado"
        nombre, parametros = cliente.rpc_llamadas[0]
        assert nombre == "registrar_alumno"
        assert parametros["p_codigo"] == "A-009"   # tabla perfiles
        assert parametros["p_grado"] == 2          # tabla usuarios
        assert parametros["p_grupo"] == "A"

    def test_el_codigo_repetido_llega_explicado(self, base, app):
        clientes = base(error=Exception(
            'duplicate key value violates unique constraint '
            '"perfiles_codigo_key"'))
        formulario = FormularioAlumno()
        formulario.ui.campoCodigo.setText("A-001")
        formulario.ui.campoNombre.setText("Luis")
        formulario.ui.campoApellido.setText("Ramírez")
        formulario.ui.campoTelefono.setText("2281234567")

        formulario.ui.botonGuardar.click()

        aviso = formulario.ui.etiquetaError.text()
        assert "ese código" in aviso
        assert "duplicate key" not in aviso
        assert clientes["biblioteca.repositorios.personas"].rpc_llamadas


# ===========================================================================
# La ventana completa
# ===========================================================================

class TestVentanaPrincipal:
    """Equivale a `VentanaManiTest`, que comprobaba cuatro cosas de la ventana.

    Aquí se comprueba además que las cinco pestañas se construyan contra la
    base: es el arranque real de la aplicación, y la prueba que falla si
    cualquiera de las nueve pantallas se rompe.
    """

    def test_la_ventana_abre_con_sus_cinco_pestanas(self, base, sesion_abierta):
        base(respuesta=[])

        ventana = VentanaPrincipal(sesion_abierta)

        assert ventana.pestanas.count() == 5
        titulos = [ventana.pestanas.tabText(i) for i in range(5)]
        assert titulos == ["Catálogo", "Préstamos", "Alumnos", "Deudores",
                           "Empleados"]

    def test_la_barra_dice_quien_esta_dentro(self, base, sesion_abierta):
        """El sistema Java abría directo en el menú sin validar quién entraba."""
        base(respuesta=[])

        ventana = VentanaPrincipal(sesion_abierta)

        assert "María Hernández" in ventana.sesion.saludo
        assert "Administrador" in ventana.sesion.saludo

    def test_la_ventana_tiene_titulo_y_tamano(self, base, sesion_abierta):
        base(respuesta=[])

        ventana = VentanaPrincipal(sesion_abierta)

        assert "Adalberto Tejeda" in ventana.windowTitle()
        assert ventana.width() > 0 and ventana.height() > 0

    def test_cerrar_la_ventana_cierra_la_sesion(self, base, sesion_abierta):
        """Lo contrario del sistema Java, donde cada ventana llevaba
        `EXIT_ON_CLOSE` y ninguna cerraba sesión porque no había sesión."""
        base(respuesta=[])
        ventana = VentanaPrincipal(sesion_abierta)

        ventana.close()

        assert modulo_sesion._sesion_actual is None

    def test_las_cinco_pestanas_cargan_sus_datos(self, base, sesion_abierta):
        """Un arranque con la base respondiendo: las nueve pantallas a la vez."""
        clientes = base(respuesta=[])

        VentanaPrincipal(sesion_abierta)

        consultadas = set()
        for cliente in clientes.values():
            consultadas.update(cliente.tablas)
        assert "libros" in consultadas
        assert "v_prestamos" in consultadas
        assert "v_deudores" in consultadas
        assert "perfiles" in consultadas


# ===========================================================================
# Que la búsqueda siga funcionando con los datos que la escuela captura
# ===========================================================================

@pytest.mark.parametrize("texto", [
    "García, Ana",          # la coma de un apellido capturado al estilo cuaderno
    "Momo, la niña",        # la coma de un título
    'El libro "raro"',      # comillas
    "Saint-Exupéry",        # acentos y guion
])
def test_un_texto_corriente_no_rompe_la_busqueda(base, app, texto):
    """El defecto de la auditoría, recorrido de extremo a extremo.

    Dentro de `or_` la coma separa condiciones de PostgREST, así que el texto
    se escapa en `core/consultas.py`. Como la búsqueda se dispara sola a los
    250 ms, el error salía mientras la persona seguía escribiendo.
    """
    clientes = base(respuesta=[FILA_LIBRO])
    catalogo = PantallaCatalogo()
    catalogo.ui.campoBusqueda.setText(texto)

    catalogo.recargar()

    cliente = clientes["biblioteca.repositorios.libros"]
    filtro = cliente.consulta.argumentos_de("or_")[0][0]
    assert filtro.count("ilike") == 3, "el texto partió el filtro en dos"
    assert catalogo.ui.tablaLibros.rowCount() == 1
