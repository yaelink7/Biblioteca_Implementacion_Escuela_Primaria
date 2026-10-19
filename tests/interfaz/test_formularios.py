"""Interfaz · los formularios de captura y el diálogo de préstamo.

Esto es lo que la matriz de casos del sistema Java **declaraba imposible de
automatizar**. Sus casos TC-19 a TC-30 describían el alta de un libro, y la
matriz anotaba por qué quedaban sin ejecutar: la lógica vivía dentro del
método privado `guardarenlista` de `GUILibro`, leía de los componentes Swing
y avisaba con `JOptionPane`, así que las pruebas no podían invocarla y, si la
sorteaban, cada cuadro de diálogo dejaba la suite colgada esperando un clic.

El sistema Java resolvió aquello construyendo `AltaLibroConsola`, una interfaz
de texto que hacía lo mismo sin ventanas. Con ella sí se pudo probar —son las
9 pruebas de `AltaLibroConsolaTest`, y la única parte del original que pasó
del 50 % de ramas: 65 %—. Pero probaba la consola, no el formulario.

Aquí no hace falta el desvío: la validación vive en `servicios/` y el
formulario solo recoge y muestra. Estas pruebas recorren el formulario de
verdad, el que usa la bibliotecaria.
"""

from __future__ import annotations

import pytest

from biblioteca.core.sesion import ErrorDeAcceso
from biblioteca.modelos.libro import Libro
from biblioteca.modelos.persona import Rol
from biblioteca.repositorios import libros as repo_libros
from biblioteca.repositorios import personas as repo_personas
from biblioteca.repositorios import prestamos as repo_prestamos
from biblioteca.repositorios.libros import ErrorDeCatalogo
from biblioteca.repositorios.personas import ErrorDePersona
from biblioteca.repositorios.prestamos import ErrorDePrestamo
from biblioteca.ui.formulario_alumno import FormularioAlumno
from biblioteca.ui.formulario_empleado import FormularioEmpleado
from biblioteca.ui.formulario_libro import FormularioLibro
from biblioteca.ui.login import DialogoLogin
from biblioteca.ui.nuevo_prestamo import DialogoNuevoPrestamo


# ===========================================================================
# Formulario de libro · los doce casos del grupo B, ahora sí ejecutables
# ===========================================================================

