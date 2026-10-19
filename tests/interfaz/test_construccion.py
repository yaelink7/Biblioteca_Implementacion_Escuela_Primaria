"""Interfaz · que cada pantalla se construya y tenga los controles que dice.

Es el equivalente directo del paquete **`GUIBiblia`** del sistema Java, que
eran 47 de sus 70 pruebas repartidas en diez archivos: `GUILibroTest`,
`DatosLibroTest`, `VentanaManiTest` y los demás. Cada uno comprobaba cuatro o
cinco cosas sobre su ventana:

| Prueba en Java | Aquí |
|---|---|
| `seConstruyeSinLanzarExcepciones` | `test_cada_pantalla_se_construye` |
| `noEsVisiblePorDefecto` | `test_ninguna_pantalla_nace_visible` |
| `tieneUnTamanoDefinidoTrasElPack` | `test_cada_pantalla_tiene_tamano` |
| `cierraLaAplicacionAlCerrarLaVentana` | `test_ningun_dialogo_cierra_la_aplicacion` |
| `laTablaDeLibrosTieneLasNueveColumnasEsperadas` | `test_las_tablas_tienen_sus_columnas` |

La cuarta cambió de sentido y conviene saber por qué. En el sistema Java cada
ventana tenía `EXIT_ON_CLOSE`, de modo que cerrar un formulario de alta
**cerraba el programa entero**. La prueba lo daba por correcto porque
describía lo que había. Aquí los diálogos son modales y la única ventana que
termina la aplicación es la principal, así que la prueba comprueba lo
contrario: que cerrar un formulario no se lleve la sesión con él.

El informe de métricas del sistema Java dejaba esta capa en 14 % de ramas, y
señalaba la causa: las reglas vivían dentro de los formularios, así que no se
podían interrogar sin abrir ventanas. Aquí las reglas están en `servicios/`
—probadas en `tests/caja_negra/`— y estas pruebas se limitan a lo que de
verdad le toca a la interfaz: estar armada y conectada.
"""

from __future__ import annotations

import pytest
from PySide6.QtWidgets import QDialog, QTableWidget, QWidget

from biblioteca.repositorios import libros as repo_libros
from biblioteca.repositorios import personas as repo_personas
from biblioteca.repositorios import prestamos as repo_prestamos
from biblioteca.ui.alumnos import PantallaAlumnos
from biblioteca.ui.catalogo import PantallaCatalogo
from biblioteca.ui.deudores import PantallaDeudores
from biblioteca.ui.empleados import PantallaEmpleados
from biblioteca.ui.formulario_alumno import FormularioAlumno
from biblioteca.ui.formulario_empleado import FormularioEmpleado
from biblioteca.ui.formulario_libro import FormularioLibro
from biblioteca.ui.historial_alumno import DialogoHistorial
from biblioteca.ui.login import DialogoLogin
from biblioteca.ui.nuevo_prestamo import DialogoNuevoPrestamo
from biblioteca.ui.prestamos import PantallaPrestamos
from biblioteca.ui.ventana_principal import VentanaPrincipal


@pytest.fixture
def todo_vacio(sin_base, con_sesion):
    """Responde a cada consulta con una lista vacía.

    Las pantallas consultan la base al construirse, así que no hay forma de
    crearlas sin contestarles. Vacío es además el caso más duro: una tabla
    sin filas es donde revientan los índices.
    """
    sin_base(repo_libros, listar=[], buscar=[])
    sin_base(repo_personas, listar_alumnos=[], buscar_alumnos=[],
             buscar_alumnos_o_salon=[], listar_empleados=[])
    sin_base(repo_prestamos, activos=[], deudores=[], historial_de=[])


def construir(clase, *args, **kwargs):
    return clase(*args, **kwargs)


# Las once pantallas, con lo que cada constructor necesita.
PANTALLAS = [
    ("login", DialogoLogin, ()),
    ("catalogo", PantallaCatalogo, ()),
    ("prestamos", PantallaPrestamos, ()),
    ("alumnos", PantallaAlumnos, ()),
    ("deudores", PantallaDeudores, ()),
    ("empleados", PantallaEmpleados, ()),
    ("formulario_libro", FormularioLibro, ()),
    ("nuevo_prestamo", DialogoNuevoPrestamo, ()),
    ("formulario_alumno", FormularioAlumno, ()),
    ("formulario_empleado", FormularioEmpleado, ()),
]

