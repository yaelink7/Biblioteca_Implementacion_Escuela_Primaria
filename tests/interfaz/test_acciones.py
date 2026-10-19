"""Interfaz · los botones que abren un diálogo y lo que pasa al volver.

Son los caminos que ninguna prueba del sistema Java recorría, y por una razón
concreta: cada uno abre una ventana modal, y una ventana modal deja la suite
esperando un clic que nadie va a dar. La matriz de casos lo anotaba como el
motivo por el que TC-19 a TC-30 quedaban sin ejecutar, y el informe de
métricas lo medía: 14 % de ramas en `GUIBiblia`.

Aquí el diálogo se sustituye por un doble que contesta de inmediato lo que la
prueba quiera —aceptado, cancelado, o aceptado sin guardar nada— y así se
puede recorrer lo que ocurre **después** de cerrarlo, que es donde está la
lógica: recargar la tabla, limpiar la búsqueda, avisar, o no hacer nada.

Cada caso cubre las tres salidas de un mismo botón:

| Salida | Qué debe pasar |
|---|---|
| Aceptado y guardado | se recarga y se avisa |
| Cancelado | no se recarga ni se avisa |
| Aceptado sin guardar | tampoco, aunque el diálogo diga que sí |
"""

from __future__ import annotations

import pytest
from PySide6.QtWidgets import QDialog, QMessageBox

from biblioteca.repositorios import libros as repo_libros
from biblioteca.repositorios import personas as repo_personas
from biblioteca.repositorios import prestamos as repo_prestamos
from biblioteca.ui import alumnos as ui_alumnos
from biblioteca.ui import catalogo as ui_catalogo
from biblioteca.ui import empleados as ui_empleados
from biblioteca.ui import prestamos as ui_prestamos
from biblioteca.ui.alumnos import PantallaAlumnos
from biblioteca.ui.catalogo import PantallaCatalogo
from biblioteca.ui.deudores import CeldaDeRetraso, PantallaDeudores
from biblioteca.ui.empleados import PantallaEmpleados
from biblioteca.ui.historial_alumno import DialogoHistorial
from biblioteca.ui.prestamos import PantallaPrestamos

ACEPTADO = QDialog.DialogCode.Accepted
CANCELADO = QDialog.DialogCode.Rejected


class DialogoFalso:
    """Doble de un diálogo modal: contesta sin abrirse.

    `exec()` es lo único que hacía falta interceptar. Todo lo demás —qué se
    guardó, si se registró el préstamo— son los atributos que la pantalla lee
    al volver.
    """

    def __init__(self, resultado=ACEPTADO, **atributos):
        self.resultado = resultado
        self.aperturas = 0
        self.recibido: dict = {}
        for nombre, valor in atributos.items():
            setattr(self, nombre, valor)

    def exec(self):
        self.aperturas += 1
        return self.resultado


@pytest.fixture
def dialogo_falso(monkeypatch):
    """Sustituye la clase del diálogo en el módulo de la pantalla."""
    def instalar(modulo, nombre, doble):
        def fabricar(*args, **kwargs):
            doble.recibido = {"posicionales": args, "nombrados": kwargs}
            return doble
        monkeypatch.setattr(modulo, nombre, fabricar)
        return doble
    return instalar


@pytest.fixture
def respuestas(monkeypatch):
    """Doble de `QMessageBox` y `QInputDialog` para las pantallas.

    Se sustituye el nombre que importa cada módulo, no el atributo de la
    clase: `QMessageBox` es un tipo de Shiboken y asignarle un método estático
    no prende, de modo que el cuadro se abriría de verdad.
    """
    avisos: list[tuple[str, str]] = []

    def instalar(modulo, *, confirma=True, texto=None, acepta=True):
        class CuadroFalso:
            StandardButton = QMessageBox.StandardButton

            @staticmethod
            def _anotar(_padre, titulo="", mensaje="", *args, **kwargs):
                avisos.append((titulo, mensaje))
                return (QMessageBox.StandardButton.Yes if confirma
                        else QMessageBox.StandardButton.No)

            warning = information = critical = question = _anotar

        class EntradaFalsa:
            @staticmethod
            def getText(_padre, titulo="", etiqueta="", *args, **kwargs):
                avisos.append((titulo, etiqueta))
                return (texto if texto is not None else ""), acepta

        monkeypatch.setattr(modulo, "QMessageBox", CuadroFalso)
        if hasattr(modulo, "QInputDialog"):
            monkeypatch.setattr(modulo, "QInputDialog", EntradaFalsa)
        return avisos

    instalar.avisos = avisos
    return instalar


# ===========================================================================
# Catálogo · registrar, modificar, dar de baja
# ===========================================================================

