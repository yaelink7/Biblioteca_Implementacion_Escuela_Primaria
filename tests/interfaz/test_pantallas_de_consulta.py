"""Interfaz · que las cinco pestañas muestren lo que la base les entrega.

Esto es lo que el paquete `GUIBiblia` del sistema Java **no** probaba. Sus 47
pruebas comprobaban que la ventana se construyera, que no fuera visible y que
la tabla tuviera nueve columnas; ninguna metía una fila y comprobaba qué
aparecía en pantalla. De ahí el 14 % de ramas que señalaba el informe de
métricas: las pruebas recorrían la capa gráfica sin interrogarla.

Aquí cada pantalla recibe datos de ejemplo y se comprueba la celda. También
el camino que ninguna prueba del original tocaba: **qué pasa cuando la
consulta falla**, que es el caso en que la bibliotecaria necesita entender
algo.
"""

from __future__ import annotations

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox

from biblioteca.repositorios import libros as repo_libros
from biblioteca.repositorios import personas as repo_personas
from biblioteca.repositorios import prestamos as repo_prestamos
from biblioteca.ui import alumnos as ui_alumnos
from biblioteca.ui import catalogo as ui_catalogo
from biblioteca.ui import deudores as ui_deudores
from biblioteca.ui import empleados as ui_empleados
from biblioteca.ui import prestamos as ui_prestamos
from biblioteca.ui.alumnos import PantallaAlumnos
from biblioteca.ui.catalogo import PantallaCatalogo
from biblioteca.ui.deudores import PantallaDeudores
from biblioteca.ui.empleados import PantallaEmpleados
from biblioteca.ui.prestamos import PantallaPrestamos


@pytest.fixture
def sin_avisos(monkeypatch):
    """Intercepta los cuadros de aviso y los anota.

    Un `QMessageBox.warning` de verdad bloquea la prueba esperando un clic,
    que es exactamente lo que impedía automatizar la capa gráfica del sistema
    Java: la matriz de casos anotaba que TC-19 a TC-30 no se podían ejecutar
    porque cada `JOptionPane` dejaba la suite colgada.
    """
    recibidos: list[tuple[str, str]] = []

    class CuadroFalso:
        StandardButton = QMessageBox.StandardButton
        Icon = QMessageBox.Icon

        @staticmethod
        def _anotar(_padre, titulo="", texto="", *args, **kwargs):
            recibidos.append((titulo, texto))
            return QMessageBox.StandardButton.Ok

        warning = information = critical = question = _anotar

    # Hay que sustituir el nombre que importa cada modulo, no el atributo de
    # la clase: `QMessageBox` es un tipo de Shiboken y asignarle un metodo
    # estatico no prende, de modo que el cuadro se abria de verdad y la suite
    # se quedaba esperando un clic. Es la misma razon por la que la matriz
    # del sistema Java anotaba que TC-19 a TC-30 no se podian automatizar.
    for modulo in (ui_catalogo, ui_prestamos, ui_alumnos, ui_deudores,
                   ui_empleados):
        monkeypatch.setattr(modulo, "QMessageBox", CuadroFalso)
    return recibidos


def textos(tabla, fila: int) -> list[str]:
    return [tabla.item(fila, c).text() for c in range(tabla.columnCount())]


# ===========================================================================
# Catálogo
# ===========================================================================

