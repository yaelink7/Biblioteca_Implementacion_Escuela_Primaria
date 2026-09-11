"""Personas del sistema: perfil base, alumnos y empleados.

Migra Persona.java, Usuario.java y Empleado.java del sistema Java.
La herencia del proyecto original se conserva: Alumno y Empleado
heredan de Perfil igual que Usuario y Empleado heredaban de Persona.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from datetime import date
from enum import StrEnum
from typing import Any, Self


class Rol(StrEnum):
    """Perfiles definidos en la seccion 1.5 del Avance 1."""

    ADMINISTRADOR = "administrador"
    BIBLIOTECARIO = "bibliotecario"
    ALUMNO = "alumno"

    @property
    def es_personal(self) -> bool:
        """Administrador y bibliotecario operan la biblioteca; el alumno no."""
        return self in (Rol.ADMINISTRADOR, Rol.BIBLIOTECARIO)


@dataclass
class Perfil:
    """Datos comunes de cualquier persona registrada (clase Persona)."""

    codigo: str
    nombre: str
    apellido: str
    rol: Rol = Rol.ALUMNO
    calle: str | None = None
    colonia: str | None = None
    numero: int | None = None
    codigo_postal: str | None = None
    telefono: str | None = None
    correo: str | None = None
    activo: bool = True

    id: str | None = None
    auth_id: str | None = None

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}".strip()

    @property
    def direccion(self) -> str:
        """Arma la direccion a partir de los campos sueltos que venian del Java."""
        partes = [p for p in (self.calle, self.numero, self.colonia) if p]
        return ", ".join(str(p) for p in partes)

    @classmethod
    def desde_fila(cls, fila: dict[str, Any]) -> Self:
        return cls(
            id=fila.get("id"),
            auth_id=fila.get("auth_id"),
            codigo=fila["codigo"],
            nombre=fila["nombre"],
            apellido=fila["apellido"],
            rol=Rol(fila.get("rol", Rol.ALUMNO)),
            calle=fila.get("calle"),
            colonia=fila.get("colonia"),
            numero=fila.get("numero"),
            codigo_postal=fila.get("codigo_postal"),
            telefono=fila.get("telefono"),
            correo=fila.get("correo"),
            activo=fila.get("activo", True),
        )

    def a_fila(self) -> dict[str, Any]:
        """Convierte a las columnas de la tabla perfiles, omitiendo lo vacio."""
        fila = {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "rol": str(self.rol),
            "calle": self.calle,
            "colonia": self.colonia,
            "numero": self.numero,
            "codigo_postal": self.codigo_postal,
            "telefono": self.telefono,
            "correo": self.correo,
            "activo": self.activo,
        }
        if self.id:
            fila["id"] = self.id
        if self.auth_id:
            fila["auth_id"] = self.auth_id
        return fila


@dataclass
class Alumno(Perfil):
    """Alumno lector. Migra Usuario.java del sistema Java.

    grado y grupo permiten la busqueda "por nombre o grupo" que exige la
    Factibilidad Operativa del Avance 1.
    """

    grado: int | None = None
    grupo: str | None = None

    def __post_init__(self) -> None:
        self.rol = Rol.ALUMNO

    @property
    def salon(self) -> str:
        if self.grado and self.grupo:
            return f"{self.grado}{self.grupo}"
        return "-"

    @classmethod
    def desde_fila(cls, fila: dict[str, Any]) -> Self:
        alumno = cls(**_campos_de_perfil(fila))
        alumno.grado = fila.get("grado")
        alumno.grupo = fila.get("grupo")
        return alumno

    def datos_propios(self) -> dict[str, Any]:
        """Columnas de la tabla usuarios (las que no van en perfiles)."""
        return {"grado": self.grado, "grupo": self.grupo}


@dataclass
class Empleado(Perfil):
    """Bibliotecaria o auxiliar. Migra Empleado.java del sistema Java."""

    tipo_empleado: str = "Bibliotecario"
    fecha_ingreso: date | None = None

    @classmethod
    def desde_fila(cls, fila: dict[str, Any]) -> Self:
        empleado = cls(**_campos_de_perfil(fila))
        empleado.tipo_empleado = fila.get("tipo_empleado", "Bibliotecario")
        ingreso = fila.get("fecha_ingreso")
        empleado.fecha_ingreso = date.fromisoformat(ingreso) if ingreso else None
        return empleado

    def datos_propios(self) -> dict[str, Any]:
        """Columnas de la tabla empleados (las que no van en perfiles)."""
        datos: dict[str, Any] = {"tipo_empleado": self.tipo_empleado}
        if self.fecha_ingreso:
            datos["fecha_ingreso"] = self.fecha_ingreso.isoformat()
        return datos


def _campos_de_perfil(fila: dict[str, Any]) -> dict[str, Any]:
    """Extrae de una fila solo los campos que declara Perfil.

    Las consultas traen perfiles y sus datos propios en un mismo diccionario;
    esto separa la parte que corresponde a la clase base.
    """
    base = Perfil.desde_fila(fila)
    return {campo.name: getattr(base, campo.name) for campo in fields(Perfil)}