DIALOGOS = [
    ("login", DialogoLogin),
    ("formulario_libro", FormularioLibro),
    ("nuevo_prestamo", DialogoNuevoPrestamo),
    ("formulario_alumno", FormularioAlumno),
    ("formulario_empleado", FormularioEmpleado),
]


# ===========================================================================
# seConstruyeSinLanzarExcepciones
# ===========================================================================

@pytest.mark.parametrize("nombre,clase,argumentos", PANTALLAS,
                         ids=[p[0] for p in PANTALLAS])
def test_cada_pantalla_se_construye(todo_vacio, nombre, clase, argumentos):
    """Que el `.ui` compilado y el código que lo usa sigan de acuerdo.

    Es la prueba que falla cuando alguien renombra un control en Qt Designer
    y olvida recompilar, o recompila y olvida actualizar el código.
    """
    pantalla = construir(clase, *argumentos)

    assert pantalla is not None
    assert isinstance(pantalla, QWidget)


def test_la_ventana_principal_se_construye(todo_vacio, sesion_de_administradora):
    ventana = VentanaPrincipal(sesion_de_administradora)

    assert ventana is not None


def test_el_historial_se_construye(todo_vacio, alumnos_de_ejemplo):
    dialogo = DialogoHistorial(None, alumnos_de_ejemplo[0])

    assert dialogo is not None


# ===========================================================================
# noEsVisiblePorDefecto
# ===========================================================================

@pytest.mark.parametrize("nombre,clase,argumentos", PANTALLAS,
                         ids=[p[0] for p in PANTALLAS])
def test_ninguna_pantalla_nace_visible(todo_vacio, nombre, clase, argumentos):
    """Construir no es mostrar: quien la crea decide cuándo se ve."""
    assert not construir(clase, *argumentos).isVisible()


# ===========================================================================
# tieneUnTamanoDefinidoTrasElPack
# ===========================================================================

@pytest.mark.parametrize("nombre,clase,argumentos", PANTALLAS,
                         ids=[p[0] for p in PANTALLAS])
def test_cada_pantalla_tiene_tamano(todo_vacio, nombre, clase, argumentos):
    pantalla = construir(clase, *argumentos)

    assert pantalla.width() > 0
    assert pantalla.height() > 0


# ===========================================================================
# cierraLaAplicacionAlCerrarLaVentana, al revés
# ===========================================================================

@pytest.mark.parametrize("nombre,clase", DIALOGOS, ids=[d[0] for d in DIALOGOS])
def test_ningun_dialogo_cierra_la_aplicacion(todo_vacio, nombre, clase):
    """En el sistema Java cada ventana llevaba `EXIT_ON_CLOSE`.

    Cerrar el formulario de alta de un libro cerraba el programa, y había que
    volver a entrar. Aquí son diálogos: cerrarlos devuelve a la ventana que
    los abrió.
    """
    dialogo = construir(clase)

    assert isinstance(dialogo, QDialog)
    assert dialogo.isModal() or dialogo.windowModality() is not None


@pytest.mark.parametrize("nombre,clase", DIALOGOS, ids=[d[0] for d in DIALOGOS])
def test_cerrar_un_dialogo_no_deja_la_sesion_abierta(todo_vacio, nombre, clase):
    """`reject()` es lo que ejecuta el botón Cancelar y la tecla Escape."""
    dialogo = construir(clase)

    dialogo.reject()

    assert dialogo.result() == QDialog.DialogCode.Rejected


# ===========================================================================
# laTablaDeLibrosTieneLasNueveColumnasEsperadas
# ===========================================================================

COLUMNAS = {
    "catalogo": (PantallaCatalogo, "tablaLibros",
                 ["Título", "Autor", "Tipo", "Año", "Estado"]),
    "prestamos": (PantallaPrestamos, "tablaPrestamos",
                  ["Alumno", "Libro", "Prestado", "Vence", "Situación"]),
    "alumnos": (PantallaAlumnos, "tablaAlumnos",
                ["Código", "Alumno", "Salón", "Contacto del tutor", "Situación"]),
    "deudores": (PantallaDeudores, "tablaDeudores",
                 ["Alumno", "Salón", "Libro", "Debió entregar", "Retraso",
                  "Contacto del tutor"]),
    "empleados": (PantallaEmpleados, "tablaEmpleados",
                  ["Código", "Nombre", "Puesto", "Correo", "Perfil"]),
}