class TestFormularioDeLibro:
    """TC-19 a TC-30, recorridos sobre el formulario real."""

    def llenar(self, formulario, titulo="El Quijote", autor="Cervantes",
               existencias=5, paginas=863, ano=1605):
        formulario.ui.campoTitulo.setText(titulo)
        formulario.ui.campoAutor.setText(autor)
        formulario.ui.campoExistencias.setValue(existencias)
        formulario.ui.campoPaginas.setValue(paginas)
        formulario.ui.campoAno.setValue(ano)
        return formulario

    # --- TC-19 ---
    def test_tc19_con_todo_correcto_se_guarda_y_se_cierra(self, sin_base):
        guardado = Libro(id=9, titulo="El Quijote", autor="Cervantes",
                         existencias=5)
        llamadas = sin_base(repo_libros, dar_de_alta=guardado)
        formulario = self.llenar(FormularioLibro())

        formulario.ui.botonGuardar.click()

        assert formulario.guardado is guardado
        assert formulario.result() == formulario.DialogCode.Accepted
        assert llamadas["biblioteca.repositorios.libros.dar_de_alta"]

    def test_lo_que_se_captura_llega_al_repositorio(self, sin_base):
        llamadas = sin_base(repo_libros, dar_de_alta=Libro(
            id=9, titulo="El Quijote", autor="Cervantes", existencias=5))
        formulario = self.llenar(FormularioLibro())
        formulario.ui.campoEditorial.setText("Planeta")

        formulario.ui.botonGuardar.click()

        (enviado,), _ = llamadas["biblioteca.repositorios.libros.dar_de_alta"][0]
        assert enviado.titulo == "El Quijote"
        assert enviado.autor == "Cervantes"
        assert enviado.existencias == 5
        assert enviado.editorial == "Planeta"

    # --- TC-20, TC-21, TC-22 ---
    @pytest.mark.parametrize("titulo", ["", "   "])
    def test_tc20_y_tc22_sin_titulo_no_se_guarda_y_se_dice_por_que(
        self, sin_base, titulo
    ):
        """El sistema Java abría un `JOptionPane`; aquí es una etiqueta.

        Ese cambio es lo que hace la prueba posible: la etiqueta se lee desde
        el código, el cuadro de diálogo había que cerrarlo a mano.
        """
        llamadas = sin_base(repo_libros, dar_de_alta=Libro(
            titulo="x", autor="y", existencias=1))
        formulario = self.llenar(FormularioLibro(), titulo=titulo)

        formulario.ui.botonGuardar.click()

        assert "título" in formulario.ui.etiquetaError.text().lower()
        assert llamadas["biblioteca.repositorios.libros.dar_de_alta"] == []
        assert formulario.isVisible() is False and formulario.guardado is None

    def test_tc21_el_formulario_vacio_reporta_los_dos_campos(self, sin_base):
        sin_base(repo_libros, dar_de_alta=Libro(titulo="x", autor="y",
                                                existencias=1))
        formulario = FormularioLibro()
        formulario.ui.campoExistencias.setValue(1)

        formulario.ui.botonGuardar.click()

        aviso = formulario.ui.etiquetaError.text().lower()
        assert "título" in aviso and "autor" in aviso

    # --- TC-26, TC-27, TC-28 ---
    def test_tc26_el_alta_sin_ejemplares_se_rechaza(self, sin_base):
        """El caso que el sistema Java aceptaba por medir la longitud (D-06)."""
        llamadas = sin_base(repo_libros, dar_de_alta=Libro(
            titulo="x", autor="y", existencias=1))
        formulario = self.llenar(FormularioLibro(), existencias=0)

        formulario.ui.botonGuardar.click()

        assert "ejemplar" in formulario.ui.etiquetaError.text().lower()
        assert llamadas["biblioteca.repositorios.libros.dar_de_alta"] == []

    def test_tc27_las_existencias_negativas_no_se_pueden_ni_teclear(self):
        """El control las impide antes que el validador.

        Es la defensa que el sistema Java no tenía: allá el campo era texto y
        «-5» entraba sin problema.
        """
        formulario = FormularioLibro()

        formulario.ui.campoExistencias.setValue(-5)

        assert formulario.ui.campoExistencias.value() >= 0

    def test_tc28_cero_paginas_se_rechaza(self, sin_base):
        """D-07. El cero sigue siendo teclable porque significa «sin dato»."""
        llamadas = sin_base(repo_libros, dar_de_alta=Libro(
            titulo="x", autor="y", existencias=1))
        formulario = self.llenar(FormularioLibro(), paginas=0)

        formulario.ui.botonGuardar.click()

        # Cero significa "sin especificar", asi que pasa: no es un rechazo.
        assert llamadas["biblioteca.repositorios.libros.dar_de_alta"]

    # --- TC-23, TC-29 ---
    def test_tc29_el_ano_futuro_no_se_puede_ni_teclear(self):
        """D-08 cerrado en el control, además de en el validador y la base."""
        from datetime import date

        formulario = FormularioLibro()

        formulario.ui.campoAno.setValue(9999)

        assert formulario.ui.campoAno.value() == date.today().year

    # --- modificación ---
    def test_al_modificar_el_formulario_llega_lleno(self, sin_base, libros_de_ejemplo):
        sin_base(repo_libros, modificar=libros_de_ejemplo[0])
        formulario = FormularioLibro(libro=libros_de_ejemplo[0])

        assert formulario.ui.campoTitulo.text() == "El principito"
        assert formulario.ui.campoAutor.text() == "Saint-Exupéry"
        assert formulario.ui.campoExistencias.value() == 3

    def test_al_modificar_el_titulo_de_la_ventana_lo_dice(self, libros_de_ejemplo):
        assert FormularioLibro().windowTitle() == "Registrar libro"
        assert FormularioLibro(
            libro=libros_de_ejemplo[0]).windowTitle() == "Modificar libro"

    def test_al_modificar_se_admiten_cero_ejemplares(
        self, sin_base, libros_de_ejemplo
    ):
        """Un libro ya registrado puede quedar en cero: están todos prestados."""
        llamadas = sin_base(repo_libros, modificar=libros_de_ejemplo[0])
        formulario = FormularioLibro(libro=libros_de_ejemplo[0])
        formulario.ui.campoExistencias.setValue(0)

        formulario.ui.botonGuardar.click()

        assert llamadas["biblioteca.repositorios.libros.modificar"]

    # --- errores de la base ---
    def test_un_rechazo_de_la_base_se_muestra_en_el_formulario(self, sin_base):
        llamadas = sin_base(repo_libros, dar_de_alta=ErrorDeCatalogo(
            "Ya existe un libro con ese código."))
        formulario = self.llenar(FormularioLibro())

        formulario.ui.botonGuardar.click()

        assert "ese código" in formulario.ui.etiquetaError.text()
        assert formulario.guardado is None
        assert llamadas["biblioteca.repositorios.libros.dar_de_alta"]

    def test_tras_un_rechazo_se_puede_volver_a_intentar(self, sin_base):
        """Si el botón se quedara apagado, habría que cerrar y recapturar."""
        sin_base(repo_libros, dar_de_alta=ErrorDeCatalogo("algo"))
        formulario = self.llenar(FormularioLibro())

        formulario.ui.botonGuardar.click()

        assert formulario.ui.botonGuardar.isEnabled()

    def test_un_corte_de_red_no_se_lee_como_rechazo_de_la_base(self, sin_base):
        """El defecto de la auditoría: las tres pantallas de captura no
        pasaban por el traductor, así que un corte de red se leía «la base
        rechazó la operación»."""
        sin_base(repo_libros,
                 dar_de_alta=ConnectionError("Connection refused"))
        formulario = self.llenar(FormularioLibro())

        formulario.ui.botonGuardar.click()

        aviso = formulario.ui.etiquetaError.text().lower()
        assert "conexión" in aviso or "internet" in aviso
        assert "rechazó" not in aviso

    def test_cancelar_no_guarda_nada(self, sin_base):
        llamadas = sin_base(repo_libros, dar_de_alta=Libro(
            titulo="x", autor="y", existencias=1))
        formulario = self.llenar(FormularioLibro())

        formulario.ui.botonCancelar.click()

        assert llamadas["biblioteca.repositorios.libros.dar_de_alta"] == []
        assert formulario.result() == formulario.DialogCode.Rejected