class TestAccionesDelCatalogo:
    @pytest.fixture
    def catalogo(self, sin_base, con_sesion, libros_de_ejemplo):
        self.llamadas = sin_base(repo_libros, listar=libros_de_ejemplo,
                                 buscar=libros_de_ejemplo[:1],
                                 dar_de_baja=None)
        return PantallaCatalogo()

    def consultas(self) -> int:
        return len(self.llamadas["biblioteca.repositorios.libros.listar"])

    # --- registrar ---
    def test_registrar_abre_el_formulario_y_recarga(
        self, catalogo, dialogo_falso, libros_de_ejemplo
    ):
        doble = dialogo_falso(ui_catalogo, "FormularioLibro",
                              DialogoFalso(guardado=libros_de_ejemplo[0]))
        antes = self.consultas()

        catalogo.ui.botonNuevo.click()

        assert doble.aperturas == 1
        assert self.consultas() == antes + 1
        assert "Se registró" in catalogo.ui.etiquetaResumen.text()

    def test_registrar_limpia_la_busqueda(
        self, catalogo, dialogo_falso, libros_de_ejemplo
    ):
        """Si no se limpiara, el libro recién dado de alta podría no aparecer
        en la lista filtrada y parecería no haberse guardado."""
        dialogo_falso(ui_catalogo, "FormularioLibro",
                      DialogoFalso(guardado=libros_de_ejemplo[0]))
        catalogo.ui.campoBusqueda.setText("zzz")

        catalogo.ui.botonNuevo.click()

        assert catalogo.ui.campoBusqueda.text() == ""

    def test_cancelar_el_alta_no_recarga_ni_avisa(self, catalogo, dialogo_falso):
        dialogo_falso(ui_catalogo, "FormularioLibro",
                      DialogoFalso(CANCELADO, guardado=None))
        antes = self.consultas()
        resumen = catalogo.ui.etiquetaResumen.text()

        catalogo.ui.botonNuevo.click()

        assert self.consultas() == antes
        assert catalogo.ui.etiquetaResumen.text() == resumen

    def test_aceptar_sin_guardar_tampoco_recarga(self, catalogo, dialogo_falso):
        """El diálogo puede cerrarse en aceptado sin haber guardado nada."""
        dialogo_falso(ui_catalogo, "FormularioLibro",
                      DialogoFalso(ACEPTADO, guardado=None))
        antes = self.consultas()

        catalogo.ui.botonNuevo.click()

        assert self.consultas() == antes

    # --- modificar ---
    def test_modificar_le_pasa_el_libro_seleccionado(
        self, catalogo, dialogo_falso, libros_de_ejemplo
    ):
        doble = dialogo_falso(ui_catalogo, "FormularioLibro",
                              DialogoFalso(guardado=libros_de_ejemplo[0]))
        catalogo.ui.tablaLibros.selectRow(0)

        catalogo.ui.botonEditar.click()

        assert doble.recibido["nombrados"]["libro"] is libros_de_ejemplo[0]
        assert "Se actualizó" in catalogo.ui.etiquetaResumen.text()

    def test_modificar_sin_seleccion_no_abre_nada(self, catalogo, dialogo_falso):
        doble = dialogo_falso(ui_catalogo, "FormularioLibro", DialogoFalso())

        catalogo._modificar()

        assert doble.aperturas == 0

    def test_doble_clic_en_la_tabla_abre_la_modificacion(
        self, catalogo, dialogo_falso, libros_de_ejemplo
    ):
        """Atajo que el sistema Java no tenía: había que usar el botón."""
        doble = dialogo_falso(ui_catalogo, "FormularioLibro",
                              DialogoFalso(guardado=libros_de_ejemplo[0]))
        catalogo.ui.tablaLibros.selectRow(0)

        catalogo.ui.tablaLibros.itemDoubleClicked.emit(
            catalogo.ui.tablaLibros.item(0, 0))

        assert doble.aperturas == 1

    # --- dar de baja ---
    def test_la_baja_pide_el_motivo_y_lo_envia(self, catalogo, respuestas):
        """REQ-LIB-03: la baja es lógica y exige decir por qué."""
        respuestas(ui_catalogo, texto="Extraviado", acepta=True)
        catalogo.ui.tablaLibros.selectRow(0)

        catalogo.ui.botonBaja.click()

        clave = "biblioteca.repositorios.libros.dar_de_baja"
        assert self.llamadas[clave][0][0] == (1, "Extraviado")
        assert "fuera del acervo" in catalogo.ui.etiquetaResumen.text()

    def test_cancelar_la_baja_no_da_de_baja_nada(self, catalogo, respuestas):
        respuestas(ui_catalogo, texto="Extraviado", acepta=False)
        catalogo.ui.tablaLibros.selectRow(0)

        catalogo.ui.botonBaja.click()

        assert self.llamadas["biblioteca.repositorios.libros.dar_de_baja"] == []

    @pytest.mark.parametrize("motivo", ["", "   "])
    def test_un_motivo_en_blanco_se_rechaza_con_aviso(
        self, catalogo, respuestas, motivo
    ):
        avisos = respuestas(ui_catalogo, texto=motivo, acepta=True)
        catalogo.ui.tablaLibros.selectRow(0)

        catalogo.ui.botonBaja.click()

        assert self.llamadas["biblioteca.repositorios.libros.dar_de_baja"] == []
        assert any("motivo" in t.lower() for t, _ in avisos)

    def test_el_motivo_se_recorta_antes_de_enviarlo(self, catalogo, respuestas):
        respuestas(ui_catalogo, texto="  Deteriorado  ", acepta=True)
        catalogo.ui.tablaLibros.selectRow(0)

        catalogo.ui.botonBaja.click()

        clave = "biblioteca.repositorios.libros.dar_de_baja"
        assert self.llamadas[clave][0][0] == (1, "Deteriorado")

    def test_si_la_base_rechaza_la_baja_se_explica(
        self, sin_base, con_sesion, libros_de_ejemplo, respuestas
    ):
        """El disparador `validar_baja_de_libro` la rechaza si hay préstamos."""
        self.llamadas = sin_base(
            repo_libros, listar=libros_de_ejemplo, buscar=[],
            dar_de_baja=Exception('No se puede dar de baja "El principito": '
                                  'tiene 2 prestamo(s) sin devolver.'))
        catalogo = PantallaCatalogo()
        avisos = respuestas(ui_catalogo, texto="Extraviado", acepta=True)
        catalogo.ui.tablaLibros.selectRow(0)

        catalogo.ui.botonBaja.click()

        assert any("ejemplares prestados" in m for _, m in avisos)
        assert "fuera del acervo" not in catalogo.ui.etiquetaResumen.text()

    def test_la_baja_sin_seleccion_no_pide_nada(self, catalogo, respuestas):
        avisos = respuestas(ui_catalogo, texto="x", acepta=True)

        catalogo._dar_de_baja()

        assert avisos == []