class TestCatalogo:
    def test_la_tabla_se_llena_con_lo_que_devuelve_la_base(
        self, sin_base, libros_de_ejemplo, con_sesion
    ):
        sin_base(repo_libros, listar=libros_de_ejemplo, buscar=[])

        catalogo = PantallaCatalogo()

        assert catalogo.ui.tablaLibros.rowCount() == 3
        assert textos(catalogo.ui.tablaLibros, 0)[:2] == [
            "El principito", "Saint-Exupéry"]

    def test_un_libro_agotado_lo_dice_en_la_columna_de_estado(
        self, sin_base, libros_de_ejemplo, con_sesion
    ):
        sin_base(repo_libros, listar=libros_de_ejemplo, buscar=[])

        catalogo = PantallaCatalogo()

        assert textos(catalogo.ui.tablaLibros, 1)[4] == "Sin ejemplares"

    def test_un_libro_dado_de_baja_muestra_su_motivo(
        self, sin_base, libros_de_ejemplo, con_sesion
    ):
        sin_base(repo_libros, listar=libros_de_ejemplo, buscar=[])

        catalogo = PantallaCatalogo()

        assert textos(catalogo.ui.tablaLibros, 2)[4] == "Baja: Extraviado"

    def test_lo_agotado_y_lo_dado_de_baja_se_marcan_en_rojo(
        self, sin_base, libros_de_ejemplo, con_sesion
    ):
        """Para que se distinga de un vistazo, sin leer cada fila."""
        sin_base(repo_libros, listar=libros_de_ejemplo, buscar=[])

        pantalla = PantallaCatalogo()
        tabla = pantalla.ui.tablaLibros

        assert tabla.item(1, 4).foreground().color() == Qt.GlobalColor.darkRed
        assert tabla.item(2, 4).foreground().color() == Qt.GlobalColor.darkRed

    def test_un_campo_sin_dato_muestra_una_raya_y_no_la_palabra_none(
        self, sin_base, libros_de_ejemplo, con_sesion
    ):
        sin_base(repo_libros, listar=libros_de_ejemplo, buscar=[])

        pantalla = PantallaCatalogo()
        fila = textos(pantalla.ui.tablaLibros, 2)

        assert fila[2] == "—"
        assert "None" not in fila

    def test_el_resumen_cuenta_titulos_ejemplares_y_disponibles(
        self, sin_base, libros_de_ejemplo, con_sesion
    ):
        """Es lo que reemplaza a contar las hojas del cuaderno."""
        sin_base(repo_libros, listar=libros_de_ejemplo, buscar=[])

        pantalla = PantallaCatalogo()
        resumen = pantalla.ui.etiquetaResumen.text()

        assert "3 títulos" in resumen
        assert "3 ejemplares" in resumen       # el de baja no cuenta
        assert "1 con disponibilidad" in resumen

    def test_la_casilla_de_bajas_cambia_la_consulta(
        self, sin_base, libros_de_ejemplo, con_sesion
    ):
        llamadas = sin_base(repo_libros, listar=libros_de_ejemplo, buscar=[])
        catalogo = PantallaCatalogo()

        catalogo.ui.casillaVerBajas.setChecked(True)

        argumentos = llamadas["biblioteca.repositorios.libros.listar"]
        assert argumentos[0][1] == {"incluir_bajas": False}
        assert argumentos[-1][1] == {"incluir_bajas": True}

    def test_escribir_en_la_busqueda_no_consulta_de_inmediato(
        self, sin_base, libros_de_ejemplo, con_sesion
    ):
        """Un temporizador de 250 ms evita una consulta por cada tecla.

        Sin él, teclear «principito» lanzaba once consultas.
        """
        llamadas = sin_base(repo_libros, listar=libros_de_ejemplo,
                            buscar=libros_de_ejemplo[:1])
        catalogo = PantallaCatalogo()

        catalogo.ui.campoBusqueda.setText("prin")

        assert llamadas["biblioteca.repositorios.libros.buscar"] == []
        assert catalogo._temporizador.isActive()

    def test_al_vencer_el_temporizador_si_se_busca(
        self, sin_base, libros_de_ejemplo, con_sesion
    ):
        llamadas = sin_base(repo_libros, listar=libros_de_ejemplo,
                            buscar=libros_de_ejemplo[:1])
        catalogo = PantallaCatalogo()
        catalogo.ui.campoBusqueda.setText("prin")

        catalogo.recargar()   # lo que hace el temporizador al disparar

        assert llamadas["biblioteca.repositorios.libros.buscar"][0][0] == ("prin",)
        assert catalogo.ui.tablaLibros.rowCount() == 1

    def test_con_busqueda_el_resumen_cuenta_resultados(
        self, sin_base, libros_de_ejemplo, con_sesion
    ):
        sin_base(repo_libros, listar=libros_de_ejemplo,
                 buscar=libros_de_ejemplo[:1])
        catalogo = PantallaCatalogo()
        catalogo.ui.campoBusqueda.setText("prin")
        catalogo.recargar()

        assert catalogo.ui.etiquetaResumen.text() == "1 resultado"

    def test_un_fallo_de_consulta_se_explica_sin_tirar_la_pantalla(
        self, sin_base, sin_avisos, con_sesion
    ):
        """El camino que el sistema Java no probaba nunca."""
        sin_base(repo_libros, listar=ConnectionError("Connection refused"),
                 buscar=[])

        catalogo = PantallaCatalogo()

        assert catalogo.ui.tablaLibros.rowCount() == 0
        titulo, texto = sin_avisos[0]
        assert "No se pudo consultar el catálogo" in titulo
        assert "conexión" in texto.lower()

    def test_un_catalogo_vacio_no_revienta(self, sin_base, con_sesion):
        sin_base(repo_libros, listar=[], buscar=[])

        catalogo = PantallaCatalogo()

        assert catalogo.ui.tablaLibros.rowCount() == 0
        assert "0 títulos" in catalogo.ui.etiquetaResumen.text()

    def test_seleccionar_una_fila_habilita_editar_y_dar_de_baja(
        self, sin_base, libros_de_ejemplo, con_sesion
    ):
        sin_base(repo_libros, listar=libros_de_ejemplo, buscar=[])
        catalogo = PantallaCatalogo()

        catalogo.ui.tablaLibros.selectRow(0)

        assert catalogo.ui.botonEditar.isEnabled()
        assert catalogo.ui.botonBaja.isEnabled()

    def test_un_libro_ya_dado_de_baja_no_se_puede_volver_a_dar_de_baja(
        self, sin_base, libros_de_ejemplo, con_sesion
    ):
        sin_base(repo_libros, listar=libros_de_ejemplo, buscar=[])
        catalogo = PantallaCatalogo()

        catalogo.ui.tablaLibros.selectRow(2)   # el de baja

        assert catalogo.ui.botonEditar.isEnabled()
        assert not catalogo.ui.botonBaja.isEnabled()