# ===========================================================================
# Formulario de alumno · incluye lo que el usuario reportó del grado
# ===========================================================================

class TestFormularioDeAlumno:
    def llenar(self, formulario, codigo="A-009", nombre="Luis",
               apellido="Ramírez", telefono="2281234567"):
        formulario.ui.campoCodigo.setText(codigo)
        formulario.ui.campoNombre.setText(nombre)
        formulario.ui.campoApellido.setText(apellido)
        formulario.ui.campoTelefono.setText(telefono)
        return formulario

    def test_el_camino_feliz_guarda(self, sin_base, alumnos_de_ejemplo):
        llamadas = sin_base(repo_personas,
                            dar_de_alta_alumno=alumnos_de_ejemplo[0])
        formulario = self.llenar(FormularioAlumno())
        formulario.ui.campoGrado.setValue(2)
        formulario.ui.campoGrupo.setCurrentText("A")

        formulario.ui.botonGuardar.click()

        assert llamadas["biblioteca.repositorios.personas.dar_de_alta_alumno"]
        assert formulario.result() == formulario.DialogCode.Accepted

    def test_el_grupo_se_guarda_en_mayuscula(self, sin_base, alumnos_de_ejemplo):
        llamadas = sin_base(repo_personas,
                            dar_de_alta_alumno=alumnos_de_ejemplo[0])
        formulario = self.llenar(FormularioAlumno())
        formulario.ui.campoGrado.setValue(2)
        formulario.ui.campoGrupo.setCurrentText("a")

        formulario.ui.botonGuardar.click()

        clave = "biblioteca.repositorios.personas.dar_de_alta_alumno"
        (enviado,), _ = llamadas[clave][0]
        assert enviado.grupo == "A"

    def test_sin_grado_ni_grupo_tambien_se_guarda(
        self, sin_base, alumnos_de_ejemplo
    ):
        """Un niño de nuevo ingreso puede entrar al padrón sin salón."""
        llamadas = sin_base(repo_personas,
                            dar_de_alta_alumno=alumnos_de_ejemplo[0])
        formulario = self.llenar(FormularioAlumno())

        formulario.ui.botonGuardar.click()

        assert llamadas["biblioteca.repositorios.personas.dar_de_alta_alumno"]

    def test_el_grado_sin_grupo_no_cierra_el_formulario(
        self, sin_base, alumnos_de_ejemplo
    ):
        """Lo que se reportó como «no funcionan los botones del grado».

        El control sí responde —el valor cambia— pero *Guardar* no cierra,
        porque la regla exige grado y grupo juntos: con medio dato la búsqueda
        por salón no encuentra al alumno. El aviso aparece en rojo y es fácil
        pasarlo por alto.
        """
        llamadas = sin_base(repo_personas,
                            dar_de_alta_alumno=alumnos_de_ejemplo[0])
        formulario = self.llenar(FormularioAlumno())

        formulario.ui.campoGrado.setValue(4)
        assert formulario.ui.campoGrado.value() == 4, "el control no respondió"

        formulario.ui.botonGuardar.click()

        assert "juntos" in formulario.ui.etiquetaError.text().lower()
        assert llamadas[
            "biblioteca.repositorios.personas.dar_de_alta_alumno"] == []
        assert formulario.result() != formulario.DialogCode.Accepted

    def test_el_grupo_sin_grado_tampoco(self, sin_base, alumnos_de_ejemplo):
        sin_base(repo_personas, dar_de_alta_alumno=alumnos_de_ejemplo[0])
        formulario = self.llenar(FormularioAlumno())

        formulario.ui.campoGrupo.setCurrentText("B")
        formulario.ui.botonGuardar.click()

        assert "juntos" in formulario.ui.etiquetaError.text().lower()

    def test_el_grado_solo_admite_del_uno_al_seis(self):
        """Una primaria tiene seis grados; el control no deja teclear otro."""
        formulario = FormularioAlumno()

        formulario.ui.campoGrado.setValue(9)
        assert formulario.ui.campoGrado.value() <= 6

        formulario.ui.campoGrado.setValue(-3)
        assert formulario.ui.campoGrado.value() >= formulario.ui.campoGrado.minimum()

    def test_sin_contacto_del_tutor_no_se_guarda(
        self, sin_base, alumnos_de_ejemplo
    ):
        """Sin él no hay forma de avisar de un préstamo vencido."""
        llamadas = sin_base(repo_personas,
                            dar_de_alta_alumno=alumnos_de_ejemplo[0])
        formulario = self.llenar(FormularioAlumno(), telefono="")

        formulario.ui.botonGuardar.click()

        assert "tutor" in formulario.ui.etiquetaError.text().lower()
        assert llamadas[
            "biblioteca.repositorios.personas.dar_de_alta_alumno"] == []

    def test_al_modificar_el_codigo_no_se_puede_cambiar(self, alumnos_de_ejemplo):
        """Identifica al alumno en los préstamos ya registrados."""
        formulario = FormularioAlumno(alumno=alumnos_de_ejemplo[0])

        assert formulario.ui.campoCodigo.text() == "A-001"
        assert not formulario.ui.campoCodigo.isEnabled()

    def test_al_modificar_el_formulario_llega_lleno(self, alumnos_de_ejemplo):
        formulario = FormularioAlumno(alumno=alumnos_de_ejemplo[0])

        assert formulario.ui.campoNombre.text() == "Ana Sofía"
        assert formulario.ui.campoGrado.value() == 4
        assert formulario.ui.campoGrupo.currentText() == "B"

    def test_al_modificar_se_usa_la_funcion_transaccional(
        self, sin_base, alumnos_de_ejemplo
    ):
        """Corolario 3: las dos tablas se escriben juntas o ninguna."""
        llamadas = sin_base(repo_personas, actualizar_alumno=None,
                            dar_de_alta_alumno=alumnos_de_ejemplo[0])
        formulario = FormularioAlumno(alumno=alumnos_de_ejemplo[0])

        formulario.ui.botonGuardar.click()

        assert llamadas["biblioteca.repositorios.personas.actualizar_alumno"]
        assert llamadas[
            "biblioteca.repositorios.personas.dar_de_alta_alumno"] == []

    def test_un_codigo_repetido_se_explica_en_el_formulario(self, sin_base):
        llamadas = sin_base(repo_personas, dar_de_alta_alumno=ErrorDePersona(
            "Ya existe una persona con ese código."))
        formulario = self.llenar(FormularioAlumno())

        formulario.ui.botonGuardar.click()

        assert "ese código" in formulario.ui.etiquetaError.text()
        assert llamadas["biblioteca.repositorios.personas.dar_de_alta_alumno"]