# ===========================================================================
# Préstamos · registrar y devolver
# ===========================================================================

class TestAccionesDePrestamos:
    @pytest.fixture
    def pantalla(self, sin_base, con_sesion, prestamos_de_ejemplo,
                 alumnos_de_ejemplo, libros_de_ejemplo):
        self.llamadas = sin_base(repo_prestamos,
                                 activos=prestamos_de_ejemplo,
                                 devolver=None)
        return PantallaPrestamos()

    def consultas(self) -> int:
        return len(self.llamadas["biblioteca.repositorios.prestamos.activos"])

    def test_registrar_abre_el_dialogo_y_recarga(
        self, pantalla, dialogo_falso, alumnos_de_ejemplo, libros_de_ejemplo
    ):
        doble = dialogo_falso(ui_prestamos, "DialogoNuevoPrestamo",
                              DialogoFalso(registrado=True,
                                           alumno=alumnos_de_ejemplo[0],
                                           libro=libros_de_ejemplo[0]))
        antes = self.consultas()

        pantalla.ui.botonNuevo.click()

        assert doble.aperturas == 1
        assert self.consultas() == antes + 1
        assert "se llevó" in pantalla.ui.etiquetaResumen.text()

    def test_cancelar_el_prestamo_no_recarga(self, pantalla, dialogo_falso):
        dialogo_falso(ui_prestamos, "DialogoNuevoPrestamo",
                      DialogoFalso(CANCELADO, registrado=False))
        antes = self.consultas()

        pantalla.ui.botonNuevo.click()

        assert self.consultas() == antes

    def test_la_devolucion_se_confirma_antes(self, pantalla, respuestas):
        """Es irreversible desde la pantalla: reabrirla exige tocar la base."""
        avisos = respuestas(ui_prestamos, confirma=True)
        pantalla.ui.tablaPrestamos.selectRow(0)

        pantalla.ui.botonDevolver.click()

        assert any("devolución" in t.lower() for t, _ in avisos)
        assert self.llamadas[
            "biblioteca.repositorios.prestamos.devolver"][0][0] == (1,)
        assert "volvió al acervo" in pantalla.ui.etiquetaResumen.text()

    def test_decir_que_no_no_devuelve_nada(self, pantalla, respuestas):
        respuestas(ui_prestamos, confirma=False)
        pantalla.ui.tablaPrestamos.selectRow(0)

        pantalla.ui.botonDevolver.click()

        assert self.llamadas["biblioteca.repositorios.prestamos.devolver"] == []

    def test_la_confirmacion_nombra_al_alumno_y_al_libro(
        self, pantalla, respuestas
    ):
        """Para que no se devuelva el préstamo de al lado por un clic."""
        avisos = respuestas(ui_prestamos, confirma=True)
        pantalla.ui.tablaPrestamos.selectRow(0)

        pantalla.ui.botonDevolver.click()

        pregunta = next(m for t, m in avisos if "devolución" in t.lower())
        assert "Ana Sofía Martínez" in pregunta
        assert "El principito" in pregunta

    def test_si_la_base_rechaza_la_devolucion_se_explica(
        self, sin_base, con_sesion, prestamos_de_ejemplo, respuestas
    ):
        self.llamadas = sin_base(
            repo_prestamos, activos=prestamos_de_ejemplo,
            devolver=ConnectionError("Connection refused"))
        pantalla = PantallaPrestamos()
        avisos = respuestas(ui_prestamos, confirma=True)
        pantalla.ui.tablaPrestamos.selectRow(0)

        pantalla.ui.botonDevolver.click()

        assert any("conexión" in m.lower() for _, m in avisos)
        assert "volvió al acervo" not in pantalla.ui.etiquetaResumen.text()

    def test_devolver_sin_seleccion_no_pregunta_nada(self, pantalla, respuestas):
        avisos = respuestas(ui_prestamos, confirma=True)

        pantalla._devolver()

        assert avisos == []


# ===========================================================================
# Alumnos · registrar, modificar, historial
# ===========================================================================

