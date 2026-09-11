"""Punto de entrada del sistema de biblioteca.

Equivale a la ventana principal VentanaMani.java del sistema Java.
Por ahora solo verifica la conexion con Supabase (historia INF-07).
"""

from biblioteca.core.supabase_cliente import obtener_cliente


def main() -> None:
    cliente = obtener_cliente()
    respuesta = cliente.table("v_catalogo").select("id, titulo, autor").limit(5).execute()

    print("Conexion establecida con Supabase.")

    if not respuesta.data:
        print()
        print("El catalogo se ve vacio porque todavia no has iniciado sesion:")
        print("las politicas RLS solo muestran los libros a usuarios autenticados.")
        print("Eso es justo lo que debe pasar (historia USU-06).")
        return

    print(f"Libros en el catalogo (primeros {len(respuesta.data)}):")
    for libro in respuesta.data:
        print(f"  [{libro['id']}] {libro['titulo']} - {libro['autor']}")


if __name__ == "__main__":
    main()
