"""Validacion del alta y modificacion de personas.

Sigue el mismo criterio que validador_libro: las reglas viven fuera de la
ventana para poder probarlas sin abrirla. En el sistema Java estaban dentro
de los formularios, que es lo que la auditoria senalo como causa de que la
cobertura de ramas de la capa grafica se quedara en 14 %.
"""

from __future__ import annotations

import re

from biblioteca.modelos.persona import Alumno, Empleado, Perfil
from biblioteca.servicios.validador_libro import Resultado

# Suficiente para atrapar erratas de captura sin rechazar correos validos
PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
GRUPOS_VALIDOS = re.compile(r"^[A-Za-z]$")


def validar_perfil(perfil: Perfil) -> Resultado:
    """Reglas comunes a cualquier persona registrada."""
    r = Resultado()

    if not perfil.codigo or not perfil.codigo.strip():
        r.errores.append("El código es obligatorio.")
    if not perfil.nombre or not perfil.nombre.strip():
        r.errores.append("El nombre es obligatorio.")
    if not perfil.apellido or not perfil.apellido.strip():
        r.errores.append("Los apellidos son obligatorios.")

    if perfil.correo and not PATRON_CORREO.match(perfil.correo.strip()):
        r.errores.append("El correo electrónico no tiene un formato válido.")

    if perfil.telefono:
        digitos = re.sub(r"\D", "", perfil.telefono)
        if len(digitos) < 7:
            r.errores.append("El teléfono parece incompleto.")

    return r


def validar_alumno(alumno: Alumno) -> Resultado:
    """REQ-USU-01, con los datos que la biblioteca necesita de un nino."""
    r = validar_perfil(alumno)

    if alumno.grado is not None and not 1 <= alumno.grado <= 6:
        r.errores.append("El grado debe estar entre 1 y 6.")

    if alumno.grupo and not GRUPOS_VALIDOS.match(alumno.grupo.strip()):
        r.errores.append("El grupo debe ser una sola letra.")

    # Media llave es peor que ninguna: con grado pero sin grupo, la busqueda
    # "por salon" que pide la Factibilidad Operativa no encuentra al alumno.
    if (alumno.grado is None) != (not alumno.grupo):
        r.errores.append(
            "Indica el grado y el grupo juntos, o deja ambos sin asignar."
        )

    if not (alumno.correo or alumno.telefono):
        r.errores.append(
            "Registra al menos un contacto del tutor: sin él no hay forma "
            "de avisar de un préstamo vencido."
        )

    return r


def validar_empleado(empleado: Empleado) -> Resultado:
    """REQ-EMP-01."""
    r = validar_perfil(empleado)

    if not empleado.tipo_empleado or not empleado.tipo_empleado.strip():
        r.errores.append("Indica el tipo de empleado.")

    if not empleado.correo:
        r.errores.append(
            "El correo es obligatorio para el personal: es con lo que "
            "inicia sesión en el sistema."
        )

    return r