# ===========================================================================
# Préstamos
# ===========================================================================

class TestPrestamos:
    def test_la_tabla_se_llena_desde_la_vista(
        self, sin_base, prestamos_de_ejemplo, con_sesion
    ):
        sin_base(repo_prestamos, activos=prestamos_de_ejemplo)

        pantalla = PantallaPrestamos()

        assert pantalla.ui.tablaPrestamos.rowCount() == 2
        assert textos(pantalla.ui.tablaPrestamos, 0)[0] == "Ana Sofía Martínez"

    def test_la_fecha_se_muestra_en_formato_de_dia_mes_ano(
        self, sin_base, prestamos_de_ejemplo, con_sesion
    ):
        """Un `2026-09-22` no es lo que una maestra lee en un cuaderno."""
        sin_base(repo_prestamos, activos=prestamos_de_ejemplo)

        pantalla = PantallaPrestamos()
        assert textos(pantalla.ui.tablaPrestamos, 0)[3] == "22/09/2026"

    def test_la_situacion_dice_cuantos_dias_faltan_o_sobran(
        self, sin_base, prestamos_de_ejemplo, con_sesion
    ):
        """El número lo calcula la base; aquí solo se redacta la frase."""
        sin_base(repo_prestamos, activos=prestamos_de_ejemplo)

        pantalla = PantallaPrestamos()
        tabla = pantalla.ui.tablaPrestamos

        assert textos(tabla, 0)[4] == "Vence en 3 días"
        assert textos(tabla, 1)[4] == "Vencido hace 11 días"

    def test_lo_vencido_se_marca_en_rojo(
        self, sin_base, prestamos_de_ejemplo, con_sesion
    ):
        sin_base(repo_prestamos, activos=prestamos_de_ejemplo)

        pantalla = PantallaPrestamos()
        tabla = pantalla.ui.tablaPrestamos

        assert tabla.item(1, 4).foreground().color() == Qt.GlobalColor.darkRed

    def test_la_casilla_de_vencidos_filtra_sin_volver_a_consultar(
        self, sin_base, prestamos_de_ejemplo, con_sesion
    ):
        """Son pocos registros y ya están cargados: filtrar en memoria
        responde al instante."""
        llamadas = sin_base(repo_prestamos, activos=prestamos_de_ejemplo)
        pantalla = PantallaPrestamos()
        consultas = len(llamadas["biblioteca.repositorios.prestamos.activos"])

        pantalla.ui.casillaSoloVencidos.setChecked(True)

        assert pantalla.ui.tablaPrestamos.rowCount() == 1
        assert textos(pantalla.ui.tablaPrestamos, 0)[0] == "Luis Ramírez"
        assert len(llamadas["biblioteca.repositorios.prestamos.activos"]) == consultas

    def test_el_filtro_de_texto_busca_en_alumno_y_en_libro(
        self, sin_base, prestamos_de_ejemplo, con_sesion
    ):
        sin_base(repo_prestamos, activos=prestamos_de_ejemplo)
        pantalla = PantallaPrestamos()

        pantalla.ui.campoFiltro.setText("momo")
        assert pantalla.ui.tablaPrestamos.rowCount() == 1

        pantalla.ui.campoFiltro.setText("ana")
        assert pantalla.ui.tablaPrestamos.rowCount() == 1

        pantalla.ui.campoFiltro.setText("zzz")
        assert pantalla.ui.tablaPrestamos.rowCount() == 0

    def test_el_filtro_no_distingue_mayusculas(
        self, sin_base, prestamos_de_ejemplo, con_sesion
    ):
        sin_base(repo_prestamos, activos=prestamos_de_ejemplo)
        pantalla = PantallaPrestamos()

        pantalla.ui.campoFiltro.setText("MOMO")

        assert pantalla.ui.tablaPrestamos.rowCount() == 1

    def test_el_resumen_cuenta_los_vencidos(
        self, sin_base, prestamos_de_ejemplo, con_sesion
    ):
        sin_base(repo_prestamos, activos=prestamos_de_ejemplo)

        pantalla = PantallaPrestamos()
        resumen = pantalla.ui.etiquetaResumen.text()

        assert "2 préstamos activos" in resumen
        assert "1 vencido" in resumen

    def test_el_resumen_cuenta_sobre_el_total_y_no_sobre_lo_filtrado(
        self, sin_base, prestamos_de_ejemplo, con_sesion
    ):
        """Si contara lo visible, filtrar parecería haber devuelto libros."""
        sin_base(repo_prestamos, activos=prestamos_de_ejemplo)
        pantalla = PantallaPrestamos()

        pantalla.ui.casillaSoloVencidos.setChecked(True)

        assert "2 préstamos activos" in pantalla.ui.etiquetaResumen.text()

    def test_sin_prestamos_lo_dice_con_palabras(self, sin_base, con_sesion):
        sin_base(repo_prestamos, activos=[])

        pantalla = PantallaPrestamos()
        assert pantalla.ui.etiquetaResumen.text() == (
            "No hay préstamos activos.")

    def test_un_fallo_de_consulta_se_explica(self, sin_base, sin_avisos, con_sesion):
        sin_base(repo_prestamos, activos=ConnectionError("Connection refused"))

        pantalla = PantallaPrestamos()

        assert pantalla.ui.tablaPrestamos.rowCount() == 0
        assert "conexión" in sin_avisos[0][1].lower()

    def test_devolver_nace_apagado_hasta_que_haya_seleccion(
        self, sin_base, prestamos_de_ejemplo, con_sesion
    ):
        sin_base(repo_prestamos, activos=prestamos_de_ejemplo)
        pantalla = PantallaPrestamos()

        assert not pantalla.ui.botonDevolver.isEnabled()

        pantalla.ui.tablaPrestamos.selectRow(0)
        assert pantalla.ui.botonDevolver.isEnabled()


