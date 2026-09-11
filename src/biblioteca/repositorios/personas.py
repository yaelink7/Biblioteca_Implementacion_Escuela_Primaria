"""Acceso a alumnos y empleados. Migra UsuarioDao.java y EmpleadoDao.java del sistema Java.

Perfil guarda los datos comunes; usuarios y empleados, lo propio de cada uno.
Por eso cada alta escribe en dos tablas.
"""

from __future__ import annotations

import re

from biblioteca.core.supabase_cliente import obtener_cliente
from biblioteca.modelos.persona import Alumno, Empleado, Perfil, Rol

TABLA_PERFILES = "perfiles"


class ErrorDePersona(Exception):
    """El alta o la modificacion fue rechazada."""


def listar_alumnos() -> list[Alumno]:
    filas = (
        obtener_cliente()
        .table(TABLA_PERFILES)
        .select("*, usuarios(grado, grupo)")
        .eq("rol", str(Rol.ALUMNO))
        .eq("activo", True)
        .order("apellido")
        .execute()
    )
    return [Alumno.desde_fila(_aplanar(f, "usuarios")) for f in filas.data]


def buscar_alumnos(texto: str) -> list[Alumno]:
    """Busca por nombre, apellido o codigo.

    La Factibilidad Operativa pide registrar un prestamo en menos de treinta
    segundos "buscando al alumno por nombre o grupo"; esto es la mitad de eso.
    """
    texto = texto.strip()
    if not texto:
        return listar_alumnos()

    patron = f"%{texto}%"
    filas = (
        obtener_cliente()
        .table(TABLA_PERFILES)
        .select("*, usuarios(grado, grupo)")
        .eq("rol", str(Rol.ALUMNO))
        .eq("activo", True)
        .or_(f"nombre.ilike.{patron},apellido.ilike.{patron},codigo.ilike.{patron}")
        .order("apellido")
        .execute()
    )
    return [Alumno.desde_fila(_aplanar(f, "usuarios")) for f in filas.data]


def buscar_alumnos_o_salon(texto: str) -> list[Alumno]:
    """Busca por nombre, codigo o salon, segun lo que el usuario escriba.

    La Factibilidad Operativa pide registrar un prestamo en menos de treinta
    segundos "buscando al alumno por nombre o grupo". Que el bibliotecario
    tenga que elegir antes en que campo busca le cuesta tiempo, asi que se
    deduce: "4B" es un salon, "Ana" es un nombre.
    """
    texto = texto.strip()
    salon = re.fullmatch(r"([1-6])\s*([A-Za-z])", texto)
    if salon:
        grado = int(salon.group(1))
        grupo = salon.group(2).upper()
        return alumnos_del_salon(grado, grupo)
    return buscar_alumnos(texto)


def alumnos_del_salon(grado: int, grupo: str) -> list[Alumno]:
    """La otra mitad de la busqueda: por salon."""
    filas = (
        obtener_cliente()
        .table("usuarios")
        .select("grado, grupo, perfiles(*)")
        .eq("grado", grado)
        .eq("grupo", grupo)
        .execute()
    )

    alumnos = []
    for fila in filas.data:
        perfil = fila.pop("perfiles", None)
        if perfil:
            alumnos.append(Alumno.desde_fila({**perfil, **fila}))
    return sorted(alumnos, key=lambda a: a.apellido)


def dar_de_alta_alumno(alumno: Alumno) -> Alumno:
    """Crea el perfil y su ficha de alumno en una sola transaccion.

    Los datos viven en dos tablas, y hacer los dos INSERT por separado dejaba
    un perfil huerfano cuando el segundo fallaba. La funcion registrar_alumno
    de Postgres los agrupa: o entran ambos, o ninguno.

    No crea cuenta de acceso: la bibliotecaria registra a un nino de primaria
    sin darle correo ni contrasena.
    """
    try:
        respuesta = obtener_cliente().rpc(
            "registrar_alumno",
            {
                "p_codigo": alumno.codigo,
                "p_nombre": alumno.nombre,
                "p_apellido": alumno.apellido,
                "p_grado": alumno.grado,
                "p_grupo": alumno.grupo,
                "p_correo": alumno.correo,
                "p_telefono": alumno.telefono,
                "p_calle": alumno.calle,
                "p_colonia": alumno.colonia,
                "p_codigo_postal": alumno.codigo_postal,
                "p_numero": alumno.numero,
            },
        ).execute()
    except Exception as error:
        raise ErrorDePersona(_mensaje_claro(error)) from error

    alumno.id = respuesta.data
    return alumno


