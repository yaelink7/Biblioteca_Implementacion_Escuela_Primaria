"""Piezas para armar consultas a PostgREST sin que el texto del usuario rompa.

Va aparte de los repositorios a proposito: no importa el cliente de Supabase,
asi que se puede probar sin `.env` ni conexion. Los repositorios leen las
credenciales al importarse, de modo que hasta sus funciones puras eran
inprobables en una maquina sin configurar.
"""

from __future__ import annotations


def patron_de_busqueda(texto: str) -> str:
    """Convierte lo que el usuario escribio en un valor seguro para `or_`.

    Dentro de un filtro `or_` la coma separa condiciones y el parentesis
    cierra el grupo, asi que buscar «Momo, la nina» o «Garcia, Ana» partia el
    filtro y la consulta fallaba con entradas perfectamente normales. Entre
    comillas dobles el valor viaja entero; dentro solo hay que escapar la
    comilla y la barra invertida.

    No es una inyeccion de SQL —PostgREST parametriza el valor y las politicas
    RLS siguen aplicando—, pero si rompe la busqueda con nombres corrientes.
    """
    escapado = texto.replace("\\", "\\\\").replace('"', '\\"')
    return f'"%{escapado}%"'