# ===========================================================================
# Alumnos
# ===========================================================================

class TestAlumnos:
    def test_el_padron_se_llena(self, sin_base, alumnos_de_ejemplo, con_sesion):
        sin_base(repo_personas, listar_alumnos=alumnos_de_ejemplo,
                 buscar_alumnos_o_salon=[])
        sin_base(repo_prestamos, activos=[])

        pantalla = PantallaAlumnos()

        assert pantalla.ui.tablaAlumnos.rowCount() == 2
        assert textos(pantalla.ui.tablaAlumnos, 0)[0] == "A-001"

    def test_el_salon_se_muestra_junto(
        self, sin_base, alumnos_de_ejemplo, con_sesion
    ):
        sin_base(repo_personas, listar_alumnos=alumnos_de_ejemplo,
                 buscar_alumnos_o_salon=[])
        sin_base(repo_prestamos, activos=[])

        pantalla = PantallaAlumnos()
        assert textos(pantalla.ui.tablaAlumnos, 0)[2] == "4B"

    def test_se_ve_quien_tiene_un_libro_prestado(
        self, sin_base, alumnos_de_ejemplo, prestamos_de_ejemplo, con_sesion
    ):
        """Responde al primer problema de la entrevista: no se sabía
        rápido quién tiene cada ejemplar."""
        sin_base(repo_personas, listar_alumnos=alumnos_de_ejemplo,
                 buscar_alumnos_o_salon=[])
        sin_base(repo_prestamos, activos=prestamos_de_ejemplo)

        pantalla = PantallaAlumnos()
        situaciones = [textos(pantalla.ui.tablaAlumnos, f)[4] for f in range(2)]

        assert any(s != "—" and s.strip() for s in situaciones)

    def test_la_busqueda_usa_la_funcion_que_deduce_el_criterio(
        self, sin_base, alumnos_de_ejemplo, con_sesion
    ):
        """Nombre, código o salón, sin que el bibliotecario elija antes.

        Lo pide `RNF-USA-01`: elegir el campo cuesta tiempo.
        """
        llamadas = sin_base(repo_personas, listar_alumnos=alumnos_de_ejemplo,
                            buscar_alumnos_o_salon=alumnos_de_ejemplo[:1])
        sin_base(repo_prestamos, activos=[])
        pantalla = PantallaAlumnos()

        pantalla.ui.campoBusqueda.setText("4B")
        pantalla.recargar()

        clave = "biblioteca.repositorios.personas.buscar_alumnos_o_salon"
        assert llamadas[clave][0][0] == ("4B",)

    def test_un_fallo_de_consulta_se_explica(self, sin_base, sin_avisos, con_sesion):
        sin_base(repo_personas,
                 listar_alumnos=ConnectionError("Connection refused"),
                 buscar_alumnos_o_salon=[])
        sin_base(repo_prestamos, activos=[])

        pantalla = PantallaAlumnos()

        assert pantalla.ui.tablaAlumnos.rowCount() == 0
        assert sin_avisos, "un fallo de red no avisó de nada"

    def test_los_botones_que_necesitan_alumno_nacen_apagados(
        self, sin_base, alumnos_de_ejemplo, con_sesion
    ):
        sin_base(repo_personas, listar_alumnos=alumnos_de_ejemplo,
                 buscar_alumnos_o_salon=[])
        sin_base(repo_prestamos, activos=[])

        pantalla = PantallaAlumnos()

        assert not pantalla.ui.botonEditar.isEnabled()
        assert not pantalla.ui.botonHistorial.isEnabled()

    def test_el_boton_de_editar_existe_como_pidio_la_escuela(
        self, sin_base, alumnos_de_ejemplo, con_sesion
    ):
        """La escuela lo pidió en la reunión y ya estaba: permite cambiar
        grado y grupo sin recapturar al niño cada ciclo."""
        sin_base(repo_personas, listar_alumnos=alumnos_de_ejemplo,
                 buscar_alumnos_o_salon=[])
        sin_base(repo_prestamos, activos=[])
        pantalla = PantallaAlumnos()

        pantalla.ui.tablaAlumnos.selectRow(0)

        assert pantalla.ui.botonEditar.isEnabled()