class TestAccionesDeAlumnos:
    @pytest.fixture
    def pantalla(self, sin_base, con_sesion, alumnos_de_ejemplo):
        self.llamadas = sin_base(repo_personas,
                                 listar_alumnos=alumnos_de_ejemplo,
                                 buscar_alumnos_o_salon=alumnos_de_ejemplo)
        sin_base(repo_prestamos, activos=[], historial_de=[])
        return PantallaAlumnos()

    def consultas(self) -> int:
        clave = "biblioteca.repositorios.personas.listar_alumnos"
        return len(self.llamadas[clave])

    def test_registrar_abre_el_formulario_y_recarga(
        self, pantalla, dialogo_falso, alumnos_de_ejemplo
    ):
        doble = dialogo_falso(ui_alumnos, "FormularioAlumno",
                              DialogoFalso(guardado=alumnos_de_ejemplo[0]))
        antes = self.consultas()

        pantalla.ui.botonNuevo.click()

        assert doble.aperturas == 1
        assert self.consultas() == antes + 1
        assert "Se registró" in pantalla.ui.etiquetaResumen.text()

    def test_cancelar_el_alta_no_recarga(self, pantalla, dialogo_falso):
        dialogo_falso(ui_alumnos, "FormularioAlumno",
                      DialogoFalso(CANCELADO, guardado=None))
        antes = self.consultas()

        pantalla.ui.botonNuevo.click()

        assert self.consultas() == antes

    def test_modificar_le_pasa_el_alumno_seleccionado(
        self, pantalla, dialogo_falso, alumnos_de_ejemplo
    ):
        """Lo que la escuela pidió: cambiar grado y grupo sin recapturar."""
        doble = dialogo_falso(ui_alumnos, "FormularioAlumno",
                              DialogoFalso(guardado=alumnos_de_ejemplo[0]))
        pantalla.ui.tablaAlumnos.selectRow(0)

        pantalla.ui.botonEditar.click()

        assert doble.recibido["nombrados"]["alumno"] is alumnos_de_ejemplo[0]
        assert "Se actualizaron" in pantalla.ui.etiquetaResumen.text()

    def test_modificar_sin_seleccion_no_abre_nada(self, pantalla, dialogo_falso):
        doble = dialogo_falso(ui_alumnos, "FormularioAlumno", DialogoFalso())

        pantalla._modificar()

        assert doble.aperturas == 0

    def test_el_historial_se_abre_con_el_alumno(
        self, pantalla, dialogo_falso, alumnos_de_ejemplo
    ):
        doble = dialogo_falso(ui_alumnos, "DialogoHistorial", DialogoFalso())
        pantalla.ui.tablaAlumnos.selectRow(0)

        pantalla.ui.botonHistorial.click()

        assert doble.aperturas == 1
        assert alumnos_de_ejemplo[0] in doble.recibido["posicionales"]

    def test_el_historial_sin_seleccion_no_se_abre(self, pantalla, dialogo_falso):
        doble = dialogo_falso(ui_alumnos, "DialogoHistorial", DialogoFalso())

        pantalla._ver_historial()

        assert doble.aperturas == 0


# ===========================================================================
# Empleados · registrar y modificar
# ===========================================================================

class TestAccionesDeEmpleados:
    @pytest.fixture
    def pantalla(self, sin_base, con_sesion, empleados_de_ejemplo):
        self.llamadas = sin_base(repo_personas,
                                 listar_empleados=empleados_de_ejemplo)
        return PantallaEmpleados()

    def consultas(self) -> int:
        clave = "biblioteca.repositorios.personas.listar_empleados"
        return len(self.llamadas[clave])

    def test_registrar_abre_el_formulario_y_recarga(
        self, pantalla, dialogo_falso, empleados_de_ejemplo
    ):
        doble = dialogo_falso(ui_empleados, "FormularioEmpleado",
                              DialogoFalso(guardado=empleados_de_ejemplo[1]))
        antes = self.consultas()

        pantalla.ui.botonNuevo.click()

        assert doble.aperturas == 1
        assert self.consultas() == antes + 1
        assert "Se registró" in pantalla.ui.etiquetaResumen.text()

    def test_cancelar_el_alta_no_recarga(self, pantalla, dialogo_falso):
        dialogo_falso(ui_empleados, "FormularioEmpleado",
                      DialogoFalso(CANCELADO, guardado=None))
        antes = self.consultas()

        pantalla.ui.botonNuevo.click()

        assert self.consultas() == antes

    def test_modificar_le_pasa_el_empleado_seleccionado(
        self, pantalla, dialogo_falso, empleados_de_ejemplo
    ):
        doble = dialogo_falso(ui_empleados, "FormularioEmpleado",
                              DialogoFalso(guardado=empleados_de_ejemplo[0]))
        pantalla.ui.tablaEmpleados.selectRow(0)

        pantalla.ui.botonEditar.click()

        assert doble.recibido["nombrados"]["empleado"] is empleados_de_ejemplo[0]
        assert "Se actualizaron" in pantalla.ui.etiquetaResumen.text()

    def test_modificar_sin_seleccion_no_abre_nada(self, pantalla, dialogo_falso):
        doble = dialogo_falso(ui_empleados, "FormularioEmpleado", DialogoFalso())

        pantalla._modificar()

        assert doble.aperturas == 0


# ===========================================================================
# Historial del alumno · la pantalla que menos se ejercitaba
# ===========================================================================