def listar_empleados() -> list[Empleado]:
    """Plantilla de la biblioteca. Solo el personal puede consultarla (RLS)."""
    filas = (
        obtener_cliente()
        .table(TABLA_PERFILES)
        .select("*, empleados(tipo_empleado, fecha_ingreso)")
        .neq("rol", str(Rol.ALUMNO))
        .eq("activo", True)
        .order("apellido")
        .execute()
    )
    return [Empleado.desde_fila(_aplanar(f, "empleados")) for f in filas.data]


def dar_de_alta_empleado(empleado: Empleado) -> Empleado:
    """Alta de personal, restringida a administradores por RLS (REQ-EMP-01).

    Va por la funcion registrar_empleado para que el perfil y la ficha entren
    juntos: cuando un bibliotecario lo intenta, RLS rechaza el segundo INSERT
    y ahora el primero se revierte con el.
    """
    try:
        respuesta = obtener_cliente().rpc(
            "registrar_empleado",
            {
                "p_codigo": empleado.codigo,
                "p_nombre": empleado.nombre,
                "p_apellido": empleado.apellido,
                "p_tipo_empleado": empleado.tipo_empleado,
                "p_rol": str(empleado.rol),
                "p_correo": empleado.correo,
                "p_telefono": empleado.telefono,
                "p_calle": empleado.calle,
                "p_colonia": empleado.colonia,
                "p_codigo_postal": empleado.codigo_postal,
                "p_numero": empleado.numero,
            },
        ).execute()
    except Exception as error:
        raise ErrorDePersona(_mensaje_claro(error)) from error

    empleado.id = respuesta.data
    return empleado


def actualizar_datos_de_alumno(alumno: Alumno) -> None:
    """Actualiza grado y grupo, que viven en la tabla usuarios.

    Va aparte de actualizar() porque los datos de una persona estan
    repartidos en dos tablas: lo comun en perfiles y lo propio en usuarios.
    """
    if not alumno.id:
        raise ErrorDePersona("No se puede actualizar un alumno sin identificador.")

    try:
        (
            obtener_cliente()
            .table("usuarios")
            .update(alumno.datos_propios())
            .eq("perfil_id", alumno.id)
            .execute()
        )
    except Exception as error:
        raise ErrorDePersona(_mensaje_claro(error)) from error


def actualizar(perfil: Perfil) -> Perfil:
    """Consulta y actualizacion de datos personales (REQ-USU-03)."""
    if not perfil.id:
        raise ErrorDePersona("No se puede actualizar un perfil sin identificador.")

    datos = perfil.a_fila()
    datos.pop("id")
    datos.pop("rol", None)  # el rol solo lo cambia un administrador

    try:
        filas = (
            obtener_cliente()
            .table(TABLA_PERFILES)
            .update(datos)
            .eq("id", perfil.id)
            .execute()
        )
    except Exception as error:
        raise ErrorDePersona(_mensaje_claro(error)) from error

    return Perfil.desde_fila(filas.data[0])


def _aplanar(fila: dict, anidada: str) -> dict:
    """Sube al primer nivel las columnas de la tabla relacionada."""
    hija = fila.pop(anidada, None) or {}
    if isinstance(hija, list):
        hija = hija[0] if hija else {}
    return {**fila, **hija}


def _mensaje_claro(error: Exception) -> str:
    texto = str(error)

    if "perfiles_codigo_key" in texto or ("duplicate key" in texto and "codigo" in texto):
        return "Ya existe una persona registrada con ese código."
    if "correo" in texto and "check" in texto:
        return "El correo electrónico no tiene un formato válido."
    if "nombre" in texto and "check" in texto:
        return "El nombre y el apellido no pueden ir vacíos."
    if "grado" in texto and "check" in texto:
        return "El grado debe estar entre 1 y 6."
    if "violates row-level security" in texto or "42501" in texto:
        return "Tu perfil no tiene permiso para registrar personas."
    return f"La base de datos rechazó la operación: {texto}"