# ===========================================================================
# Deudores
# ===========================================================================

class TestDeudores:
    def test_el_reporte_abre_ya_generado(
        self, sin_base, deudores_de_ejemplo, con_sesion
    ):
        """Es el reemplazo del segundo problema de la entrevista: sacar la
        lista exigía revisar el cuaderno entero a mano."""
        sin_base(repo_prestamos, deudores=deudores_de_ejemplo)

        pantalla = PantallaDeudores()

        assert pantalla.ui.tablaDeudores.rowCount() == 1
        assert textos(pantalla.ui.tablaDeudores, 0)[0] == "Luis Ramírez"

    def test_trae_el_contacto_del_tutor(
        self, sin_base, deudores_de_ejemplo, con_sesion
    ):
        """Sin él, saber quién debe no sirve para avisarle a nadie."""
        sin_base(repo_prestamos, deudores=deudores_de_ejemplo)

        pantalla = PantallaDeudores()
        assert "2287654321" in textos(pantalla.ui.tablaDeudores, 0)[5]

    def test_el_retraso_se_muestra_en_dias(
        self, sin_base, deudores_de_ejemplo, con_sesion
    ):
        sin_base(repo_prestamos, deudores=deudores_de_ejemplo)

        pantalla = PantallaDeudores()
        assert textos(pantalla.ui.tablaDeudores, 0)[4] == "11 días"

    def test_los_totales_resumen_el_reporte(
        self, sin_base, deudores_de_ejemplo, con_sesion
    ):
        sin_base(repo_prestamos, deudores=deudores_de_ejemplo)

        pantalla = PantallaDeudores()

        assert "1" in pantalla.ui.etiquetaTotal.text()
        assert pantalla.ui.etiquetaGenerado.text().strip()

    def test_sin_deudores_el_reporte_lo_dice(self, sin_base, con_sesion):
        """El caso que la escuela querría."""
        sin_base(repo_prestamos, deudores=[])

        pantalla = PantallaDeudores()

        assert pantalla.ui.tablaDeudores.rowCount() == 0
        assert pantalla.ui.etiquetaTotal.text().strip()

    def test_el_filtro_de_salon_se_llena_con_los_salones_que_hay(
        self, sin_base, deudores_de_ejemplo, con_sesion
    ):
        sin_base(repo_prestamos, deudores=deudores_de_ejemplo)

        pantalla = PantallaDeudores()
        combo = pantalla.ui.campoSalon

        assert combo.count() >= 2          # "todos" más el salón 2A
        assert any("2A" in combo.itemText(i) for i in range(combo.count()))

    def test_un_fallo_de_consulta_se_explica(self, sin_base, sin_avisos, con_sesion):
        sin_base(repo_prestamos, deudores=ConnectionError("Connection refused"))

        pantalla = PantallaDeudores()

        assert pantalla.ui.tablaDeudores.rowCount() == 0
        assert sin_avisos