class TestHistorialDelAlumno:
    """REQ-PRE-03: el historial completo, también lo ya devuelto.

    Es lo que el `ON DELETE RESTRICT` protege. El sistema Java usaba
    `CASCADE` y borrar un libro se llevaba su historial con él.
    """

    def test_se_llena_con_los_movimientos(
        self, sin_base, con_sesion, alumnos_de_ejemplo, prestamos_de_ejemplo
    ):
        sin_base(repo_prestamos, historial_de=prestamos_de_ejemplo)

        dialogo = DialogoHistorial(None, alumnos_de_ejemplo[0])

        assert dialogo.ui.tablaHistorial.rowCount() == 2

    def test_el_encabezado_identifica_al_alumno(
        self, sin_base, con_sesion, alumnos_de_ejemplo
    ):
        sin_base(repo_prestamos, historial_de=[])

        dialogo = DialogoHistorial(None, alumnos_de_ejemplo[0])

        encabezado = dialogo.ui.etiquetaAlumno.text()
        assert "Ana Sofía Martínez" in encabezado
        assert "4B" in encabezado
        assert "A-001" in encabezado

    def test_un_prestamo_devuelto_muestra_su_fecha(
        self, sin_base, con_sesion, alumnos_de_ejemplo, prestamos_de_ejemplo
    ):
        from datetime import date

        from biblioteca.modelos.prestamo import EstadoPrestamo

        devuelto = prestamos_de_ejemplo[0]
        devuelto.estado = EstadoPrestamo.DEVUELTO
        devuelto.fecha_devolucion = date(2026, 9, 20)
        sin_base(repo_prestamos, historial_de=[devuelto])

        dialogo = DialogoHistorial(None, alumnos_de_ejemplo[0])
        fila = [dialogo.ui.tablaHistorial.item(0, c).text() for c in range(5)]

        assert fila[3] == "20/09/2026"
        assert fila[4] == "Devuelto"

    def test_un_prestamo_sin_devolver_lo_dice(
        self, sin_base, con_sesion, alumnos_de_ejemplo, prestamos_de_ejemplo
    ):
        sin_base(repo_prestamos, historial_de=[prestamos_de_ejemplo[1]])

        dialogo = DialogoHistorial(None, alumnos_de_ejemplo[0])
        fila = [dialogo.ui.tablaHistorial.item(0, c).text() for c in range(5)]

        assert fila[3] == "—"
        assert "Vencido" in fila[4]

    def test_un_alumno_sin_movimientos_no_revienta(
        self, sin_base, con_sesion, alumnos_de_ejemplo
    ):
        sin_base(repo_prestamos, historial_de=[])

        dialogo = DialogoHistorial(None, alumnos_de_ejemplo[0])

        assert dialogo.ui.tablaHistorial.rowCount() == 0
        assert dialogo.ui.etiquetaResumen.text().strip()

    def test_un_alumno_sin_id_no_se_consulta(
        self, sin_base, con_sesion, alumnos_de_ejemplo
    ):
        """Salida temprana: un alumno sin guardar no tiene historial que pedir."""
        llamadas = sin_base(repo_prestamos, historial_de=[])
        alumnos_de_ejemplo[0].id = None

        DialogoHistorial(None, alumnos_de_ejemplo[0])

        assert llamadas["biblioteca.repositorios.prestamos.historial_de"] == []

    def test_un_fallo_de_consulta_se_explica(
        self, sin_base, con_sesion, alumnos_de_ejemplo, respuestas
    ):
        from biblioteca.ui import historial_alumno as ui_historial

        sin_base(repo_prestamos,
                 historial_de=ConnectionError("Connection refused"))
        avisos = respuestas(ui_historial)

        dialogo = DialogoHistorial(None, alumnos_de_ejemplo[0])

        assert dialogo.ui.tablaHistorial.rowCount() == 0
        assert any("conexión" in m.lower() for _, m in avisos)


# ===========================================================================
# Login · las dos ramas que faltaban
# ===========================================================================