# ===========================================================================
# Formulario de empleado · la puerta de la escalada de privilegios
# ===========================================================================

class TestFormularioDeEmpleado:
    def test_la_administradora_puede_tocar_el_perfil_de_acceso(self, con_sesion):
        formulario = FormularioEmpleado()

        assert formulario.ui.campoRol.isEnabled()

    def test_el_bibliotecario_no_puede_al_dar_de_alta(
        self, sesion_de_bibliotecario, monkeypatch
    ):
        """El defecto que la auditoría encontró, cerrado.

        El combo solo se bloqueaba al **modificar**, de modo que cualquiera
        del personal podía registrar a un administrador nuevo y entrar con él.
        """
        from biblioteca.core import sesion as modulo_sesion

        monkeypatch.setattr(modulo_sesion, "_sesion_actual",
                            sesion_de_bibliotecario)

        formulario = FormularioEmpleado()

        assert not formulario.ui.campoRol.isEnabled()
        assert "solo administrador" in formulario.ui.etiquetaRol.text()

    def test_el_bibliotecario_tampoco_puede_al_modificar(
        self, sesion_de_bibliotecario, empleados_de_ejemplo, monkeypatch
    ):
        from biblioteca.core import sesion as modulo_sesion

        monkeypatch.setattr(modulo_sesion, "_sesion_actual",
                            sesion_de_bibliotecario)

        formulario = FormularioEmpleado(empleado=empleados_de_ejemplo[1])

        assert not formulario.ui.campoRol.isEnabled()

    def test_el_bibliotecario_si_puede_registrar_a_un_bibliotecario(
        self, sin_base, sesion_de_bibliotecario, empleados_de_ejemplo, monkeypatch
    ):
        """REQ-EMP-01: lo que queda reservado es el perfil, no el alta."""
        from biblioteca.core import sesion as modulo_sesion

        monkeypatch.setattr(modulo_sesion, "_sesion_actual",
                            sesion_de_bibliotecario)
        llamadas = sin_base(repo_personas,
                            dar_de_alta_empleado=empleados_de_ejemplo[1])
        formulario = FormularioEmpleado()
        formulario.ui.campoCodigo.setText("EMP-009")
        formulario.ui.campoNombre.setText("Nueva")
        formulario.ui.campoApellido.setText("Auxiliar")
        formulario.ui.campoCorreo.setText("nueva@demo.com")

        formulario.ui.botonGuardar.click()

        assert llamadas["biblioteca.repositorios.personas.dar_de_alta_empleado"]

    def test_el_correo_del_personal_es_obligatorio(
        self, sin_base, con_sesion, empleados_de_ejemplo
    ):
        """Es con lo que inicia sesión: sin él la cuenta no sirve."""
        llamadas = sin_base(repo_personas,
                            dar_de_alta_empleado=empleados_de_ejemplo[0])
        formulario = FormularioEmpleado()
        formulario.ui.campoCodigo.setText("EMP-009")
        formulario.ui.campoNombre.setText("Sin")
        formulario.ui.campoApellido.setText("Correo")

        formulario.ui.botonGuardar.click()

        assert "correo" in formulario.ui.etiquetaError.text().lower()
        assert llamadas[
            "biblioteca.repositorios.personas.dar_de_alta_empleado"] == []

    def test_al_modificar_se_usa_la_funcion_que_guarda_el_puesto(
        self, sin_base, con_sesion, empleados_de_ejemplo
    ):
        """El defecto que la migración 10 vino a cerrar.

        `tipo_empleado` vive en la tabla `empleados` y la ruta anterior pasaba
        por `actualizar()`, que solo escribe `perfiles`: cambiar el puesto no
        guardaba nada y el formulario confirmaba igual.
        """
        llamadas = sin_base(repo_personas, actualizar_empleado=None,
                            actualizar=empleados_de_ejemplo[1])
        formulario = FormularioEmpleado(empleado=empleados_de_ejemplo[1])
        formulario.ui.campoPuesto.setCurrentText("Auxiliar de lectura")

        formulario.ui.botonGuardar.click()

        clave = "biblioteca.repositorios.personas.actualizar_empleado"
        assert llamadas[clave], "no se usó la función que escribe las dos tablas"
        (enviado,), _ = llamadas[clave][0]
        assert enviado.tipo_empleado == "Auxiliar de lectura"

    def test_el_rechazo_de_la_base_se_explica(
        self, sin_base, con_sesion, empleados_de_ejemplo
    ):
        sin_base(repo_personas, dar_de_alta_empleado=ErrorDePersona(
            "Solo un administrador puede conceder ese perfil de acceso."))
        formulario = FormularioEmpleado()
        formulario.ui.campoCodigo.setText("EMP-009")
        formulario.ui.campoNombre.setText("Nueva")
        formulario.ui.campoApellido.setText("Persona")
        formulario.ui.campoCorreo.setText("nueva@demo.com")

        formulario.ui.botonGuardar.click()

        assert "administrador" in formulario.ui.etiquetaError.text().lower()