# ===========================================================================
# Empleados · es la pantalla que decide permisos
# ===========================================================================

class TestEmpleados:
    def test_la_plantilla_se_llena(
        self, sin_base, empleados_de_ejemplo, con_sesion
    ):
        sin_base(repo_personas, listar_empleados=empleados_de_ejemplo)

        pantalla = PantallaEmpleados()

        assert pantalla.ui.tablaEmpleados.rowCount() == 2
        assert textos(pantalla.ui.tablaEmpleados, 0)[1] == "María Hernández"

    def test_el_perfil_de_acceso_se_muestra_en_su_columna(
        self, sin_base, empleados_de_ejemplo, con_sesion
    ):
        sin_base(repo_personas, listar_empleados=empleados_de_ejemplo)

        pantalla = PantallaEmpleados()
        tabla = pantalla.ui.tablaEmpleados

        assert textos(tabla, 0)[4] == "Administrador"
        assert textos(tabla, 1)[4] == "Bibliotecario"

    def test_el_administrador_se_resalta(
        self, sin_base, empleados_de_ejemplo, con_sesion
    ):
        """Para que se vea cuántos hay sin contar fila por fila."""
        sin_base(repo_personas, listar_empleados=empleados_de_ejemplo)

        pantalla = PantallaEmpleados()
        tabla = pantalla.ui.tablaEmpleados

        assert tabla.item(0, 4).foreground().color() == Qt.GlobalColor.darkYellow

    def test_un_empleado_sin_correo_se_marca(self, sin_base, con_sesion):
        """Sin correo no puede iniciar sesión: es un dato que falta, no un
        campo opcional."""
        from biblioteca.modelos.persona import Empleado, Rol

        sin_base(repo_personas, listar_empleados=[
            Empleado(id="e-3", codigo="EMP-003", nombre="Sin",
                     apellido="Correo", tipo_empleado="Auxiliar",
                     rol=Rol.BIBLIOTECARIO)])

        pantalla = PantallaEmpleados()
        tabla = pantalla.ui.tablaEmpleados

        assert textos(tabla, 0)[3] == "Sin correo"
        assert tabla.item(0, 3).foreground().color() == Qt.GlobalColor.darkRed

    def test_la_administradora_lee_que_puede_cambiar_perfiles(
        self, sin_base, empleados_de_ejemplo, con_sesion
    ):
        """Se dice de entrada, en vez de dejar que lo descubra al fallar."""
        sin_base(repo_personas, listar_empleados=empleados_de_ejemplo)

        pantalla = PantallaEmpleados()
        aviso = pantalla.ui.etiquetaAviso.text()

        assert "perfil de acceso" in aviso
        assert "administrador" in aviso.lower()

    def test_el_bibliotecario_lee_que_eso_le_queda_reservado(
        self, sin_base, empleados_de_ejemplo, sesion_de_bibliotecario, monkeypatch
    ):
        from biblioteca.core import sesion as modulo_sesion

        monkeypatch.setattr(modulo_sesion, "_sesion_actual",
                            sesion_de_bibliotecario)
        sin_base(repo_personas, listar_empleados=empleados_de_ejemplo)

        pantalla = PantallaEmpleados()
        aviso = pantalla.ui.etiquetaAviso.text()

        assert "reservado al administrador" in aviso

    def test_el_bibliotecario_si_puede_registrar_personal(
        self, sin_base, empleados_de_ejemplo, sesion_de_bibliotecario, monkeypatch
    ):
        """REQ-EMP-01. En una primaria la biblioteca la atiende una sola
        persona: exigir un segundo perfil para registrar a un auxiliar la
        dejaba bloqueada."""
        from biblioteca.core import sesion as modulo_sesion

        monkeypatch.setattr(modulo_sesion, "_sesion_actual",
                            sesion_de_bibliotecario)
        sin_base(repo_personas, listar_empleados=empleados_de_ejemplo)

        pantalla = PantallaEmpleados()
        assert pantalla.ui.botonNuevo.isEnabled()

    def test_un_fallo_de_consulta_se_explica(self, sin_base, sin_avisos, con_sesion):
        sin_base(repo_personas,
                 listar_empleados=ConnectionError("Connection refused"))

        pantalla = PantallaEmpleados()

        assert pantalla.ui.tablaEmpleados.rowCount() == 0
        assert sin_avisos