class TestEntradaAlSistema:
    def test_sin_correo_o_sin_contrasena_no_se_consulta(self, monkeypatch):
        """Se avisa antes de salir a la red: es más rápido y no gasta viaje."""
        from biblioteca.ui import login as ui_login
        from biblioteca.ui.login import DialogoLogin

        intentos = []
        monkeypatch.setattr(ui_login, "iniciar_sesion",
                            lambda c, p: intentos.append((c, p)))

        for correo, contrasena in (("", "x"), ("a@b.com", ""), ("", "")):
            dialogo = DialogoLogin()
            dialogo.ui.campoCorreo.setText(correo)
            dialogo.ui.campoContrasena.setText(contrasena)

            dialogo.ui.botonEntrar.click()

            assert "correo y tu contraseña" in dialogo.ui.etiquetaError.text()

        assert intentos == []

    def test_el_boton_se_apaga_mientras_verifica(self, monkeypatch,
                                                 sesion_de_administradora):
        """Evita que un doble clic mande dos intentos de inicio de sesión."""
        from biblioteca.ui import login as ui_login
        from biblioteca.ui.login import DialogoLogin

        estados = []

        def espiar(correo, contrasena):
            estados.append(dialogo.ui.botonEntrar.isEnabled())
            return sesion_de_administradora

        monkeypatch.setattr(ui_login, "iniciar_sesion", espiar)
        dialogo = DialogoLogin()
        dialogo.ui.campoCorreo.setText("bibliotecaria@demo.com")
        dialogo.ui.campoContrasena.setText("123456")

        dialogo.ui.botonEntrar.click()

        assert estados == [False], "el botón siguió pulsable mientras verificaba"

    def test_tras_un_rechazo_se_vacia_la_contrasena(self, monkeypatch):
        """Para no reenviar la misma por inercia, y por no dejarla escrita."""
        from biblioteca.ui import login as ui_login
        from biblioteca.ui.login import DialogoLogin

        def rechazar(correo, contrasena):
            raise ErrorDeAccesoLocal("Correo o contraseña incorrectos.")

        from biblioteca.core.sesion import ErrorDeAcceso as ErrorDeAccesoLocal

        monkeypatch.setattr(ui_login, "iniciar_sesion", rechazar)
        dialogo = DialogoLogin()
        dialogo.ui.campoCorreo.setText("a@b.com")
        dialogo.ui.campoContrasena.setText("equivocada")

        dialogo.ui.botonEntrar.click()

        assert dialogo.ui.campoContrasena.text() == ""
        assert dialogo.ui.campoCorreo.text() == "a@b.com", (
            "el correo sí se conserva: reescribirlo cada vez cuesta tiempo")

    def test_un_fallo_inesperado_se_explica_sin_jerga(self, monkeypatch):
        """La rama del `except Exception`, distinta de `ErrorDeAcceso`."""
        from biblioteca.ui import login as ui_login
        from biblioteca.ui.login import DialogoLogin

        def reventar(correo, contrasena):
            raise TypeError("'NoneType' object is not subscriptable")

        monkeypatch.setattr(ui_login, "iniciar_sesion", reventar)
        dialogo = DialogoLogin()
        dialogo.ui.campoCorreo.setText("a@b.com")
        dialogo.ui.campoContrasena.setText("x")

        dialogo.ui.botonEntrar.click()

        aviso = dialogo.ui.etiquetaError.text()
        assert aviso.strip()
        assert "NoneType" not in aviso
        assert dialogo.ui.botonEntrar.isEnabled()

    def test_pedir_sesion_devuelve_la_sesion_o_nada(self, monkeypatch,
                                                    sesion_de_administradora):
        """La función que `main.py` llama al arrancar."""
        from biblioteca.ui import login as ui_login
        from biblioteca.ui.login import pedir_sesion

        class LoginFalso:
            def __init__(self, resultado, sesion):
                self.resultado, self.sesion = resultado, sesion

            def exec(self):
                return self.resultado

        monkeypatch.setattr(
            ui_login, "DialogoLogin",
            lambda padre=None: LoginFalso(ACEPTADO, sesion_de_administradora))
        assert pedir_sesion() is sesion_de_administradora

        monkeypatch.setattr(
            ui_login, "DialogoLogin",
            lambda padre=None: LoginFalso(CANCELADO, None))
        assert pedir_sesion() is None


# ===========================================================================
# Deudores · el filtro de salón y el orden por retraso
# ===========================================================================

class TestFiltroDeDeudores:
    def test_el_filtro_deja_solo_el_salon_elegido(
        self, sin_base, con_sesion, deudores_de_ejemplo
    ):
        from biblioteca.repositorios.prestamos import Deudor

        otro = Deudor(prestamo_id=3, codigo="A-003", alumno="Sara Díaz",
                      grado=4, grupo="B", correo=None, telefono="2281110000",
                      libro="Momo", fecha_prestamo=None, fecha_limite=None,
                      dias_de_retraso=2)
        sin_base(repo_prestamos, deudores=[*deudores_de_ejemplo, otro])
        pantalla = PantallaDeudores()

        pantalla.ui.campoSalon.setCurrentText("4B")

        assert pantalla.ui.tablaDeudores.rowCount() == 1
        assert pantalla.ui.tablaDeudores.item(0, 0).text() == "Sara Díaz"

    def test_el_boton_de_actualizar_vuelve_a_consultar(
        self, sin_base, con_sesion, deudores_de_ejemplo
    ):
        llamadas = sin_base(repo_prestamos, deudores=deudores_de_ejemplo)
        pantalla = PantallaDeudores()
        antes = len(llamadas["biblioteca.repositorios.prestamos.deudores"])

        pantalla.ui.botonActualizar.click()

        assert len(llamadas[
            "biblioteca.repositorios.prestamos.deudores"]) == antes + 1

    def test_la_columna_de_retraso_ordena_por_dias_y_no_por_texto(self):
        """«2 días» y «11 días» en orden alfabético salen al revés.

        La celda guarda el número y compara con él, que es lo que hace útil
        ordenar por esa columna.
        """
        dos = CeldaDeRetraso("2 días", 2)
        once = CeldaDeRetraso("11 días", 11)

        assert dos < once
        assert not (once < dos)
        assert "11 días" < "2 días", "el orden alfabético sí los invierte"


# ===========================================================================
# Las ramas que quedaban sin recorrer
# ===========================================================================