@pytest.mark.parametrize("nombre", list(COLUMNAS), ids=list(COLUMNAS))
def test_las_tablas_tienen_sus_columnas(todo_vacio, nombre):
    """Los encabezados están en el `.ui`, no en el código.

    Si alguien agrega una columna en Qt Designer sin tocar `_pintar`, la
    columna nueva sale vacía: esta prueba y la de contenido lo delatan juntas.
    """
    clase, atributo, esperadas = COLUMNAS[nombre]
    pantalla = clase()
    tabla: QTableWidget = getattr(pantalla.ui, atributo)

    assert tabla.columnCount() == len(esperadas)
    reales = [tabla.horizontalHeaderItem(c).text()
              for c in range(tabla.columnCount())]
    assert reales == esperadas


def test_el_historial_tiene_sus_cinco_columnas(todo_vacio, alumnos_de_ejemplo):
    dialogo = DialogoHistorial(None, alumnos_de_ejemplo[0])

    assert dialogo.ui.tablaHistorial.columnCount() == 5


@pytest.mark.parametrize("nombre", list(COLUMNAS), ids=list(COLUMNAS))
def test_ninguna_tabla_se_edita_a_mano(todo_vacio, nombre):
    """Una tabla editable deja cambiar lo que se ve sin cambiar la base.

    El dato quedaría distinto en pantalla y en Postgres hasta la siguiente
    recarga, que es la clase de contradicción que este proyecto evita por
    diseño.
    """
    clase, atributo, _ = COLUMNAS[nombre]
    # La referencia hay que guardarla: si la pantalla queda como temporal,
    # Python la recoge y Qt destruye el objeto C++ antes de la asercion.
    pantalla = clase()
    tabla: QTableWidget = getattr(pantalla.ui, atributo)

    assert tabla.editTriggers() == QTableWidget.EditTrigger.NoEditTriggers


@pytest.mark.parametrize("nombre", list(COLUMNAS), ids=list(COLUMNAS))
def test_las_tablas_seleccionan_la_fila_completa(todo_vacio, nombre):
    """El bibliotecario selecciona un préstamo, no una celda."""
    clase, atributo, _ = COLUMNAS[nombre]
    pantalla = clase()
    tabla: QTableWidget = getattr(pantalla.ui, atributo)

    assert tabla.selectionBehavior() == QTableWidget.SelectionBehavior.SelectRows


# ===========================================================================
# Lo que no estaba en el sistema Java
# ===========================================================================

def test_la_contrasena_no_se_muestra_al_escribirla(todo_vacio):
    """El sistema Java no tenía inicio de sesión: no hay caso que heredar."""
    from PySide6.QtWidgets import QLineEdit

    login = DialogoLogin()

    assert login.ui.campoContrasena.echoMode() == QLineEdit.EchoMode.Password


def test_los_botones_que_necesitan_seleccion_nacen_apagados(todo_vacio):
    """Sin fila elegida, *Editar* y *Dar de baja* no deben poder pulsarse.

    Es lo que evita el `IndexError` de pulsar un botón sin selección, que en
    el sistema Java se manejaba con un `JOptionPane` después del hecho.
    """
    catalogo = PantallaCatalogo()

    assert not catalogo.ui.botonEditar.isEnabled()
    assert not catalogo.ui.botonBaja.isEnabled()


def test_el_nuevo_libro_siempre_se_puede_pulsar(todo_vacio):
    assert PantallaCatalogo().ui.botonNuevo.isEnabled()


def test_el_tope_del_ano_es_el_ano_de_hoy(todo_vacio):
    """D-08 cerrado en la interfaz, además de en el validador y en la base.

    El control no deja escribir un año futuro, así que el defecto que el
    sistema Java tenía no se puede ni teclear.
    """
    from datetime import date

    formulario = FormularioLibro()

    assert formulario.ui.campoAno.maximum() == date.today().year
