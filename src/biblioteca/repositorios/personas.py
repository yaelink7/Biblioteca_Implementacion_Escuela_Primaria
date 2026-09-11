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
    """Crea el perfil y su ficha de alumno.

    No crea cuenta de acceso: la bibliotecaria registra a un nino de primaria
    sin darle correo ni contrasena.
    """
    cliente = obtener_cliente()
    try:
        perfil = cliente.table(TABLA_PERFILES).insert(alumno.a_fila()).execute()
        perfil_id = perfil.data[0]["id"]
        cliente.table("usuarios").insert(
            {"perfil_id": perfil_id, **alumno.datos_propios()}
        ).execute()
    except Exception as error:
        raise ErrorDePersona(_mensaje_claro(error)) from error

    alumno.id = perfil_id
    return alumno


def dar_de_alta_empleado(empleado: Empleado) -> Empleado:
    """Alta de personal, restringida a administradores por RLS (REQ-EMP-01)."""
    cliente = obtener_cliente()
    try:
        perfil = cliente.table(TABLA_PERFILES).insert(empleado.a_fila()).execute()
        perfil_id = perfil.data[0]["id"]
        cliente.table("empleados").insert(
            {"perfil_id": perfil_id, **empleado.datos_propios()}
        ).execute()
    except Exception as error:
        raise ErrorDePersona(_mensaje_claro(error)) from error

    empleado.id = perfil_id
    return empleado


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