class TestSeleccionQueSobreviveALaBusqueda:
    """Un temporizador pendiente no debe borrar lo que se acaba de elegir.

    Las dos búsquedas del diálogo se disparan solas a los 250 ms. Si una
    salta justo después de que el bibliotecario eligió, la lista se vuelve a
    llenar: sin esta protección la selección desaparecería y el botón se
    apagaría solo, delante de él.
    """

    @pytest.fixture
    def dialogo(self, sin_base, con_sesion, alumnos_de_ejemplo,
                libros_de_ejemplo):
        from biblioteca.ui.nuevo_prestamo import DialogoNuevoPrestamo

        sin_base(repo_personas, buscar_alumnos_o_salon=alumnos_de_ejemplo)
        sin_base(repo_libros, listar=libros_de_ejemplo,
                 buscar=libros_de_ejemplo)
        return DialogoNuevoPrestamo()

    def test_el_alumno_elegido_se_conserva(self, dialogo):
        dialogo.ui.listaAlumnos.setCurrentRow(0)
        elegido = dialogo.alumno

        dialogo._buscar_alumnos()          # lo que haría el temporizador

        assert dialogo.alumno is not None
        assert dialogo.alumno.id == elegido.id

    def test_el_libro_elegido_se_conserva(self, dialogo):
        dialogo.ui.listaLibros.setCurrentRow(0)
        elegido = dialogo.libro

        dialogo._buscar_libros()

        assert dialogo.libro is not None
        assert dialogo.libro.id == elegido.id

    def test_si_el_elegido_ya_no_esta_en_los_resultados_se_suelta(
        self, dialogo, sin_base, alumnos_de_ejemplo
    ):
        """Y entonces el botón vuelve a apagarse, que es lo correcto."""
        dialogo.ui.listaAlumnos.setCurrentRow(0)
        sin_base(repo_personas, buscar_alumnos_o_salon=alumnos_de_ejemplo[1:])

        dialogo._buscar_alumnos()

        assert dialogo.alumno is None
        assert not dialogo.ui.botonPrestar.isEnabled()

    def test_un_libro_que_se_quedo_sin_ejemplares_se_suelta(
        self, dialogo, sin_base, libros_de_ejemplo
    ):
        """Otra persona pudo llevárselo mientras este diálogo estaba abierto."""
        dialogo.ui.listaLibros.setCurrentRow(0)
        agotado = libros_de_ejemplo[0]
        agotado.existencias = 0
        sin_base(repo_libros, listar=[agotado], buscar=[agotado])

        dialogo._buscar_libros()

        assert dialogo.libro is None

    def test_un_fallo_al_buscar_el_libro_se_explica(
        self, sin_base, con_sesion, alumnos_de_ejemplo
    ):
        from biblioteca.ui.nuevo_prestamo import DialogoNuevoPrestamo

        sin_base(repo_personas, buscar_alumnos_o_salon=alumnos_de_ejemplo)
        sin_base(repo_libros, listar=ConnectionError("Connection refused"),
                 buscar=[])

        dialogo = DialogoNuevoPrestamo()

        assert "No se pudo buscar el libro" in dialogo.ui.etiquetaError.text()
        assert dialogo.ui.listaLibros.count() == 0

    def test_prestar_sin_los_dos_elegidos_no_hace_nada(self, dialogo, sin_base):
        """Guarda del método, por si alguien lo invoca sin pasar por el botón."""
        llamadas = sin_base(repo_prestamos, registrar=None)

        dialogo._prestar()

        assert llamadas["biblioteca.repositorios.prestamos.registrar"] == []


