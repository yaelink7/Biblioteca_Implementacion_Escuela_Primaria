# DIA-06a · Modelo entidad-relación

> Issue [#64](https://github.com/yaelink7/Biblioteca_Implementacion_Escuela_Primaria/issues/64) · Pedro Cabrera Barrios Ángel
> Primera parte del entregable. La segunda es [DIA-06b · Modelo relacional](DIA-06b_modelo_relacional.md).

El modelo **conceptual**: qué entidades existen, qué guarda cada una y cómo se
relacionan. Todavía sin decidir cómo se implementa.

```mermaid
erDiagram
    perfiles {
        uuid id PK
        uuid auth_id FK "único, admite nulo"
        enum rol "administrador|bibliotecario|alumno"
        text codigo UK
        text nombre
        text apellido
        text calle
        text colonia
        int numero
        text codigo_postal
        text telefono
        text correo
        bool activo
        timestamptz creado_en
        timestamptz actualizado_en
    }

    usuarios {
        uuid perfil_id PK "FK a perfiles"
        smallint grado "1 a 6"
        text grupo "máx. 4 caracteres"
    }

    empleados {
        uuid perfil_id PK "FK a perfiles"
        text tipo_empleado
        date fecha_ingreso
    }

    libros {
        bigint id PK
        text titulo
        text autor
        text tipo_libro
        text editorial
        int existencias ">= 0"
        smallint ano_publicacion
        int num_paginas "> 0"
        bool activo
        text motivo_baja
        timestamptz dado_baja_en
        timestamptz creado_en
        timestamptz actualizado_en
    }

    prestamos {
        bigint id PK
        bigint libro_id FK
        uuid usuario_id FK
        uuid registrado_por FK "admite nulo"
        date fecha_prestamo
        date fecha_limite
        date fecha_devolucion "admite nulo"
        enum estado "activo|devuelto|vencido"
        timestamptz creado_en
    }

    bitacora_libros {
        bigint id PK
        bigint libro_id FK
        uuid perfil_id FK "admite nulo"
        text accion "alta|modificacion|baja"
        jsonb datos_antes
        jsonb datos_despues
        timestamptz ocurrido_en
    }

    notificaciones {
        bigint id PK
        uuid perfil_id FK
        bigint prestamo_id FK "admite nulo"
        text tipo
        text destinatario
        text estado
        text detalle
        timestamptz enviada_en
        timestamptz creada_en
    }

    perfiles ||--o| usuarios        : "es un"
    perfiles ||--o| empleados       : "es un"
    perfiles ||--o{ prestamos       : "recibe"
    perfiles ||--o{ prestamos       : "registra"
    perfiles ||--o{ bitacora_libros : "es responsable de"
    perfiles ||--o{ notificaciones  : "es destinatario de"
    libros   ||--o{ prestamos       : "se presta en"
    libros   ||--o{ bitacora_libros : "tiene registrados"
    prestamos ||--o{ notificaciones : "origina"
```

## Las siete entidades

| Entidad | Qué representa |
|---|---|
| `perfiles` | Toda persona del sistema, sea alumno o empleado |
| `usuarios` | La parte de un perfil que solo tiene un alumno: grado y grupo |
| `empleados` | La parte que solo tiene un empleado: puesto y fecha de ingreso |
| `libros` | Cada título del acervo, con sus ejemplares |
| `prestamos` | Cada préstamo y su ciclo hasta la devolución |
| `bitacora_libros` | El registro de cambios del catálogo |
| `notificaciones` | Los avisos a las familias |

## Las nueve relaciones, con su cardinalidad

| Relación | Cardinalidad | Qué significa |
|---|---|---|
| `perfiles` – `usuarios` | 1 : 0..1 | Un perfil es alumno, o no lo es |
| `perfiles` – `empleados` | 1 : 0..1 | Un perfil es empleado, o no lo es |
| `perfiles` – `prestamos` · *recibe* | 1 : 0..N | Un alumno recibe muchos préstamos con el tiempo, **pero solo uno abierto a la vez** |
| `perfiles` – `prestamos` · *registra* | 1 : 0..N | Qué empleado capturó la operación |
| `libros` – `prestamos` | 1 : 0..N | El historial completo del ejemplar |
| `libros` – `bitacora_libros` | 1 : 0..N | Los cambios registrados de ese libro |
| `perfiles` – `bitacora_libros` | 1 : 0..N | Quién hizo cada cambio |
| `perfiles` – `notificaciones` | 1 : 0..N | A quién se le avisó |
| `prestamos` – `notificaciones` | 1 : 0..N | Por qué préstamo se avisó |

**Hay dos relaciones distintas entre `perfiles` y `prestamos`**, y el diagrama debe
distinguirlas: quién se lleva el libro, y quién capturó la operación. No son la misma
persona, y confundirlas sería perder la trazabilidad de quién prestó qué.

## Especialización

`usuarios` y `empleados` son una **especialización** de `perfiles`. Es:

- **Disjunta** — nadie es alumno y empleado a la vez.
- **Parcial** — un perfil puede no ser ninguna de las dos mientras su ficha existe
  sin tipo asignado.

Se modela así porque las dos comparten todos los datos de contacto y solo difieren
en dos o tres atributos propios. Repetir nombre, apellido, teléfono y dirección en
dos entidades habría roto la tercera forma normal.

## La restricción que el E-R no puede expresar

**«Un solo préstamo abierto por alumno» no es una cardinalidad.** La cardinalidad
entre `perfiles` y `prestamos` es 1:N —un alumno recibe muchos préstamos a lo largo
del ciclo escolar—; lo que está limitado es cuántos puede tener **abiertos al mismo
tiempo**, y eso es una restricción sobre un subconjunto de filas.

En el E-R se anota como nota adjunta a la relación *recibe*. En el modelo relacional
se implementa con un índice único parcial, y ahí sí se puede ver — está dibujado en
[DIA-06b](DIA-06b_modelo_relacional.md).

Vale la pena señalarlo en la exposición: es el ejemplo más claro de una regla de
negocio que la base impone y que ningún diagrama conceptual captura por sí solo.

## Un atributo que no existe, y es deliberado

`libros` **no tiene un atributo `disponible`**. Sería derivable de `existencias`, y
por tanto una violación de la tercera forma normal. El sistema Java lo almacenaba y
podía contradecir al inventario: fue el defecto D-09 de la auditoría de calidad.

Aquí la disponibilidad se deduce cuando se consulta, en la vista `v_catalogo`.

---

> **Aviso de vigencia.** Los issues #72 a #79 modifican este modelo: colección del
> libro, asignatura, CURP, maestro de grupo, datos del tutor, retiro del correo del
> alumno y costo de reposición. Conviene actualizarlo después de la migración 10.