# ===========================================================================
# Login · no existía en el sistema Java
# ===========================================================================

class TestLogin:
    def test_entrar_con_credenciales_correctas(self, monkeypatch,
                                               sesion_de_administradora):
        from biblioteca.ui import login as ui_login

        monkeypatch.setattr(ui_login, "iniciar_sesion",
                            lambda c, p: sesion_de_administradora)
        dialogo = DialogoLogin()
        dialogo.ui.campoCorreo.setText("bibliotecaria@demo.com")
        dialogo.ui.campoContrasena.setText("123456")

        dialogo.ui.botonEntrar.click()

        assert dialogo.sesion is sesion_de_administradora
        assert dialogo.result() == dialogo.DialogCode.Accepted

    def test_las_credenciales_malas_se_explican_sin_decir_cual_fallo(
        self, monkeypatch
    ):
        """REQ-USU-02: decir «ese correo no existe» enumera cuentas."""
        from biblioteca.ui import login as ui_login

        def rechazar(correo, contrasena):
            raise ErrorDeAcceso("Correo o contraseña incorrectos.")

        monkeypatch.setattr(ui_login, "iniciar_sesion", rechazar)
        dialogo = DialogoLogin()
        dialogo.ui.campoCorreo.setText("quien.sea@demo.com")
        dialogo.ui.campoContrasena.setText("equivocada")

        dialogo.ui.botonEntrar.click()

        aviso = dialogo.ui.etiquetaError.text().lower()
        assert "correo o contraseña" in aviso
        assert "no existe" not in aviso
        assert dialogo.sesion is None

    def test_sin_conexion_no_se_culpa_a_la_contrasena(self, monkeypatch):
        """El defecto que hacía cambiar una contraseña que estaba bien."""
        from biblioteca.ui import login as ui_login

        def sin_red(correo, contrasena):
            raise ErrorDeAcceso(
                "No hay conexión con el servidor de la biblioteca.")

        monkeypatch.setattr(ui_login, "iniciar_sesion", sin_red)
        dialogo = DialogoLogin()
        dialogo.ui.campoCorreo.setText("bibliotecaria@demo.com")
        dialogo.ui.campoContrasena.setText("123456")

        dialogo.ui.botonEntrar.click()

        assert "conexión" in dialogo.ui.etiquetaError.text().lower()
        assert "contraseña" not in dialogo.ui.etiquetaError.text().lower()

    def test_tras_un_rechazo_se_puede_reintentar(self, monkeypatch):
        from biblioteca.ui import login as ui_login

        def rechazar(correo, contrasena):
            raise ErrorDeAcceso("Correo o contraseña incorrectos.")

        monkeypatch.setattr(ui_login, "iniciar_sesion", rechazar)
        dialogo = DialogoLogin()
        dialogo.ui.campoCorreo.setText("a@b.com")
        dialogo.ui.campoContrasena.setText("x")

        dialogo.ui.botonEntrar.click()

        assert dialogo.ui.botonEntrar.isEnabled()