class TestAvisosDeLasTablas:
    """Guardas y detalles de presentación que ninguna prueba recorría."""

    def test_un_alumno_sin_contacto_del_tutor_se_marca(
        self, sin_base, con_sesion, alumnos_de_ejemplo
    ):
        """Es un dato que falta, no un campo opcional: sin él no se avisa."""
        from PySide6.QtCore import Qt

        alumnos_de_ejemplo[0].telefono = None
        alumnos_de_ejemplo[0].correo = None
        sin_base(repo_personas, listar_alumnos=alumnos_de_ejemplo,
                 buscar_alumnos_o_salon=[])
        sin_base(repo_prestamos, activos=[], historial_de=[])

        pantalla = PantallaAlumnos()

        tabla = pantalla.ui.tablaAlumnos
        assert tabla.item(0, 3).foreground().color() == Qt.GlobalColor.darkRed
        assert "sin contacto del tutor" in pantalla.ui.etiquetaResumen.text()

    def test_el_resumen_cuenta_a_quien_tiene_libro(
        self, sin_base, con_sesion, alumnos_de_ejemplo, prestamos_de_ejemplo
    ):
        sin_base(repo_personas, listar_alumnos=alumnos_de_ejemplo,
                 buscar_alumnos_o_salon=[])
        sin_base(repo_prestamos, activos=prestamos_de_ejemplo, historial_de=[])

        pantalla = PantallaAlumnos()

        assert "con libro prestado" in pantalla.ui.etiquetaResumen.text()

    @pytest.mark.parametrize("pantalla_y_metodo", [
        ("catalogo", "_seleccionado"),
        ("alumnos", "_seleccionado"),
        ("empleados", "_seleccionado"),
    ])
    def test_una_fila_seleccionada_sin_celda_no_revienta(
        self, sin_base, con_sesion, libros_de_ejemplo, alumnos_de_ejemplo,
        empleados_de_ejemplo, pantalla_y_metodo
    ):
        """Pasa mientras la tabla se repinta: la fila existe y la celda no.

        Sin la guarda, pulsar un botón en ese instante levantaba un error que
        ninguna pantalla atrapa.
        """
        nombre, metodo = pantalla_y_metodo
        sin_base(repo_libros, listar=libros_de_ejemplo, buscar=[])
        sin_base(repo_personas, listar_alumnos=alumnos_de_ejemplo,
                 buscar_alumnos_o_salon=[],
                 listar_empleados=empleados_de_ejemplo)
        sin_base(repo_prestamos, activos=[], historial_de=[])

        # La celda que guarda el índice es la 0 en el catálogo y la 1 en las
        # dos pantallas de personas.
        clases = {"catalogo": (PantallaCatalogo, "tablaLibros", 0),
                  "alumnos": (PantallaAlumnos, "tablaAlumnos", 1),
                  "empleados": (PantallaEmpleados, "tablaEmpleados", 1)}
        clase, atributo, columna = clases[nombre]
        pantalla = clase()
        tabla = getattr(pantalla.ui, atributo)
        tabla.selectRow(0)
        # La fila sigue seleccionada, pero la celda que guarda el índice ya no
        # está: es el instante exacto que la guarda cubre. Vaciar la tabla
        # entera no serviría, porque entonces no quedaría fila seleccionada y
        # el método saldría por la guarda anterior.
        tabla.takeItem(0, columna)

        assert getattr(pantalla, metodo)() is None

    def test_el_reporte_destaca_los_retrasos_criticos(
        self, sin_base, con_sesion
    ):
        """Un retraso largo no es lo mismo que uno de dos días."""
        from biblioteca.repositorios.prestamos import Deudor
        from biblioteca.ui.deudores import DIAS_CRITICOS

        grave = Deudor(prestamo_id=1, codigo="A-001", alumno="Luis Ramírez",
                       grado=2, grupo="A", correo=None, telefono="2287654321",
                       libro="Momo", fecha_prestamo=None, fecha_limite=None,
                       dias_de_retraso=DIAS_CRITICOS + 5)
        sin_base(repo_prestamos, deudores=[grave])

        pantalla = PantallaDeudores()

        detalle = pantalla.ui.etiquetaMasAtrasado.text()
        assert "Luis Ramírez" in detalle
        assert f"más de {DIAS_CRITICOS} días" in detalle

    def test_la_celda_de_retraso_se_compara_con_cualquier_otra(self):
        """Si la columna se ordena junto a celdas corrientes, no debe romper."""
        from PySide6.QtWidgets import QTableWidgetItem

        celda = CeldaDeRetraso("2 días", 2)

        assert isinstance(celda < QTableWidgetItem("11 días"), bool)


class TestCancelarUnaModificacion:
    """La otra salida de los tres botones *Editar*.

    Cancelar no debe recargar ni avisar. Sin esta prueba la rama quedaba sin
    recorrer en las tres pantallas, porque solo se probaba el camino en que
    se guarda.
    """

    def test_en_el_catalogo(self, sin_base, con_sesion, libros_de_ejemplo,
                            dialogo_falso):
        llamadas = sin_base(repo_libros, listar=libros_de_ejemplo, buscar=[])
        catalogo = PantallaCatalogo()
        dialogo_falso(ui_catalogo, "FormularioLibro",
                      DialogoFalso(CANCELADO, guardado=None))
        catalogo.ui.tablaLibros.selectRow(0)
        antes = len(llamadas["biblioteca.repositorios.libros.listar"])
        resumen = catalogo.ui.etiquetaResumen.text()

        catalogo.ui.botonEditar.click()

        assert len(llamadas["biblioteca.repositorios.libros.listar"]) == antes
        assert catalogo.ui.etiquetaResumen.text() == resumen

    def test_en_el_padron(self, sin_base, con_sesion, alumnos_de_ejemplo,
                          dialogo_falso):
        llamadas = sin_base(repo_personas, listar_alumnos=alumnos_de_ejemplo,
                            buscar_alumnos_o_salon=[])
        sin_base(repo_prestamos, activos=[], historial_de=[])
        pantalla = PantallaAlumnos()
        dialogo_falso(ui_alumnos, "FormularioAlumno",
                      DialogoFalso(CANCELADO, guardado=None))
        pantalla.ui.tablaAlumnos.selectRow(0)
        clave = "biblioteca.repositorios.personas.listar_alumnos"
        antes = len(llamadas[clave])

        pantalla.ui.botonEditar.click()

        assert len(llamadas[clave]) == antes

    def test_en_la_plantilla(self, sin_base, con_sesion, empleados_de_ejemplo,
                             dialogo_falso):
        llamadas = sin_base(repo_personas,
                            listar_empleados=empleados_de_ejemplo)
        pantalla = PantallaEmpleados()
        dialogo_falso(ui_empleados, "FormularioEmpleado",
                      DialogoFalso(CANCELADO, guardado=None))
        pantalla.ui.tablaEmpleados.selectRow(0)
        clave = "biblioteca.repositorios.personas.listar_empleados"
        antes = len(llamadas[clave])

        pantalla.ui.botonEditar.click()

        assert len(llamadas[clave]) == antes
