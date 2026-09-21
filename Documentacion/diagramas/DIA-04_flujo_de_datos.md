# DIA-04 · Diagrama de flujo de datos

> Issue [#62](https://github.com/yaelink7/Biblioteca_Implementacion_Escuela_Primaria/issues/62) · 5 puntos · Rey David Montes Ciriaco

## Nivel 0 · Diagrama de contexto

El sistema como una sola caja, con quién le habla y qué le dice.

```mermaid
flowchart LR
    BIB["👤 Bibliotecario"]
    ADM["👤 Administrador"]
    ALU["👤 Alumno"]

    SIS(("0<br/>Sistema de<br/>Biblioteca Escolar"))

    BIB -- "datos de libros, alumnos<br/>y empleados · préstamos<br/>y devoluciones" --> SIS
    SIS -- "catálogo · lista de préstamos<br/>reporte de deudores<br/>mensajes de rechazo" --> BIB

    ADM -- "perfiles de acceso<br/>cuentas nuevas" --> SIS
    SIS -- "plantilla de personal" --> ADM

    ALU -- "consulta del catálogo<br/><i>fase 2 · móvil</i>" --> SIS
    SIS -- "acervo disponible<br/>sus propios préstamos" --> ALU

    style SIS fill:#EEF2F8,stroke:#2D4B73,stroke-width:2px
    style ALU stroke-dasharray: 5 4
```

El alumno va punteado: **hoy no interactúa con el sistema**. Su perfil existe y las
políticas de acceso ya lo contemplan, pero la aplicación que usará es la móvil de la
fase 2. En el sistema de escritorio actual, quien teclea siempre es un adulto.

## Nivel 1 · Procesos, almacenes y flujos

```mermaid
flowchart TB
    BIB["👤 Bibliotecario /<br/>Administrador"]
    ALU["👤 Alumno"]

    P1(("1<br/>Controlar<br/>acceso"))
    P2(("2<br/>Gestionar<br/>catálogo"))
    P3(("3<br/>Buscar<br/>y filtrar"))
    P4(("4<br/>Gestionar<br/>padrón"))
    P5(("5<br/>Gestionar<br/>plantilla"))
    P6(("6<br/>Operar<br/>préstamos"))
    P7(("7<br/>Generar<br/>reportes"))

    D1[("D1 · perfiles")]
    D2[("D2 · usuarios")]
    D3[("D3 · empleados")]
    D4[("D4 · libros")]
    D5[("D5 · prestamos")]
    D6[("D6 · bitacora_libros")]
    D7[("D7 · notificaciones")]
    AU[("auth.users<br/><i>Supabase Auth</i>")]

    BIB -- credenciales --> P1
    P1 <--> AU
    P1 -- lee perfil y rol --> D1
    P1 -- sesión iniciada --> BIB

    BIB -- alta, cambio, baja --> P2
    P2 --> D4
    P2 -. "sin implementar<br/>(LIB-04)" .-> D6

    BIB -- texto de búsqueda --> P3
    D4 -- títulos, autores, tipo --> P3
    P3 -- resultados --> BIB

    BIB -- ficha del alumno --> P4
    P4 --> D1
    P4 --> D2
    D5 -- quién tiene préstamo --> P4

    BIB -- ficha del empleado --> P5
    P5 --> D1
    P5 --> D3

    BIB -- alumno + libro --> P6
    D1 -- alumno --> P6
    D4 -- libro y existencias --> P6
    P6 --> D5
    P6 -- descuenta y reintegra --> D4
    P6 -- lista de préstamos --> BIB

    D5 -- préstamos vencidos --> P7
    D1 -- contacto --> P7
    D4 -- libros dados de baja --> P7
    P7 -- reporte de deudores --> BIB

    ALU -. "fase 2" .-> P3
    ALU -. "fase 2" .-> P7

    style D6 fill:#FDF3E7,stroke:#A8621B,stroke-dasharray: 5 4
    style D7 fill:#FDF3E7,stroke:#A8621B,stroke-dasharray: 5 4
    style ALU stroke-dasharray: 5 4
```

## Los siete almacenes

| Almacén | Tabla | Quién escribe | Quién lee |
|---|---|---|---|
| D1 | `perfiles` | Procesos 4 y 5 | 1, 4, 5, 6, 7 |
| D2 | `usuarios` | Proceso 4 | 4, 6 |
| D3 | `empleados` | Proceso 5 | 5 |
| D4 | `libros` | Procesos 2 y 6 | 2, 3, 6, 7 |
| D5 | `prestamos` | Proceso 6 | 4, 6, 7 |
| D6 | `bitacora_libros` | **nadie** | nadie |
| D7 | `notificaciones` | **nadie** | nadie |

**D6 y D7 se dibujan sin flujo de escritura, y está bien así.** Las dos tablas
existen con sus políticas de acceso, y ninguna línea de código escribe en ellas. La
bitácora espera su disparador (`LIB-04`, issue #24); las notificaciones perdieron su
requisito cuando la escuela confirmó que no se comunica por correo con las familias.

Dibujar un almacén al que no llega ninguna flecha **es el diagrama diciendo la
verdad**, y además deja ver el hueco a simple vista.

## Un detalle que suele documentarse mal

El proceso 6 lee `libros` y el proceso 3 también. **Ninguno de los dos usa la vista
`v_catalogo`**, aunque la vista exista para eso: el repositorio consulta la tabla
directamente. Tiene un motivo — la vista filtra `where activo`, y el catálogo
necesita poder mostrar los libros dados de baja cuando se activa esa casilla.

Conviene que el diagrama muestre la tabla y no la vista, porque es lo que ocurre.

## Notas sobre notación

Se usa la notación **Yourdon/DeMarco**: círculos para procesos, rectángulos para
entidades externas, y los almacenes con su identificador `Dn`. Si el profesor pide
Gane-Sarson, los procesos van en rectángulos redondeados y los almacenes en
rectángulos abiertos a la derecha; el contenido no cambia.

Los flujos del nivel 1 conservan la numeración del nivel 0: todo lo que entra y sale
de la caja única del contexto tiene su correspondencia aquí, sin flujos nuevos ni
perdidos.