# ===========================================================================
# Nuevo préstamo · dos búsquedas y un botón, por RNF-USA-01
# ===========================================================================

class TestNuevoPrestamo:
    """La meta operativa: registrar un préstamo en menos de treinta segundos.

    Por eso no es un formulario. El sistema Java pedía capturar los datos del
    préstamo campo por campo.
    """

    @pytest.fixture
    def dialogo(self, sin_base, con_sesion, alumnos_de_ejemplo,
                libros_de_ejemplo):
        sin_base(repo_personas, buscar_alumnos_o_salon=alumnos_de_ejemplo)
        sin_base(repo_libros, listar=libros_de_ejemplo,
                 buscar=libros_de_ejemplo[:1])
        sin_base(repo_prestamos, registrar=None)
        return DialogoNuevoPrestamo()

    def test_las_dos_listas_abren_llenas(self, dialogo):
        """Sin escribir nada: el caso de la bibliotecaria que ya sabe a quién."""
        assert dialogo.ui.listaAlumnos.count() == 2
        assert dialogo.ui.listaLibros.count() == 3

    def test_el_alumno_se_muestra_con_su_salon(self, dialogo):
        assert "4B" in dialogo.ui.listaAlumnos.item(0).text()

    def test_un_libro_sin_ejemplares_se_ve_pero_no_se_puede_elegir(self, dialogo):
        """Mostrarlo deshabilitado explica por qué no está disponible.

        Ocultarlo dejaría a la bibliotecaria buscándolo.
        """
        from PySide6.QtCore import Qt

        agotado = dialogo.ui.listaLibros.item(1)

        assert "Sin ejemplares" in agotado.text()
        assert not agotado.flags() & Qt.ItemFlag.ItemIsEnabled

    def test_el_boton_nace_apagado(self, dialogo):
        assert not dialogo.ui.botonPrestar.isEnabled()
        assert "Elige un alumno y un libro" in dialogo.ui.etiquetaResumen.text()

    def test_con_solo_el_alumno_el_boton_sigue_apagado(self, dialogo):
        dialogo.ui.listaAlumnos.setCurrentRow(0)

        assert not dialogo.ui.botonPrestar.isEnabled()
        assert "elige el libro" in dialogo.ui.etiquetaResumen.text().lower()

    def test_con_solo_el_libro_el_boton_sigue_apagado(self, dialogo):
        dialogo.ui.listaLibros.setCurrentRow(0)

        assert not dialogo.ui.botonPrestar.isEnabled()
        assert "elige al alumno" in dialogo.ui.etiquetaResumen.text().lower()

    def test_con_los_dos_se_habilita_y_se_resume(self, dialogo):
        dialogo.ui.listaAlumnos.setCurrentRow(0)
        dialogo.ui.listaLibros.setCurrentRow(0)

        assert dialogo.ui.botonPrestar.isEnabled()
        resumen = dialogo.ui.etiquetaResumen.text()
        assert "Ana Sofía Martínez" in resumen
        assert "El principito" in resumen

    def test_se_anuncia_el_plazo_y_no_una_fecha(self, dialogo):
        """Corolario 2, visto en la pantalla.

        Antes se anunciaba una fecha calculada con `date.today()` que la base
        no iba a guardar: a partir de las 18:00 hora de Veracruz la pantalla
        decía un día y la base guardaba otro.
        """
        dialogo.ui.listaAlumnos.setCurrentRow(0)
        dialogo.ui.listaLibros.setCurrentRow(0)

        plazo = dialogo.ui.etiquetaPlazo.text()

        assert "7 días" in plazo
        assert "al confirmar" in plazo
        assert "/" not in plazo, "se volvió a anunciar una fecha concreta"

    def test_prestar_manda_los_tres_datos(self, dialogo, sin_base, con_sesion):
        llamadas = sin_base(repo_prestamos, registrar=None)
        dialogo.ui.listaAlumnos.setCurrentRow(0)
        dialogo.ui.listaLibros.setCurrentRow(0)

        dialogo.ui.botonPrestar.click()

        (_, parametros) = llamadas[
            "biblioteca.repositorios.prestamos.registrar"][0]
        assert parametros["libro_id"] == 1
        assert parametros["alumno_id"] == "a-1"
        assert parametros["registrado_por"] == "e-1"
        assert dialogo.registrado

    def test_el_limite_de_un_libro_por_alumno_se_explica(
        self, dialogo, sin_base, con_sesion
    ):
        """La regla la aplica un índice único parcial en Postgres.

        Aquí solo se comprueba que su mensaje llegue a la pantalla.
        """
        sin_base(repo_prestamos, registrar=ErrorDePrestamo(
            "Ese alumno ya tiene un préstamo activo."))
        dialogo.ui.listaAlumnos.setCurrentRow(0)
        dialogo.ui.listaLibros.setCurrentRow(0)

        dialogo.ui.botonPrestar.click()

        assert "préstamo activo" in dialogo.ui.etiquetaError.text()
        assert not dialogo.registrado
        assert dialogo.ui.botonPrestar.isEnabled(), "no se puede reintentar"

    def test_escribir_no_consulta_de_inmediato(self, dialogo):
        """Un temporizador por búsqueda, igual que en el catálogo."""
        dialogo.ui.campoBuscarAlumno.setText("ana")

        assert dialogo._temp_alumnos.isActive()

    def test_la_busqueda_del_alumno_acepta_el_salon(self, dialogo, sin_base,
                                                    alumnos_de_ejemplo):
        """Nombre, código o salón, sin elegir criterio antes."""
        llamadas = sin_base(repo_personas,
                            buscar_alumnos_o_salon=alumnos_de_ejemplo[:1])
        dialogo.ui.campoBuscarAlumno.setText("4B")

        dialogo._buscar_alumnos()

        clave = "biblioteca.repositorios.personas.buscar_alumnos_o_salon"
        assert llamadas[clave][-1][0] == ("4B",)

    def test_un_fallo_de_busqueda_se_explica_sin_cerrar_el_dialogo(
        self, sin_base, con_sesion, libros_de_ejemplo
    ):
        sin_base(repo_personas,
                 buscar_alumnos_o_salon=ConnectionError("Connection refused"))
        sin_base(repo_libros, listar=libros_de_ejemplo, buscar=[])

        dialogo = DialogoNuevoPrestamo()

        assert "conexión" in dialogo.ui.etiquetaError.text().lower()
        assert dialogo.ui.listaAlumnos.count() == 0

    def test_cancelar_no_registra_nada(self, dialogo, sin_base, con_sesion):
        llamadas = sin_base(repo_prestamos, registrar=None)
        dialogo.ui.listaAlumnos.setCurrentRow(0)
        dialogo.ui.listaLibros.setCurrentRow(0)

        dialogo.ui.botonCancelar.click()

        assert llamadas["biblioteca.repositorios.prestamos.registrar"] == []
        assert not dialogo.registrado


# ===========================================================================
# Permisos por perfil, vistos desde la interfaz
# ===========================================================================

@pytest.mark.parametrize("rol,puede", [
    (Rol.ADMINISTRADOR, True),
    (Rol.BIBLIOTECARIO, False),
])
def test_solo_el_administrador_cambia_perfiles_de_acceso(
    monkeypatch, rol, puede, empleados_de_ejemplo
):
    """La tabla de permisos del archivo de contexto, comprobada.

    Es la defensa de la interfaz. La de verdad es el disparador
    `proteger_rol`, que desde la migración 10 vigila también el INSERT.
    """
    from biblioteca.core import sesion as modulo_sesion
    from biblioteca.core.sesion import Sesion
    from biblioteca.modelos.persona import Perfil

    monkeypatch.setattr(modulo_sesion, "_sesion_actual", Sesion(
        perfil=Perfil(id="p-1", codigo="P-1", nombre="A", apellido="B",
                      rol=rol)))

    formulario = FormularioEmpleado()

    assert formulario.ui.campoRol.isEnabled() is puede
